"""Simple chain of custody representation."""
from dataclasses import dataclass, field, asdict
from datetime import datetime
import hashlib
import json
from typing import List, Dict, Optional


@dataclass
class ChainOfCustodyRecord:
    evidence_id: str
    created_by: str
    hash_algo: str = 'SHA-256'
    previous_hash: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    record_hash: str = ''
    events: List[Dict] = field(default_factory=list)

    def add_event(self, actor: str, action: str, note: str = ''):
        e = {'time': datetime.utcnow().isoformat(), 'actor': actor, 'action': action, 'note': note}
        self.events.append(e)

    def to_canonical(self) -> str:
        """Serialize the record deterministically (canonical JSON with sorted keys)."""
        # Build a canonical dict
        payload = {
            'evidence_id': self.evidence_id,
            'created_by': self.created_by,
            'hash_algo': self.hash_algo,
            'previous_hash': self.previous_hash,
            'created_at': self.created_at,
            'events': self.events,
        }
        return json.dumps(payload, separators=(',', ':'), sort_keys=True)

    def finalize(self) -> str:
        """Compute and store the SHA-256 hash of the canonical serialization."""
        canonical = self.to_canonical().encode('utf-8')
        self.record_hash = hashlib.sha256(canonical).hexdigest()
        return self.record_hash
