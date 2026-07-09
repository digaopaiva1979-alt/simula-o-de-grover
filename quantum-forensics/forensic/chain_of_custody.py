"""Simple chain of custody representation."""
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
from typing import List, Dict


@dataclass
class ChainOfCustodyRecord:
    evidence_id: str
    created_by: str
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    integrity_hash: str = ''
    events: List[Dict] = field(default_factory=list)

    def add_event(self, actor: str, action: str, note: str = ''):
        e = {'time': datetime.utcnow().isoformat(), 'actor': actor, 'action': action, 'note': note}
        self.events.append(e)

    def finalize(self):
        # Compute a simple integrity hash over the record's content
        s = (self.evidence_id + self.created_by + self.created_at + ''.join(str(e) for e in self.events)).encode('utf-8')
        self.integrity_hash = hashlib.sha256(s).hexdigest()
        return self.integrity_hash
