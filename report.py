import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt

st.write("# Rapport d'utilisation numérique")
st.write("## Données collectées")

df = pd.read_csv("Donnees/donnees_con.csv")

# nettoyage des données
df.rename(columns={"Age ": "Age", "Appareil ": "Appareil", "Temps_Réseau": "Temps_Reseau", "Plateforme_Préférée": "Plateforme_Preferee"}, inplace=True)
df.drop(columns={"Horodateur"}, inplace=True)
# ------------------------------------------------------------------------------------------------------------

st.write(df)

# ------------------------------------------------------------------------------------------------------------

st.write("## Histogramme représentatif du temps passé sur les réseaux sociaux")

# fig, ax = plt.subplots() 
# ax.hist(df["Temps_Reseau"], color="#500120", edgecolor='white') 
# ax.set_xlabel("Nombre d'heures par jour")  
# ax.set_title("Temps passé sur les réseaux sociaux")
# st.pyplot(fig)

hist_values = df["Temps_Reseau"].value_counts().sort_index()
st.bar_chart(hist_values, x_label="Temps passé sur les réseaux sociaux", y_label="Nombre d'utilisateurs")

# ------------------------------------------------------------------------------------------------------------

st.write("## Diagramme en barre des plateformes les plus utilisées")

utilisation_plateforme =  df.groupby("Plateforme_Preferee", as_index=False)["Sexe"].count()
utilisation_plateforme.rename(columns={"Sexe": "Nombre"}, inplace=True)
top_plateforme = utilisation_plateforme.sort_values("Nombre", ascending=False).head(10)

st.bar_chart(top_plateforme, x="Plateforme_Preferee", y="Nombre", x_label="Plateforme préférée", y_label="Nombre d'utilisateurs")   


# ------------------------------------------------------------------------------------------------------------
st.write("## Répartition des types d'appareils utilisés")

appareils_utilises = df.groupby("Appareil", as_index=False)["Sexe"].count()
appareils_utilises.rename(columns={"Sexe": "Nombre"}, inplace=True)
sections = appareils_utilises['Nombre']
names = appareils_utilises["Appareil"]

fig, ax = plt.subplots()
ax.pie(sections, labels=names, autopct="%1.1f%%", explode=(0, 0.05))
ax.set_title("Appareils utilisés")

st.pyplot(fig)

# ------------------------------------------------------------------------------------------------------------
st.write("## Bonus")
st.write("### Plateformes les plus utilisées par sexe")

# Hommes
print("Nombre d'hommes: ", df[df['Sexe'] == 'Masculin']['Sexe'].count())
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
    ax.pie(sections, labels=names, autopct="%1.1f%%", explode=(0.05, 0, 0))
    ax.set_title("Plateformes utilisées par les hommes")
    st.pyplot(fig1)

# Femmes
print("Nombre de femmes: ", df[df['Sexe'] == 'Feminin']['Sexe'].count())
plateformes_femme = df[df["Sexe"] == 'Feminin'].groupby('Plateforme_Preferee', as_index=False)['Sexe'].count()
plateformes_femme.rename(columns={'Sexe': "Nombre"}, inplace=True)
plateformes_femme.sort_values("Nombre", ascending=False, inplace=True)
sections = plateformes_femme["Nombre"]
names = plateformes_femme["Plateforme_Preferee"]
# colonne 2
with col2: 
    fig2, ax = plt.subplots()
    ax.pie(sections, labels=names, autopct="%1.1f%%", explode=(0.05, 0, 0, 0))
    ax.set_title("Plateformes utilisées par les Femmes")
    st.pyplot(fig2)

# ------------------------------------------------------------------------------------------------------------


