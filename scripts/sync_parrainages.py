#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/sync_parrainages.py
Outil de mise à jour et synchronisation des 500 Parrainages officiels (Conseil Constitutionnel) :
- Met à jour les décomptes et statuts (🔴 <300, 🟠 300-499, 🟢 500+ validés) dans data/candidats.json
- Met à jour le document récapitulatif candidats/ETAT_DES_PARRAINAGES_2027.md
- Synchronise automatiquement l'affichage sur mobile et desktop via scripts/sync_data.py
"""

import sys
import io
import json
import argparse
from pathlib import Path
from datetime import datetime

# Encodage universel UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
CANDS_PATH = DATA_DIR / "candidats.json"
MD_PATH = ROOT / "candidats" / "ETAT_DES_PARRAINAGES_2027.md"

def calculate_status(count):
    """Détermine le statut et le badge de parrainage selon le seuil légal des 500."""
    if count >= 500:
        return "green", f"🟢 {count} parrainages (seuil 500 validé)"
    elif count >= 300:
        return "orange", f"🟠 {count} parrainages (en voie de qualification)"
    else:
        return "red", f"🔴 {count} parrainages (<300 en difficulté)"

def update_candidate_parrainages(candidate_name, count):
    """Met à jour un candidat spécifique dans data/candidats.json."""
    if not CANDS_PATH.exists():
        print(f"Erreur : {CANDS_PATH} introuvable.")
        return False

    cands = json.loads(CANDS_PATH.read_text(encoding="utf-8"))
    found = False

    for c in cands:
        if candidate_name.lower() in c["name"].lower():
            color_status, label = calculate_status(count)
            c["parr_status"] = color_status
            c["parr_label"] = label
            c["parrainages_count"] = count
            found = True
            print(f"✓ Mis à jour : {c['name']} -> {label}")
            break

    if not found:
        print(f"Erreur : Aucun candidat correspondant à '{candidate_name}' trouvé.")
        return False

    CANDS_PATH.write_text(json.dumps(cands, ensure_ascii=False, indent=2), encoding="utf-8")
    return True

def generate_parrainages_markdown():
    """Régénère le document synthétique candidats/ETAT_DES_PARRAINAGES_2027.md."""
    if not CANDS_PATH.exists():
        return

    cands = json.loads(CANDS_PATH.read_text(encoding="utf-8"))
    now_str = datetime.now().strftime("%d/%m/%Y")

    greens = [c for c in cands if c.get("parr_status") == "green"]
    oranges = [c for c in cands if c.get("parr_status") == "orange"]
    reds = [c for c in cands if c.get("parr_status") == "red"]

    lines = [
        "# ÉTAT DES LIEUX DES PARRAINAGES - PRÉSIDENTIELLE 2027",
        f"*(Suivi officiel Conseil Constitutionnel • Actualisation du {now_str})*\n",
        "Chaque candidat doit recueillir au moins **500 parrainages valides** d'élus d'au moins 30 départements ou collectivités d'outre-mer différents pour que sa candidature soit validée par le Conseil constitutionnel.\n",
        "---",
        f"## 🟢 1. PARRAINAGES ASSURÉS / VALIDÉS (500+ ÉLUS) - {len(greens)} CANDIDATS",
        "Ces candidats ont franchi ou ont la garantie de franchir le seuil grâce à leur ancrage territorial :"
    ]
    for i, c in enumerate(greens, 1):
        lines.append(f"{i}. **{c['name']}** ({c['parti']}) : {c.get('parr_label', '500+ validés')}")

    lines.append("\n---")
    lines.append(f"## 🟠 2. EN BONNE VOIE (300 À 499 PARRAINAGES) - {len(oranges)} CANDIDATS")
    lines.append("Candidats en campagne active de signature auprès des maires :")
    for i, c in enumerate(oranges, 1):
        lines.append(f"{i}. **{c['name']}** ({c['parti']}) : {c.get('parr_label', 'En voie')}")

    lines.append("\n---")
    lines.append(f"## 🔴 3. EN DIFFICULTÉ (< 300 PARRAINAGES) - {len(reds)} CANDIDATS")
    lines.append("Risque réel de non-qualification par manque d'élus signataires :")
    for i, c in enumerate(reds, 1):
        lines.append(f"{i}. **{c['name']}** ({c['parti']}) : {c.get('parr_label', '<300')}")

    lines.append("\n---\n*Observatoire Indépendant des Candidats & Budgets 2027*")

    MD_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"✓ Fiche Markdown régénérée : {MD_PATH.name}")

def main():
    parser = argparse.ArgumentParser(description="Gestion et synchronisation des parrainages 2027")
    parser.add_argument("--candidate", type=str, help="Nom ou partie du nom du candidat")
    parser.add_argument("--count", type=int, help="Nombre de parrainages certifiés")
    parser.add_argument("--sync", action="store_true", default=True, help="Déclencher la synchronisation vers les pages HTML")

    args = parser.parse_args()

    if args.candidate and args.count is not None:
        if update_candidate_parrainages(args.candidate, args.count):
            generate_parrainages_markdown()
    else:
        # Simple récapitulatif
        print("=== ÉTAT ACTUEL DES PARRAINAGES ===")
        if CANDS_PATH.exists():
            cands = json.loads(CANDS_PATH.read_text(encoding="utf-8"))
            for c in cands:
                print(f"- {c['name']:<22} : {c.get('parr_label', 'N/A')}")

    # Synchronisation HTML
    if args.sync:
        import subprocess
        sync_script = ROOT / "scripts" / "sync_data.py"
        subprocess.run([sys.executable, str(sync_script)], check=False)

if __name__ == "__main__":
    main()
