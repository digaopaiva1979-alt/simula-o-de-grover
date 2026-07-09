from pathlib import Path

from forensic.export.json_exporter import export_case_json
from forensic.export.stix_exporter import export_case_stix
from forensic.models.case import Case
from forensic.models.evidence import Evidence
from forensic.storage.repositories import CaseRepository


def test_exporters_generate_case_outputs(tmp_path: Path) -> None:
    repo = CaseRepository(str(tmp_path / "export.sqlite"))
    case = Case(case_id="case-003", title="Export case", description="desc", investigator="Bob", status="open")
    repo.create_case(case)
    repo.add_evidence(
        case.case_id,
        Evidence(
            evidence_id="ev-003",
            case_id=case.case_id,
            filename="sample.exe",
            original_path="/tmp/sample.exe",
            sha256="1234",
            source="disk",
            evidence_type="binary",
        ),
    )

    json_path = tmp_path / "case.json"
    export_case_json(repo, case.case_id, str(json_path))
    assert json_path.exists()

    stix_path = tmp_path / "case.stix.json"
    export_case_stix(repo, case.case_id, str(stix_path))
    assert stix_path.exists()
