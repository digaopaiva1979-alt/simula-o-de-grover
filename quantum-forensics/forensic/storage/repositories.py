from __future__ import annotations

from typing import Any, Dict, Optional

from ..models.artifact import Artifact
from ..models.case import Case
from ..models.evidence import Evidence
from ..models.finding import Finding
from ..models.ioc import IOC
from ..models.timeline_event import TimelineEvent
from .database import ForensicDatabase


class CaseRepository:
    def __init__(self, db_path: str = ":memory:"):
        self.db = ForensicDatabase(db_path)

    def create_case(self, case: Case) -> None:
        self.db.save_case(case.to_dict())

    def get_case(self, case_id: str) -> Optional[Case]:
        data = self.db.load_case(case_id)
        if data is None:
            return None

        case = Case(
            case_id=data["case_id"],
            title=data["title"],
            description=data["description"],
            investigator=data["investigator"],
            status=data["status"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            notes=data.get("notes", []),
        )
        case.evidences = [
            Evidence(
                evidence_id=item["evidence_id"],
                case_id=item["case_id"],
                filename=item["filename"],
                original_path=item["original_path"],
                sha256=item["sha256"],
                source=item["source"],
                evidence_type=item["evidence_type"],
                metadata=item.get("metadata", {}),
                created_at=item.get("created_at"),
            )
            for item in data.get("evidences", [])
        ]
        case.artifacts = [
            Artifact(
                artifact_id=item["artifact_id"],
                case_id=item["case_id"],
                evidence_id=item.get("evidence_id"),
                artifact_type=item["artifact_type"],
                name=item["name"],
                metadata=item.get("metadata", {}),
                created_at=item.get("created_at"),
            )
            for item in data.get("artifacts", [])
        ]
        case.iocs = [
            IOC(
                ioc_id=item["ioc_id"],
                case_id=item["case_id"],
                ioc_type=item["ioc_type"],
                value=item["value"],
                description=item.get("description"),
                severity=item["severity"],
                confidence=item["confidence"],
                metadata=item.get("metadata", {}),
                created_at=item.get("created_at"),
            )
            for item in data.get("iocs", [])
        ]
        case.findings = [
            Finding(
                finding_id=item["finding_id"],
                case_id=item["case_id"],
                title=item["title"],
                description=item["description"],
                severity=item["severity"],
                confidence=item["confidence"],
                evidence_ids=item.get("evidence_ids", []),
                metadata=item.get("metadata", {}),
                created_at=item.get("created_at"),
            )
            for item in data.get("findings", [])
        ]
        case.timeline_events = [
            TimelineEvent(
                event_id=item["event_id"],
                case_id=item["case_id"],
                event_type=item["event_type"],
                title=item["title"],
                description=item["description"],
                timestamp_utc=item["timestamp_utc"],
                metadata=item.get("metadata", {}),
                created_at=item.get("created_at"),
            )
            for item in data.get("timeline_events", [])
        ]
        return case

    def add_evidence(self, case_id: str, evidence: Evidence) -> None:
        self.db.save_evidence(evidence.to_dict())

    def add_artifact(self, case_id: str, artifact: Artifact) -> None:
        self.db.save_artifact(artifact.to_dict())

    def add_ioc(self, case_id: str, ioc: IOC) -> None:
        self.db.save_ioc(ioc.to_dict())

    def add_finding(self, case_id: str, finding: Finding) -> None:
        self.db.save_finding(finding.to_dict())

    def add_timeline_event(self, case_id: str, event: TimelineEvent) -> None:
        self.db.save_timeline_event(event.to_dict())

    def add_custody_record(self, case_id: str, record: Dict[str, Any]) -> None:
        self.db.save_custody_record(record)
