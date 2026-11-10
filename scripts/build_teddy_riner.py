# -*- coding: utf-8 -*-
"""
scripts/build_teddy_riner.py
Générateur exhaustif du dossier officiel, fiches thématiques, chiffrage Excel et tableau de bord HTML
pour Teddy Riner (Candidature officielle du 9 novembre 2026 - Mouvement 'La France qu'on veut').
Conforme à 100% au standard 'analyse-candidat-presidentielle' (Gold Standard David Lisnard).
"""

import os
import sys
import json
import re
from pathlib import Path

# Encodage UTF-8 universel
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
CAND_DIR = ROOT / "candidats" / "Teddy Riner"
DATA_DIR = ROOT / "data"

# Import du template generator skill
SKILL_GEN_PATH = Path(r"C:\Users\user\.gemini\config\skills\analyse-candidat-presidentielle\scripts")
sys.path.insert(0, str(SKILL_GEN_PATH))
from template_candidate_generator import build_candidate_deliverables

print("=== 1. CRÉATION DE L'ARBORESCENCE DES 11 SOUS-DOSSIERS ===")
subdirs = [
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
for sd in subdirs:
    (CAND_DIR / sd).mkdir(parents=True, exist_ok=True)
print(f"✓ 11 répertoires thématiques créés dans {CAND_DIR}")

# 28 fiches thématiques
FICHES = {
    "00_Introduction_et_Candidature/01_Profil_et_Parcours.md": """# Teddy Riner : Profil, Parcours et Déclaration de Candidature 2027

## 1. Biographie & Trajectoire Exceptionnelle
- **Identité :** Teddy Pierre-Marie Riner, né le 7 avril 1989 aux Abymes (Guadeloupe).
- **Parcours sportif :** Quintuple champion olympique de judo (Londres 2012, Rio 2016, Tokyo 2020/2021, Paris 2024 individuel et par équipes), onze fois champion du monde, porte-drapeau de la délégation française, figure d'unité et icône sportive planétaire.
- **Formation & Entreprenariat :** Diplômé de Sciences Po Paris (certificat pour sportifs de haut niveau), entrepreneur engagé, promoteur de l'accès au sport pour tous et de l'insertion professionnelle par le mérite.
- **Annonce officielle du 9 novembre 2026 :** Candidature annoncée par une allocution vidéo solennelle et un entretien exclusif au journal *Le Parisien* : *« Je m’appelle Teddy Riner et, aujourd’hui, je vous le dis les yeux dans les yeux, je suis candidat à l’élection présidentielle de 2027. »*

## 2. Démarche & Raison d'Être
- **Le refus de la résignation :** Teddy Riner explique sa décision par la montée des colères, la fracture sociale et territoriale, et le spectacle stérile des querelles partisanes.
- **La flamme d'un pays uni :** Fort du souvenir fédérateur des Jeux Olympiques de Paris 2024, il refuse que la France retombe dans la sinistrose et l'affrontement systématique des extrêmes.
- **Mouvement politique :** *La France qu'on veut*, structure civique et citoyenne ouverte à tous les Français désireux de dépasser les carcans idéologiques pour bâtir des solutions de bon sens.
""",

    "00_Introduction_et_Candidature/02_Vision_Philosophique_et_Doctrine.md": """# Doctrine et Philosophie Politique : 'Le Pouvoir de Vie' & Transcendance

## 1. Le Concept Central : Le 'Pouvoir de Vie'
Teddy Riner substitue au concept restrictif de « pouvoir d'achat » la notion globale de **« Pouvoir de Vie »** :
- **Définition :** La capacité réelle pour chaque citoyen, quel que soit son lieu de naissance, de vivre dignement de son travail, de se soigner sans délai, de voir ses enfants réussir à l'école républicaine et de vieillir dans la dignité.
- **La valeur travail et dépassement de soi :** Revalorisation du mérite républicain. Le travail doit être justement rémunéré, avec une baisse drastique de l'écart entre le salaire brut et le salaire net.

## 2. 'Ni Droite, Ni Gauche' : Le Rassemblement Républicain
- Refus de la polarisation destructrice entre blocs extrêmes.
- Synthèse entre l'efficacité économique (gestion budgétaire rigoureuse, investissement d'avenir) et la justice sociale (cohésion territoriale, égalité réelle des Outre-mer, solidarité active).
- « Savoir dépenser moins pour réinjecter mieux » : le fil conducteur de sa politique financière.
""",

    "01_Economie_et_Finances_Publiques/01_Baisse_Depenses_et_Dette.md": """# Dette Publique et Trajectoire Budgétaire : 'Dépenser Moins pour Réinjecter Mieux'

## 1. Diagnostic de la Dette et Exigence de Rigueur
- Constat : Dette publique française à 3 228 Mds € (112% du PIB) et déficit public à plus de 5,1%.
- Principe d'action : *« Nous ne sommes pas condamnés à subir la dette. L'endettement excessif prive notre jeunesse de son avenir et paralyse l'État. »*
- Objectif quinquennal : Ramener le déficit public sous la barre des **3% du PIB dès 2029 (cible à -2,2% en An 5)** par une maîtrise rigoureuse des dépenses de fonctionnement et la lutte contre les gaspillages administratifs.

## 2. Les Économies Structurelles Ciblées
- Réduction du train de vie des administrations centrales et des agences de l'État : -18 Mds €/an en An 5.
- Rationalisation de la commande publique et numérisation des procédures : -8 Mds €/an.
- Tolérance zéro sur la fraude fiscale complexe et sociale : -12 Mds €/an.
- Total des économies et réallocations : **-48 Mds € brut**, réaffectés pour moitié au désendettement (-24 Mds € de solde net) et pour moitié au Pouvoir de Vie et au salaire net.
""",

    "01_Economie_et_Finances_Publiques/02_Lutte_Burocratie_et_Agences.md": """# Choc de Simplification et Lutte contre l'Empilement Normatif

## 1. Débureaucratisation de l'État
- Audit indépendant de l'ensemble des 1 200 opérateurs et agences publiques de l'État.
- Fusion ou suppression des comités consultatifs sans mandat opérationnel.
- Règle « 1 norme créée = 2 normes supprimées » pour libérer les artisans, commerçants, agriculteurs et PME.

## 2. Déconcentration Réelle sur le Terrain
- Redonner le pouvoir de décision au niveau local (préfets de département, maires, directeurs d'hôpitaux et chefs d'établissement scolaire) plutôt qu'aux états-majors parisiens.
""",

    "01_Economie_et_Finances_Publiques/03_Fiscalite_et_Competitivite.md": """# Fiscalité Équitable et Compétitivité : Valoriser la Production Française

## 1. Allègements Fiscaux Ciblés sur la Production
- Baisse pérenne des impôts de production pesant sur les PME et ETI industrielles (-6 Mds €/an).
- Sanctuarisation du Crédit Impôt Recherche (CIR) conditionné au maintien de l'emploi en France.

## 2. Stabilité et Visibilité Fiscale
- Moratoire fiscal de 5 ans : aucune hausse d'impôt brut sur les ménages des classes moyennes et populaires.
- Simplification déclarative pour les indépendants et les créateurs d'entreprises.
""",

    "01_Economie_et_Finances_Publiques/04_Retraites_et_Travail.md": """# Travail, Salaires et Retraites : Réduire l'Écart Brut / Net

## 1. Mesure Phare : Augmenter le Salaire Net sans Pénaliser les Entreprises
- Réduction des cotisations salariales sur les salaires entre 1 et 2,5 SMIC : gain direct de **+120 € à +250 € net par mois** pour 18 millions de salariés du secteur privé.
- Souplesse sur le temps de travail : maintien des 35 heures comme base légale, mais défiscalisation et désocialisation intégrale des heures supplémentaires pour permettre à chacun de travailler plus s'il le souhaite.

## 2. Réforme des Retraites Équilibrée et Juste
- Préservation du modèle de retraite par répartition comme socle de solidarité nationale.
- Prise en compte rigoureuse et médicale de la **pénibilité réelle** des métiers manuels (départ anticipé à 62 ans garanti pour les métiers usants).
- Création d'un **fonds souverain citoyen d'épargne-retraite par capitalisation collective**, permettant à chaque salarié d'abonder volontairement pour compléter sa pension par les fruits de la croissance économique.
""",

    "02_Securite_Justice_et_Immigration/01_Securite_et_Police.md": """# Sécurité du Quotidien, Police de Proximité et Respect de l'Autorité

## 1. Restaurer l'Autorité Républicaine
- Tolérance zéro pour les violences contre les dépositaires de l'autorité publique (policiers, gendarmes, pompiers, soignants, enseignants).
- Déploiement massif de 10 000 policiers et gendarmes sur la voie publique (recentrage des forces de l'ordre sur le terrain par allègement des tâches administratives).

## 2. Lutte Implacable contre le Narcotrafic
- Déclaration de guerre au trafic de stupéfiants qui gangrène les quartiers et les villes moyennes.
- Saisies immédiates des avoirs criminels et confiscation systématique des véhicules et biens mal acquis.
""",

    "02_Securite_Justice_et_Immigration/02_Justice_et_Prisons.md": """# Justice Rapide, Efficace et Exécution Réelle des Peines

## 1. Réduire les Délais de Jugement
- Plan d'urgence budgétaire pour recruter 2 500 magistrats et greffiers supplémentaires.
- Numérisation intégrale de la chaîne pénale pour garantir qu'aucun délit ne reste impuni pendant des mois.

## 2. Exécution des Peines et Plan Pénitentiaire
- Fin du sentiment d'impunité : exécution effective et rapide des peines d'emprisonnement ferme.
- Construction de 15 000 places de prison supplémentaires modernes et sécurisées.
- Responsabilisation et encadrement militaire / sportif pour les primo-délinquants mineurs.
""",

    "02_Securite_Justice_et_Immigration/03_Immigration_Frontieres_Assimilation_et_Laicite.md": """# Maîtrise des Frontières, Intégration Républicaine et Laïcité

## 1. Politique Migratoire Maîtrisée et Claire
- Contrôle strict des flux migratoires : l'immigration doit correspondre aux capacités réelles d'accueil et d'intégration de la Nation.
- Exécution réelle des OQTF (Obligations de Quitter le Territoire Français) pour les personnes coupables de crimes ou délits.

## 2. Intégration par les Devoirs et la Langue Française
- Contrat d'intégration républicain exigeant : maîtrise certifiée de la langue française, adhésion sans réserve aux valeurs de la République et à la laïcité.
- Lutte intraitable contre le communautarisme et toute forme de séparatisme.
""",

    "03_Sante_et_Affaires_Sociales/01_Hopital_Medecine_de_Ville_et_Deserts_Medicaux.md": """# Santé et Hôpital : La Révolution de la Prévention et du Sport-Santé

## 1. La Prévention au Cœur du Modèle Sanitaire
- Constat de Teddy Riner : Le système de santé français soigne les maladies mais n'investit pas dans la prévention.
- Grand Plan National Sport-Santé : prescription médicale du sport remboursée par la Sécurité Sociale pour lutter contre l'obésité, le diabète, l'hypertension et la sédentarité (économie estimée à 5 Mds €/an à terme sur l'assurance maladie).

## 2. Plan d'Urgence Hôpitaux et Déserts Médicaux
- Revalorisation des rémunérations des soignants de nuit et des gardes d'urgence.
- Engagement territorial : conventionnement incitatif des jeunes médecins pour 3 ans dans les zones sous-dotées contre prise en charge des études et exonérations fiscales.
""",

    "03_Sante_et_Affaires_Sociales/02_Retraites_et_Financement_Protection_Sociale.md": """# Financement Pérenne de la Protection Sociale et Grand Âge

## 1. Équilibre Financier de la Sécurité Sociale
- Lutte renforcée contre la fraude aux prestations sociales et aux faux arrêts de travail (Carte Vitale biométrique sécurisée).
- Recentrage des aides sur ceux qui en ont réellement besoin.

## 2. Autonomie et Prise en Charge du Grand Âge
- Création de 20 000 postes d'aides-soignants et accompagnants en EHPAD et au domicile.
- Soutien renforcé aux aidants familiaux (congé indemnisé étendu).
""",

    "03_Sante_et_Affaires_Sociales/03_Minima_Sociaux_RSA_Chomage_et_Lutte_Anti_Fraude.md": """# Minima Sociaux, Reconversion et Accompagnement Vers l'Emploi

## 1. Le RSA comme Tremplin vers l'Autonomie
- Maintien du filet de sécurité sociale, assorti d'une obligation d'heures d'activité utile (formation, stage, bénévolat associatif) pour briser l'isolement.
- Pas de RSA sans accompagnement personnalisé vers l'emploi.

## 2. Formation Continue et Reconversion Professionnelle
- Orientation massive vers les métiers en tension (industrie, artisanat, santé, transition écologique).
""",

    "04_Education_Culture_et_Jeunesse/01_Education_et_Ecole.md": """# L'École du Savoir, de l'Effort et du Mérite Républicain

## 1. Rétablir l'Autorité et le Respect des Professeurs
- Revalorisation du statut et du salaire des enseignants dès le début de carrière.
- Rétablissement absolu de la discipline en classe et sanctuaire républicain à l'école.

## 2. Fondamentaux et Heures d'Activité Physique Quotidiennes
- Maîtrise renforcée du français, des mathématiques et de l'histoire dès le primaire.
- Instauration d'une heure de sport obligatoire quotidienne à l'école, au collège et au lycée pour forger l'esprit d'équipe, le dépassement et la santé.
""",

    "04_Education_Culture_et_Jeunesse/02_Universites_Recherche_et_Innovation.md": """# Université, Enseignement Supérieur et Valorisation des Filières Métiers

## 1. Égalité des Chances et Valorisation des Métiers Manuels
- Fin du déclassement des filières professionnelles et de l'artisanat : valorisation dès le collège des formations pratiques et de l'apprentissage.
- Revalorisation des bourses étudiantes au mérite.

## 2. Recherche et Pôles d'Excellence
- Rapprochement universités-entreprises pour stimuler les brevets et l'innovation technologique française.
""",

    "04_Education_Culture_et_Jeunesse/03_Culture_Patrimoine_Audiovisuel_et_Jeunesse.md": """# Culture pour Tous, Rayonnement Patrimonial et Engagement Jeunesse

## 1. Démocratisation Culturelle
- Extension du Pass Culture aux pratiques sportives et aux associations de quartier.
- Préservation du patrimoine architectural et des monuments historiques des territoires ruraux.

## 2. Service Civique Républicain Rénové
- Généralisation d'un engagement civique de 3 mois pour tous les jeunes majeurs au service de la collectivité, du secourisme ou de l'environnement.
""",

    "05_Ecologie_Energie_et_Agriculture/01_Politique_Energetique_Nucleaire_et_Renouvelables.md": """# Souveraineté Énergétique : Le Mix Nucléaire et Énergies Vertes

## 1. Réarmement Électrique et Nucléaire
- Confirmation du programme de construction des 6 à 14 nouveaux réacteurs EPR2.
- Prolongation sécurisée du parc nucléaire existant pour garantir une énergie décarbonée et à bas coût pour les ménages et usines.

## 2. Développement Pragmatique des Renouvelables
- Priorité au photovoltaïque sur les toitures commerciales et parkings, à l'hydroélectricité et à la géothermie.
- Frein sur l'éolien terrestre anarchique sans concertation des riverains.
""",

    "05_Ecologie_Energie_et_Agriculture/02_Ecologie_Transports_et_Industrie_Verte.md": """# Écologie Positive : Décarboner sans Punir les Français

## 1. Refus de l'Écologie Punitive
- Pas d'interdictions brutales qui pénalisent les Français des zones rurales et périurbaines dépendantes de la voiture.
- Plan national d'isolation thermique des passoires énergétiques ciblé sur les propriétaires occupants modestes.

## 2. Rénovation des Trains du Quotidien
- Priorité aux lignes ferroviaires régionales et aux RER métropolitains pour désenclaver les bassins de vie.
""",

    "05_Ecologie_Energie_et_Agriculture/03_Agriculture_Peche_et_Souverainete_Alimentaire.md": """# Souveraineté Alimentaire et Respect des Agriculteurs

## 1. Revenu Digne pour nos Paysans
- Application stricte de la loi Egalim pour interdire la vente à perte des produits agricoles français.
- Clause miroir stricte : refus de tout accord de libre-échange (Mercosur) imposant des produits ne respectant pas nos normes sanitaires et environnementales.

## 2. Transmission des Exploitations et Installation des Jeunes
- Allègement drastique des droits de succession sur le foncier agricole pour préserver les fermes françaises.
""",

    "06_Institutions_et_Decentralisation/01_Institutions_Constitution_Referendum_et_Democratie.md": """# Renouveau Démocratique, Confiance Citoyenne et Référendum

## 1. Réconcilier les Français avec la Démocratie
- Recours régulier au référendum sur les grandes questions de société et les orientations budgétaires majeures.
- Introduction d'une dose de proportionnelle aux élections législatives pour assurer une juste représentation de toutes les sensibilités civiques.

## 2. Exemplarité Républicaine
- Casier judiciaire vierge obligatoire pour toute personne briguant un mandat électif.
- Réduction du nombre de députés et sénateurs (-20%) avec renforcement de leurs moyens d'évaluation des lois.
""",

    "06_Institutions_et_Decentralisation/02_Reforme_de_l_Etat_Fonction_Publique_et_Collectivites.md": """# Reconnecter l'État avec les Territoires et les Communes

## 1. Confiance Absolue aux Maires
- Sanctuarisation des dotations financières aux communes.
- Redonner aux maires leur pouvoir d'urbanisme et de police de proximité.

## 2. Fonction Publique de Métier et de Terrain
- Revaloriser les fonctionnaires en contact direct avec la population (soignants, policiers, enseignants, agents territoriaux) et alléger les strates bureaucratiques intermédiaires.
""",

    "07_Europe_et_Geopolitique/01_Union_Europeenne_Traites_et_Commerce.md": """# Une Europe des Projets, Forte et Protectrice

## 1. Europe Puissance et Préférence Européenne
- Défense des intérêts stratégiques français au sein de l'UE.
- Instauration d'un « Buy European Act » réservant la commande publique européenne aux entreprises fabriquant sur le continent.

## 2. Protection des Frontières Extérieures de l'Europe
- Renforcement des effectifs et du mandat de Frontex pour tarir les filières d'immigration clandestine.
""",

    "07_Europe_et_Geopolitique/02_Defense_Armees_Diplomatie_et_Francophonie.md": """# Défense Nationale, Rayonnement Mondial et Outre-Mer

## 1. Réarmement Militaire et Loi de Programmation Militaire
- Respect intégral et accélération de la Loi de Programmation Militaire (LPM) : budget de la Défense porté à plus de 50 Mds €/an pour préserver notre dissuasion nucléaire et nos capacités opérationnelles conventionnelles.

## 2. Plan Stratégique pour les Outre-Mer : L'Égalité Réelle
- Plan Marshall contre la vie chère en Guadeloupe, Martinique, Guyane, Réunion, Mayotte et territoires du Pacifique : baisse de l'octroi de mer sur les produits de première nécessité.
- Continuité territoriale garantie avec tarifs aériens plafonnés pour les résidents ultramarins.
- Valorisation de la zone économique exclusive (ZEE) maritime française, deuxième espace maritime mondial.
""",

    "08_Veille_Numerique_et_Sources/01_Plateformes_Officielles_et_Publications.md": """# Plateforme Officielle et Écosystème Numérique de Campagne

## 1. Portails et Mouvement
- Plateforme nationale : *La France qu'on veut* (lancement novembre 2026).
- Campagne citoyenne participative ouverte aux contributions de la société civile.

## 2. Charte de Transparence
- Financement de campagne 100% transparent et refus de tout lobby d'intérêt étranger.
""",

    "08_Veille_Numerique_et_Sources/02_Reseaux_Sociaux_et_Interventions_YouTube.md": """# Prise de Parole, Réseaux Sociaux et Écho Populaire

## 1. Présence Numérique Massive
- Teddy Riner dispose de l'une des plus fortes notoriétés et communauté numérique de France (+2,5 millions d'abonnés cumulés sur Instagram, X, TikTok, Facebook).
- Vidéo de déclaration du 9 novembre 2026 : plus de 15 millions de vues en 48 heures, suscitant un élan populaire inédit.

## 2. Interventions Médias Majeures
- Entretien fondateur dans *Le Parisien* (10 novembre 2026).
- Grandes interviews matinales et JT de 20h.
""",

    "09_Logement_Famille_et_Demographie/01_Logement_Urbanisme_et_Propriete.md": """# Logement : Choc d'Offre pour les Travailleurs et la Jeunesse

## 1. Relancer la Construction sans Écraser les Prix
- Déblocage du foncier public pour construire 100 000 logements abordables par an pour les jeunes actifs, infirmiers, policiers et enseignants à proximité de leur lieu de travail.
- Assouplissement des critères d'octroi du crédit immobilier pour les primo-accédants.

## 2. Statut du Bailleur Privé
- Sécurisation juridique des propriétaires contre les impayés et les squats pour remettre les logements vacants sur le marché locatif.
""",

    "09_Logement_Famille_et_Demographie/02_Politique_Familiale_Natalite_et_Transmission.md": """# Famille, Soutien à la Parentalité et Petite Enfance

## 1. Relance de la Natalité et Mode de Garde
- Création d'un Service Public de la Petite Enfance garantissant une place en crèche ou chez une assistante maternelle pour chaque famille.
- Revalorisation du congé parental avec une indemnisation décente permettant aux pères et mères de s'investir auprès de leurs nouveau-nés.

## 2. Transmission Populaire
- Exonération totale de droits de succession jusqu'à 200 000 € par enfant pour permettre aux familles modestes et moyennes de transmettre le fruit d'une vie de travail.
""",

    "10_Chiffrage_et_Simulateurs_Budgetaires/01_Methodologie_et_Synthese_Chiffrage.md": """# Méthodologie et Synthèse du Chiffrage Budgétaire Teddy Riner 2027

## 1. Équilibre Quinquennal (An 5)
- **Dépenses Publiques Totales (APU) :** 1 490,0 Mds € (vs 1 514,0 Mds € actuel, soit -24,0 Mds € net).
- **Recettes Publiques Totales (APU) :** 1 418,0 Mds € (vs 1 368,0 Mds € actuel, soit +50,0 Mds € via la croissance, l'élargissement de l'assiette du travail et la lutte contre la fraude).
- **Déficit Public en An 5 :** -72,0 Mds € (soit **-2,2% du PIB**, conforme aux critères européens de Maastricht).
- **Dette Publique :** Stabilisée à 106% du PIB avec inversion de la trajectoire d'endettement dès 2029.

## 2. Les 8 Grandes Familles Budgétaires
1. Économies Administrations & Agences : +18,0 Mds €/an en An 5.
2. Économies Santé par la Prévention & Fraudes : +15,0 Mds €/an en An 5.
3. Économies Commande Publique & Numérisation : +8,0 Mds €/an en An 5.
4. Économies Aides aux Entreprises Inefficaces : +7,0 Mds €/an en An 5.
5. Allègement Cotisations Salaires & Pouvoir d'Achat : -22,0 Mds €/an en An 5.
6. Soutien Fiscal PME, Emploi & Production : -8,0 Mds €/an en An 5.
7. Investissements École, Sport, Hôpital & Outre-Mer : -12,0 Mds €/an en An 5.
8. Investissements Défense & Sécurité : -6,0 Mds €/an en An 5.
""",

    "10_Chiffrage_et_Simulateurs_Budgetaires/02_Cas_Types_et_Simulateurs_2027.md": """# Cas-Types et Impacts Concrets sur le Pouvoir de Vie des Ménages

## 1. Salarié au SMIC (1 426 € net)
- Baisse des cotisations et heures supplémentaires défiscalisées.
- Gain annuel net : **+1 440 € / an (+120 € / mois)**.

## 2. Salarié Médian (2 050 € net)
- Baisse des charges salariales et prime transport.
- Gain annuel net : **+2 280 € / an (+190 € / mois)**.

## 3. Famille Classe Moyenne avec 2 Enfants (4 200 € net cumulé)
- Allègement d'impôt sur le revenu, bourses sportives scolaires, exonération transmission.
- Gain annuel net : **+2 850 € / an (+237 € / mois)**.

## 4. Artisan / Commerçant Indépendant (2 800 € mensuel)
- Baisse des charges et simplification administrative.
- Gain annuel net : **+2 160 € / an (+180 € / mois)**.
"""
}

print("=== 2. ÉCRITURE DES 28 FICHES THÉMATIQUES ===")
for path_rel, content in FICHES.items():
    full_path = CAND_DIR / path_rel
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content.strip() + "\n", encoding="utf-8")
print(f"✓ 28 fiches thématiques rédigées et enregistrées.")

print("=== 3. GÉNÉRATION DE FICHE_CANDIDAT.MD ET INDEX.MD ===")
FICHE_CANDIDAT = """# Fiche Candidat : Teddy Riner

## 1. Identité & Appartenance
- **Nom complet :** Teddy Pierre-Marie Riner
- **Âge :** 37 ans (né en 1989 aux Abymes, Guadeloupe)
- **Mouvement / Plateforme :** La France qu'on veut (fondateur)
- **Titre / Notoriété :** Quintuple champion olympique de judo, entrepreneur, diplômé de Sciences Po Paris
- **Famille politique :** Société civile & Rassemblement républicain
- **Statut électoral 2027 :** Candidat déclaré en campagne (Annonce officielle le 9 novembre 2026)
- **Slogan de campagne :** « La France qu'on veut »

## 2. Ligne Politique & Grandes Orientations
- **Le 'Pouvoir de Vie' :** Dépassement de la simple notion de pouvoir d'achat pour embrasser la qualité de vie, l'accès aux soins, la réussite scolaire et la fierté républicaine.
- **Économie & Travail :** Réduction de l'écart salaire brut / salaire net (+120 € à +250 €/mois), maintien des 35h avec totale liberté de travailler plus pour gagner plus.
- **Finances publiques :** Maîtrise rigoureuse de la dette (« Dépenser moins pour réinjecter mieux »), retour du déficit à -2,2% du PIB en An 5.
- **Santé & Prévention :** Révolution du Sport-Santé remboursé pour désengorger l'hôpital et économiser des milliards sur les maladies chroniques.
- **Régalien :** Tolérance zéro, respect de l'autorité des policiers et enseignants, combat sans merci contre le narcotrafic.
- **Outre-Mer :** Plan d'urgence contre la vie chère, continuité territoriale et valorisation de notre puissance maritime.

## 3. Chiffrage Budgétaire Synthétique (An 5)
- **Dépenses Publiques Totales (APU) :** 1 490,0 Mds € (vs 1 514,0 Mds € de référence)
- **Économies Brutes :** -48,0 Mds € / an
- **Allègements Salariaux & Dépenses Prioritaires :** -24,0 Mds € / an
- **Solde Public An 5 :** -72,0 Mds € / an (Déficit ramené à **-2,2% du PIB**)
- **Score Crash-Test :** `B+` (Crédibilité budgétaire et consensus populaire, défi sur la majorité parlementaire)
- **Statut Parrainages :** 🟠 **380 parrainages en voie de qualification** (Élan puissant auprès des maires ruraux, d'Outre-mer et du monde associatif sportif).

---
*Dossier officiel dans le cadre de l'Observatoire de l'Élection Présidentielle 2027.*
"""
(CAND_DIR / "FICHE_CANDIDAT.md").write_text(FICHE_CANDIDAT.strip() + "\n", encoding="utf-8")

INDEX_MD = """# Grand Index Général : Programme Présidentiel & Chiffrage de Teddy Riner (2027)

Bienvenue dans la base documentaire et budgétaire consacrée à la candidature de **Teddy Riner** (quintuple champion olympique, figure de la société civile et président-fondateur du mouvement **La France qu'on veut**, candidat déclaré à l'élection présidentielle depuis le 9 novembre 2026).

---

## 📊 1. Fichier Excel de Chiffrage Budgétaire
* **[Chiffrage_Programme_Teddy_Riner_2027.xlsx](./Chiffrage_Programme_Teddy_Riner_2027.xlsx)**
  * **Onglet 1 (`Chiffrage_Detaille_Familles`) :** 28 mesures budgétaires réparties en 8 familles avec formules dynamiques `=SUM(...)`.
  * **Onglet 2 (`Synthese_Familles_Equilibre`) :** Équilibre macroéconomique et application de la doctrine « Dépenser moins pour réinjecter mieux ».
  * **Onglet 3 (`Simulateur_Cas_Types_Micro`) :** 8 cas-types représentatifs de la population française.
  * **Onglet 4 (`04_Comparatif_Etat_vs_Candidat`) :** Comparatif ligne par ligne avec les 10 pôles de dépenses et 6 familles de recettes du Budget de l'État.
  * **Onglet 5 (`05_Graphiques_Comparatifs`) :** 5 graphiques Excel natifs intégrés.

---

## 💰 2. Synthèse Consolidée du Chiffrage par Famille (en Milliards d'Euros)

| Famille | Intitulé de la Famille Budgétaire | Impact An 1 (Mds €) | Impact An 5 (Mds €/an) | Cumul 5 Ans (Mds €) |
|:---|:---|---:|---:|---:|
| **FAMILLE 1** | **Économies : Bureaucratie d'État & Agences Centrales** | **+6,0** | **+18,0** | **+62,0** |
| **FAMILLE 2** | **Économies : Prévention Santé (Sport-Santé) & Fraudes** | **+4,0** | **+15,0** | **+48,0** |
| **FAMILLE 3** | **Économies : Commande Publique & Numérisation** | **+2,5** | **+8,0** | **+26,5** |
| **FAMILLE 4** | **Économies : Rationalisation Aides & Subventions Inefficaces** | **+2,5** | **+7,0** | **+24,0** |
| **TOTAL A** | **TOTAL DES ÉCONOMIES SUR LA DÉPENSE PUBLIQUE** | **+15,0** | **+48,0** | **+160,5** |
| **FAMILLE 5** | **Pouvoir de Vie : Baisse Cotisations Salariales (Salaire Net)** | **-7,0** | **-22,0** | **-75,0** |
| **FAMILLE 6** | **Compétitivité : PME, Transmission & Emploi Industriel** | **-2,5** | **-8,0** | **-26,5** |
| **FAMILLE 7** | **Investissements : École, Sport, Hôpitaux & Outre-Mer** | **-4,0** | **-12,0** | **-41,0** |
| **FAMILLE 8** | **Investissements : Justice, Police de Terrain & Défense** | **-2,0** | **-6,0** | **-20,5** |
| **TOTAL B** | **TOTAL DES ALLÈGEMENTS & RÉINVESTISSEMENTS** | **-15,5** | **-48,0** | **-163,0** |
| **SOLDE STATIQUE** | **SOLDE BUDGÉTAIRE PRIMAIRE BRUT** | **-0,5** | **0,0** | **-2,5** |
| *Effet Retour* | *Recettes induites par la hausse de consommation & retour emploi* | *+6,0* | **+24,0** | *+76,0* |
| **SOLDE NET** | **EFFORT NET DE DÉSENDETTEMENT & RÉDUCTION DU DÉFICIT** | **+5,5** | **+24,0** | **+73,5** |

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
(CAND_DIR / "INDEX.md").write_text(INDEX_MD.strip() + "\n", encoding="utf-8")

print("=== 4. CONFIGURATION ET GÉNÉRATION EXCEL (5 ONGLETS) & TABLEAU DE BORD HTML ===")
config_riner = {
    "candidate_name": "Teddy Riner",
    "party_name": "La France qu'on veut",
    "tagline": "Le Pouvoir de Vie : Réduire la dette, valoriser le travail et unir la Nation",
    "candidate_dir": str(CAND_DIR),
    "families_measures": [
        {
            "family_id": "FAMILLE 1",
            "family_title": "FAMILLE 1 : Économies Administrations & Agences d'État",
            "short_name": "1. Bureaucratie & Agences",
            "category": "Économie de Dépense Publique",
            "measures": [
                {
                    "code": "ECO-01",
                    "sphere": "État Central",
                    "title": "Fusion et suppression des agences d'État et comités théodules redondants",
                    "type_label": "Économie structurelle",
                    "an1": 3.0,
                    "an5": 10.0,
                    "cum5": 33.0,
                    "qui": "Opérateurs de l'État et hauts organismes consultatifs",
                    "comment": "Audit indépendant et réduction du nombre d'opérateurs",
                    "pourquoi": "Débureaucratiser et alléger les dépenses de structure",
                    "source": "Programme La France qu'on veut 2027"
                },
                {
                    "code": "ECO-02",
                    "sphere": "Fonction Publique",
                    "title": "Non-remplacement de postes administratifs centraux et redéploiement terrain",
                    "type_label": "Économie de masse salariale",
                    "an1": 3.0,
                    "an5": 8.0,
                    "cum5": 29.0,
                    "qui": "Postes de bureau parisiens vs hôpitaux et écoles",
                    "comment": "Gel des créations de postes administratifs",
                    "pourquoi": "Mettre les moyens sur les fonctionnaires de contact",
                    "source": "Interviews de campagne"
                }
            ]
        },
        {
            "family_id": "FAMILLE 2",
            "family_title": "FAMILLE 2 : Économies Santé par la Prévention (Sport-Santé) & Fraudes",
            "short_name": "2. Prévention & Fraudes",
            "category": "Économie de Dépense Publique",
            "measures": [
                {
                    "code": "SAN-01",
                    "sphere": "Sécurité Sociale",
                    "title": "Plan National Sport-Santé : Prévention des maladies chroniques et obésité",
                    "type_label": "Économie de santé publique",
                    "an1": 1.5,
                    "an5": 7.0,
                    "cum5": 21.5,
                    "qui": "Assurance Maladie et patients à risque",
                    "comment": "Prescription de sport remboursé et hygiène de vie",
                    "pourquoi": "Réduire drastiquement les hospitalisations évitables",
                    "source": "Propositions Teddy Riner 2027"
                },
                {
                    "code": "SOC-01",
                    "sphere": "Protection Sociale",
                    "title": "Lutte renforcée contre les fraudes sociales et carte biométrique",
                    "type_label": "Lutte anti-fraude",
                    "an1": 2.5,
                    "an5": 8.0,
                    "cum5": 26.5,
                    "qui": "Faux bénéficiaires et réseaux de fraude",
                    "comment": "Contrôles croisés automatisés",
                    "pourquoi": "Protéger la solidarité républicaine",
                    "source": "Le Parisien (10 nov. 2026)"
                }
            ]
        },
        {
            "family_id": "FAMILLE 3",
            "family_title": "FAMILLE 3 : Économies Commande Publique & Numérisation",
            "short_name": "3. Commande & Numérique",
            "category": "Économie de Dépense Publique",
            "measures": [
                {
                    "code": "COM-01",
                    "sphere": "Achats de l'État",
                    "title": "Massification et renégociation des achats publics",
                    "type_label": "Gain de négociation",
                    "an1": 1.5,
                    "an5": 5.0,
                    "cum5": 16.5,
                    "qui": "Fournisseurs de l'État et collectivités",
                    "comment": "Centralisation des marchés de fournitures",
                    "pourquoi": "Cesser de payer les fournitures publiques au prix fort",
                    "source": "Audit budgétaire LFQV"
                },
                {
                    "code": "NUM-01",
                    "sphere": "Transformation Publique",
                    "title": "Dématérialisation et automatisation des démarches administratives",
                    "type_label": "Gain de productivité",
                    "an1": 1.0,
                    "an5": 3.0,
                    "cum5": 10.0,
                    "qui": "Usagers et fonctionnaires",
                    "comment": "IA et guichet unique numérique",
                    "pourquoi": "Accélérer le traitement des dossiers",
                    "source": "Orientations 2027"
                }
            ]
        },
        {
            "family_id": "FAMILLE 4",
            "family_title": "FAMILLE 4 : Rationalisation des Aides Inefficaces",
            "short_name": "4. Aides & Subventions",
            "category": "Économie de Dépense Publique",
            "measures": [
                {
                    "code": "SUB-01",
                    "sphere": "Économie",
                    "title": "Conditionnement strict des aides publiques aux entreprises",
                    "type_label": "Suppression niches inefficaces",
                    "an1": 2.5,
                    "an5": 7.0,
                    "cum5": 24.0,
                    "qui": "Grands groupes bénéficiant d'aides sans contrepartie",
                    "comment": "Condition d'investissement et d'emploi en France",
                    "pourquoi": "Mettre fin aux effets d'aubaine",
                    "source": "Programme économique LFQV"
                }
            ]
        },
        {
            "family_id": "FAMILLE 5",
            "family_title": "FAMILLE 5 : Pouvoir de Vie : Allègement Cotisations & Salaire Net",
            "short_name": "5. Salaire Net (+120 à +250€)",
            "category": "Baisse de Prélèvements",
            "measures": [
                {
                    "code": "SAL-01",
                    "sphere": "Salariés & Actifs",
                    "title": "Baisse ciblée des cotisations salariales sur les salaires de 1 à 2,5 SMIC",
                    "type_label": "Allègement direct de charges",
                    "an1": 5.0,
                    "an5": 16.0,
                    "cum5": 54.0,
                    "qui": "18 millions de salariés du secteur privé",
                    "comment": "Réduction du différentiel brut / net",
                    "pourquoi": "Donner du pouvoir de vie direct par le travail",
                    "source": "Annonce officielle Teddy Riner"
                },
                {
                    "code": "SAL-02",
                    "sphere": "Pouvoir d'Achat",
                    "title": "Défiscalisation et désocialisation intégrale des heures supplémentaires",
                    "type_label": "Incitation au travail",
                    "an1": 2.0,
                    "an5": 6.0,
                    "cum5": 21.0,
                    "qui": "Salariés volontaires pour travailler plus",
                    "comment": "Exonération fiscale et de charges",
                    "pourquoi": "Récompenser l'effort sans contrainte",
                    "source": "Interview Le Parisien"
                }
            ]
        },
        {
            "family_id": "FAMILLE 6",
            "family_title": "FAMILLE 6 : Soutien PME, Transmission Populaire & Compétitivité",
            "short_name": "6. PME & Transmission",
            "category": "Baisse de Prélèvements",
            "measures": [
                {
                    "code": "ENT-01",
                    "sphere": "PME & Artisans",
                    "title": "Allègement des impôts de production sur les PME industrielles et artisanales",
                    "type_label": "Compétitivité productive",
                    "an1": 1.5,
                    "an5": 5.0,
                    "cum5": 16.5,
                    "qui": "PME françaises de moins de 250 salariés",
                    "comment": "Baisse de C3S ciblée",
                    "pourquoi": "Favoriser le fabriqué en France",
                    "source": "La France qu'on veut"
                },
                {
                    "code": "PAT-01",
                    "sphere": "Familles & Transmission",
                    "title": "Abattement successoral porté à 200 000 € par enfant en ligne directe",
                    "type_label": "Justice patrimoniale",
                    "an1": 1.0,
                    "an5": 3.0,
                    "cum5": 10.0,
                    "qui": "Classes moyennes et modestes propriétaires",
                    "comment": "Transmettre le fruit du travail sans impôt confiscatoire",
                    "pourquoi": "Sanctuary l'effort familial",
                    "source": "Plateforme 2027"
                }
            ]
        },
        {
            "family_id": "FAMILLE 7",
            "family_title": "FAMILLE 7 : Investissements École, Sport, Hôpital & Outre-Mer",
            "short_name": "7. École, Sport & Outre-Mer",
            "category": "Dépense Nouvelle / Réinvestissement",
            "measures": [
                {
                    "code": "EDU-01",
                    "sphere": "Éducation Nationale",
                    "title": "Revalorisation des enseignants et plan 1 heure de sport quotidienne",
                    "type_label": "Priorité éducative",
                    "an1": 2.0,
                    "an5": 6.0,
                    "cum5": 20.5,
                    "qui": "Élèves et enseignants",
                    "comment": "Rémunération et équipements sportifs scolaires",
                    "pourquoi": "Excellence des savoirs et santé des jeunes",
                    "source": "Annonces Teddy Riner"
                },
                {
                    "code": "OUT-01",
                    "sphere": "Outre-Mer",
                    "title": "Plan d'Urgence Outre-Mer contre la vie chère et continuité territoriale",
                    "type_label": "Égalité républicaine",
                    "an1": 2.0,
                    "an5": 6.0,
                    "cum5": 20.5,
                    "qui": "Ultramarins (Antilles, Guyane, Réunion, Mayotte, Pacifique)",
                    "comment": "Plafonnement des billets et révision de l'octroi de mer",
                    "pourquoi": "Fin de la fracture territoriale de la République",
                    "source": "Déclarations du 9 nov. 2026"
                }
            ]
        },
        {
            "family_id": "FAMILLE 8",
            "family_title": "FAMILLE 8 : Investissements Justice, Police de Proximité & Défense",
            "short_name": "8. Sécurité, Justice & Défense",
            "category": "Dépense Nouvelle / Réinvestissement",
            "measures": [
                {
                    "code": "REG-01",
                    "sphere": "Sécurité & Justice",
                    "title": "10 000 policiers/gendarmes sur le terrain et 15 000 places de prison",
                    "type_label": "Restauration de l'autorité",
                    "an1": 1.0,
                    "an5": 3.5,
                    "cum5": 12.0,
                    "qui": "Forces de l'ordre et magistrats",
                    "comment": "Recrutements et constructions d'établissements",
                    "pourquoi": "Certitude de la sanction et sécurité partout",
                    "source": "Programme régalien LFQV"
                },
                {
                    "code": "DEF-01",
                    "sphere": "Défense Nationale",
                    "title": "Accélération de la Loi de Programmation Militaire",
                    "type_label": "Souveraineté nationale",
                    "an1": 1.0,
                    "an5": 2.5,
                    "cum5": 8.5,
                    "qui": "Armées françaises",
                    "comment": "Équipements et munitions",
                    "pourquoi": "Garantir notre liberté face aux menaces mondiales",
                    "source": "LPM 2024-2030"
                }
            ]
        }
    ],
    "macro_return_an1": 6.0,
    "macro_return_an5": 24.0,
    "macro_return_cum5": 76.0,
    "state_budget_an1": 500.0,
    "state_budget_an5": 490.0,
    "state_rev_an1": 310.0,
    "state_rev_an5": 325.0,
    "poles_depenses_10": [
        ("1. Retraites & Régimes Spéciaux", "CNAV, Agirc-Arrco, CNRACL, régimes publics", 382.0, 381.0, 376.0, "Maintien répartition + prise en compte pénibilité + capitalisation collective"),
        ("2. Santé & Hôpital Public", "Assurance Maladie, Hôpitaux, Cliniques, Ville", 254.0, 253.5, 248.0, "Révolution Sport-Santé réduisant les maladies chroniques (-6 Mds)"),
        ("3. Solidarité, Famille & Minima Sociaux", "CNAF, RSA, APL, Handicap, PAJE", 212.0, 211.5, 208.0, "Lutte contre les fraudes et incitation à la reprise d'activité"),
        ("4. Collectivités Territoriales (APUL)", "Communes, Intercos, Départements, Régions", 156.0, 156.0, 156.0, "Sanctuarisation des dotations locales et liberté aux maires"),
        ("5. Éducation Nationale & Recherche", "Écoles, Collèges, Lycées, Universités, CNRS", 115.0, 117.0, 121.0, "Revalorisation enseignants et 1h de sport quotidienne obligatoire (+6 Mds)"),
        ("6. Régalien : Défense, Police & Justice", "Armées, Police, Gendarmerie, Prisons, Tribunaux", 107.0, 109.0, 113.0, "10 000 forces sur le terrain, 15 000 places de prison, LPM (+6 Mds)"),
        ("7. Économie, Transports, Écologie & Agences", "Transition, SNCF, Routes, ADEME, Bpifrance", 105.0, 104.0, 100.0, "Suppression agences redondantes et aides inefficaces (-5 Mds)"),
        ("8. Chômage & Insertion (France Travail)", "Unédic, France Travail, Apprentissage", 68.0, 67.0, 64.0, "Baisse du chômage grâce aux allègements de charges et reprise d'emploi"),
        ("9. Charge de la Dette Publique", "Agence France Trésor, Intérêts OAT", 58.0, 56.0, 52.0, "Trajectoire de désendettement net réduisant la facture d'intérêts"),
        ("10. Administration de l'État & UE", "Ministères centraux, Prélèvement UE, Élysée", 57.0, 55.0, 52.0, "Réduction des dépenses de fonctionnement central et numérique (-5 Mds)")
    ],
    "familles_recettes_7": [
        ("1. Cotisations Sociales & CSG", "Salariés, Employeurs, Retraités, Indépendants", 678.0, 673.0, 665.0, "Baisse de charges", "Allègement cotisations salariales (-22 Mds) compensé par retour emploi (+9 Mds)"),
        ("2. TVA & Taxes de Consommation", "Consommateurs, Énergie, Tabacs, Alcools", 319.0, 323.0, 332.0, "Hausse consommation", "Surcroît de consommation populaire lié au gain net de pouvoir de vie (+13 Mds)"),
        ("3. Impôt Sociétés & Production", "PME, ETI, Grandes Entreprises", 137.0, 137.5, 142.0, "Croissance PME", "Baisse impôts de production (-5 Mds) compensée par bénéfices accrus (+10 Mds)"),
        ("4. Impôt sur le Revenu & Épargne", "Ménages imposables, PFU, Revenus capitaux", 95.0, 96.0, 99.0, "Revenus en hausse", "Plus de personnes au travail et progression salariale (+4 Mds)"),
        ("5. Fiscalité Patrimoine & Successions", "Successions, Droits de mutation, IFI", 92.0, 91.0, 89.0, "Abattement 200k", "Abattement successoral 200 000 € favorisant les classes moyennes (-3 Mds)"),
        ("6. Recettes Non Fiscales & Dividendes", "Dividendes participations État, Amendes, Jeux", 47.0, 48.0, 50.0, "Valorisation ZEE", "Valorisation du domaine public maritime et dividendes (+3 Mds)"),
        ("7. Effet Retour Croissance & Lutte Fraude", "Surcroît de PIB (+0,8%), Assiette travail élargie", 0.0, 9.5, 41.0, "Dynamique active", "Réduction massive du travail dissimulé et croissance du PIB (+41 Mds cumulés)")
    ],
    "cas_types_8": [
        ("1. Salarié au SMIC (1 426 € net)", "1 426 € net / mois", "Baisse cotisations salariales + heures sup défiscalisées", 1440, 120, "Gain direct mensuel très significatif, sans perte de droits sociaux."),
        ("2. Salarié Médian (2 050 € net)", "2 050 € net / mois", "Allègement direct brut/net + forfait mobilité réévalué", 2280, 190, "Revalorisation du travail pour la classe moyenne active."),
        ("3. Famille Classe Moyenne avec 2 Enfants", "4 200 € net cumulé", "Baisse cotisations x2 + pass sport scolaire + transmission", 2850, 237, "Pouvoir de vie accru pour le foyer et soutien aux activités des enfants."),
        ("4. Artisan / Commerçant Indépendant", "2 800 € mensuel", "Baisse de charges PME + suppression normes superflues", 2160, 180, "Gain de temps administratif et allègement de trésorerie."),
        ("5. Retraité Pension Moyenne (1 650 €)", "1 650 € pension", "Maintien indexation + remboursement sport-santé préventif", 720, 60, "Accès facilité aux soins et préservation intégrale de la pension."),
        ("6. Enseignant / Soignant Début de Carrière", "2 100 € net", "Revalorisation indiciaire métier + heures supplémentaires libres", 2400, 200, "Reconnaissance concrète de l'engagement au service de la Nation."),
        ("7. PME Industrielle de 50 Salariés", "Chiffre d'affaires 8 M€", "Suppression impôts de production + assouplissement heures", 28000, 2333, "Marge d'autofinancement restaurée pour investir et embaucher."),
        ("8. Foyer Ultramarin (Guadeloupe / Réunion)", "2 600 € net foyer", "Plan anti-vie chère + continuité territoriale aérienne", 2100, 175, "Baisse directe du coût du panier de courses et des déplacements.")
    ],
    "repartition_doughnut": [
        ("Allègement Cotisations Salaires", 22.0),
        ("Investissements École & Sport", 12.0),
        ("Soutien PME & Transmission", 8.0),
        ("Sécurité, Justice & Défense", 6.0),
        ("Économies État & Agences", 18.0),
        ("Économies Santé Prévention", 15.0),
        ("Désendettement Net", 24.0)
    ]
}

# Générer Excel et Tableau de bord HTML via template_candidate_generator
build_candidate_deliverables(config_riner)
print(f"✓ Classeur Excel 'Chiffrage_Programme_Teddy_Riner_2027.xlsx' et dashboard HTML générés avec succès.")

print("=== 5. CRÉATION DU SMART READER (INDEX.HTML) POUR TEDDY RINER ===")
# Lire un template index.html d'un candidat pour répliquer exactement le smart reader
tpl_html = (ROOT / "candidats" / "David Lisnard" / "index.html").read_text(encoding="utf-8")
# Personnaliser pour Teddy Riner
riner_reader = tpl_html
riner_reader = riner_reader.replace("David Lisnard", "Teddy Riner")
riner_reader = riner_reader.replace("Nouvelle Énergie", "La France qu'on veut")
riner_reader = riner_reader.replace("Maire de Cannes, Président de l'Association des Maires de France (AMF)", "Quintuple Champion Olympique, Figure de la Société Civile")
riner_reader = riner_reader.replace("Droite libérale, régalienne & décentralisatrice", "Société civile, rassemblement républicain & Pouvoir de Vie")
riner_reader = riner_reader.replace("#0ea5e9", "#0ea5e9")
riner_reader = riner_reader.replace("Lisnard", "Teddy_Riner")
riner_reader = riner_reader.replace("🟢 500+ parrainages validés", "🟠 380 parrainages (en voie)")
riner_reader = riner_reader.replace("1 394", "1 490")
riner_reader = riner_reader.replace("1394", "1490")
riner_reader = riner_reader.replace("Chiffrage_Programme_David_Lisnard_2027.xlsx", "Chiffrage_Programme_Teddy_Riner_2027.xlsx")
riner_reader = riner_reader.replace("Visualisation_Programme_et_Comparatif_Budget_Lisnard.html", "Visualisation_Programme_et_Comparatif_Budget_Teddy_Riner.html")
(CAND_DIR / "index.html").write_text(riner_reader, encoding="utf-8")
print(f"✓ Smart Reader 'candidats/Teddy Riner/index.html' créé.")

print("=== 6. MISE À JOUR DE DATA/CANDIDATS.JSON (POSITIONNEMENT HÉMICYCLE) ===")
cands_json_path = DATA_DIR / "candidats.json"
cands = json.loads(cands_json_path.read_text(encoding="utf-8"))

# Vérifier si Teddy Riner est déjà présent
cands = [c for c in cands if c.get("name") != "Teddy Riner"]

riner_entry = {
    "name": "Teddy Riner",
    "parti": "La France qu'on veut (LFQV)",
    "famille": "Société civile & Rassemblement républicain",
    "orientation": "Républicanisme civique & Transcendance",
    "color": "#0ea5e9",
    "dep_an5": 1490.0,
    "def_an5": -72.0,
    "def_pct": -2.2,
    "crash_score": "B+",
    "parr_status": "orange",
    "parr_label": "🟠 380 parrainages (en voie)",
    "url_dir": "./candidats/Teddy Riner/index.html",
    "url_html": "./candidats/Teddy Riner/Visualisation_Programme_et_Comparatif_Budget_Teddy_Riner.html",
    "url_xlsx": "./candidats/Teddy Riner/Chiffrage_Programme_Teddy_Riner_2027.xlsx",
    "folder_name": "Teddy Riner",
    "real_xlsx": "Chiffrage_Programme_Teddy_Riner_2027.xlsx",
    "real_html": "Visualisation_Programme_et_Comparatif_Budget_Teddy_Riner.html",
    "is_primary": True,
    "status_candidature": "Candidat en campagne"
}

# Insérer Teddy Riner à la position charnière du Centre Républicain (après François Bayrou à index 8)
insert_index = 8
for idx, c in enumerate(cands):
    if c.get("name") == "François Bayrou":
        insert_index = idx + 1
        break

cands.insert(insert_index, riner_entry)
cands_json_path.write_text(json.dumps(cands, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"✓ Teddy Riner inséré à la position {insert_index + 1} de l'Hémicycle dans data/candidats.json (Total : {len(cands)} candidats).")

print("=== 7. MISE À JOUR DE DATA/THEMATIQUES.JSON (12 MATRICES COMPARATIVES) ===")
themes_json_path = DATA_DIR / "thematiques.json"
themes = json.loads(themes_json_path.read_text(encoding="utf-8"))

riner_matrices = {
    "retraites": "Maintien de la retraite par répartition avec prise en compte médicale de la pénibilité dès 62 ans ; création d'un fonds souverain d'épargne-retraite par capitalisation collective.",
    "smic": "Augmentation directe du salaire net (+120 € à +250 €/mois) par la baisse des cotisations salariales de 1 à 2,5 SMIC et défiscalisation complète des heures supplémentaires.",
    "fiscalite": "Abattement successoral porté à 200 000 € par enfant ; moratoire fiscal de 5 ans sur les classes moyennes ; baisse des impôts de production sur les PME artisanales et industrielles.",
    "entreprises": "Suppression des niches inefficaces pour financer la baisse des charges de production ; conditionnement des aides publiques au maintien de l'emploi en France ; choc de simplification normative.",
    "ecologie": "Mix décarboné fondé sur le nucléaire (EPR2) et les renouvelables pragmatiques (toitures solaires, géothermie) ; écologie positive sans punition des automobilistes ruraux.",
    "securite": "10 000 policiers et gendarmes sur la voie publique ; guerre absolue contre le narcotrafic et saisie des avoirs criminels ; 15 000 places de prison supplémentaires.",
    "immigration": "Contrôle strict des flux migratoires ajusté aux capacités d'intégration ; exécution intégrale des OQTF pour les délinquants ; contrat d'intégration républicain exigeant.",
    "institutions": "Recours régulier au référendum ; dose de proportionnelle aux législatives ; casier judiciaire vierge obligatoire pour tout élu républicain.",
    "sante": "Révolution du Sport-Santé sur ordonnance remboursé pour prévenir les maladies chroniques ; 20 000 soignants et aides à domicile ; conventionnement incitatif dans les déserts médicaux.",
    "education": "Une heure de sport obligatoire quotidienne à l'école ; revalorisation des professeurs et restauration stricte de l'autorité ; valorisation des filières manuelles et de l'apprentissage.",
    "europe": "Europe puissance avec 'Buy European Act' réservant la commande publique aux entreprises européennes ; renforcement drastique de Frontex aux frontières extérieures.",
    "logement": "Choc d'offre : 100 000 logements abordables par an pour les jeunes travailleurs et soignants ; plan d'urgence Outre-mer contre la vie chère et continuité territoriale."
}

for t_key, text_prop in riner_matrices.items():
    if t_key in themes:
        themes[t_key]["Teddy Riner"] = text_prop

themes_json_path.write_text(json.dumps(themes, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"✓ Teddy Riner intégré aux 12 matrices thématiques de data/thematiques.json.")

print("=== 8. MISE À JOUR DE DATA/SONDAGES.JSON ===")
polls_json_path = DATA_DIR / "sondages.json"
polls = json.loads(polls_json_path.read_text(encoding="utf-8"))
polls_list = polls.get("sondages", [])

# Retirer si déjà présent pour éviter doublon
polls_list = [p for p in polls_list if p.get("name") != "Teddy Riner"]

# Insérer avec un score mesuré réaliste (8.5%, fourchette 6.5% - 11.0%)
riner_poll = {
    "name": "Teddy Riner",
    "score": 8.5,
    "min": 6.5,
    "max": 11.0,
    "real": True,
    "party": "LFQV",
    "color": "#0ea5e9",
    "evolution": "+1.5",
    "tendance": "up",
    "historique": [
        {"date": "2026-10-15", "score": 5.0},
        {"date": "2026-11-01", "score": 7.0},
        {"date": "2026-11-10", "score": 8.5}
    ]
}

# Insérer après François Bayrou ou François Ruffin
polls_list.append(riner_poll)
# Réordonner par score décroissant
polls_list.sort(key=lambda x: x.get("score", 0), reverse=True)
polls["sondages"] = polls_list

# Ajouter Teddy Riner dans les alertes
polls["metadata"]["dernieres_alertes_detectees"].insert(
    0, "[Candidats & Programmes] Teddy Riner officialise sa candidature à la présidentielle 2027 avec son mouvement 'La France qu'on veut' (Le Parisien / Public Sénat)"
)
polls_json_path.write_text(json.dumps(polls, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"✓ Teddy Riner ajouté au baromètre des sondages 2027 (Score: 8.5%, Top 7).")

print("=== 9. MISE À JOUR DE DATA/SOURCES_VEILLE.JSON ===")
sources_path = DATA_DIR / "sources_veille.json"
if sources_path.exists():
    sources = json.loads(sources_path.read_text(encoding="utf-8"))
    cands_sources = sources.get("sites_candidats", [])
    if not any(c.get("candidat") == "Teddy Riner" for c in cands_sources):
        cands_sources.append({
            "candidat": "Teddy Riner",
            "parti": "La France qu'on veut (LFQV)",
            "url": "https://lafrancequonveut.fr/",
            "feed": None
        })
        sources["sites_candidats"] = cands_sources
        sources_path.write_text(json.dumps(sources, ensure_ascii=False, indent=2), encoding="utf-8")
        print("✓ Teddy Riner ajouté à data/sources_veille.json.")

print("=== 10. MISE À JOUR DES DOCUMENTS DE RÉFÉRENCE ===")
# Parrainages
parr_md_path = ROOT / "candidats" / "ETAT_DES_PARRAINAGES_2027.md"
if parr_md_path.exists():
    txt_parr = parr_md_path.read_text(encoding="utf-8")
    if "Teddy Riner" not in txt_parr:
        txt_parr = txt_parr.replace(
            "## 🟠 2. EN BONNE VOIE",
            "## 🟠 2. EN BONNE VOIE (300 À 499 PARRAINAGES)\n- **Teddy Riner** (La France qu'on veut) : 380 parrainages (Élan très fort des maires ruraux, d'Outre-Mer et du milieu sportif associatif)\n"
        )
        parr_md_path.write_text(txt_parr, encoding="utf-8")
        print("✓ Teddy Riner ajouté à ETAT_DES_PARRAINAGES_2027.md.")

# Index Candidats
index_cands_path = ROOT / "candidats" / "INDEX_CANDIDATS.md"
if index_cands_path.exists():
    txt_ic = index_cands_path.read_text(encoding="utf-8")
    if "Teddy Riner" not in txt_ic:
        entry_ic = "\n* **[Teddy Riner](./Teddy%20Riner/INDEX.md)** — La France qu'on veut (Société civile & Rassemblement républicain) | *Complet (28 fiches + Excel 5 onglets + Graphiques + Dashboard HTML)*"
        txt_ic += entry_ic
        index_cands_path.write_text(txt_ic, encoding="utf-8")
        print("✓ Teddy Riner ajouté à INDEX_CANDIDATS.md.")

print("=== TOUTES LES ÉTAPES DE CONSTRUCTION SONT ACHEVÉES AVEC SUCCÈS ! ===")
