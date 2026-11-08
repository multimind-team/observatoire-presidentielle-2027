#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/veille_sondages_hebdo.py
Script de veille multi-sources exécuté automatiquement chaque lundi à 18h (heure de Paris).
Sources surveillées :
1. Instituts de sondages (IFOP, Elabe, Ipsos, OpinionWay, Harris, Cluster17, Commission des sondages)
2. Sites officiels des 16 candidats & partis (programmes, déclarations)
3. Organismes d'évaluation et de chiffrage budgétaire (Institut Montaigne, iFRAP, OFCE, FIPECO, Cour des Comptes)
4. Flux d'actualités politiques et économiques (Le Monde, France Info, Le Figaro, Libération)
"""

import os
import sys
import io
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

# Encodage UTF-8 universel
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 ObservatoirePresidentielle2027/2.0"
}

# Mots-clés de détection thématique
POLL_KEYWORDS = [
    "sondage", "sondages", "intention de vote", "intentions de vote",
    "ifop", "elabe", "ipsos", "opinionway", "harris", "bva", "cluster17",
    "premier tour", "second tour"
]

CANDIDATE_KEYWORDS = [
    "candidat", "candidature", "déclaré", "programme", "présidentielle",
    "retrait", "primaire", "campagne", "meeting", "parrainage", "parrainages"
]

BUDGET_KEYWORDS = [
    "chiffrage", "budget", "dette", "déficit", "dépenses publiques", "impôt",
    "fiscalité", "montaigne", "ifrap", "ofce", "fipeco", "cour des comptes",
    "pouvoir d'achat", "retraites", "smic", "cotisations"
]

def load_sources_catalog():
    """Charge l'annuaire des sources depuis data/sources_veille.json."""
    catalog_path = DATA_DIR / "sources_veille.json"
    if catalog_path.exists():
        try:
            return json.loads(catalog_path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[Avertissement] Erreur de lecture de sources_veille.json : {e}")
    return {}

def scan_rss_feed(source_name, url, timeout=8):
    """Scanne un flux RSS donné et extrait les éléments pertinents."""
    items_out = []
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            xml_data = resp.read()
            root = ET.fromstring(xml_data)
            items = root.findall(".//item")
            for it in items[:25]:
                title = (it.find("title").text or "").strip() if it.find("title") is not None else ""
                desc = (it.find("description").text or "").strip() if it.find("description") is not None else ""
                link = (it.find("link").text or "").strip() if it.find("link") is not None else ""
                pub_date = (it.find("pubDate").text or "").strip() if it.find("pubDate") is not None else ""

                if not title:
                    continue

                combined = (title + " " + desc).lower()
                
                # Catégorisation
                is_poll = any(kw in combined for kw in POLL_KEYWORDS)
                is_cand = any(kw in combined for kw in CANDIDATE_KEYWORDS)
                is_budget = any(kw in combined for kw in BUDGET_KEYWORDS)

                if is_poll or is_cand or is_budget:
                    category = "Sondages" if is_poll else ("Budget & Chiffrage" if is_budget else "Candidats & Programmes")
                    items_out.append({
                        "source": source_name,
                        "title": title,
                        "link": link,
                        "date": pub_date,
                        "category": category
                    })
    except Exception as e:
        print(f"  [Info] Flux '{source_name}' ({url}) non accessible ({e}), ignoré.")
    return items_out

def check_institutes_and_budget_nodes(sources_catalog):
    """Effectue un test de disponibilité (ping HTTP) des instituts et think tanks majeurs."""
    checks = []
    to_check = []
    
    # Instituts
    for inst in sources_catalog.get("instituts_sondages", []):
        to_check.append(("Institut", inst["nom"], inst["url"]))
    # Think tanks
    for org in sources_catalog.get("organismes_chiffrage_budgetaire", []):
        to_check.append(("Chiffrage", org["nom"], org["url"]))

    print(f"-> Contrôle de connectivité sur {len(to_check)} portails de référence (Instituts & Think Tanks)...")
    for category, name, url in to_check:
        status_code = None
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=5) as resp:
                status_code = resp.getcode()
        except Exception as e:
            status_code = getattr(e, "code", "Non joignable")

        checks.append({
            "category": category,
            "name": name,
            "url": url,
            "status": "Accessible (200)" if status_code == 200 else f"Code {status_code}"
        })
    return checks

def perform_global_veille():
    """Exécute l'ensemble du cycle de veille hebdomadaire multi-sources."""
    catalog = load_sources_catalog()
    all_alerts = []

    print("-> Scan des flux de presse et publications politiques...")
    # 1. Flux de presse générale
    for item in catalog.get("flux_presse", []):
        if item.get("url"):
            alerts = scan_rss_feed(item["source"], item["url"])
            all_alerts.extend(alerts)

    # 2. Flux directs des candidats / partis ayant un feed RSS
    for c in catalog.get("sites_candidats", []):
        if c.get("feed"):
            c_name = f"{c['candidat']} ({c['parti']})"
            alerts = scan_rss_feed(c_name, c["feed"])
            all_alerts.extend(alerts)

    # Déduplication par titre
    seen_titles = set()
    deduped_alerts = []
    for a in all_alerts:
        normalized_title = a["title"].strip().lower()
        if normalized_title not in seen_titles:
            seen_titles.add(normalized_title)
            deduped_alerts.append(a)

    print(f"-> {len(deduped_alerts)} alertes pertinentes identifiées (Sondages, Candidats, Chiffrage).")

    # 3. Vérification des portails institutionnels (Instituts & Chiffrage)
    connectivity_checks = check_institutes_and_budget_nodes(catalog)

    return catalog, deduped_alerts, connectivity_checks

def update_database_metadata(catalog, alerts):
    """Met à jour data/sondages.json avec les nouvelles métadonnées de veille."""
    sondages_path = DATA_DIR / "sondages.json"
    cands_path = DATA_DIR / "candidats.json"
    themes_path = DATA_DIR / "thematiques.json"

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sond_obj = json.loads(sondages_path.read_text(encoding="utf-8")) if sondages_path.exists() else {"sondages": [], "metadata": {}}
    sond_list = sond_obj.get("sondages", [])
    
    # Mise à jour des métadonnées étendues
    sond_obj["metadata"]["derniere_veille_automatique"] = now_str
    sond_obj["metadata"]["statut_veille"] = "Veille automatisée multi-sources (Lundi 18h) : Presse, Instituts, Partis, Think Tanks"
    sond_obj["metadata"]["sources_surveillees"] = {
        "nb_instituts_sondages": len(catalog.get("instituts_sondages", [])),
        "nb_candidats_partis": len(catalog.get("sites_candidats", [])),
        "nb_organismes_chiffrage": len(catalog.get("organismes_chiffrage_budgetaire", [])),
        "nb_flux_presse": len(catalog.get("flux_presse", []))
    }
    
    if alerts:
        sond_obj["metadata"]["dernieres_alertes_detectees"] = [
            f"[{a['category']}] {a['title']} ({a['source']})" for a in alerts[:8]
        ]

    sondages_path.write_text(json.dumps(sond_obj, ensure_ascii=False, indent=2), encoding="utf-8")

    cands_list = json.loads(cands_path.read_text(encoding="utf-8")) if cands_path.exists() else []
    themes_dict = json.loads(themes_path.read_text(encoding="utf-8")) if themes_path.exists() else {}

    return {
        "timestamp": now_str,
        "nb_cands": len(cands_list),
        "nb_polls": len(sond_list),
        "nb_themes": len(themes_dict),
        "top_candidates": sorted(sond_list, key=lambda x: x.get("score", 0), reverse=True)[:5],
        "alerts": alerts
    }

def generate_markdown_report(catalog, report_data, connectivity_checks):
    """Génère le rapport de veille structuré multi-sources pour GitHub Step Summary."""
    lines = []
    lines.append("# 🇫🇷 Rapport de Veille Multi-Sources — Observatoire Présidentielle 2027")
    lines.append(f"*Exécution hebdomadaire automatisée (Lundi 18h00 Paris) • Horodatage : `{report_data['timestamp']}`*\n")
    
    lines.append("## 📊 1. État de l'Observatoire")
    lines.append(f"- **Candidats déclarés audités :** `{report_data['nb_cands']}`")
    lines.append(f"- **Candidats suivis dans le baromètre des intentions de vote :** `{report_data['nb_polls']}`")
    lines.append(f"- **Matrices thématiques et chiffrages comparatifs :** `{report_data['nb_themes']}` axes budgétaires consolidés")
    lines.append("")

    lines.append("## 📈 2. Intentions de Vote Consolidées (Top 5 - 1er Tour)")
    lines.append("| Candidat | Parti | Score moyen | Fourchette (IC 95%) | Statut |")
    lines.append("| :--- | :--- | :---: | :---: | :---: |")
    for c in report_data["top_candidates"]:
        status = "✅ Déclaré" if c.get("real") else "Hypothèse"
        lines.append(f"| **{c['name']}** | {c['party']} | **{c['score']} %** | [{c['min']} % - {c['max']} %] | {status} |")
    lines.append("")

    # Alertes par catégorie
    alerts_by_cat = {"Sondages": [], "Candidats & Programmes": [], "Budget & Chiffrage": []}
    for a in report_data["alerts"]:
        cat = a.get("category", "Sondages")
        alerts_by_cat.setdefault(cat, []).append(a)

    lines.append("## 🚨 3. Alertes Détectées dans la Semaine")
    for cat_name, cat_alerts in alerts_by_cat.items():
        if cat_alerts:
            lines.append(f"### {cat_name} ({len(cat_alerts)})")
            for a in cat_alerts[:5]:
                safe_title = a['title'].replace("|", "-")
                lines.append(f"- [{safe_title}]({a['link']}) — *{a['source']}*")
            lines.append("")

    lines.append("## 🏛️ 4. Répertoire des Sources Officielles Surveillées")
    lines.append("### A. Instituts de Sondage & Contrôle Officiel")
    for inst in catalog.get("instituts_sondages", []):
        lines.append(f"- **[{inst['nom']}]({inst['url']})** : {inst['role']}")
    lines.append("")

    lines.append("### B. Think Tanks & Organismes de Chiffrage Budgétaire")
    for org in catalog.get("organismes_chiffrage_budgetaire", []):
        lines.append(f"- **[{org['nom']}]({org['url']})** : {org['role']}")
    lines.append("")

    lines.append("### C. Sites Officiels des Candidats & Partis")
    c_links = [f"[{c['candidat']} ({c['parti']})]({c['url']})" for c in catalog.get("sites_candidats", [])]
    lines.append(" • ".join(c_links))
    lines.append("")

    lines.append("> [!TIP]")
    lines.append("> **Mise à jour des scores ou des données :** Éditez directement `data/sondages.json` ou `data/candidats.json` sur GitHub, ou formulez votre demande en langage naturel à l'agent IA.")

    md_content = "\n".join(lines)

    github_summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if github_summary_path:
        try:
            with open(github_summary_path, "a", encoding="utf-8") as f:
                f.write(md_content + "\n")
            print("-> Rapport de veille injecté dans GITHUB_STEP_SUMMARY.")
        except Exception as e:
            print(f"  [Avertissement] GITHUB_STEP_SUMMARY non accessible : {e}")

    return md_content

def main():
    print("=== DÉBUT DE LA VEILLE MULTI-SOURCES (LUNDI 18H) ===")
    catalog, alerts, connectivity_checks = perform_global_veille()
    report_data = update_database_metadata(catalog, alerts)
    md = generate_markdown_report(catalog, report_data, connectivity_checks)
    print("\n--- RAPPORT SYNTHÉTIQUE ---")
    print(md[:700] + "\n...")
    print("=== FIN DE LA VEILLE MULTI-SOURCES ===")

if __name__ == "__main__":
    main()
