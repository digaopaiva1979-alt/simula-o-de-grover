from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .artifact import Artifact
from .evidence import Evidence
from .finding import Finding
from .ioc import IOC
from .timeline_event import TimelineEvent


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


@dataclass
class Case:
    case_id: str
    title: str
    description: str
    investigator: str
    status: str = "open"
    created_at: str = field(default_factory=_utc_timestamp)
    updated_at: str = field(default_factory=_utc_timestamp)
    evidences: List[Evidence] = field(default_factory=list)
    artifacts: List[Artifact] = field(default_factory=list)
    iocs: List[IOC] = field(default_factory=list)
    findings: List[Finding] = field(default_factory=list)
    timeline_events: List[TimelineEvent] = field(default_factory=list)
    risk_score: Optional[Dict[str, Any]] = None
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["evidences"] = [evidence.to_dict() for evidence in self.evidences]
        data["artifacts"] = [artifact.to_dict() for artifact in self.artifacts]
        data["iocs"] = [ioc.to_dict() for ioc in self.iocs]
        data["findings"] = [finding.to_dict() for finding in self.findings]
        data["timeline_events"] = [event.to_dict() for event in self.timeline_events]
        return data
