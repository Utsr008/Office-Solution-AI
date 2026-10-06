VISUAL_MAP = {
    "bar": "Clustered bar chart",
    "line": "Line chart",
    "area": "Area chart",
    "pie": "Pie chart",
    "donut": "Donut chart",
    "scatter": "Scatter chart",
    "table": "Table",
    "kpi": "KPI",
    "map": "Map"
}


def map_visual(metadata):

    visual_type = metadata["visual_type"].lower()

    return VISUAL_MAP.get(
        visual_type,
        "Needs manual review"
    )