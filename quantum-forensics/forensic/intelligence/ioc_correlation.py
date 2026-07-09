from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional

from ..models.evidence import Evidence
from ..ioc_database import sample_iocs
from ..malware_signature import MalwareSignature, sample_signatures


@dataclass
class IocCorrelationResult:
    hash: Optional[str]
    ip: Optional[str]
    domain: Optional[str]
    matched_signatures: List[str]
    matched_iocs: List[str]
    related_evidence_ids: List[str]


def correlate_ioc(observed: Dict[str, str], evidences: List[Evidence]) -> IocCorrelationResult:
    """Correlate observed indicators with signatures, IOC database, and evidence."""
    hash_value = observed.get('hash')
    ip_value = observed.get('ip')
    domain_value = observed.get('domain')

    matched_signatures: List[str] = []
    matched_iocs: List[str] = []
    related_evidence_ids: List[str] = []

    if hash_value:
        for signature in sample_signatures():
            if signature.hex_pattern and signature.hex_pattern in hash_value:
                matched_signatures.append(signature.name)

    iocs = sample_iocs()
    if hash_value and hash_value in iocs.get('hashes', []):
        matched_iocs.append(f'hash:{hash_value}')
    if ip_value and ip_value in iocs.get('ips', []):
        matched_iocs.append(f'ip:{ip_value}')
    if domain_value and domain_value in iocs.get('domains', []):
        matched_iocs.append(f'domain:{domain_value}')

    for evidence in evidences:
        if hash_value and evidence.sha256 == hash_value:
            related_evidence_ids.append(evidence.id)
        if ip_value and evidence.metadata.get('source_ip') == ip_value:
            related_evidence_ids.append(evidence.id)
        if domain_value and evidence.metadata.get('domain') == domain_value:
            related_evidence_ids.append(evidence.id)

    return IocCorrelationResult(
        hash=hash_value,
        ip=ip_value,
        domain=domain_value,
        matched_signatures=matched_signatures,
        matched_iocs=matched_iocs,
        related_evidence_ids=list(dict.fromkeys(related_evidence_ids)),
    )
