import json
import xml.etree.ElementTree as ET


def parse_json(data):
    if isinstance(data, str):
        data = json.loads(data)

    return data


def parse_xml(xml_text):
    root = ET.fromstring(xml_text)

    result = []

    for node in root.iter("calculation"):
        result.append({
            "name": node.attrib.get("name", "XML_CALC"),
            "formula": node.attrib.get("formula", "")
        })

    return result