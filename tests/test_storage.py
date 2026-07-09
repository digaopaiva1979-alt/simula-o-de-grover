from pathlib import Path

from forensic.models.artifact import Artifact
from forensic.models.case import Case
from forensic.models.evidence import Evidence
from forensic.models.finding import Finding
from forensic.models.ioc import IOC
from forensic.models.timeline_event import TimelineEvent
from forensic.storage.repositories import CaseRepository


def test_case_persistence_and_recovery(tmp_path: Path) -> None:
    db_path = tmp_path / "case.sqlite"
    repository = CaseRepository(str(db_path))

    case = Case(
        case_id="case-001",
        title="Phishing Investigation",
        description="Investigate suspicious email",
        investigator="Dr. Ada",
        status="open",
    )
    repository.create_case(case)

    evidence = Evidence(
        evidence_id="ev-001",
        case_id="case-001",
        filename="invoice.pdf",
        original_path="/tmp/invoice.pdf",
        sha256="abc123",
        source="email",
        evidence_type="document",
        metadata={"size": 2048},
    )
    repository.add_evidence(case.case_id, evidence)

    artifact = Artifact(
        artifact_id="art-001",
        case_id="case-001",
        evidence_id="ev-001",
        artifact_type="derived",
        name="invoice-analysis",
        metadata={"analysis": "pdf parser"},
    )
    repository.add_artifact(case.case_id, artifact)

    ioc = IOC(
        ioc_id="ioc-001",
        case_id="case-001",
        ioc_type="domain",
        value="malicious.example",
        description="Known phishing domain",
        severity="high",
        confidence="high",
    )
    repository.add_ioc(case.case_id, ioc)

    finding = Finding(
        finding_id="finding-001",
        case_id="case-001",
        title="Credential harvesting",
        description="The document contains phishing instructions",
        severity="high",
        confidence="high",
        evidence_ids=["ev-001"],
    )
    repository.add_finding(case.case_id, finding)

    timeline_event = TimelineEvent(
        event_id="event-001",
        case_id="case-001",
        event_type="received",
        title="Email received",
        description="Suspicious email arrived",
        timestamp_utc="2026-07-09T12:00:00Z",
    )
    repository.add_timeline_event(case.case_id, timeline_event)

    loaded_case = repository.get_case("case-001")

    assert loaded_case is not None
    assert loaded_case.case_id == case.case_id
    assert loaded_case.title == case.title
    assert len(loaded_case.evidences) == 1
    assert loaded_case.evidences[0].filename == "invoice.pdf"
    assert len(loaded_case.artifacts) == 1
    assert loaded_case.artifacts[0].name == "invoice-analysis"
    assert len(loaded_case.iocs) == 1
    assert loaded_case.iocs[0].value == "malicious.example"
    assert len(loaded_case.findings) == 1
    assert loaded_case.findings[0].title == "Credential harvesting"
    assert len(loaded_case.timeline_events) == 1
    assert loaded_case.timeline_events[0].title == "Email received"
