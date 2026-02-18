import os
import json
import math
import shutil
import datetime

# 🟢 Tâche 1 — Lecture du journal de bord
def tache1_journal():
    chemin = "mission_data/journal_bord.txt"
    with open(chemin, "r", encoding="utf-8") as f:
        lignes = f.readlines()
    print(f"Journal de bord : {len(lignes)} entrées")
    alertes = [l for l in lignes if "alerte" in l.lower()]
    print(f"--- Alertes détectées ({len(alertes)}) ---")
    for a in alertes:
        print(a.strip())
    with open("mission_data/alertes.txt", "w", encoding="utf-8") as f:
        f.writelines(alertes)
    print(" Fichier alertes.txt créé.")

# 🟢 Tâche 2 — Exploration du dossier
def tache2_os():
    dossier = "mission_data"
    if not os.path.exists(dossier):
        print(" Dossier introuvable")
        return
    for fichier in os.listdir(dossier):
        chemin = os.path.join(dossier, fichier)
        if os.path.isfile(chemin):
            taille = os.path.getsize(chemin) / 1024
            print(f" {fichier:<20} ({taille:.1f} Ko)")
    for sous in ["rapports", "archives"]:
        chemin = os.path.join(dossier, sous)
        if not os.path.exists(chemin):
            os.makedirs(chemin)
            print(f" {sous}/ [créé]")

# 🟢 Tâche 3 — Missions JSON
def tache3_missions():
    with open("mission_data/missions.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    missions = data["missions"]
    budget_total = sum(m["budget_millions_usd"] for m in missions)
    plus_longue = max(missions, key=lambda m: m["duree_jours"])
    plus_courte = min(missions, key=lambda m: m["duree_jours"])
    for m in missions:
        print(f"[{m['id']}] {m['nom']} → {m['destination']} | {m['duree_jours']} jours | "
              f"Équipage : {len(m['equipage'])} | Budget : {m['budget_millions_usd']:,} M$")
    print(f"Budget total : {budget_total:,} M$")
    print(f"Mission la plus longue : {plus_longue['nom']} ({plus_longue['duree_jours']} jours)")
    print(f"Mission la plus courte : {plus_courte['nom']} ({plus_courte['duree_jours']} jours)")

# 🟡 Tâche 4 — Chargement robuste
def charger_json_securise(chemin):
    try:
        if not os.path.exists(chemin):
            raise FileNotFoundError
        with open(chemin, "r", encoding="utf-8") as f:
            contenu = f.read().strip()
            if not contenu:
                print(f"Fichier vide : {chemin}")
                return None
            return json.loads(contenu)
    except FileNotFoundError:
        print(f"Fichier introuvable : {chemin}")
    except json.JSONDecodeError as e:
        print(f"JSON invalide dans {chemin} : {e}")
    return None

# 🟡 Tâche 5 — Archivage
def tache5_archivage():
    src = os.path.join("mission_data", "journal_bord.txt")
    dest = os.path.join("mission_data", "archives", f"journal_bord_{datetime.date.today()}.txt")
    shutil.copy(src, dest)
    print(f" Copie archivée : {dest}")

# 🟡 Tâche 6 — Ajouter/Supprimer mission
def ajouter_mission(chemin_json, nouvelle_mission):
    with open(chemin_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    for m in data["missions"]:
        if m["id"] == nouvelle_mission["id"]:
            raise ValueError("Mission déjà existante")
    data["missions"].append(nouvelle_mission)
    with open(chemin_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Mission {nouvelle_mission['id']} ajoutée.")

def supprimer_mission(chemin_json, mission_id):
    with open(chemin_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    data["missions"] = [m for m in data["missions"] if m["id"] != mission_id]
    with open(chemin_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f" Mission {mission_id} supprimée.")

# 🟡 Tâche 7 — Analyse télémétrie
def tache7_telemetrie():
    with open("mission_data/telemetrie.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    print("Phase               | Altitude        | Vitesse   | Carburant | Alertes")
    print("--------------------|-----------------|-----------|-----------|--------")
    for r in data["releves"]:
        alertes = [k for k,v in r["systemes"].items() if v != "nominal"]
        alertes_str = ", ".join(alertes) if alertes else "-"
        print(f"{r['phase']:<20} | {r['altitude_km']:,} km | {r['vitesse_km_s']} km/s | "
              f"{r['carburant_pct']}% | {alertes_str}")

# 🔴 Tâche 8 — Fonctions navigation
def distance_interplanetaire(corps1, corps2, donnees_corps):
    d1 = next(c["distance_soleil_mkm"] for c in donnees_corps if c["nom"] == corps1)
    d2 = next(c["distance_soleil_mkm"] for c in donnees_corps if c["nom"] == corps2)
    return abs(d1 - d2)

def temps_trajet(distance_mkm, vitesse_km_s):
    distance_km = distance_mkm * 1e6
    secondes = distance_km / vitesse_km_s
    return secondes / 86400

def poids_sur_corps(masse_kg, gravite_m_s2):
    return masse_kg * gravite_m_s2

# 🔴 Tâche 9 — Exceptions personnalisées
class NavigationError(Exception): pass
class MissionDataError(NavigationError): pass
class TrajectoireError(NavigationError): pass
class CarburantError(NavigationError): pass

# 🔴 Tâche 10 — Menu interactif
def centre_controle():
    while True:
        print("""
CENTRE DE CONTRÔLE DE MISSION 
  1. Afficher toutes les missions                 
  2. Journal de bord                              
  3. Télémétrie                                   
  0. Quitter                                      

""")
        choix = input("Votre choix : ")
        if choix == "0":
            break
        elif choix == "1":
            tache3_missions()
        elif choix == "2":
            tache1_journal()
        elif choix == "3":
            tache7_telemetrie()

if __name__ == "__main__":
    centre_controle()
