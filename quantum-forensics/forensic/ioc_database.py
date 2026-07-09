"""Simulated IOC (Indicators of Compromise) database for demos."""

from typing import Dict, List


def sample_iocs() -> Dict[str, List[str]]:
    """Return a simple dictionary of fake IOCs for demonstration."""
    return {
        'hashes': ['deadbeef', 'badc0ffee', 'a94a8fe5'],
        'ips': ['192.0.2.1', '198.51.100.23'],
        'domains': ['malicious.example', 'phish.example'],
        'signatures': ['MAL_SIG_001', 'MAL_SIG_ABC']
    }
