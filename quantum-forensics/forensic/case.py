from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional

from .chain_of_custody import ChainOfCustodyRecord
from .intelligence import build_forensic_timeline, compute_risk_score, correlate_ioc, IocCorrelationResult
from .models.evidence import Evidence
from .quantum_interface import simulate_search
from .storage.sqlite_store import SqliteForensicStore


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


@dataclass
class ForensicCase:
    case_id: str
    investigator: str
    evidences: List[Evidence] = field(default_factory=list)
    timeline: List[Dict[str, str]] = field(default_factory=list)
    indicators_found: Optional[IocCorrelationResult] = None
    risk_score: Optional[Dict[str, object]] = None
    chain_of_custody: List[ChainOfCustodyRecord] = field(default_factory=list)
    quantum_result: Optional[Dict[str, object]] = None
    created_at: str = field(default_factory=_utc_timestamp)
    updated_at: str = field(default_factory=_utc_timestamp)


class ForensicPipeline:
    def __init__(self, case: ForensicCase):
        self.case = case

    def collect_evidence(self, evidences: List[Evidence]) -> None:
        self.case.evidences.extend(evidences)

    def analyze_hashes(self) -> List[str]:
        hashes = [e.sha256 for e in self.case.evidences]
        self.case.timeline.append({'step': 'hash_analysis', 'hashes': hashes})
        return hashes

    def correlate_iocs(self, observed: Dict[str, str]) -> IocCorrelationResult:
        self.case.indicators_found = correlate_ioc(observed, self.case.evidences)
        self.case.timeline = [vars(event) for event in build_forensic_timeline(observed)]
        return self.case.indicators_found

    def calculate_risk(self) -> Dict[str, object]:
        if self.case.indicators_found is None:
            raise RuntimeError('IOC correlation must be performed before risk calculation.')

        evidence = self.case.evidences[0].to_dict() if self.case.evidences else {}
        score_result = compute_risk_score(self.case.indicators_found.__dict__, evidence)
        self.case.risk_score = {
            'total_score': score_result.total_score,
            'factors': score_result.factors,
            'level': score_result.level,
        }
        return self.case.risk_score

    def run_quantum_search(self, shots: int = 500) -> Dict[str, object]:
        if self.case.indicators_found is None or self.case.indicators_found.hash is None:
            raise RuntimeError('IOC correlation with a valid hash must be performed before quantum search.')

        found, probability = simulate_search(self.case.evidences, self.case.indicators_found.hash, shots=shots)
        self.case.quantum_result = {
            'found': found,
            'probability': probability,
        }

        if found:
            record = ChainOfCustodyRecord(evidence_id=found.id if hasattr(found, 'id') else str(found), created_by=self.case.investigator)
            record.add_event('investigator', 'quantum_search', 'Simulated Grover search completed', tool_version='quantum-forensics/phase3')
            record.finalize()
            self.case.chain_of_custody.append(record)

        return self.case.quantum_result

    def generate_report(self) -> str:
        report_lines = [
            f'Case ID: {self.case.case_id}',
            f'Investigator: {self.case.investigator}',
            '',
            'Evidences:',
        ]
        for evidence in self.case.evidences:
            report_lines.append(f'- {evidence.id} ({evidence.filename}) source={evidence.source} sha256={evidence.sha256}')

        report_lines.extend(['', 'IOC Correlation:', ''])
        if self.case.indicators_found:
            report_lines.append(f'- hash: {self.case.indicators_found.hash}')
            report_lines.append(f'- ip: {self.case.indicators_found.ip}')
            report_lines.append(f'- domain: {self.case.indicators_found.domain}')
            report_lines.append(f'- matched_signatures: {self.case.indicators_found.matched_signatures}')
            report_lines.append(f'- matched_iocs: {self.case.indicators_found.matched_iocs}')
            report_lines.append(f'- related_evidence_ids: {self.case.indicators_found.related_evidence_ids}')
        else:
            report_lines.append('- no ioc correlation performed')

        report_lines.extend(['', 'Risk Score:', ''])
        if self.case.risk_score:
            report_lines.append(f'- total_score: {self.case.risk_score["total_score"]}')
            report_lines.append(f'- level: {self.case.risk_score["level"]}')
            report_lines.append(f'- factors: {self.case.risk_score["factors"]}')
        else:
            report_lines.append('- no risk score computed')

        report_lines.extend(['', 'Quantum Search Result:', ''])
        if self.case.quantum_result:
            report_lines.append(f'- probability: {self.case.quantum_result["probability"]:.2%}')
            report_lines.append(f'- found: {getattr(self.case.quantum_result["found"], "id", self.case.quantum_result["found"])}')
        else:
            report_lines.append('- no quantum search performed')

        report_lines.extend(['', 'Chain of Custody:', ''])
        for record in self.case.chain_of_custody:
            report_lines.append(f'- evidence_id: {record.evidence_id} record_hash: {record.record_hash}')
            for event in record.events:
                report_lines.append(f'  - event_id: {event["event_id"]} action: {event["action"]} timestamp: {event["timestamp_utc"]}')

        return '\n'.join(report_lines)

    def save_to_store(self, store: SqliteForensicStore) -> None:
        """Persist the current case state to a SQLite forensic store."""
        store.upsert_case(self.case.case_id, self.case.investigator)

        for evidence in self.case.evidences:
            store.save_evidence(self.case.case_id, evidence)

        for index, event in enumerate(self.case.timeline):
            event_id = event.get('event_id') or f'{self.case.case_id}-event-{index}'
            store.save_timeline_event(
                self.case.case_id,
                event_id,
                event.get('timestamp_utc', _utc_timestamp()),
                event.get('description', ''),
                event.get('details', {}),
            )

        if self.case.indicators_found:
            store.save_ioc_correlation(self.case.case_id, {
                'hash': self.case.indicators_found.hash,
                'ip': self.case.indicators_found.ip,
                'domain': self.case.indicators_found.domain,
                'matched_signatures': self.case.indicators_found.matched_signatures,
                'matched_iocs': self.case.indicators_found.matched_iocs,
                'related_evidence_ids': self.case.indicators_found.related_evidence_ids,
            })

        if self.case.risk_score:
            store.save_risk_score(self.case.case_id, self.case.risk_score)

        if self.case.quantum_result:
            store.save_quantum_result(
                self.case.case_id,
                self.case.quantum_result.get('found').id if isinstance(self.case.quantum_result.get('found'), Evidence) else self.case.quantum_result.get('found'),
                self.case.quantum_result.get('probability', 0.0),
            )

        for record in self.case.chain_of_custody:
            store.save_chain_of_custody(record)

        self.case.updated_at = _utc_timestamp()
