#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/manage_candidate.py
Gestionnaire du cycle de vie des candidatures 2027 :
- Ajouter un nouveau candidat sans casser l'ordre de l'Hémicycle ni les 12 matrices
- Archiver ou marquer un candidat comme "Retiré / Rallié"
- Lister l'état des candidatures (parti, orientation, budget, crash-score)
- Synchronise automatiquement les modifications vers l'ensemble des pages HTML (desktop & mobile)
"""

import sys
import io
import json
import argparse
from pathlib import Path

# Encodage UTF-8 universel
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
CANDS_PATH = DATA_DIR / "candidats.json"
THEMES_PATH = DATA_DIR / "thematiques.json"
POLLS_PATH = DATA_DIR / "sondages.json"

def list_candidates():
    """Affiche la liste ordonnée des candidats selon l'Hémicycle parlementaire."""
    if not CANDS_PATH.exists():
        print("Erreur : data/candidats.json introuvable.")
        return

    cands = json.loads(CANDS_PATH.read_text(encoding="utf-8"))
    print(f"\n=== CANDIDATS DE L'OBSERVATOIRE 2027 ({len(cands)} au total) ===")
    print(f"{'#':<3} {'Nom':<22} {'Parti':<25} {'Dépenses (An 5)':<16} {'Crash':<6} {'Statut':<18}")
    print("-" * 95)
    for i, c in enumerate(cands, 1):
        status = c.get("status_candidature", "En campagne")
        dep = f"{c.get('dep_an5', 0)} Mds €"
        score = c.get("crash_score", "N/A")
        print(f"{i:<3} {c['name']:<22} {c['parti']:<25} {dep:<16} {score:<6} {status:<18}")
    print("-" * 95)

def archive_candidate(candidate_name, reason="Retrait / Ralliement"):
    """Marque un candidat comme retiré/archivé sans supprimer ses données historiques."""
    if not CANDS_PATH.exists():
        return False

    cands = json.loads(CANDS_PATH.read_text(encoding="utf-8"))
    found = False

    for c in cands:
        if candidate_name.lower() in c["name"].lower():
            c["status_candidature"] = f"Retiré ({reason})"
            c["is_active"] = False
            found = True
            print(f"✓ Candidat '{c['name']}' marqué comme : Retiré ({reason})")
            break

    if not found:
        print(f"Erreur : Candidat '{candidate_name}' introuvable.")
        return False

    CANDS_PATH.write_text(json.dumps(cands, ensure_ascii=False, indent=2), encoding="utf-8")
    return True

def add_candidate(name, party, family, orientation, color, dep_an5=1550.0, def_pct=-3.5, crash_score="B", position=None):
    """Ajoute proprement un nouveau candidat dans la base data/candidats.json et thematiques.json."""
    if not CANDS_PATH.exists():
        return False

    cands = json.loads(CANDS_PATH.read_text(encoding="utf-8"))

    # Vérification doublon
    if any(c["name"].lower() == name.lower() for c in cands):
        print(f"Erreur : Le candidat '{name}' existe déjà.")
        return False

    folder_name = name
    new_candidate = {
        "name": name,
        "parti": party,
        "famille": family,
        "orientation": orientation,
        "color": color,
        "dep_an5": float(dep_an5),
        "def_an5": -100.0,
        "def_pct": float(def_pct),
        "crash_score": crash_score,
        "parr_status": "orange",
        "parr_label": "🟠 En cours de collecte (300-499)",
        "url_dir": f"./candidats/{folder_name}/index.html",
        "url_html": f"./candidats/{folder_name}/Visualisation_Programme_et_Comparatif_Budget_{name.replace(' ', '_')}.html",
        "url_xlsx": f"./candidats/{folder_name}/Chiffrage_Programme_{name.replace(' ', '_')}_2027.xlsx",
        "folder_name": folder_name,
        "real_xlsx": f"Chiffrage_Programme_{name.replace(' ', '_')}_2027.xlsx",
        "real_html": f"Visualisation_Programme_et_Comparatif_Budget_{name.replace(' ', '_')}.html",
        "is_primary": True,
        "status_candidature": "Candidat en campagne"
    }

    if position is not None and 0 <= position <= len(cands):
        cands.insert(position, new_candidate)
    else:
        cands.append(new_candidate)

    CANDS_PATH.write_text(json.dumps(cands, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ Candidat '{name}' ajouté avec succès dans data/candidats.json.")

    # Compléter thematiques.json si nécessaire pour maintenir la cohérence des 12 matrices
    if THEMES_PATH.exists():
        themes = json.loads(THEMES_PATH.read_text(encoding="utf-8"))
        updated_themes = False
        for t_key, t_val in themes.items():
            if isinstance(t_val, dict) and name not in t_val:
                t_val[name] = f"Mesures en cours de consolidation pour {name} ({party})."
                updated_themes = True
        if updated_themes:
            THEMES_PATH.write_text(json.dumps(themes, ensure_ascii=False, indent=2), encoding="utf-8")
            print("✓ Matrices thématiques complétées avec l'entrée du candidat.")

    return True

def main():
    parser = argparse.ArgumentParser(description="Gestion du cycle de vie des candidatures 2027")
    parser.add_argument("--list", action="store_true", help="Lister tous les candidats")
    parser.add_argument("--add", type=str, help="Nom du candidat à ajouter")
    parser.add_argument("--party", type=str, help="Parti ou mouvement politique")
    parser.add_argument("--family", type=str, default="Centre Républicain", help="Famille politique")
    parser.add_argument("--orientation", type=str, default="Réformisme", help="Orientation idéologique")
    parser.add_argument("--color", type=str, default="#3b82f6", help="Code couleur Hexadécimal")
    parser.add_argument("--dep", type=float, default=1550.0, help="Dépenses estimées An 5 (en Mds €)")
    parser.add_argument("--def-pct", type=float, default=-3.5, help="Déficit public estimé An 5 (en points de PIB)")
    parser.add_argument("--crash", type=str, default="B", help="Score Crash Test (A, B+, C, etc.)")
    parser.add_argument("--pos", type=int, default=None, help="Position dans l'hémicycle (0 = gauche max)")
    parser.add_argument("--archive", type=str, help="Nom du candidat à retirer/archiver")
    parser.add_argument("--reason", type=str, default="Retrait de candidature", help="Raison du retrait")
    parser.add_argument("--sync", action="store_true", default=True, help="Synchroniser le HTML après modification")

    args = parser.parse_args()

    if args.list:
        list_candidates()
        return

    modified = False
    if args.add and args.party:
        modified = add_candidate(
            name=args.add,
            party=args.party,
            family=args.family,
            orientation=args.orientation,
            color=args.color,
            dep_an5=args.dep,
            def_pct=args.def_pct,
            crash_score=args.crash,
            position=args.pos
        )
    elif args.archive:
        modified = archive_candidate(args.archive, args.reason)
    else:
        parser.print_help()
        return

    if modified and args.sync:
        import subprocess
        sync_script = ROOT / "scripts" / "sync_data.py"
        subprocess.run([sys.executable, str(sync_script)], check=False)

if __name__ == "__main__":
    main()
