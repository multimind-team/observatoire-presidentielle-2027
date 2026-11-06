import json
import re
from pathlib import Path

root = Path(r"C:\Users\user\Desktop\projets_IA\projets\presidentielle")
data_dir = root / "data"
data_dir.mkdir(exist_ok=True)
scripts_dir = root / "scripts"
scripts_dir.mkdir(exist_ok=True)

# 1. Candidats (16 déclarés ordonnés selon l'Hémicycle)
idx_html = (root / "index.html").read_text(encoding="utf-8")
s_cands = idx_html.find("const cands = [") + len("const cands = ")
e_cands = idx_html.find("];", s_cands) + 1
cands = json.loads(idx_html[s_cands:e_cands])

(data_dir / "candidats.json").write_text(json.dumps(cands, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Created data/candidats.json with {len(cands)} candidates.")

# 2. Thématiques (12 matrices)
s_tm = idx_html.find("const thematicMatrices = ") + len("const thematicMatrices = ")
brace_count = 0
end_pos = -1
for i, ch in enumerate(idx_html[s_tm:]):
    if ch == "{":
        brace_count += 1
    elif ch == "}":
        brace_count -= 1
        if brace_count == 0:
            end_pos = s_tm + i + 1
            break

tm = json.loads(idx_html[s_tm:end_pos])
(data_dir / "thematiques.json").write_text(json.dumps(tm, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Created data/thematiques.json with {len(tm)} topics.")

# 3. Sondages 2027
sond_file = root / "comparatifs candidats" / "Observatoire_Sondages_2027.html"
c_sond = sond_file.read_text(encoding="utf-8")

s_sond = c_sond.find("const pollsData = [")
e_sond = c_sond.find("];", s_sond) + 2
raw_polls_block = c_sond[s_sond:e_sond]

items = []
pattern = re.compile(r'\{\s*name:\s*"([^"]+)",\s*score:\s*([\d\.]+),\s*min:\s*([\d\.]+),\s*max:\s*([\d\.]+),\s*real:\s*(true|false),\s*party:\s*"([^"]+)",\s*color:\s*"([^"]+)"\s*\}')
for m in pattern.finditer(raw_polls_block):
    items.append({
        "name": m.group(1),
        "score": float(m.group(2)),
        "min": float(m.group(3)),
        "max": float(m.group(4)),
        "real": m.group(5) == "true",
        "party": m.group(6),
        "color": m.group(7)
    })

polls_data = {
    "metadata": {
        "last_updated": "2026-11-06",
        "titre": "Observatoire des Intentions de Vote 2027",
        "hypothese": "1er tour Élection Présidentielle 2027 (Hypothèse avec Édouard Philippe pour le bloc central)",
        "institut_reference": "Agrégation consolidée des intentions de vote (IFOP, Elabe, OpinionWay, Ipsos)",
        "echantillon_moyen": 1500,
        "marge_erreur_statistique": "± 1,5 à 2,5 points (IC 95%)"
    },
    "sondages": items
}
(data_dir / "sondages.json").write_text(json.dumps(polls_data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Created data/sondages.json with {len(items)} candidates polled.")
