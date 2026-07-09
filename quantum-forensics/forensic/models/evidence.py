from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


@dataclass
class Evidence:
    evidence_id: str = ""
    case_id: str = ""
    filename: str = ""
    original_path: str = ""
    sha256: str = ""
    source: str = ""
    evidence_type: str = "unknown"
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: Optional[str] = None

    def __post_init__(self) -> None:
        if self.created_at is None:
            self.created_at = _utc_timestamp()

    @property
    def id(self) -> str:
        return self.evidence_id

    @property
    def collected_at(self) -> Optional[str]:
        return self.created_at

    @classmethod
    def create(cls, id: str, filename: str, sha256: str, source: str, metadata: Dict[str, Any], case_id: str = "", evidence_type: str = "unknown", original_path: str = "") -> "Evidence":
        return cls(
            evidence_id=id,
            case_id=case_id,
            filename=filename,
            original_path=original_path or source,
            sha256=sha256,
            source=source,
            evidence_type=evidence_type,
            metadata=metadata,
            created_at=_utc_timestamp(),
        )

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["id"] = self.id
        data["collected_at"] = self.collected_at
        return data
