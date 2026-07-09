from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


@dataclass
class IOC:
    ioc_id: str
    case_id: str
    ioc_type: str
    value: str
    description: Optional[str] = None
    severity: str = "medium"
    confidence: str = "medium"
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_utc_timestamp)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
