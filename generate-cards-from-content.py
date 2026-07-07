"""
Generate index.html from injecting definitions.yaml content into input.html.

Uses Jinaj2 for injection. Requires pyyaml.
"""

from pathlib import Path
from collections import defaultdict

import yaml
from jinja2 import Environment, FileSystemLoader

data = yaml.safe_load(Path("definitions.yaml").read_text())
groups = defaultdict(list)

for item in data["definitions"]:
    groups[item["term"]].append(item)

cards = []

for term, defs in groups.items():
    cards.append(
        {
            "term": term,
            "subtitle": defs[0].get("subtitle"),
            "image": defs[0].get("image"),
            "definitions": [d["definition"] for d in defs],
        }
    )

cards.sort(key=lambda c: c["term"])

env = Environment(loader=FileSystemLoader("."))
template = env.get_template("template.html")
html = template.render(
    page_title=data["page_title"],
    page_subtitle=data["page_subtitle"],
    cards=cards
)

Path("index.html").write_text(html)

print("Generated index.html")
