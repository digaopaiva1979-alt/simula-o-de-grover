from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple


class RelationshipGraph:
    def __init__(self) -> None:
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, Any]] = []

    def add_relationship(self, source: str, target: str, relation: str) -> None:
        self.nodes.setdefault(source, {"id": source, "type": "node"})
        self.nodes.setdefault(target, {"id": target, "type": "node"})
        self.edges.append({"source": source, "target": target, "relation": relation})

    def find_connections(self, node_id: str) -> List[Dict[str, Any]]:
        return [edge for edge in self.edges if edge["source"] == node_id or edge["target"] == node_id]

    def export_graph(self) -> Dict[str, Any]:
        return {"nodes": list(self.nodes.values()), "edges": self.edges}
