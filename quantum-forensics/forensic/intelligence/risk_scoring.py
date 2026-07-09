from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class RiskScoreResult:
    total_score: int
    factors: Dict[str, int]
    level: str


def compute_risk_score(correlation: Dict[str, List[str]], evidence: Dict[str, str]) -> RiskScoreResult:
    """Compute a forensic risk score based on IOC correlation and evidence attributes."""
    score = 0
    factors: Dict[str, int] = {}

    if correlation.get('matched_signatures'):
        factors['known_malware_hash'] = 40
        score += 40

    if correlation.get('matched_iocs'):
        factors['related_ioc'] = 30
        score += 30

    suspicious = evidence.get('behavior', '')
    if suspicious:
        factors['suspicious_behavior'] = 20
        score += 20

    if evidence.get('source', '').lower() in ('unknown', 'desconhecido', ''):
        factors['unknown_origin'] = 10
        score += 10

    level = 'low'
    if score >= 80:
        level = 'high'
    elif score >= 50:
        level = 'medium'

    return RiskScoreResult(total_score=score, factors=factors, level=level)
