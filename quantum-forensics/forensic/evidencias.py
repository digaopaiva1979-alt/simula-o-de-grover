from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass
class Evidence:
    identifier: str
    filename: str
    hash: str
    origin: str
    integrity: str
    metadata: Dict[str, str]


def sample_evidences() -> List[Evidence]:
    """Return a small list of sample evidences for demonstration."""
    return [
        Evidence('EV-001', 'documento.pdf', 'a94a8fe5', 'imagem_forense.dd', 'válida', {'size': '2MB'}),
        Evidence('EV-002', 'foto.jpg', '5d41402a', 'disco02.img', 'válida', {'size': '4MB'}),
        Evidence('EV-003', 'script.sh', '9e107d9d', 'backup.tar', 'válida', {'size': '1KB'}),
        Evidence('EV-004', 'malware.bin', 'deadbeef', 'isolated.img', 'suspeita', {'size': '512KB'}),
    ]


def to_dict_list(evidences: List[Evidence]) -> List[Dict]:
    return [asdict(e) for e in evidences]
