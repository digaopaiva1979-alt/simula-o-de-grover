from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from ..chain_of_custody import ChainOfCustodyRecord
from ..models.evidence import Evidence


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


class SqliteForensicStore:
    def __init__(self, path: str = ':memory:'):
        self.path = path
        self.connection = sqlite3.connect(self.path, check_same_thread=False)
        self.connection.execute('PRAGMA foreign_keys = ON')
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        cursor = self.connection.cursor()
        cursor.executescript(
            '''
            CREATE TABLE IF NOT EXISTS forensic_case (
                case_id TEXT PRIMARY KEY,
                investigator TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS evidence (
                id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                filename TEXT NOT NULL,
                sha256 TEXT NOT NULL,
                source TEXT NOT NULL,
                collected_at TEXT NOT NULL,
                metadata TEXT NOT NULL,
                FOREIGN KEY(case_id) REFERENCES forensic_case(case_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS custody_record (
                record_hash TEXT PRIMARY KEY,
                evidence_id TEXT NOT NULL,
                created_by TEXT NOT NULL,
                schema_version TEXT NOT NULL,
                hash_algo TEXT NOT NULL,
                previous_hash TEXT,
                created_at TEXT NOT NULL,
                events TEXT NOT NULL,
                FOREIGN KEY(evidence_id) REFERENCES evidence(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS timeline_event (
                event_id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                timestamp_utc TEXT NOT NULL,
                description TEXT NOT NULL,
                details TEXT NOT NULL,
                FOREIGN KEY(case_id) REFERENCES forensic_case(case_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS ioc_correlation (
                case_id TEXT PRIMARY KEY,
                hash_value TEXT,
                ip TEXT,
                domain TEXT,
                matched_signatures TEXT NOT NULL,
                matched_iocs TEXT NOT NULL,
                related_evidence_ids TEXT NOT NULL,
                FOREIGN KEY(case_id) REFERENCES forensic_case(case_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS risk_score (
                case_id TEXT PRIMARY KEY,
                total_score INTEGER NOT NULL,
                level TEXT NOT NULL,
                factors TEXT NOT NULL,
                FOREIGN KEY(case_id) REFERENCES forensic_case(case_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS quantum_result (
                case_id TEXT PRIMARY KEY,
                found_evidence_id TEXT,
                probability REAL NOT NULL,
                FOREIGN KEY(case_id) REFERENCES forensic_case(case_id) ON DELETE CASCADE,
                FOREIGN KEY(found_evidence_id) REFERENCES evidence(id)
            );
            '''
        )
        self.connection.commit()

    def upsert_case(self, case_id: str, investigator: str) -> None:
        now = _utc_timestamp()
        self.connection.execute(
            '''
            INSERT INTO forensic_case(case_id, investigator, created_at, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(case_id) DO UPDATE SET
                investigator=excluded.investigator,
                updated_at=excluded.updated_at
            ''',
            (case_id, investigator, now, now),
        )
        self.connection.commit()

    def save_evidence(self, case_id: str, evidence: Evidence) -> None:
        self.connection.execute(
            '''
            INSERT OR REPLACE INTO evidence(id, case_id, filename, sha256, source, collected_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                evidence.id,
                case_id,
                evidence.filename,
                evidence.sha256,
                evidence.source,
                evidence.collected_at,
                json.dumps(evidence.metadata, sort_keys=True),
            ),
        )
        self.connection.commit()

    def save_chain_of_custody(self, record: ChainOfCustodyRecord) -> None:
        record.finalize()
        self.connection.execute(
            '''
            INSERT OR REPLACE INTO custody_record(
                record_hash,
                evidence_id,
                created_by,
                schema_version,
                hash_algo,
                previous_hash,
                created_at,
                events
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                record.record_hash,
                record.evidence_id,
                record.created_by,
                record.schema_version,
                record.hash_algo,
                record.previous_hash,
                record.created_at,
                json.dumps(record.events, sort_keys=True),
            ),
        )
        self.connection.commit()

    def save_timeline_event(self, case_id: str, event_id: str, timestamp_utc: str, description: str, details: Dict[str, str]) -> None:
        self.connection.execute(
            '''
            INSERT OR REPLACE INTO timeline_event(event_id, case_id, timestamp_utc, description, details)
            VALUES (?, ?, ?, ?, ?)
            ''',
            (event_id, case_id, timestamp_utc, description, json.dumps(details, sort_keys=True)),
        )
        self.connection.commit()

    def save_ioc_correlation(self, case_id: str, correlation: Dict[str, object]) -> None:
        self.connection.execute(
            '''
            INSERT OR REPLACE INTO ioc_correlation(
                case_id, hash_value, ip, domain, matched_signatures, matched_iocs, related_evidence_ids
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                case_id,
                correlation.get('hash'),
                correlation.get('ip'),
                correlation.get('domain'),
                json.dumps(correlation.get('matched_signatures', []), sort_keys=True),
                json.dumps(correlation.get('matched_iocs', []), sort_keys=True),
                json.dumps(correlation.get('related_evidence_ids', []), sort_keys=True),
            ),
        )
        self.connection.commit()

    def save_risk_score(self, case_id: str, score: Dict[str, object]) -> None:
        self.connection.execute(
            '''
            INSERT OR REPLACE INTO risk_score(case_id, total_score, level, factors)
            VALUES (?, ?, ?, ?)
            ''',
            (
                case_id,
                score['total_score'],
                score['level'],
                json.dumps(score['factors'], sort_keys=True),
            ),
        )
        self.connection.commit()

    def save_quantum_result(self, case_id: str, found_evidence_id: Optional[str], probability: float) -> None:
        self.connection.execute(
            '''
            INSERT OR REPLACE INTO quantum_result(case_id, found_evidence_id, probability)
            VALUES (?, ?, ?)
            ''',
            (case_id, found_evidence_id, probability),
        )
        self.connection.commit()

    def load_case(self, case_id: str) -> Optional[Dict[str, object]]:
        cursor = self.connection.cursor()
        cursor.execute('SELECT case_id, investigator, created_at, updated_at FROM forensic_case WHERE case_id = ?', (case_id,))
        row = cursor.fetchone()
        if row is None:
            return None

        case_data = {
            'case_id': row[0],
            'investigator': row[1],
            'created_at': row[2],
            'updated_at': row[3],
        }

        cursor.execute('SELECT id, filename, sha256, source, collected_at, metadata FROM evidence WHERE case_id = ?', (case_id,))
        case_data['evidences'] = [
            Evidence(
                id=evidence_row[0],
                filename=evidence_row[1],
                sha256=evidence_row[2],
                source=evidence_row[3],
                collected_at=evidence_row[4],
                metadata=json.loads(evidence_row[5]),
            )
            for evidence_row in cursor.fetchall()
        ]

        cursor.execute('SELECT record_hash, evidence_id, created_by, schema_version, hash_algo, previous_hash, created_at, events FROM custody_record WHERE evidence_id IN (SELECT id FROM evidence WHERE case_id = ?)', (case_id,))
        case_data['chain_of_custody'] = [
            ChainOfCustodyRecord(
                evidence_id=record_row[1],
                created_by=record_row[2],
                schema_version=record_row[3],
                hash_algo=record_row[4],
                previous_hash=record_row[5],
                created_at=record_row[6],
                record_hash=record_row[0],
                events=json.loads(record_row[7]),
            )
            for record_row in cursor.fetchall()
        ]

        cursor.execute('SELECT event_id, timestamp_utc, description, details FROM timeline_event WHERE case_id = ?', (case_id,))
        case_data['timeline'] = [
            {
                'event_id': row[0],
                'timestamp_utc': row[1],
                'description': row[2],
                'details': json.loads(row[3]),
            }
            for row in cursor.fetchall()
        ]

        cursor.execute('SELECT hash_value, ip, domain, matched_signatures, matched_iocs, related_evidence_ids FROM ioc_correlation WHERE case_id = ?', (case_id,))
        row = cursor.fetchone()
        case_data['ioc_correlation'] = None
        if row:
            case_data['ioc_correlation'] = {
                'hash': row[0],
                'ip': row[1],
                'domain': row[2],
                'matched_signatures': json.loads(row[3]),
                'matched_iocs': json.loads(row[4]),
                'related_evidence_ids': json.loads(row[5]),
            }

        cursor.execute('SELECT total_score, level, factors FROM risk_score WHERE case_id = ?', (case_id,))
        row = cursor.fetchone()
        case_data['risk_score'] = None
        if row:
            case_data['risk_score'] = {
                'total_score': row[0],
                'level': row[1],
                'factors': json.loads(row[2]),
            }

        cursor.execute('SELECT found_evidence_id, probability FROM quantum_result WHERE case_id = ?', (case_id,))
        row = cursor.fetchone()
        case_data['quantum_result'] = None
        if row:
            case_data['quantum_result'] = {
                'found_evidence_id': row[0],
                'probability': row[1],
            }

        return case_data

    def export_case_json(self, case_id: str, output_path: str) -> None:
        case_data = self.load_case(case_id)
        if case_data is None:
            raise ValueError(f'Case {case_id} not found')

        serializable_case = {
            **case_data,
            'evidences': [e.to_dict() for e in case_data.get('evidences', [])],
            'chain_of_custody': [record.to_dict() for record in case_data.get('chain_of_custody', [])],
        }
        Path(output_path).write_text(json.dumps(serializable_case, indent=2, sort_keys=True), encoding='utf-8')

    def close(self) -> None:
        self.connection.close()
