#!/usr/bin/env python3
"""Sincroniza os plugins enxutos a partir dos repositórios originais.

Uso: python3 -I scripts/sync.py [--repo-root .]

- Clona cada upstream (shallow) num diretório temporário.
- Recria plugins/<nome>/ apenas com as skills/agentes listados em sources.json.
- Grava UPSTREAM.lock.json (commit de origem de cada plugin).
- Gera SECURITY-SCAN.md com a varredura do conteúdo publicado.
- Atualiza .claude-plugin/marketplace.json.

Nada é executado a partir do código baixado: só arquivos .md/.json são copiados.
"""
import argparse
import datetime as dt
import fnmatch
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TEXT_SUFFIXES = {".md", ".json", ".txt"}
# Código que algumas skills executam (ex.: deploy-to-vercel, vercel-optimize).
# É copiado, mas sempre listado à parte na varredura para revisão humana.
CODE_SUFFIXES = {".sh", ".mjs", ".js", ".cjs", ".ts", ".py"}
ALLOWED_SUFFIXES = TEXT_SUFFIXES | CODE_SUFFIXES
RISK_PATTERNS = {
    "pipe-to-shell": r"(curl|wget)[^\n|]*\|\s*(ba|z)?sh",
    "rm -rf": r"rm\s+-rf\s+[/~$]",
    "eval": r"(?<![.\w])eval\s*\(|new Function\s*\(",
    "spawn de processo": r"child_process|execSync\s*\(|spawnSync?\s*\(",
    "base64 decode": r"base64\s+(-d|--decode)",
    "prompt injection": r"ignore (all |any )?(previous|prior) instructions|disregard (the|your) (system|previous)",
    "credential paths": r"~/\.ssh|~/\.aws|id_rsa|\.npmrc|\.netrc",
    "sudo": r"\bsudo\s",
}


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def excluded(path: Path, globs):
    return any(fnmatch.fnmatch(path.name, g) for g in globs)


def copy_tree(src: Path, dst: Path, globs, report):
    for f in sorted(src.rglob("*")):
        if f.is_dir() or excluded(f, globs) or ".git" in f.parts:
            continue
        rel = f.relative_to(src)
        if f.suffix.lower() not in ALLOWED_SUFFIXES:
            report["skipped"].append(f"{dst.name}/{rel}")
            continue
        out = dst / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, out)


def scan(plugin_dir: Path):
    hits, urls, code, endpoints = [], {}, [], []
    for f in sorted(plugin_dir.rglob("*")):
        if not f.is_file():
            continue
        text = f.read_text(errors="replace")
        for label, pat in RISK_PATTERNS.items():
            for m in re.finditer(pat, text, re.IGNORECASE):
                line = text.count("\n", 0, m.start()) + 1
                hits.append((label, f"{f.relative_to(plugin_dir)}:{line}"))
        for u in re.findall(r"https?://([A-Za-z0-9.-]+)", text):
            urls[u] = urls.get(u, 0) + 1
        if f.suffix.lower() in CODE_SUFFIXES:
            rel = str(f.relative_to(plugin_dir))
            code.append(rel)
            for u in sorted(set(re.findall(r"https?://[A-Za-z0-9.-]+[^\s\"'`)]*", text))):
                if not re.search(r"example\.com|localhost|127\.0\.0\.1", u):
                    endpoints.append((rel, u))
    return hits, urls, code, endpoints


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    args = ap.parse_args()
    root = Path(args.repo_root).resolve()
    cfg = json.loads((root / "sources.json").read_text())
    globs = cfg.get("exclude_globs", [])
    lock, entries, report_md = {}, [], []
    today = dt.date.today()
    new_version = f"{today.year}.{today.month * 100 + today.day}.0"
    lock_path = root / "UPSTREAM.lock.json"
    old_lock = json.loads(lock_path.read_text()) if lock_path.exists() else {}

    with tempfile.TemporaryDirectory() as tmp:
        for p in cfg["plugins"]:
            name = p["name"]
            src = Path(tmp) / name
            run(["git", "clone", "-q", "--depth", "1", p["upstream"], str(src)])
            sha = run(["git", "rev-parse", "HEAD"], cwd=src)
            prev = old_lock.get(name, {})
            # Só muda a versão quando o upstream mudou: evita PRs vazios.
            version = prev["version"] if prev.get("commit") == sha and prev.get("version") else new_version
            dst = root / "plugins" / name
            if dst.exists():
                shutil.rmtree(dst)
            (dst / ".claude-plugin").mkdir(parents=True)
            report = {"skipped": []}

            skills_root = src / p["skills_dir"]
            wanted = p["skills"]
            if wanted == "*":
                wanted = sorted(d.name for d in skills_root.iterdir() if (d / "SKILL.md").is_file())
            missing = [s for s in wanted if not (skills_root / s / "SKILL.md").is_file()]
            if missing:
                sys.exit(f"[{name}] skills ausentes no upstream: {missing}")
            for s in wanted:
                copy_tree(skills_root / s, dst / "skills" / s, globs, report)

            if p.get("agents_dir"):
                copy_tree(src / p["agents_dir"], dst / "agents", globs, report)
            if p.get("license_file") and (src / p["license_file"]).is_file():
                shutil.copy2(src / p["license_file"], dst / "LICENSE")

            manifest = {
                "name": name,
                "version": version,
                "description": p["description"],
                "author": {"name": p["author"]},
                "homepage": p["upstream"].removesuffix(".git"),
                "license": p["license"],
            }
            (dst / ".claude-plugin" / "plugin.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")

            lock[name] = {"upstream": p["upstream"], "commit": sha, "version": version, "skills": wanted}
            entries.append({
                "name": name,
                "source": f"./plugins/{name}",
                "description": p["description"],
                "version": version,
            })

            hits, urls, code, endpoints = scan(dst)
            report_md.append(f"## {name}\n\nUpstream: `{p['upstream']}` @ `{sha[:12]}`  \n"
                             f"Skills: {len(wanted)} · Agentes: {len(list((dst / 'agents').glob('*.md'))) if (dst / 'agents').exists() else 0}\n")
            report_md.append(f"Versão: `{version}`\n\n**Padrões de risco:** " + ("nenhum" if not hits else ""))
            for label, where in hits:
                report_md.append(f"- ⚠️ `{label}` em `{where}`")
            report_md.append("\n**Domínios citados:** " + ", ".join(f"{d} ({n})" for d, n in sorted(urls.items(), key=lambda x: (-x[1], x[0]))))
            if code:
                report_md.append(f"\n**⚙️ Código executável ({len(code)} arquivos)** — revise o diff destes com atenção:")
                by_skill = {}
                for c in code:
                    key = "/".join(c.split("/")[:2])
                    by_skill[key] = by_skill.get(key, 0) + 1
                report_md.extend(f"- `{k}`: {n} arquivo(s)" for k, n in sorted(by_skill.items()))
            if endpoints:
                report_md.append("\n**🌐 Endpoints chamados pelo código:**")
                report_md.extend(f"- `{u}` em `{w}`" for w, u in endpoints)
            if report["skipped"]:
                report_md.append("\n**Arquivos não-texto ignorados:** " + ", ".join(f"`{s}`" for s in report["skipped"]))
            report_md.append("")

    market = {
        "name": "grupo-ivm-plugins",
        "description": "Plugins do Grupo IVM: recortes revisados de oh-my-claudecode, Supabase e Vercel.",
        "owner": {"name": "VoIPMundoTelecom"},
        "plugins": entries,
    }
    (root / ".claude-plugin").mkdir(exist_ok=True)
    (root / ".claude-plugin" / "marketplace.json").write_text(json.dumps(market, indent=2, ensure_ascii=False) + "\n")
    (root / "UPSTREAM.lock.json").write_text(json.dumps(lock, indent=2) + "\n")
    (root / "SECURITY-SCAN.md").write_text("# Varredura de segurança\n\nGerada por `scripts/sync.py`. "
                                           "Revise antes de aprovar o PR.\n\n" + "\n".join(report_md) + "\n")
    print(json.dumps({k: v["commit"][:12] for k, v in lock.items()}))


if __name__ == "__main__":
    main()
