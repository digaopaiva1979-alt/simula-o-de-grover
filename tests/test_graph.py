from forensic.graph.relationship_graph import RelationshipGraph


def test_relationship_graph_tracks_connections() -> None:
    graph = RelationshipGraph()
    graph.add_relationship("evidence-1", "ioc-1", "related_to")
    graph.add_relationship("evidence-1", "finding-1", "supports")
    graph.add_relationship("finding-1", "timeline-1", "derived_from")

    connections = graph.find_connections("evidence-1")
    assert any(connection["target"] == "ioc-1" and connection["relation"] == "related_to" for connection in connections)
    assert any(connection["target"] == "finding-1" and connection["relation"] == "supports" for connection in connections)

    exported = graph.export_graph()
    assert exported["nodes"][0]["id"] == "evidence-1"
    assert len(exported["edges"]) == 3
