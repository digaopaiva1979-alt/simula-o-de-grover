from dataclasses import asdict
from typing import Dict, List

from .models.evidence import Evidence


def sample_evidences() -> List[Evidence]:
    """Return a small list of sample evidences for demonstration."""
    return [
        Evidence.create('EV-001', 'documento.pdf', 'a94a8fe5', 'imagem_forense.dd', {'integrity': 'válida', 'size': '2MB'}),
        Evidence.create('EV-002', 'foto.jpg', '5d41402a', 'disco02.img', {'integrity': 'válida', 'size': '4MB'}),
        Evidence.create('EV-003', 'script.sh', '9e107d9d', 'backup.tar', {'integrity': 'válida', 'size': '1KB'}),
        Evidence.create('EV-004', 'malware.bin', 'deadbeef', 'isolated.img', {'integrity': 'suspeita', 'size': '512KB'}),
    ]


def to_dict_list(evidences: List[Evidence]) -> List[Dict]:
    return [e.to_dict() for e in evidences]
