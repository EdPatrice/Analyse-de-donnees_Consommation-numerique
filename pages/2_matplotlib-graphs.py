import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from functions import temps_moyen

# Set the page title and icon
st.set_page_config(page_title="Matplotlib", page_icon="📊")

st.markdown("<h1 style='text-align: center;'>Rapport de consommation numérique</h1>", unsafe_allow_html=True)

st.markdown("***", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

st.write("#### Données collectées")

df = pd.read_csv("Donnees/donnees_con.csv")

# nettoyage des données
df.rename(columns={"Age ": "Age", "Appareil ": "Appareil", "Temps_Réseau": "Temps_Reseau", "Plateforme_Préférée": "Plateforme_Preferee"}, inplace=True)
df.drop(columns={"Horodateur"}, inplace=True)
df["Age"] = df["Age"].astype("string")
df["Temps_Reseau"] = df["Temps_Reseau"].astype("string")
df["Temps_Streaming"] = df["Temps_Streaming"].astype("string")
df["Temps_Jeux"] = df["Temps_Jeux"].astype("string")
df["Plateforme_Preferee"] = df["Plateforme_Preferee"].astype("string")
df["Appareil"] = df["Appareil"].astype("string")

og_df = df.copy()
og_df["Temps_Reseau"] = og_df["Temps_Reseau"].apply(temps_moyen)
og_df["Temps_Streaming"] = og_df["Temps_Streaming"].apply(temps_moyen)
og_df["Temps_Jeux"] = og_df["Temps_Jeux"].apply(temps_moyen)
og_df["Age"] = og_df['Age'].str.replace(' ans', '')

# Convertir les colonnes ayant plusieurs valeurs en liste
df["Plateforme_Preferee"] = df["Plateforme_Preferee"].str.split(";")
df["Appareil"] = df["Appareil"].str.split(";")

# Explosion de la premiere colonne
df = df.explode("Plateforme_Preferee")

# Explosion de la deuxieme colonne
df = df.explode("Appareil")
# ------------------------------------------------------------------------------------------------------------

st.write(df)

# ------------------------------------------------------------------------------------------------------------

st.markdown("<br><br>", unsafe_allow_html=True)

st.write("#### Histogramme représentatif du temps passé sur les réseaux sociaux")

hist_values = df["Temps_Reseau"].value_counts().sort_index()
st.bar_chart(hist_values, x_label="Temps passé sur les réseaux sociaux", y_label="Nombre d'utilisateurs")

# ------------------------------------------------------------------------------------------------------------

st.markdown("<br><br>", unsafe_allow_html=True)

st.write("#### Diagramme en barre des plateformes les plus utilisées")

utilisation_plateforme =  df.groupby("Plateforme_Preferee", as_index=False)["Sexe"].count()
utilisation_plateforme.rename(columns={"Sexe": "Nombre"}, inplace=True)
top_plateforme = utilisation_plateforme.sort_values("Nombre", ascending=False).head(10)

# Afficher la 'bar chart' en ordre decroissant de telle sorte que les plateforme les plus utilisees apparaissent en premier
st.write(alt.Chart(top_plateforme).mark_bar().encode(
    x = alt.X('Plateforme_Preferee', sort=None),
    y = 'Nombre'
))


# ------------------------------------------------------------------------------------------------------------

st.markdown("<br><br>", unsafe_allow_html=True)

st.write("#### Répartition des types d'appareils utilisés")

appareils_utilises = df.groupby("Appareil", as_index=False)["Sexe"].count()
appareils_utilises.rename(columns={"Sexe": "Nombre"}, inplace=True)
sections = appareils_utilises['Nombre']
names = appareils_utilises["Appareil"]
explode = [0.05 if i == 3 else 0 for i in range(len(sections))]  # faire que explode soit dynamique

fig, ax = plt.subplots()
ax.pie(sections, labels=names, autopct="%1.1f%%", explode=explode)
ax.set_title("Appareils utilisés")

st.pyplot(fig)

# ------------------------------------------------------------------------------------------------------------

# Bonus


st.markdown("<br><br>", unsafe_allow_html=True)

st.title("Bonus")
st.markdown("***", unsafe_allow_html=True)
# st.markdown("<br><br>", unsafe_allow_html=True)
st.write("### Plateformes les plus utilisées par sexe")

# Hommes
# print("Nombre d'hommes: ", df[df['Sexe'] == 'Masculin']['Sexe'].count())
plateformes_homme = df[df["Sexe"] == 'Masculin'].groupby('Plateforme_Preferee', as_index=False)['Sexe'].count()
plateformes_homme.rename(columns={"Sexe": "Nombre"}, inplace=True)
plateformes_homme.sort_values("Nombre", ascending=False, inplace=True)
sections = plateformes_homme['Nombre']
names = plateformes_homme['Plateforme_Preferee']

# layout pour les colonnes
col1, col2 = st.columns(2)

# colonne 1
with col1:
    fig1, ax = plt.subplots()
    explode = [0.05 if i == 0 else 0 for i in range(len(sections))]  # faire que explode soit dynamique
    ax.pie(sections, labels=names, autopct="%1.1f%%", explode=explode)
    ax.set_title("Plateformes utilisées par les hommes")
    st.pyplot(fig1)

# Femmes
# print("Nombre de femmes: ", df[df['Sexe'] == 'Feminin']['Sexe'].count())
plateformes_femme = df[df["Sexe"] == 'Feminin'].groupby('Plateforme_Preferee', as_index=False)['Sexe'].count()
plateformes_femme.rename(columns={'Sexe': "Nombre"}, inplace=True)
plateformes_femme.sort_values("Nombre", ascending=False, inplace=True)
sections = plateformes_femme["Nombre"]
names = plateformes_femme["Plateforme_Preferee"]
# colonne 2
with col2: 
    fig2, ax = plt.subplots()
    explode = [0.05 if i == 0 else 0 for i in range(len(sections))]  # faire que explode soit dynamique
    ax.pie(sections, labels=names, autopct="%1.1f%%", explode=explode)
    ax.set_title("Plateformes utilisées par les Femmes")
    st.pyplot(fig2)

# ------------------------------------------------------------------------------------------------------------

# Calculer la moyenne de temps passé sur les réseaux sociaux par tranche d'âge
temps_par_age = og_df.groupby('Age')['Temps_Reseau'].mean().sort_values(ascending=False)

# Créer une figure et des axes avec fig, ax
fig, ax = plt.subplots(figsize=(12, 6))

# Créer un graphique à barres
temps_par_age.plot(kind='bar', ax=ax)
ax.set_title('Temps moyen passé sur les réseaux sociaux par tranche d\'âge')
ax.set_xlabel('Tranche d\'âge')
ax.set_ylabel('Temps moyen (heures)')
ax.tick_params(axis='x', rotation=45)  # Rotation des étiquettes de l'axe x
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Ajouter les valeurs au-dessus des barres
for i, v in enumerate(temps_par_age):
    ax.text(i, v, f'{v:.1f}h', ha='center', va='bottom')

# Ajuster la mise en page
fig.tight_layout()

# Afficher le graphique
# plt.show()
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("### Temps passé sur les réseaux sociaux par tranche d'âge")
st.pyplot(fig)

# Afficher les statistiques détaillées
st.markdown("#### Statistiques par tranche d'âge :")
st.write(og_df.groupby('Age')['Temps_Reseau'].agg(['mean', 'count', 'std']).round(2))

#-------------------------------------------------------------------------------------------------------------
# Conclusion
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("# Conclusion")
st.markdown("***", unsafe_allow_html=True)
st.markdown("Les données recueillies montrent que la plupart des participants à cette étude passent environ **3 à 4 heures** sur les réseaux sociaux. " \
'<br>**Les hommes** utilisent majoritairement **WhatsApp** pour communiquer avec leurs proches et se divertir `24%`. '\
'<br>Tandis que, chez **les femmes**, la plateforme préférée est **TikTok** `38%`. '\
'<br>Ils accèdent à ces plateforme en grande partie depuis leurs **Smartphones** `53%` ou leurs **ordinateurs** `25%`.'\
'<br>Les jeunes adultes (18-24 ans) passent plus de temps sur les réseaux sociaux que les autres tranches d\'âge.', unsafe_allow_html=True)

