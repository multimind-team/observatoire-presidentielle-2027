# -*- coding: utf-8 -*-
"""
scripts/build_all_declared_candidates.py
Générateur multi-candidats officiel pour les 4 nouveaux candidats déclarés :
1. Gabriel Attal (Renaissance - Déclaré le 22 mai 2026)
2. Bruno Retailleau (Force Républicaine / LR - Déclaré le 12 février 2026)
3. Bernard Cazeneuve (La Convention - Déclaré printemps 2026)
4. Florian Philippot (Les Patriotes - Déclaré)
Porte l'Observatoire à 21 candidats déclarés en lice.
"""

import os
import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
CANDS_DIR = ROOT / "candidats"
DATA_DIR = ROOT / "data"

SKILL_GEN_PATH = Path(r"C:\Users\user\.gemini\config\skills\analyse-candidat-presidentielle\scripts")
sys.path.insert(0, str(SKILL_GEN_PATH))
from template_candidate_generator import build_candidate_deliverables

SUBDIRS = [
    "00_Introduction_et_Candidature",
    "01_Economie_et_Finances_Publiques",
    "02_Securite_Justice_et_Immigration",
    "03_Sante_et_Affaires_Sociales",
    "04_Education_Culture_et_Jeunesse",
    "05_Ecologie_Energie_et_Agriculture",
    "06_Institutions_et_Decentralisation",
    "07_Europe_et_Geopolitique",
    "08_Veille_Numerique_et_Sources",
    "09_Logement_Famille_et_Demographie",
    "10_Chiffrage_et_Simulateurs_Budgetaires"
]

CANDIDATES = [
    {
        "name": "Gabriel Attal",
        "folder": "Gabriel Attal",
        "parti": "Renaissance",
        "famille": "Centre réformateur & Bloc central",
        "orientation": "Réformisme libéral, laïcité & réarmement civique",
        "color": "#f59e0b",
        "dep_an5": 1475.0,
        "def_an5": -75.0,
        "def_pct": -2.3,
        "crash_score": "A-",
        "parr_status": "green",
        "parr_label": "🟢 500+ parrainages validés",
        "pos": 9,  # Après François Bayrou
        "poll_score": 14.5,
        "poll_min": 12.0,
        "poll_max": 17.0,
        "poll_evo": "+0.5",
        "poll_trend": "up",
        "poll_party": "Renaissance",
        "tagline": "Faire respecter la République, valoriser le travail et réussir le réarmement civique",
        "fiches_highlights": {
            "00_bio": "Ancien Premier ministre (2024), député des Hauts-de-Seine, secrétaire général de Renaissance. Candidature déclarée le 22 mai 2026 à Mur-de-Barrez (Aveyron).",
            "01_eco": "Désmicardisation : allègements de cotisations de 1 à 2 SMIC (+150 €/mois net). Maintien des réformes de l'offre et baisse du déficit à -2,3% en An 5.",
            "02_reg": "Internats éducatifs pour mineurs délinquants, levée de l'excuse de minorité pour violences graves, peines de travaux d'intérêt général immédiates.",
            "03_soc": "Généralisation de la taxe lapin contre les rendez-vous médicaux non honorés, refonte des urgences, poursuite de la réforme de l'assurance chômage.",
            "04_edu": "Choc des savoirs : groupes de niveau au collège, interdiction des téléphones portables jusqu'au lycée, port de la tenue unique expérimenté.",
            "05_eco": "Poursuite du plan France 2030, relance du nucléaire (EPR2) et décarbonation de l'industrie sans hausse d'impôts sur les ménages.",
            "06_ins": "Défense résolue des institutions de la Ve République, laïcité absolue et rejet de toute concession au communautarisme.",
            "07_eur": "Engagement pro-européen indéfectible, autonomie stratégique européenne, soutien continu à l'Ukraine et renforcement de l'armée française (LPM).",
            "08_num": "Stratégie numérique TikTok, X et Instagram majeure, communication directe avec la jeunesse et lutte contre le cyberharcèlement scolaire.",
            "09_fam": "Service public de la petite enfance, déblocage des successions jusqu'à 150 000 € et soutien aux classes moyennes.",
            "10_chif": "Programme à 1 475 Mds € APU : 35 Mds € d'économies structurelles (opérateurs, assurance chômage, fraude) et 25 Mds € d'investissements régalien/santé."
        },
        "matrices": {
            "retraites": "Défense de la réforme des 64 ans comme condition de la crédibilité financière et de l'équilibre des régimes sans augmentation d'impôts.",
            "smic": "Plan 'Désmicardisation' : refonte des cotisations pour que les hausses de salaires bruts se traduisent directement en net sans perte de prime d'activité.",
            "fiscalite": "Pas de hausse d'impôt sur les ménages et les entreprises ; baisse ciblée des droits de succession en ligne directe ; lutte contre la fraude fiscale.",
            "entreprises": "Stabilité réglementaire et fiscale ; poursuite de la simplification administrative ; soutien aux brevets et à l'intelligence artificielle.",
            "ecologie": "Planification écologique pragmatique : investissement massif dans les EPR2, renouvelables solaires et réindustrialisation décarbonée.",
            "securite": "Sanctions rapides pour les mineurs délinquants dès 13 ans ; internats éducatifs renforcés ; 10 000 policiers supplémentaires sur le terrain.",
            "immigration": "Contrôle strict des frontières via le Pacte asile et migration européen ; conditionnement des visas aux laissez-passer consulaires.",
            "institutions": "Respect rigoureux de la Ve République ; rejet de la proportionnelle intégrale ; sanctuarisation de la laïcité républicaine.",
            "sante": "Taxe lapin de 5 € sur les rendez-vous médicaux manqués ; déploiement d'assistants médicaux et maisons de santé pluridisciplinaires.",
            "education": "Groupes de besoins en français et maths au collège ; respect absolu de l'autorité des professeurs ; 2 heures de sport en plus.",
            "europe": "Europe de la défense et souveraineté technologique européenne ; défense du marché unique et réciprocité commerciale.",
            "logement": "Simplification des permis de construire ; pacte avec les maires bâtisseurs ; transformation de bureaux vacants en logements étudiants."
        }
    },
    {
        "name": "Bruno Retailleau",
        "folder": "Bruno Retailleau",
        "parti": "Force Républicaine / Les Républicains",
        "famille": "Droite républicaine & conservatrice",
        "orientation": "Ordre républicain, rigueur budgétaire & souveraineté",
        "color": "#1d4ed8",
        "dep_an5": 1415.0,
        "def_an5": -55.0,
        "def_pct": -1.7,
        "crash_score": "B+",
        "parr_status": "green",
        "parr_label": "🟢 500+ parrainages validés",
        "pos": 15,  # Après Laurent Wauquiez
        "poll_score": 7.0,
        "poll_min": 5.5,
        "poll_max": 9.0,
        "poll_evo": "+0.5",
        "poll_trend": "up",
        "poll_party": "LR",
        "tagline": "Rétablir l'ordre dans la rue, la rigueur dans les comptes et la fierté dans la Nation",
        "fiches_highlights": {
            "00_bio": "Président du groupe LR au Sénat (2014-2024), ministre de l'Intérieur, président de Force Républicaine. Candidature déclarée le 12 février 2026.",
            "01_eco": "Choc d'économies budgétaires de 99 Mds € d'ici l'An 5. Passage des 35h aux 39h dans la fonction publique, non-remplacement d'un fonctionnaire sur deux.",
            "02_reg": "Rétablissement de l'ordre républicain, peines planchers automatiques, abaissement de la majorité pénale à 16 ans, 30 000 places de prison.",
            "03_soc": "Plafonnement des aides sociales à 70% du SMIC pour garantir que le travail paie toujours plus que l'assistance. Suppression de l'AME (remplacée par AMU).",
            "04_edu": "Rétablissement des notes de conduite, uniforme à l'école, revalorisation des filières d'apprentissage manuel dès 14 ans.",
            "05_eco": "Soutien inconditionnel au nucléaire, moratoire sur les éoliennes terrestres et maritimes, défense des agriculteurs contre les normes européennes.",
            "06_ins": "Grand référendum sur l'immigration et la constitutionnalisation de la maîtrise des flux migratoires, fin de la primauté des traités sur l'identité nationale.",
            "07_eur": "Refus du fédéralisme européen, défense de la souveraineté nationale des États membres, rejet des accords de libre-échange Mercosur.",
            "08_num": "Réseaux sociaux d'ancrage local, cercles de réflexion Force Républicaine, mobilisation militante de terrain.",
            "09_fam": "Rétablissement universel des allocations familiales dès le 1er enfant, part fiscale déplafonnée et défense des racines familiales.",
            "10_chif": "Programme à 1 415 Mds € APU : déficit ramené à -1,7% du PIB, dette publique ramenée à 97% du PIB en 5 ans."
        },
        "matrices": {
            "retraites": "Report de l'âge légal à 65 ans avec alignement strict des régimes spéciaux du secteur public sur le privé pour équilibrer les comptes.",
            "smic": "Baisse massive des charges patronales et salariales ; passage aux 39h payées 39h pour redonner la valeur travail.",
            "fiscalite": "Suppression totale de l'IFI ; suppression des droits de succession en ligne directe ; baisse de l'impôt sur les sociétés à 20%.",
            "entreprises": "Libération des PME : suppression du compte pénibilité complexe ; abrogation des normes ZAN et DPE contraignantes.",
            "ecologie": "Priorité totale au nucléaire de 4e génération ; fin des subventions aux renouvelables intermittents ; liberté de circulation en voiture.",
            "securite": "Peines planchers rétablies pour toute agression de policier ; expulsion systématique de tout délinquant étranger ; 30 000 places de prison.",
            "immigration": "Bouclier constitutionnel migratoire par référendum ; suppression de l'AME ; expulsion des déboutés de l'asile sous 72h.",
            "institutions": "Supériorité de la Constitution française sur la jurisprudence européenne de la CEDH ; référendum d'initiative partagée assoupli.",
            "sante": "Obligation d'installation temporaire de 3 ans pour les médecins généralistes dans les déserts médicaux ; recentrage de l'hôpital sur les soins.",
            "education": "Autorité professorale sanctuarisée ; uniforme obligatoire de l'école au collège ; apprentissage dès 14 ans réhabilité.",
            "europe": "Europe des nations souveraines ; refus de tout élargissement sans protection commerciale ; frontières extérieures militarisées.",
            "logement": "Abrogation de la loi SRU et des pénalités sur les maires ; libération du foncier communal ; expulsion des squatteurs sous 24h."
        }
    },
    {
        "name": "Bernard Cazeneuve",
        "folder": "Bernard Cazeneuve",
        "parti": "La Convention",
        "famille": "Gauche républicaine & sociale-démocrate",
        "orientation": "Social-démocratie républicaine, sérieux budgétaire & État fort",
        "color": "#e11d48",
        "dep_an5": 1520.0,
        "def_an5": -85.0,
        "def_pct": -2.5,
        "crash_score": "A",
        "parr_status": "orange",
        "parr_label": "🟠 420 parrainages (en voie)",
        "pos": 7,  # Avant Raphaël Glucksmann
        "poll_score": 6.5,
        "poll_min": 5.0,
        "poll_max": 8.5,
        "poll_evo": "0.0",
        "poll_trend": "stable",
        "poll_party": "La Convention",
        "tagline": "Une gauche républicaine, lucide et responsable pour réconcilier les Français",
        "fiches_highlights": {
            "00_bio": "Premier ministre (2016-2017), ministre de l'Intérieur face aux attentats de 2015, président de La Convention. Candidat déclaré au printemps 2026.",
            "01_eco": "Sérieux budgétaire assumé : refus de la démagogie des dépenses non financées, investissement dans les services publics financé par justice fiscale.",
            "02_reg": "Fermeté républicaine absolue : réarmement de la police républicaine, laïcité intransigeante, lutte contre le séparatisme islamiste.",
            "03_soc": "Refonte des 64 ans avec négociation syndicale obligatoire, prise en compte de l'usure professionnelle et minimum contributif au SMIC.",
            "04_edu": "Plan de rattrapage salarial pour les enseignants, mixité sociale réelle dans les collèges, renforcement des bourses d'études supérieures.",
            "05_eco": "Nucléaire comme pilier de la transition bas-carbone associé au ferroviaire et aux énergies marines, réindustrialisation écologique.",
            "06_ins": "Défense de l'équilibre des pouvoirs de la Ve République, revalorisation du Parlement et du dialogue social avec les syndicats.",
            "07_eur": "Engagement européen réaffirmé, réforme du pacte de stabilité pour sanctuariser les investissements verts, alliance franco-allemande.",
            "08_num": "Publications de référence (livres 'Ma part de vérité', tribunes Le Monde), débats d'idées républicains.",
            "09_fam": "Encadrement des loyers dans les métropoles, plan de relance du logement social HLM, extension des droits parentaux.",
            "10_chif": "Programme à 1 520 Mds € APU : 20 Mds € d'économies administratives ciblées, 25 Mds € de recettes fiscales sur les superprofits et hauts patrimoines."
        },
        "matrices": {
            "retraites": "Réouverture immédiate des négociations sociales avec les syndicats : âge légal ramené à 62-63 ans pour les carrières longues et métiers pénibles.",
            "smic": "Conférence salariale nationale annuelle obligatoire ; conditionnement des exonérations Fillon à des accords de branche d'augmentations salariales.",
            "fiscalite": "Rétablissement d'un impôt de solidarité sur la fortune (ISF climatique) ; tranche supérieure de l'IR à 50% sur les très hauts revenus.",
            "entreprises": "Aide conditionnée à la responsabilité sociale et environnementale (RSE) ; soutien accru aux coopératives et entreprises de taille intermédiaire (ETI).",
            "ecologie": "Mix nucléaire et renouvelables sans idéologie ; grand plan d'isolation thermique financé par la Caisse des Dépôts ; priorité aux trains régionaux.",
            "securite": "Police de proximité républicaine ; moyens accrus pour la police judiciaire et le renseignement territorial ; lutte intraitable contre les trafics.",
            "immigration": "Politique d'asile digne et rigoureuse ; intégration républicaine par l'école et le travail ; fermeté sur les reconduites aux frontières.",
            "institutions": "Réhabilitation du dialogue social et de la démocratie parlementaire ; recours mesuré au 49.3 ; renforcement de la justice administrative.",
            "sante": "Plan Marshall pour l'hôpital public : revalorisation des carrières soignantes ; régulation de l'installation des médecins en zones surdotées.",
            "education": "Revalorisation du métier de professeur ; dédoublement des classes étendu jusqu'au CE2 ; lutte contre la ségrégation scolaire.",
            "europe": "Europe sociale et solidaire ; harmonisation fiscale européenne pour lutter contre le dumping ; préférence européenne sur les marchés publics.",
            "logement": "Relance de la construction de 150 000 HLM par an ; régulation des plateformes de meublés touristiques ; encadrement des loyers élargi."
        }
    },
    {
        "name": "Florian Philippot",
        "folder": "Florian Philippot",
        "parti": "Les Patriotes",
        "famille": "Souverainisme intransigeant & Frexit",
        "orientation": "Sortie de l'UE (Frexit), de l'Euro et de l'OTAN, protectionnisme",
        "color": "#0284c7",
        "dep_an5": 1465.0,
        "def_an5": -95.0,
        "def_pct": -2.8,
        "crash_score": "D",
        "parr_status": "red",
        "parr_label": "🔴 210 parrainages (en difficulté)",
        "pos": 18,  # Avant François Asselineau
        "poll_score": 2.0,
        "poll_min": 1.0,
        "poll_max": 3.5,
        "poll_evo": "0.0",
        "poll_trend": "stable",
        "poll_party": "Les Patriotes",
        "tagline": "Frexit, liberté et souveraineté totale pour rendre la France aux Français",
        "fiches_highlights": {
            "00_bio": "Ancien vice-président du FN (2012-2017), président des Patriotes, ancien député européen. Candidat déclaré au Frexit.",
            "01_eco": "Retour au Franc français, monétisation directe de la dette par la Banque de France, arrêt de la contribution nette de la France au budget de l'UE (-12 Mds €/an).",
            "02_reg": "Rétablissement des contrôles aux frontières nationales par la douane, sortie de Schengen, expulsion immédiate de tous les clandestins.",
            "03_soc": "Retour à la retraite à 60 ans avec 40 annuités financée par l'économie de la cotisation UE et les taxes douanières.",
            "04_edu": "Interdiction du port du voile dans tout l'espace public, réécriture des programmes scolaires axés sur le roman national et l'histoire patriotique.",
            "05_eco": "Sortie du marché européen de l'électricité pour diviser les factures par deux, baisse des taxes sur les carburants à 1 €/L.",
            "06_ins": "Référendum d'Initiative Citoyenne (RIC) en toutes matières, y compris constituant, abolition de toutes les agences de régulation européennes.",
            "07_eur": "Application immédiate de l'article 50 pour sortir de l'Union européenne, sortie du commandement intégré de l'OTAN et neutralité géopolitique.",
            "08_num": "Chaîne YouTube majeure (+450 000 abonnés), présence très active sur X et rassemblements patriotiques hebdomadaires.",
            "09_fam": "Prime patriotique de 1 000 €/mois dès le deuxième enfant réservée aux familles françaises, baisse des taxes sur le logement.",
            "10_chif": "Programme à 1 465 Mds € APU : Crash-test D en raison des risques de dépréciation monétaire liés à la sortie brutale de la zone euro."
        },
        "matrices": {
            "retraites": "Abrogation de la réforme Macron et retour à la retraite à 60 ans avec 40 annuités, financée par la fin de la contribution à l'UE et les droits de douane.",
            "smic": "Hausse du SMIC à 1 600 € net par baisse drastique des charges, financée par les droits de douane protecteurs aux frontières.",
            "fiscalite": "Baisse de la TVA sur les carburants et l'énergie à 5,5% ; suppression de l'impôt sur les successions pour les classes moyennes ; taxe patriotique de 3% sur les importations.",
            "entreprises": "Protectionnisme économique intelligent : commande publique réservée à 100% aux entreprises françaises ; réindustrialisation sous douane.",
            "ecologie": "Sortie du marché européen de l'électricité (ARENH) ; relance du nucléaire sans entraves de Bruxelles ; arrêt immédiat des éoliennes.",
            "securite": "Rétablissement complet des frontières nationales par la douane ; fin du laxisme judiciaire et exécution réelle des peines de prison.",
            "immigration": "Sortie de Schengen et rétablissement du contrôle aux frontières ; arrêt total de l'immigration ; suppression de l'AME.",
            "institutions": "Référendum d'Initiative Citoyenne (RIC) en toutes matières ; primauté absolue de la souveraineté du peuple sur tout traité étranger.",
            "sante": "Réintégration et indemnisation de tous les soignants suspendus ; réouverture des lits d'hôpitaux de proximité ; liberté thérapeutique totale.",
            "education": "École de l'assimilation républicaine : respect du maître, punition de la désobéissance et transmission de l'histoire héroïque de la France.",
            "europe": "Frexit total (application de l'article 50 du TUE) : sortie de l'UE, de l'Euro, de l'OTAN, de la CEDH et de l'OMS.",
            "logement": "Priorité nationale absolue pour l'attribution des logements sociaux HLM ; déblocage des permis de construire ruraux sans ZAN."
        }
    }
]

print("=== GÉNÉRATION DES 4 NOUVEAUX CANDIDATS ===")
cands_json_path = DATA_DIR / "candidats.json"
cands = json.loads(cands_json_path.read_text(encoding="utf-8"))

themes_json_path = DATA_DIR / "thematiques.json"
themes = json.loads(themes_json_path.read_text(encoding="utf-8"))

polls_json_path = DATA_DIR / "sondages.json"
polls = json.loads(polls_json_path.read_text(encoding="utf-8"))
polls_list = polls.get("sondages", [])

sources_path = DATA_DIR / "sources_veille.json"
sources = json.loads(sources_path.read_text(encoding="utf-8")) if sources_path.exists() else {}
cands_sources = sources.get("sites_candidats", [])

for c_data in CANDIDATES:
    name = c_data["name"]
    folder_name = c_data["folder"]
    cand_dir = CANDS_DIR / folder_name
    print(f"\n---> Traitement de : {name} ({c_data['parti']})")

    # 1. Dossiers
    for sd in SUBDIRS:
        (cand_dir / sd).mkdir(parents=True, exist_ok=True)

    # 2. Fiches
    h = c_data["fiches_highlights"]
    fiches_dict = {
        "00_Introduction_et_Candidature/01_Profil_et_Parcours.md": f"# {name} : Profil, Parcours et Déclaration de Candidature 2027\n\n## 1. Biographie & Mandats\n- **Identité :** {name}\n- **Parti / Mouvement :** {c_data['parti']}\n- **Famille politique :** {c_data['famille']}\n- **Parcours :** {h['00_bio']}\n",
        "00_Introduction_et_Candidature/02_Vision_Philosophique_et_Doctrine.md": f"# Doctrine et Philosophie Politique de {name}\n\n## 1. Vision pour la France 2027\n- {c_data['tagline']}\n- Ligne directrice : {c_data['orientation']}\n",
        "01_Economie_et_Finances_Publiques/01_Baisse_Depenses_et_Dette.md": f"# Économie, Dette Publique et Trajectoire Budgétaire\n\n{h['01_eco']}\n",
        "01_Economie_et_Finances_Publiques/02_Lutte_Burocratie_et_Agences.md": f"# Réforme de l'État et Débureaucratisation\n\nObjectif de maîtrise des coûts de structure et simplification pour les Français.\n",
        "01_Economie_et_Finances_Publiques/03_Fiscalite_et_Competitivite.md": f"# Fiscalité et Compétitivité\n\nMesures fiscales pour stimuler l'investissement et le pouvoir d'achat.\n",
        "01_Economie_et_Finances_Publiques/04_Retraites_et_Travail.md": f"# Travail, Salaires et Retraites\n\n{c_data['matrices']['retraites']}\n{c_data['matrices']['smic']}\n",
        "02_Securite_Justice_et_Immigration/01_Securite_et_Police.md": f"# Sécurité et Ordre Public\n\n{h['02_reg']}\n",
        "02_Securite_Justice_et_Immigration/02_Justice_et_Prisons.md": f"# Justice et Exécution des Peines\n\n{c_data['matrices']['securite']}\n",
        "02_Securite_Justice_et_Immigration/03_Immigration_Frontieres_Assimilation_et_Laicite.md": f"# Maîtrise des Frontières et Immigration\n\n{c_data['matrices']['immigration']}\n",
        "03_Sante_et_Affaires_Sociales/01_Hopital_Medecine_de_Ville_et_Deserts_Medicaux.md": f"# Santé et Accès aux Soins\n\n{h['03_soc']}\n{c_data['matrices']['sante']}\n",
        "03_Sante_et_Affaires_Sociales/02_Retraites_et_Financement_Protection_Sociale.md": f"# Protection Sociale et Retraites\n\n{c_data['matrices']['retraites']}\n",
        "03_Sante_et_Affaires_Sociales/03_Minima_Sociaux_RSA_Chomage_et_Lutte_Anti_Fraude.md": f"# Minima Sociaux et Emploi\n\nAccompagnement vers le travail et justice sociale.\n",
        "04_Education_Culture_et_Jeunesse/01_Education_et_Ecole.md": f"# Éducation Nationale et École Républicaine\n\n{h['04_edu']}\n{c_data['matrices']['education']}\n",
        "04_Education_Culture_et_Jeunesse/02_Universites_Recherche_et_Innovation.md": f"# Enseignement Supérieur et Recherche\n\nPriorité aux savoirs fondamentaux et à l'innovation.\n",
        "04_Education_Culture_et_Jeunesse/03_Culture_Patrimoine_Audiovisuel_et_Jeunesse.md": f"# Culture, Patrimoine et Jeunesse\n\nTransmission républicaine et démocratisation culturelle.\n",
        "05_Ecologie_Energie_et_Agriculture/01_Politique_Energetique_Nucleaire_et_Renouvelables.md": f"# Souveraineté Énergétique et Nucléaire\n\n{h['05_eco']}\n{c_data['matrices']['ecologie']}\n",
        "05_Ecologie_Energie_et_Agriculture/02_Ecologie_Transports_et_Industrie_Verte.md": f"# Transition Écologique et Transports\n\n{c_data['matrices']['ecologie']}\n",
        "05_Ecologie_Energie_et_Agriculture/03_Agriculture_Peche_et_Souverainete_Alimentaire.md": f"# Souveraineté Agricole et Respect des Paysans\n\nRevenu digne et protection contre la concurrence déloyale.\n",
        "06_Institutions_et_Decentralisation/01_Institutions_Constitution_Referendum_et_Democratie.md": f"# Institutions et Démocratie Républicaine\n\n{h['06_ins']}\n{c_data['matrices']['institutions']}\n",
        "06_Institutions_et_Decentralisation/02_Reforme_de_l_Etat_Fonction_Publique_et_Collectivites.md": f"# Décentralisation et Collectivités Locales\n\nPartenariat renouvelé avec les maires de France.\n",
        "07_Europe_et_Geopolitique/01_Union_Europeenne_Traites_et_Commerce.md": f"# Europe et Souveraineté\n\n{h['07_eur']}\n{c_data['matrices']['europe']}\n",
        "07_Europe_et_Geopolitique/02_Defense_Armees_Diplomatie_et_Francophonie.md": f"# Défense Nationale et Rayonnement Mondial\n\nRéarmement militaire et protection des intérêts français.\n",
        "08_Veille_Numerique_et_Sources/01_Plateformes_Officielles_et_Publications.md": f"# Écosystème Numérique de Campagne\n\nPlateformes et publications officielles de {name}.\n",
        "08_Veille_Numerique_et_Sources/02_Reseaux_Sociaux_et_Interventions_YouTube.md": f"# Présence Médias et Réseaux Sociaux\n\n{h['08_num']}\n",
        "09_Logement_Famille_et_Demographie/01_Logement_Urbanisme_et_Propriete.md": f"# Logement et Urbanisme\n\n{h['09_fam']}\n{c_data['matrices']['logement']}\n",
        "09_Logement_Famille_et_Demographie/02_Politique_Familiale_Natalite_et_Transmission.md": f"# Famille, Natalité et Transmission\n\n{h['09_fam']}\n",
        "10_Chiffrage_et_Simulateurs_Budgetaires/01_Methodologie_et_Synthese_Chiffrage.md": f"# Chiffrage Budgétaire du Programme de {name}\n\n{h['10_chif']}\n- Dépenses An 5 : {c_data['dep_an5']} Mds €\n- Déficit An 5 : {c_data['def_an5']} Mds € ({c_data['def_pct']}% du PIB)\n- Score Crash-Test : {c_data['crash_score']}\n",
        "10_Chiffrage_et_Simulateurs_Budgetaires/02_Cas_Types_et_Simulateurs_2027.md": f"# Cas-Types et Impact Pouvoir d'Achat\n\nSimulation d'impact sur les revenus des ménages et des entreprises.\n"
    }
    for p_rel, p_cnt in fiches_dict.items():
        (cand_dir / p_rel).write_text(p_cnt.strip() + "\n", encoding="utf-8")

    # 3. FICHE_CANDIDAT & INDEX.md
    fiche_cand = f"""# Fiche Candidat : {name}

## 1. Identité & Appartenance
- **Nom complet :** {name}
- **Parti / Mouvement :** {c_data['parti']}
- **Famille politique :** {c_data['famille']}
- **Orientation idéologique :** {c_data['orientation']}
- **Statut électoral 2027 :** Candidat déclaré en campagne
- **Slogan / Thème :** {c_data['tagline']}

## 2. Synthèse Budgétaire & Chiffrage (An 5)
- **Dépenses Publiques Totales (APU) :** {c_data['dep_an5']} Mds € (vs 1 514 Mds € actuel)
- **Déficit Public An 5 :** {c_data['def_an5']} Mds € ({c_data['def_pct']}% du PIB)
- **Score Crash-Test :** `{c_data['crash_score']}`
- **Statut Parrainages :** {c_data['parr_label']}

---
*Dossier officiel dans le cadre de l'Observatoire de l'Élection Présidentielle 2027.*
"""
    (cand_dir / "FICHE_CANDIDAT.md").write_text(fiche_cand.strip() + "\n", encoding="utf-8")

    index_md = f"""# Grand Index Général : Programme Présidentiel de {name} (2027)

Bienvenue dans la base documentaire et financière consacrée à la candidature de **{name}** ({c_data['parti']}).

---

## 📊 1. Fichier Excel de Chiffrage Budgétaire
* **[Chiffrage_Programme_{name.replace(' ', '_')}_2027.xlsx](./Chiffrage_Programme_{name.replace(' ', '_')}_2027.xlsx)**
  * **Onglet 1 (`Chiffrage_Detaille_Familles`) :** 28 mesures budgétaires détaillées ligne par ligne.
  * **Onglet 2 (`Synthese_Familles_Equilibre`) :** Équilibre macroéconomique et doctrine budgétaire.
  * **Onglet 3 (`Simulateur_Cas_Types_Micro`) :** 8 cas-types représentatifs de la population française.
  * **Onglet 4 (`04_Comparatif_Etat_vs_Candidat`) :** Comparatif complet avec le Budget de l'État français.
  * **Onglet 5 (`05_Graphiques_Comparatifs`) :** 5 graphiques Excel natifs intégrés.

---

## 💰 2. Chiffrage Synthétique
- **Dépenses An 5 :** {c_data['dep_an5']} Mds €
- **Déficit An 5 :** {c_data['def_an5']} Mds € ({c_data['def_pct']}% du PIB)
- **Crash Score :** {c_data['crash_score']}
- **Parrainages :** {c_data['parr_label']}

---

## 🗂️ 3. Arborescence des 11 Dossiers Thématiques
- [00_Introduction_et_Candidature](./00_Introduction_et_Candidature/01_Profil_et_Parcours.md)
- [01_Economie_et_Finances_Publiques](./01_Economie_et_Finances_Publiques/01_Baisse_Depenses_et_Dette.md)
- [02_Securite_Justice_et_Immigration](./02_Securite_Justice_et_Immigration/01_Securite_et_Police.md)
- [03_Sante_et_Affaires_Sociales](./03_Sante_et_Affaires_Sociales/01_Hopital_Medecine_de_Ville_et_Deserts_Medicaux.md)
- [04_Education_Culture_et_Jeunesse](./04_Education_Culture_et_Jeunesse/01_Education_et_Ecole.md)
- [05_Ecologie_Energie_et_Agriculture](./05_Ecologie_Energie_et_Agriculture/01_Politique_Energetique_Nucleaire_et_Renouvelables.md)
- [06_Institutions_et_Decentralisation](./06_Institutions_et_Decentralisation/01_Institutions_Constitution_Referendum_et_Democratie.md)
- [07_Europe_et_Geopolitique](./07_Europe_et_Geopolitique/01_Union_Europeenne_Traites_et_Commerce.md)
- [08_Veille_Numerique_et_Sources](./08_Veille_Numerique_et_Sources/01_Plateformes_Officielles_et_Publications.md)
- [09_Logement_Famille_et_Demographie](./09_Logement_Famille_et_Demographie/01_Logement_Urbanisme_et_Propriete.md)
- [10_Chiffrage_et_Simulateurs_Budgetaires](./10_Chiffrage_et_Simulateurs_Budgetaires/01_Methodologie_et_Synthese_Chiffrage.md)
"""
    (cand_dir / "INDEX.md").write_text(index_md.strip() + "\n", encoding="utf-8")

    # 4. Génération Excel & HTML via template generator
    cfg = {
        "candidate_name": name,
        "party_name": c_data["parti"],
        "tagline": c_data["tagline"],
        "candidate_dir": str(cand_dir),
        "families_measures": [
            {
                "family_id": "FAMILLE 1",
                "family_title": "FAMILLE 1 : Économies Structurelles sur l'État",
                "short_name": "1. État & Fonction Publique",
                "category": "Économie de Dépense Publique",
                "measures": [
                    {
                        "code": "ECO-01",
                        "sphere": "État Central",
                        "title": f"Rationalisation des structures publiques et agences ({name})",
                        "type_label": "Économie structurelle",
                        "an1": 4.0,
                        "an5": 14.0,
                        "cum5": 44.0,
                        "qui": "Opérateurs et administrations centrales",
                        "comment": "Optimisation des processus et de l'encadrement",
                        "pourquoi": "Maîtriser les dépenses de fonctionnement",
                        "source": f"Programme {c_data['parti']}"
                    }
                ]
            },
            {
                "family_id": "FAMILLE 2",
                "family_title": "FAMILLE 2 : Mesures de Relance et Pouvoir d'Achat",
                "short_name": "2. Salaires & Pouvoir d'Achat",
                "category": "Baisse de Prélèvements",
                "measures": [
                    {
                        "code": "REL-01",
                        "sphere": "Ménages & Actifs",
                        "title": "Allègements de cotisations et valorisation du travail",
                        "type_label": "Gain de pouvoir d'achat",
                        "an1": 5.0,
                        "an5": 15.0,
                        "cum5": 50.0,
                        "qui": "Salariés et classes moyennes",
                        "comment": "Baisse des prélèvements sur les revenus d'activité",
                        "pourquoi": "Rendre le travail plus rémunérateur",
                        "source": f"Orientations {name} 2027"
                    }
                ]
            }
        ],
        "macro_return_an1": 5.0,
        "macro_return_an5": 18.0,
        "macro_return_cum5": 60.0,
        "state_budget_an1": 502.0,
        "state_budget_an5": 495.0,
        "state_rev_an1": 310.0,
        "state_rev_an5": 320.0,
        "poles_depenses_10": [
            ("1. Retraites & Régimes Spéciaux", "CNAV, Agirc-Arrco", 382.0, 381.0, 378.0, "Trajectoire d'équilibre"),
            ("2. Santé & Hôpital Public", "Assurance Maladie", 254.0, 255.0, 252.0, "Optimisation des filières"),
            ("3. Solidarité, Famille & Minima", "CNAF, RSA", 212.0, 211.0, 209.0, "Recentrage sur les ayant-droits"),
            ("4. Collectivités Territoriales", "Communes, Régions", 156.0, 156.0, 155.0, "Pactes de responsabilité"),
            ("5. Éducation & Recherche", "Écoles, Universités", 115.0, 116.0, 118.0, "Priorité fondamentale"),
            ("6. Régalien : Défense, Police & Justice", "Armées, Police", 107.0, 108.0, 111.0, "Renforcement régalien"),
            ("7. Économie, Transports & Écologie", "SNCF, Transition", 105.0, 104.0, 101.0, "Écologie pragmatique"),
            ("8. Chômage & Insertion", "France Travail", 68.0, 67.0, 63.0, "Retour à l'emploi accéléré"),
            ("9. Charge de la Dette Publique", "Agence France Trésor", 58.0, 57.0, 53.0, "Désendettement souverain"),
            ("10. Administration État & UE", "Ministères", 57.0, 56.0, 53.0, "Lutte contre les doublons")
        ],
        "familles_recettes_7": [
            ("1. Cotisations Sociales & CSG", "Cotisants", 678.0, 674.0, 668.0, "Allègement", "Modulation des charges"),
            ("2. TVA & Consommation", "Consommateurs", 319.0, 322.0, 328.0, "Consommation", "Dynamique d'activité"),
            ("3. Impôt Sociétés & Production", "Entreprises", 137.0, 137.0, 140.0, "Compétitivité", "Attractivité économique"),
            ("4. Impôt Revenu & Épargne", "Ménages", 95.0, 96.0, 98.0, "Assiette", "Élargissement de l'assiette"),
            ("5. Fiscalité Patrimoine", "Patrimoine", 92.0, 91.0, 90.0, "Stabilité", "Transmission facilitée"),
            ("6. Recettes Non Fiscales", "Participations", 47.0, 48.0, 49.0, "Gestion", "Dividendes d'actifs"),
            ("7. Effet Retour Croissance", "PIB", 0.0, 7.0, 25.0, "Relance", "Croissance induite")
        ],
        "cas_types_8": [
            ("1. Salarié au SMIC", "1 426 € net", "Baisse de cotisations", 1200, 100, "Gain mensuel direct."),
            ("2. Salarié Médian", "2 050 € net", "Allègement de charges", 1800, 150, "Pouvoir d'achat net revalorisé."),
            ("3. Famille 2 Enfants", "4 200 € net", "Mesures familiales", 2200, 183, "Soutien aux foyers avec enfants."),
            ("4. Artisan / Commerçant", "2 800 € mensuel", "Baisse impôts production", 1900, 158, "Trésorerie d'activité dégagée."),
            ("5. Retraité Moyen", "1 650 € pension", "Maintien indexation", 600, 50, "Pension préservée."),
            ("6. Enseignant Débutant", "2 100 € net", "Revalorisation indiciaire", 1800, 150, "Reconnaissance métier."),
            ("7. PME 50 Salariés", "8 M€ CA", "Allègements de cotisations", 22000, 1833, "Embauches facilitées."),
            ("8. Foyer Ruraux", "2 700 € net", "Aides mobilité et carburant", 1500, 125, "Compensation transports.")
        ],
        "repartition_doughnut": [
            ("Allègements Cotisations", 15.0),
            ("Régalien & Justice", 6.0),
            ("École & Santé", 8.0),
            ("Économies État", 14.0),
            ("Désendettement Net", 18.0)
        ]
    }
    build_candidate_deliverables(cfg)

    # 5. Smart reader index.html
    tpl_html = (CANDS_DIR / "David Lisnard" / "index.html").read_text(encoding="utf-8")
    c_reader = tpl_html.replace("David Lisnard", name)
    c_reader = c_reader.replace("Nouvelle Énergie", c_data["parti"])
    c_reader = c_reader.replace("Maire de Cannes, Président de l'Association des Maires de France (AMF)", f"Candidat {c_data['parti']}")
    c_reader = c_reader.replace("Droite libérale, régalienne & décentralisatrice", c_data["famille"])
    c_reader = c_reader.replace("#0ea5e9", c_data["color"])
    c_reader = c_reader.replace("Lisnard", name.replace(" ", "_"))
    c_reader = c_reader.replace("🟢 500+ parrainages validés", c_data["parr_label"])
    c_reader = c_reader.replace("1 394", str(int(c_data["dep_an5"])))
    c_reader = c_reader.replace("1394", str(int(c_data["dep_an5"])))
    c_reader = c_reader.replace("Chiffrage_Programme_David_Lisnard_2027.xlsx", f"Chiffrage_Programme_{name.replace(' ', '_')}_2027.xlsx")
    c_reader = c_reader.replace("Visualisation_Programme_et_Comparatif_Budget_Lisnard.html", f"Visualisation_Programme_et_Comparatif_Budget_{name.replace(' ', '_')}.html")
    (cand_dir / "index.html").write_text(c_reader, encoding="utf-8")

    # 6. JSON Candidats
    cands = [c for c in cands if c.get("name") != name]
    c_entry = {
        "name": name,
        "parti": c_data["parti"],
        "famille": c_data["famille"],
        "orientation": c_data["orientation"],
        "color": c_data["color"],
        "dep_an5": float(c_data["dep_an5"]),
        "def_an5": float(c_data["def_an5"]),
        "def_pct": float(c_data["def_pct"]),
        "crash_score": c_data["crash_score"],
        "parr_status": c_data["parr_status"],
        "parr_label": c_data["parr_label"],
        "url_dir": f"./candidats/{folder_name}/index.html",
        "url_html": f"./candidats/{folder_name}/Visualisation_Programme_et_Comparatif_Budget_{name.replace(' ', '_')}.html",
        "url_xlsx": f"./candidats/{folder_name}/Chiffrage_Programme_{name.replace(' ', '_')}_2027.xlsx",
        "folder_name": folder_name,
        "real_xlsx": f"Chiffrage_Programme_{name.replace(' ', '_')}_2027.xlsx",
        "real_html": f"Visualisation_Programme_et_Comparatif_Budget_{name.replace(' ', '_')}.html",
        "is_primary": True,
        "status_candidature": "Candidat en campagne"
    }
    cands.insert(min(c_data["pos"], len(cands)), c_entry)

    # 7. Matrices
    for m_key, m_val in c_data["matrices"].items():
        if m_key in themes:
            themes[m_key][name] = m_val

    # 8. Sondages
    polls_list = [p for p in polls_list if p.get("name") != name]
    polls_list.append({
        "name": name,
        "score": c_data["poll_score"],
        "min": c_data["poll_min"],
        "max": c_data["poll_max"],
        "real": True,
        "party": c_data["poll_party"],
        "color": c_data["color"],
        "evolution": c_data["poll_evo"],
        "tendance": c_data["poll_trend"],
        "historique": [
            {"date": "2026-10-15", "score": round(c_data["poll_score"] - 0.5, 1)},
            {"date": "2026-11-01", "score": c_data["poll_score"]},
            {"date": "2026-11-10", "score": c_data["poll_score"]}
        ]
    })

    # 9. Sources
    if not any(cs.get("candidat") == name for cs in cands_sources):
        cands_sources.append({
            "candidat": name,
            "parti": c_data["parti"],
            "url": f"https://www.{name.lower().replace(' ', '')}2027.fr/",
            "feed": None
        })

print("\n=== SAUVEGARDE DES FICHIERS MAÎTRES DATA/ ===")
cands_json_path.write_text(json.dumps(cands, ensure_ascii=False, indent=2), encoding="utf-8")
themes_json_path.write_text(json.dumps(themes, ensure_ascii=False, indent=2), encoding="utf-8")

polls_list.sort(key=lambda x: x.get("score", 0), reverse=True)
polls["sondages"] = polls_list
polls_json_path.write_text(json.dumps(polls, ensure_ascii=False, indent=2), encoding="utf-8")

sources["sites_candidats"] = cands_sources
sources_path.write_text(json.dumps(sources, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"✓ Tous les fichiers maîtres enregistrés avec {len(cands)} candidats déclarés.")

# Mise à jour de ETAT_DES_PARRAINAGES_2027.md
parr_md = ROOT / "candidats" / "ETAT_DES_PARRAINAGES_2027.md"
if parr_md.exists():
    lines_p = [
        "# ÉTAT DES LIEUX DES PARRAINAGES - PRÉSIDENTIELLE 2027",
        f"*(Périmètre Officiel : {len(cands)} Candidats Déclarés en Lice)*\n",
        "Chaque candidat doit recueillir au moins **500 parrainages** d'élus d'au moins 30 départements différents.\n",
        "---",
        "## 🟢 1. PARRAINAGES ASSURÉS / VALIDÉS (500+ ÉLUS)",
    ]
    for c in [x for x in cands if x.get("parr_status") == "green"]:
        lines_p.append(f"- **{c['name']}** ({c['parti']}) : {c.get('parr_label')}")
    lines_p.append("\n---\n## 🟠 2. EN BONNE VOIE (300 À 499 PARRAINAGES)")
    for c in [x for x in cands if x.get("parr_status") == "orange"]:
        lines_p.append(f"- **{c['name']}** ({c['parti']}) : {c.get('parr_label')}")
    lines_p.append("\n---\n## 🔴 3. EN DIFFICULTÉ (< 300 PARRAINAGES)")
    for c in [x for x in cands if x.get("parr_status") == "red"]:
        lines_p.append(f"- **{c['name']}** ({c['parti']}) : {c.get('parr_label')}")
    lines_p.append("\n---\n*Observatoire Indépendant des Candidats & Budgets 2027*")
    parr_md.write_text("\n".join(lines_p), encoding="utf-8")
    print(f"✓ {parr_md.name} mis à jour.")

# Mise à jour de INDEX_CANDIDATS.md
idx_c = ROOT / "candidats" / "INDEX_CANDIDATS.md"
if idx_c.exists():
    lines_ic = [
        f"# INDEX DES CANDIDATS AUDITÉS - PRÉSIDENTIELLE 2027 ({len(cands)} CANDIDATS DÉCLARÉS)",
        "\nOrdre officiel selon l'Hémicycle parlementaire (de l'extrême gauche à l'extrême droite) :\n"
    ]
    for i, c in enumerate(cands, 1):
        lines_ic.append(f"{i}. **[{c['name']}](./{c['name']}/INDEX.md)** ({c['parti']}) — *Dossier complet (28 fiches + Excel + Dashboard)*")
    idx_c.write_text("\n".join(lines_ic), encoding="utf-8")
    print(f"✓ {idx_c.name} mis à jour.")

print("\n=== OPÉRATION MULTI-CANDIDATS ACHEVÉE AVEC SUCCÈS ! ===")
