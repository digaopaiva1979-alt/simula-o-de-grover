from forensic.models.artifact import Artifact
from forensic.models.case import Case
from forensic.models.evidence import Evidence
from forensic.models.finding import Finding
from forensic.models.ioc import IOC
from forensic.models.timeline_event import TimelineEvent


def test_model_serialization_and_defaults() -> None:
    case = Case(case_id="case-002", title="Case", description="desc", investigator="Alice", status="open")
    evidence = Evidence(
        evidence_id="ev-002",
        case_id="case-002",
        filename="sample.bin",
        original_path="/tmp/sample.bin",
        sha256="deadbeef",
        source="disk",
        evidence_type="binary",
    )
    artifact = Artifact(artifact_id="art-002", case_id="case-002", evidence_id="ev-002", artifact_type="analysis", name="sample")
    ioc = IOC(ioc_id="ioc-002", case_id="case-002", ioc_type="hash", value="deadbeef", severity="medium", confidence="medium")
    finding = Finding(finding_id="finding-002", case_id="case-002", title="Suspicious file", description="Detected", severity="medium", confidence="medium")
    timeline_event = TimelineEvent(event_id="event-002", case_id="case-002", event_type="analyzed", title="Analyzed", description="Test", timestamp_utc="2026-07-09T12:00:00Z")

    assert case.to_dict()["case_id"] == "case-002"
    assert evidence.to_dict()["filename"] == "sample.bin"
    assert artifact.to_dict()["name"] == "sample"
    assert ioc.to_dict()["value"] == "deadbeef"
    assert finding.to_dict()["severity"] == "medium"
    assert timeline_event.to_dict()["event_type"] == "analyzed"
