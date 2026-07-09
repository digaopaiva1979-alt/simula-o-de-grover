"""Simple chain of custody representation."""
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import json
from typing import List, Dict, Optional


def _utc_timestamp() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'


@dataclass
class ChainOfCustodyRecord:
    evidence_id: str
    created_by: str
    schema_version: str = '1.0'
    hash_algo: str = 'SHA-256'
    previous_hash: Optional[str] = None
    created_at: str = field(default_factory=_utc_timestamp)
    record_hash: str = ''
    events: List[Dict] = field(default_factory=list)

    def add_event(
        self,
        operator: str,
        action: str,
        note: str = '',
        tool_version: str = '',
        timestamp_utc: Optional[str] = None,
    ):
        if timestamp_utc is None:
            timestamp_utc = _utc_timestamp()
        event_id = hashlib.sha256(f'{operator}-{action}-{note}-{timestamp_utc}-{tool_version}'.encode('utf-8')).hexdigest()
        e = {
            'event_id': event_id,
            'timestamp_utc': timestamp_utc,
            'operator': operator,
            'action': action,
            'note': note,
            'tool_version': tool_version,
        }
        self.events.append(e)

    def to_canonical(self) -> str:
        """Serialize the record deterministically (canonical JSON with sorted keys)."""
        payload = {
            'created_at': self.created_at,
            'created_by': self.created_by,
            'evidence_id': self.evidence_id,
            'hash_algo': self.hash_algo,
            'previous_hash': self.previous_hash,
            'schema_version': self.schema_version,
            'events': self.events,
        }
        return json.dumps(payload, separators=(',', ':'), sort_keys=True)

    def finalize(self) -> str:
        """Compute and store the SHA-256 hash of the canonical serialization."""
        canonical = self.to_canonical().encode('utf-8')
        self.record_hash = hashlib.sha256(canonical).hexdigest()
        return self.record_hash
