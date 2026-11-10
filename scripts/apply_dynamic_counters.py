# -*- coding: utf-8 -*-
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

root = Path(r"C:\Users\user\Desktop\projets_IA\projets\presidentielle")
files = [root / "index.html", root / "PORTAIL_PRESIDENTIELLE_2027.html"]

for f in files:
    if not f.exists():
        continue
    c = f.read_text(encoding="utf-8")
    
    # 1. Remplacer les boutons et titres avec des IDs
    c = re.sub(
        r'<span>🎯 Filtrer par Parrainages [^<]+:</span>',
        '<span id="labelFilterParrainages">🎯 Filtrer par Parrainages :</span>',
        c
    )
    c = re.sub(
        r'<button class="filter-btn active" onclick="filterCands\(\'primary\'\)">🎯 [^<]+</button>',
        '<button class="filter-btn active" id="btnFilterAll" onclick="filterCands(\'primary\')">🎯 Tous les Candidats Déclarés</button>',
        c
    )
    c = re.sub(
        r'<button class="filter-btn" onclick="filterCands\(\'green\'\)">🟢 [^<]+</button>',
        '<button class="filter-btn" id="btnFilterGreen" onclick="filterCands(\'green\')">🟢 500+ parrainages validés</button>',
        c
    )
    c = re.sub(
        r'<button class="filter-btn" onclick="filterCands\(\'orange\'\)">🟠 [^<]+</button>',
        '<button class="filter-btn" id="btnFilterOrange" onclick="filterCands(\'orange\')">🟠 300-499 en bonne voie</button>',
        c
    )
    c = re.sub(
        r'<button class="filter-btn" onclick="filterCands\(\'red\'\)">🔴 [^<]+</button>',
        '<button class="filter-btn" id="btnFilterRed" onclick="filterCands(\'red\')">🔴 &lt;300 en difficulté</button>',
        c
    )
    c = re.sub(
        r'<span>⚡ Comparer instantanément [^<]+sur un thème clé :</span>',
        '<span id="labelCompareTheme">⚡ Comparer instantanément les candidats sur un thème clé :</span>',
        c
    )

    # 2. Injecter la fonction JavaScript updateDynamicCounters()
    js_func = '''
        function updateDynamicCounters() {
            if (typeof cands === 'undefined' || !Array.isArray(cands)) return;
            const total = cands.length;
            const greenCount = cands.filter(c => c.parr_status === 'green').length;
            const orangeCount = cands.filter(c => c.parr_status === 'orange').length;
            const redCount = cands.filter(c => c.parr_status === 'red').length;

            const lblFilter = document.getElementById('labelFilterParrainages');
            if (lblFilter) lblFilter.innerHTML = `🎯 Filtrer par Parrainages (${total} Candidats Déclarés) :`;

            const btnAll = document.getElementById('btnFilterAll');
            if (btnAll) btnAll.innerHTML = `🎯 Tous les ${total} Candidats Déclarés`;

            const btnGreen = document.getElementById('btnFilterGreen');
            if (btnGreen) btnGreen.innerHTML = `🟢 500+ parrainages validés (${greenCount})`;

            const btnOrange = document.getElementById('btnFilterOrange');
            if (btnOrange) btnOrange.innerHTML = `🟠 300-499 en bonne voie (${orangeCount})`;

            const btnRed = document.getElementById('btnFilterRed');
            if (btnRed) btnRed.innerHTML = `🔴 &lt;300 en difficulté (${redCount})`;

            const lblComp = document.getElementById('labelCompareTheme');
            if (lblComp) lblComp.innerHTML = `⚡ Comparer instantanément les ${total} candidats sur un thème clé :`;

            const heroNum = document.querySelector('.hero-stat .num');
            if (heroNum) heroNum.textContent = total;

            const hemiTag = document.querySelector('.hero + h2 + div div');
            if (hemiTag && hemiTag.textContent.includes('Ordre officiel Hémicycle')) {
                hemiTag.textContent = `🏛️ Ordre officiel Hémicycle (${total})`;
            }
        }
    '''

    if 'function updateDynamicCounters()' not in c:
        c = c.replace(
            "window.addEventListener('DOMContentLoaded', () => {",
            js_func + "\n        window.addEventListener('DOMContentLoaded', () => {\n            updateDynamicCounters();"
        )

    f.write_text(c, encoding="utf-8")
    print(f"✓ {f.name} configuré avec compteurs 100% dynamiques (IDs + recalcul JS) !")
