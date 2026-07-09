from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


@dataclass
class TimelineEvent:
    event_id: str
    case_id: str
    event_type: str
    title: str
    description: str
    timestamp_utc: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_utc_timestamp)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
