#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/sync_data.py
Synchronise les données maîtres JSON (dossier data/) vers les pages HTML de l'Observatoire :
- data/candidats.json   -> index.html, PORTAIL_PRESIDENTIELLE_2027.html
- data/thematiques.json -> index.html, PORTAIL_PRESIDENTIELLE_2027.html
- data/sondages.json    -> comparatifs candidats/Observatoire_Sondages_2027.html, index.html, PORTAIL_PRESIDENTIELLE_2027.html
Optimisé 100% Mobile & Responsive (aucun débordement, accordéons tactiles légers).
"""

import json
import re
import sys
import io
from pathlib import Path
from datetime import datetime

# Assurer l'encodage UTF-8 même sous console Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

def format_french_date(date_str=None):
    """Convertit une date en format français lisible (ex: 8 Novembre 2026)."""
    months = [
        "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
    ]
    if not date_str:
        now = datetime.now()
        return f"{now.day} {months[now.month - 1]} {now.year}"
    try:
        dt = datetime.strptime(date_str.split()[0], "%Y-%m-%d")
        return f"{dt.day} {months[dt.month - 1]} {dt.year}"
    except Exception:
        return date_str

def sync_candidates_and_themes():
    cands_path = DATA_DIR / "candidats.json"
    themes_path = DATA_DIR / "thematiques.json"
    sondages_path = DATA_DIR / "sondages.json"

    if not cands_path.exists() or not themes_path.exists():
        print("Erreur : fichiers data/candidats.json ou data/thematiques.json introuvables.")
        return

    cands_data = json.loads(cands_path.read_text(encoding="utf-8"))
    themes_data = json.loads(themes_path.read_text(encoding="utf-8"))
    
    sond_obj = json.loads(sondages_path.read_text(encoding="utf-8")) if sondages_path.exists() else {}
    meta = sond_obj.get("metadata", {})
    last_update_str = format_french_date(meta.get("last_updated"))
    alerts = meta.get("dernieres_alertes_detectees", [])[:5]

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

        # 3. Mise à jour du badge date dans le hero (mobile friendly)
        nb_c = len(cands_data)
        nb_green = sum(1 for c in cands_data if c.get("parr_status") == "green")
        nb_orange = sum(1 for c in cands_data if c.get("parr_status") == "orange")
        nb_red = sum(1 for c in cands_data if c.get("parr_status") == "red")

        content = re.sub(
            r'<title>Portail Officiel : Observatoire des Programmes & Budgets Présidentielle 2027 \([^)]+\)</title>',
            f'<title>Portail Officiel : Observatoire des Programmes & Budgets Présidentielle 2027 ({nb_c} Candidats)</title>',
            content
        )
        content = re.sub(
            r'simulation citoyenne pour les \d+ candidats déclarés à la présidentielle 2027',
            f'simulation citoyenne pour les {nb_c} candidats déclarés à la présidentielle 2027',
            content
        )
        content = re.sub(
            r'Programmes & Budgets des \d+ Candidats Déclarés',
            f'Programmes & Budgets des {nb_c} Candidats Déclarés',
            content
        )
        content = re.sub(
            r'crash-tests souverains des \d+ candidats déclarés',
            f'crash-tests souverains des {nb_c} candidats déclarés',
            content
        )

        content = re.sub(
            r'🟢 Plateforme actualisée\s*:\s*[^•<]+•\s*Périmètre exclusif des (\d+) candidats déclarés',
            f'🟢 Plateforme actualisée : {last_update_str} • Périmètre exclusif des {nb_c} candidats déclarés',
            content
        )
        content = re.sub(
            r'<div class="num" id="heroCandCount">\d+</div>',
            f'<div class="num" id="heroCandCount">{nb_c}</div>',
            content
        )
        content = re.sub(
            r'<div class="num">\d+</div>\s*<div class="lbl">Candidats Déclarés en Lice</div>',
            f'<div class="num" id="heroCandCount">{nb_c}</div>\n                    <div class="lbl">Candidats Déclarés en Lice</div>',
            content
        )
        content = re.sub(r'Ordre officiel Hémicycle \([^)]+\)', f'Ordre officiel Hémicycle (<span id="hemicycleCandCount">{nb_c}</span>)', content)
        content = re.sub(r'Les <strong>\d+ candidats déclarés</strong>', f'Les <strong>{nb_c} candidats déclarés</strong>', content)
        content = re.sub(r'👥 Les [^<]*Candidats', f'👥 Les <span id="titleCandCount">{nb_c}</span> Candidats', content)
        content = re.sub(r'Affichage : \d+ candidats déclarés en lice \(par défaut\)', f'Affichage : {nb_c} candidats déclarés en lice (par défaut)', content)
        content = re.sub(r'statusLabel = "\d+ candidats déclarés en lice";', f'statusLabel = "{nb_c} candidats déclarés en lice";', content)

        # Filtres et Comparateur Thématique dynamiques (Image utilisateur)
        content = re.sub(r'id="labelFilterParrainages">🎯 Filtrer par Parrainages[^<]*:</span>', f'id="labelFilterParrainages">🎯 Filtrer par Parrainages ({nb_c} Candidats Déclarés) :</span>', content)
        content = re.sub(r'id="btnFilterAll"[^>]*>[^<]+</button>', f'id="btnFilterAll" onclick="filterCands(\'all\')">🎯 Tous les {nb_c} Candidats Déclarés</button>', content)
        content = re.sub(r'id="btnFilterGreen"[^>]*>[^<]+</button>', f'id="btnFilterGreen" onclick="filterCands(\'green\')">🟢 500+ parrainages validés ({nb_green})</button>', content)
        content = re.sub(r'id="btnFilterOrange"[^>]*>[^<]+</button>', f'id="btnFilterOrange" onclick="filterCands(\'orange\')">🟠 300-499 en bonne voie ({nb_orange})</button>', content)
        content = re.sub(r'id="btnFilterRed"[^>]*>[^<]+</button>', f'id="btnFilterRed" onclick="filterCands(\'red\')">🔴 &lt;300 en difficulté ({nb_red})</button>', content)
        content = re.sub(r'id="labelCompareTheme">⚡ Comparer instantanément les[^<]*:</span>', f'id="labelCompareTheme">⚡ Comparer instantanément les {nb_c} candidats sur un thème clé :</span>', content)
        content = re.sub(r'Comparatif Transversal Instantané \(\d+ Candidats Déclarés\)', f'Comparatif Transversal Instantané ({nb_c} Candidats Déclarés)', content)
        content = re.sub(r'comparant les \d+ candidats en lice sur 10 graphiques', f'comparant les {nb_c} candidats en lice sur 10 graphiques', content)
        content = re.sub(r'Bases Excel Maîtres Consolidées \(\d+ Candidats Déclarés\)', f'Bases Excel Maîtres Consolidées ({nb_c} Candidats Déclarés)', content)
        content = re.sub(r'Plateforme Budgétaire & Stratégique \(\d+ Candidats Déclarés\)', f'Plateforme Budgétaire & Stratégique ({nb_c} Candidats Déclarés)', content)

        # 4. Injection du bloc Accordéon Veille en direct (Mobile First) si non présent
        if 'id="liveVeilleBox"' not in content:
            # Générer les items HTML pour les alertes
            alerts_html_items = []
            for a in alerts:
                # Échapper pour affichage HTML propre
                safe_a = a.replace("<", "&lt;").replace(">", "&gt;")
                alerts_html_items.append(
                    f'<div style="padding:6px 10px; background:rgba(30,41,59,0.6); border-radius:6px; border-left:3px solid #38bdf8; font-size:11.5px; line-height:1.4; color:#e2e8f0;">{safe_a}</div>'
                )
            rendered_alerts = "\n".join(alerts_html_items) if alerts_html_items else '<div style="color:#94a3b8; font-size:11.5px;">Aucune alerte critique ces dernières 24h. Prochaine veille lundi 18h.</div>'

            veille_block = f'''
        <!-- BLOC VEILLE MULTI-SOURCES EN DIRECT (OPTIMISÉ MOBILE) -->
        <div class="live-veille-box" id="liveVeilleBox" style="background:rgba(15,23,42,0.85); border:1px solid #334155; border-radius:12px; padding:10px 14px; margin-bottom:18px; max-width:100%; box-sizing:border-box;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                <div style="display:flex; align-items:center; gap:8px; font-size:12px; font-weight:700; color:#38bdf8;">
                    <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#10b981; box-shadow:0 0 6px #10b981;"></span>
                    <span>Veille Multi-Sources Active (Lundi 18h)</span>
                </div>
                <button type="button" onclick="toggleLiveVeille()" id="btnToggleVeille" style="background:#1e293b; border:1px solid #475569; color:#f8fafc; padding:5px 11px; border-radius:6px; font-size:11px; font-weight:700; cursor:pointer; display:inline-flex; align-items:center; gap:5px; -webkit-tap-highlight-color:transparent;">
                    📰 5 Dernières Alertes & Sondages <span id="chevronVeille">▼</span>
                </button>
            </div>
            <div id="liveVeilleList" style="display:none; margin-top:10px; padding-top:10px; border-top:1px solid rgba(255,255,255,0.08);">
                <div style="font-size:10.5px; color:#94a3b8; margin-bottom:8px; text-transform:uppercase; letter-spacing:0.5px;">
                    📡 Surveillé en continu : Instituts (IFOP, Elabe, Ipsos), Partis, Think tanks (Montaigne, iFRAP) & Google News
                </div>
                <div id="veilleItemsContainer" style="display:flex; flex-direction:column; gap:6px;">
{rendered_alerts}
                </div>
            </div>
        </div>
        <script>
            function toggleLiveVeille() {{
                const list = document.getElementById('liveVeilleList');
                const chevron = document.getElementById('chevronVeille');
                if (!list) return;
                const isHidden = list.style.display === 'none';
                list.style.display = isHidden ? 'block' : 'none';
                if (chevron) chevron.textContent = isHidden ? '▲' : '▼';
            }}
        </script>
'''
            # Insérer juste avant <h2 class="section-title" id="candidats">
            target_marker = '<h2 class="section-title" id="candidats">'
            if target_marker in content:
                content = content.replace(target_marker, veille_block + "\n        " + target_marker)
        else:
            # Mettre à jour les alertes existantes
            alerts_html_items = []
            for a in alerts:
                safe_a = a.replace("<", "&lt;").replace(">", "&gt;")
                alerts_html_items.append(
                    f'<div style="padding:6px 10px; background:rgba(30,41,59,0.6); border-radius:6px; border-left:3px solid #38bdf8; font-size:11.5px; line-height:1.4; color:#e2e8f0;">{safe_a}</div>'
                )
            rendered_alerts = "\n".join(alerts_html_items) if alerts_html_items else '<div style="color:#94a3b8; font-size:11.5px;">Aucune alerte critique ces dernières 24h. Prochaine veille lundi 18h.</div>'
            # Remplacement propre du bloc d'alertes sans dérive de balises div
            veille_re = r'<div id="veilleItemsContainer"[^>]*>[\s\S]*?</div>\s*</div>\s*</div>\s*<script>\s*function toggleLiveVeille'
            replacement = (
                f'<div id="veilleItemsContainer" style="display:flex; flex-direction:column; gap:6px;">\n{rendered_alerts}\n                </div>\n'
                '            </div>\n'
                '        </div>\n'
                '        <script>\n'
                '            function toggleLiveVeille'
            )
            content = re.sub(veille_re, replacement, content)

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
    last_update_str = format_french_date(meta.get("last_updated"))

    target_file = ROOT / "comparatifs candidats" / "Observatoire_Sondages_2027.html"
    if not target_file.exists():
        print(f"Erreur : {target_file} introuvable.")
        return

    content = target_file.read_text(encoding="utf-8")

    # Formatage JS enrichi pour pollsData (score, min, max, real, evolution, tendance)
    lines = ["[\n"]
    for item in polls_list:
        real_str = "true" if item.get("real", True) else "false"
        evo_str = item.get("evolution", "0.0")
        tendance_str = item.get("tendance", "stable")
        lines.append(
            f'            {{ name: "{item["name"]}", score: {item["score"]}, min: {item["min"]}, max: {item["max"]}, '
            f'real: {real_str}, party: "{item["party"]}", color: "{item["color"]}", '
            f'evolution: "{evo_str}", tendance: "{tendance_str}" }},\n'
        )
    lines_str = "".join(lines).rstrip(",\n") + "\n        ]"

    s_sond = content.find("const pollsData = [")
    if s_sond != -1:
        e_sond = content.find("];", s_sond) + 2
        content = content[:s_sond] + f"const pollsData = {lines_str};" + content[e_sond:]

    # Mise à jour date métadonnées dans le badge
    nb_polls = len(polls_list)
    content = re.sub(
        r'<div class="badge-update">.*?</div>',
        f'<div class="badge-update">🟢 Dernière consolidation statistique : {last_update_str} (Veille Hebdo Active)</div>',
        content
    )
    content = re.sub(
        r'<button class="filter-btn active"[^>]*onclick="setChartFilter\(\'all\'\)">.*?</button>',
        f'<button class="filter-btn active" id="btnFilterPollsAll" onclick="setChartFilter(\'all\')">🎯 Tous les <span id="countPollsAll">{nb_polls}</span> Candidats Déclarés</button>',
        content
    )
    content = content.replace("16 Candidats Déclarés", f"{nb_polls} Candidats Déclarés")
    content = content.replace("16 candidats déclarés", f"{nb_polls} candidats déclarés")

    # Mise à jour du tooltip du graphique pour inclure la tendance
    old_tooltip = "return `${item.name} (${item.party}) : Médiane ${item.score}% [${item.min}% - ${item.max}%]`;"
    new_tooltip = ("const evo = item.evolution ? (item.evolution.startsWith('+') || item.evolution.startsWith('-') ? item.evolution : '+' + item.evolution) : '0.0';\n"
                   "                                    const arrow = evo.startsWith('+') && evo !== '+0.0' ? '▲ ' : (evo.startsWith('-') ? '▼ ' : '▬ ');\n"
                   "                                    return `${item.name} (${item.party}) : Médiane ${item.score}% [${item.min}% - ${item.max}%] • Tendance: ${arrow}${evo}%`;")
    if old_tooltip in content:
        content = content.replace(old_tooltip, new_tooltip)

    target_file.write_text(content, encoding="utf-8")
    print(f"✓ Synchronisé avec succès : Observatoire_Sondages_2027.html ({len(polls_list)} candidats sondés avec tendances)")

def main():
    print("=== SYNCHRONISATION DES DONNÉES DU GRAND OBSERVATOIRE 2027 ===")
    sync_candidates_and_themes()
    sync_polls()
    print("=== TOUTES LES PAGES SONT À JOUR AVEC LE DOSSIER DATA/ ===")

if __name__ == "__main__":
    main()
