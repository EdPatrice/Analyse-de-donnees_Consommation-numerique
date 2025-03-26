import csv
import random

# Listes de prénoms et noms fictifs
prenoms = ["Alice", "Maxime", "Chloé", "Nicolas", "Sophie", "Julien", "Emma", "Alexandre", "Léa", "Thomas"]
noms = ["Durand", "Lefebvre", "Morel", "Garnier", "Bernard", "Dubois", "Noël", "Giraud", "Blanc", "Fontaine"]

# Listes des plateformes
reseaux_sociaux = ["Facebook", "Instagram", "Twitter", "Snapchat", "TikTok", "Reddit", "Discord", "Telegram", "LinkedIn", "WhatsApp"]
streaming = ["Netflix", "YouTube", "Amazon Prime Video", "Disney+", "HBO Max", "Hulu", "Apple TV+", "Twitch", "Canal+", "Spotify"]
jeux_videos = ["Steam", "PlayStation", "Xbox", "Nintendo Switch", "Epic Games", "Mobile Games", "VR Games"]
appareils = ["Smartphone", "Tablette", "Ordinateur", "Console", "Smart TV"]

# Fonction pour générer des données aléatoires
def generer_donnees(n):
    donnees = []
    for _ in range(n):
        nom = random.choice(noms)
        prenom = random.choice(prenoms)
        age = random.randint(18, 55)
        sexe = random.choice(["H", "F"])
        temps_reseaux = round(random.uniform(0.5, 5), 1)
        temps_streaming = round(random.uniform(0.5, 5), 1)
        temps_jeux = round(random.uniform(0, 4), 1)
        plateforme_preferee = random.choice(reseaux_sociaux + streaming + jeux_videos)
        appareil = random.choice(appareils)
        
        donnees.append([nom, prenom, age, sexe, temps_reseaux, temps_streaming, temps_jeux, plateforme_preferee, appareil])
    
    return donnees

# Fonction pour écrire dans un fichier CSV
def ecrire_csv(n, fichier="Donnees/donnees_consommation.csv"):
    donnees = generer_donnees(n)
    with open(fichier, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Nom", "Prenom", "Age", "Sexe", "Temps_Réseaux", "Temps_Streaming", "Temps_Jeux", "Plateforme_Préférée", "Appareil"])
        writer.writerows(donnees)
    print(f"Fichier {fichier} généré avec {n} entrées.")

# # Exécution
# if __name__ == "__main__":
#     n = int(input("Combien de lignes de données souhaitez-vous générer ? "))
#     ecrire_csv(n)

ecrire_csv(100)