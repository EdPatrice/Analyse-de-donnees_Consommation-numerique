import streamlit as st
import pandas as pd
from functions import convert

# Set the page title and icon
st.set_page_config(page_title="Pandas", page_icon="🐼", layout="wide")
df = pd.read_csv("Donnees/donnees_con.csv") # lecture du fichier csv

st.title("Analyse des données de consommation numérique")

# Question 1
# ------------------------------------------------------------------------------------------------------------
# Convertion des colonnes d'activités 
for col in ['Temps_Réseau', 'Temps_Streaming', 'Temps_Jeux'] : 
    df[col] = df[col].apply(convert)

# Calculer les statistiques
statistiques = {
    'Activité': ['Réseaux sociaux', 'Streaming', 'Jeux vidéo'],
    'Moyenne (min)': [
        df["Temps_Réseau"].mean(),
        df["Temps_Streaming"].mean(),
        df["Temps_Jeux"].mean()
    ],
    'Médiane (min)': [
        df["Temps_Réseau"].median(),
        df["Temps_Streaming"].median(),
        df["Temps_Jeux"].median()
    ]
}

st.write("\n Statistiques de temps quotidien par activité :")
df_resultat = pd.DataFrame(statistiques)
df_resultat
# ------------------------------------------------------------------------------------------------------------

# Question 2
# ------------------------------------------------------------------------------------------------------------
# Nettoyer et éclater les plateformes
df["Plateforme_Préférée"] = df["Plateforme_Préférée"].astype(str).str.split(";") # Convertir les valeurs en liste
df["Plateforme_Préférée"] = df["Plateforme_Préférée"].apply(
    lambda x: [item.strip() for item in x if item.strip() != "nan"]
) # Supprimer les valeurs "nan" et les espaces

df_ex = df.explode("Plateforme_Préférée").dropna(subset=["Plateforme_Préférée"]) # Éclater les listes en lignes individuelles

# Gérer les tranches d'âge
age_order = ["10 - 17 ans", "18 - 24 ans", "25 - 34 ans", "35 - 44 ans", "45 - 54 ans", "55 - et plus"] # Définir l'ordre des catégories
df_ex["Tranche_dage"] = pd.Categorical(df_ex["Age"], categories=age_order, ordered=True) # Convertir la colonne "Age" en catégorie ordonnée

# 1. Tableau par ÂGE
distribution_age = pd.crosstab(
    index=df_ex["Plateforme_Préférée"],
    columns=df_ex["Tranche_dage"]
)

# 2. Tableau par SEXE
distribution_sexe = pd.crosstab(
    index=df_ex["Plateforme_Préférée"],
    columns=df_ex["Sexe"]
)

st.write("Répartition par Sexe")
st.write(distribution_sexe)

st.write("Répartition par Âge")
st.write(distribution_age)
# ------------------------------------------------------------------------------------------------------------

# Question 3
# ------------------------------------------------------------------------------------------------------------
# Nettoyer et éclater les appareils
df["Appareil"] = df["Appareil"].str.split(";").apply(lambda x: [item.strip() for item in x])
df_ex = df.explode("Appareil")

# Calcul du taux avec df_ex
resultat = (
    df_ex.groupby("Appareil")  # <-- Utiliser df_ex ici
    .size()
    .div(len(df))  # Diviser par le nombre total de répondants (pas de doublons)
    .mul(100)
    .round(2)
    .sort_values(ascending=False)  # Trier par pourcentage décroissant
    .reset_index()
    .rename(columns={"Appareil": "Appareils utilisés", 0: "Pourcentage"})
)

st.write("Taux d'utilisation des appareils :")
st.write(resultat)
# ------------------------------------------------------------------------------------------------------------

# Bonus
# ------------------------------------------------------------------------------------------------------------
# Convertion des colonnes d'activités 
for col in ['Temps_Réseau', 'Temps_Streaming', 'Temps_Jeux'] : 
    df[col] = df[col].apply(convert)
# Calculer les statistiques
statistiques = {
    'Activités': ['Réseaux sociaux', 'Streaming', 'Jeux vidéo'],
    'Minimum': [
        df["Temps_Réseau"].min(),
        df["Temps_Streaming"].min(),
        df["Temps_Jeux"].min()
    ],
    'Maximum': [
        df["Temps_Réseau"].max(),
        df["Temps_Streaming"].max(),
        df["Temps_Jeux"].max()
    ],
    'Ecart-type' : [
        df["Temps_Réseau"].std(),
        df["Temps_Streaming"].std(),
        df["Temps_Jeux"].std()
    ]
}

st.title("Bonus")
st.write("\n Statistiques de temps quotidien par activité :")
df_resultat = pd.DataFrame(statistiques)
st.write(df_resultat)