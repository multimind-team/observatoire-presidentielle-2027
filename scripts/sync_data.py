#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/sync_data.py
Synchronise les données maîtres JSON (dossier data/) vers les pages HTML de l'Observatoire :
- data/candidats.json   -> index.html, PORTAIL_PRESIDENTIELLE_2027.html
- data/thematiques.json -> index.html, PORTAIL_PRESIDENTIELLE_2027.html
- data/sondages.json    -> comparatifs candidats/Observatoire_Sondages_2027.html
"""

import json
import re
import sys
import io
from pathlib import Path

# Assurer l'encodage UTF-8 même sous console Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

def sync_candidates_and_themes():
    cands_path = DATA_DIR / "candidats.json"
    themes_path = DATA_DIR / "thematiques.json"

    if not cands_path.exists() or not themes_path.exists():
        print("Erreur : fichiers data/candidats.json ou data/thematiques.json introuvables.")
        return

    cands_data = json.loads(cands_path.read_text(encoding="utf-8"))
    themes_data = json.loads(themes_path.read_text(encoding="utf-8"))

    cands_json_str = json.dumps(cands_data, ensure_ascii=False, indent=2)
    themes_json_str = json.dumps(themes_data, ensure_ascii=False)

    target_files = [ROOT / "index.html", ROOT / "PORTAIL_PRESIDENTIELLE_2027.html"]

    for tf in target_files:
        if not tf.exists():
            continue
        content = tf.read_text(encoding="utf-8")

        # 1. Remplacement de const cands
        s_cands = content.find("const cands = [")
        if s_cands != -1:
            e_cands = content.find("];", s_cands) + 2
            content = content[:s_cands] + f"const cands = {cands_json_str};" + content[e_cands:]

        # 2. Remplacement de const thematicMatrices
        s_tm = content.find("const thematicMatrices = {")
        if s_tm != -1:
            brace_count = 0
            end_pos = -1
            for i, ch in enumerate(content[s_tm + len("const thematicMatrices = "):]):
                if ch == "{":
                    brace_count += 1
                elif ch == "}":
                    brace_count -= 1
                    if brace_count == 0:
                        end_pos = s_tm + len("const thematicMatrices = ") + i + 1
                        break
            if end_pos != -1:
                content = content[:s_tm] + f"const thematicMatrices = {themes_json_str}" + content[end_pos:]

        tf.write_text(content, encoding="utf-8")
        print(f"✓ Synchronisé avec succès : {tf.name} ({len(cands_data)} candidats, {len(themes_data)} thématiques)")

def sync_polls():
    polls_path = DATA_DIR / "sondages.json"
    if not polls_path.exists():
        print("Erreur : data/sondages.json introuvable.")
        return

    polls_obj = json.loads(polls_path.read_text(encoding="utf-8"))
    polls_list = polls_obj.get("sondages", [])
    meta = polls_obj.get("metadata", {})

    target_file = ROOT / "comparatifs candidats" / "Observatoire_Sondages_2027.html"
    if not target_file.exists():
        print(f"Erreur : {target_file} introuvable.")
        return

    content = target_file.read_text(encoding="utf-8")

    # Formatage JS propre pour pollsData
    lines = ["[\n"]
    for item in polls_list:
        real_str = "true" if item.get("real", True) else "false"
        lines.append(f'            {{ name: "{item["name"]}", score: {item["score"]}, min: {item["min"]}, max: {item["max"]}, real: {real_str}, party: "{item["party"]}", color: "{item["color"]}" }},\n')
    lines_str = "".join(lines).rstrip(",\n") + "\n        ]"

    s_sond = content.find("const pollsData = [")
    if s_sond != -1:
        e_sond = content.find("];", s_sond) + 2
        content = content[:s_sond] + f"const pollsData = {lines_str};" + content[e_sond:]

    # Mise à jour date métadonnées dans la bannière si présente
    if "last_updated" in meta:
        content = re.sub(
            r'Dernière vague consolidée\s*:\s*[A-Za-z0-9\séèêëàâîïôùû]+202\d',
            f'Dernière vague consolidée : {meta["last_updated"]}',
            content
        )

    target_file.write_text(content, encoding="utf-8")
    print(f"✓ Synchronisé avec succès : Observatoire_Sondages_2027.html ({len(polls_list)} candidats sondés)")

def main():
    print("=== SYNCHRONISATION DES DONNÉES DU GRAND OBSERVATOIRE 2027 ===")
    sync_candidates_and_themes()
    sync_polls()
    print("=== TOUTES LES PAGES SONT À JOUR AVEC LE DOSSIER DATA/ ===")

if __name__ == "__main__":
    main()
