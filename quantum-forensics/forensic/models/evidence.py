from __future__ import annotations
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict


def _utc_timestamp() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'


@dataclass
class Evidence:
    id: str
    filename: str
    sha256: str
    source: str
    collected_at: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def create(cls, id: str, filename: str, sha256: str, source: str, metadata: Dict[str, Any]) -> 'Evidence':
        return cls(id=id, filename=filename, sha256=sha256, source=source, collected_at=_utc_timestamp(), metadata=metadata)
