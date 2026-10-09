#!/usr/bin/env python3
"""Valida a estrutura do marketplace antes de abrir o PR. Sai com código 1 se algo estiver errado."""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
errors = []

market = json.loads((root / ".claude-plugin" / "marketplace.json").read_text())
names = set()
for entry in market["plugins"]:
    name = entry["name"]
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        errors.append(f"nome inválido: {name}")
    pdir = root / entry["source"]
    manifest = pdir / ".claude-plugin" / "plugin.json"
    if not manifest.is_file():
        errors.append(f"{name}: plugin.json ausente")
        continue
    if json.loads(manifest.read_text()).get("name") != name:
        errors.append(f"{name}: nome no plugin.json diverge do marketplace")
    for skill in sorted((pdir / "skills").glob("*/")):
        md = skill / "SKILL.md"
        if not md.is_file():
            errors.append(f"{name}/{skill.name}: SKILL.md ausente")
            continue
        fm = re.match(r"^---\n(.*?)\n---", md.read_text(), re.S)
        if not fm or not re.search(r"(?m)^name:", fm.group(1)) or not re.search(r"(?m)^description:", fm.group(1)):
            errors.append(f"{name}/{skill.name}: frontmatter sem name/description")
        sname = re.search(r"(?m)^name:\s*\"?([^\"\n]+)", fm.group(1)).group(1).strip() if fm else ""
        if (name, sname) in names:
            errors.append(f"{name}: skill duplicada {sname}")
        names.add((name, sname))
    for agent in sorted((pdir / "agents").glob("*.md")) if (pdir / "agents").exists() else []:
        if not agent.read_text().startswith("---"):
            errors.append(f"{name}/agents/{agent.name}: sem frontmatter")

if errors:
    print("\n".join(f"✗ {e}" for e in errors))
    sys.exit(1)
print(f"✓ {len(market['plugins'])} plugins, {len(names)} skills válidas")
