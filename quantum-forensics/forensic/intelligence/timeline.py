from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict


def _utc_time() -> str:
    return datetime.utcnow().strftime('%H:%M')


@dataclass
class ForensicEvent:
    time: str
    description: str
    details: Dict[str, str]


def build_forensic_timeline(observed: Dict[str, str]) -> List[ForensicEvent]:
    """Build a simple simulated forensic timeline based on observed IOC data."""
    timeline: List[ForensicEvent] = [
        ForensicEvent(time='08:01', description='Arquivo coletado', details={'source': observed.get('source', 'imagem pericial')}),
        ForensicEvent(time='08:05', description='Hash calculado', details={'hash': observed.get('hash', '')}),
        ForensicEvent(time='08:07', description='IOC identificado', details={
            'ip': observed.get('ip', ''),
            'domain': observed.get('domain', ''),
        }),
        ForensicEvent(time='08:10', description='Busca Grover simulada', details={'status': 'executando'}),
        ForensicEvent(time='08:12', description='Resultado registrado', details={'status': 'concluído'}),
    ]
    return timeline
