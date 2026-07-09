from .relationship_graph import RelationshipGraph


def export_graph_json(case, output_path):
    from ..graph import export_graph_json as legacy_export_graph_json

    return legacy_export_graph_json(case, output_path)


__all__ = ["RelationshipGraph", "export_graph_json"]
