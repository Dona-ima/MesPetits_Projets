import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

st.title("Analyse des données du dataset de Tips")

with st.sidebar:
    st.header("À propos de l'auteur")
    st.write("Ce projet a été réalisé par Ariane AGBOTON.")
    st.write("Je suis étudiante en Intelligence Artificielle à l'Institut de Formation pour la Recherche en Informatique (IFRI-UAC) 😊👩🏾‍💻.")
    st.write("Email : arianeagboton70@gmail.com")
    st.write("LinkedIn :  https://www.linkedin.com/in/ariane-agboton-2a7885305")
    st.write("GitHub : https://github.com/Dona-ima")

# Chargement des données
with st.expander('Importation des données'):
    st.header('Importation des données')
    data = sns.load_dataset('tips')
    st.write(data.head())
    st.write(f"Le Dataset est constitué de {data.shape[0]} lignes et de {data.shape[1]} colonnes.")

# Information sur les colonnes
with st.expander('Information sur les colonnes'):
    st.header('Information sur les colonnes.')
    st.write(
        "- total_bill : Le montant total de la facture avant les pourboires.\n",
        "- tip : Le montant du pourboire donné par le client.\n",
        "- sex : Le sexe du client qui a payé la facture.\n",
        "- smoker : Indique si la personne est fumeuse ou non.\n",
        "- day : Le jour de la semaine où le repas a été pris.\n",
        "- time : Le moment de la journée où le repas a été pris.\n",
        "- size : Le nombre de personnes à la table.\n"
    )

# Visualisation des données
with st.expander('Visualisation des données'):
    st.header('Visualisation des données')
    st.write("Dans le dataset, nous avons 7 variables : 4 qualitatives, 2 quantitatives continues, et 1 discrète.")

    # Statistiques descriptives
    st.subheader('Statistiques Descriptives')
    st.write(data.describe(include='all').T)

# Camemberts
with st.expander('Camemberts'):
    st.subheader('Pie Chart')
    var_qualitative = data[['sex', 'smoker', 'day', 'time']]
    fig, axs = plt.subplots(2, 2, figsize=(10, 12))
    i = 0
    for var in var_qualitative:
        row = i // 2
        column = i % 2
        var_qualitative[var].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=axs[row, column])
        axs[row, column].set_title(f'Pie chart de {var}')
        i += 1
    st.pyplot(fig)
    st.markdown("**On note que le lieu est plus fréquenté le weekend principalement pour des dinnés, que les clients sont majoritairement non fumeurs et que les factures sont surtout réglés par des hommes.**")

# Pairplot
with st.expander('Pairplot'):
    st.subheader('Pairplot')
    sns.pairplot(data, hue='day')
    st.pyplot(plt)
    st.markdown("**On note que lorsque l'addition et la taille de la table augmente, le pourboir augmente. et aussi que l'addition augmente lorque la taille de la table augmante. On remarque aussi que les samedis et jeudi, le nombre de table réservées est élevé et ce sont en majorité des table de 2, et que l'addition et les pourboires sont élevés.Donc on peut dire que les samedis et jeudis il y a plus de clients et ce sont principalement des couples(duo) et vu que l'addition est élévé et que le pourboir aussi, il peut s'agir de rencard au cours desquels l'un essai d'impressionner l'autre.**")

# Boxplots
with st.expander('Boxplots'):
    st.subheader('Boîtes à Moustaches')
    fig, axs = plt.subplots(1, 3, figsize=(18, 8))
    var_quantitativeCont = data[['total_bill', 'tip', 'size']]
    for i, col in enumerate(var_quantitativeCont.columns):
        sns.boxplot(data=var_quantitativeCont[col], ax=axs[i])
        axs[i].set_title(f'Boxplot de {col}')
    st.pyplot(fig)
    st.markdown("**On note au niveau du boxplot de l'addition une faible dispersion sur 50% des données et la valeur de l'addition varie d'environs 13 à 24 dollards.Au niveau du boxplot du pourboire on fait également le même constat sur 50% des données et la valeur du pourboire varie de 2 à 3.8$.De même sur le boxplot de la taille de la table on note une faible dispersion sur 50% des données et les types de table les plus prises sont celles de 2 à 3 places.Et sur tous les boxplots on note des valeurs extrêmes ie des valeurs plutôt éloignées des autres et qui sont rares.**")

# Matrice de Corrélation
with st.expander('Matrice de corrélation'):
    st.subheader('Matrice de corrélation')
    corr_matrix = var_quantitativeCont.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='crest', fmt='.2f', center=0)
    st.pyplot(plt)
    

# Pourboires par sexe et statut de fumeur
with st.expander('Individus les plus généreux côté pourboire'):
    st.subheader('Individus les plus généreux côté pourboire')
    plt.figure(figsize=(10, 6))
    data.groupby(['sex', 'smoker'])['tip'].mean().plot(kind='line')
    plt.title('Moyenne des pourboires en fonction du sexe et du moment du repas')
    st.pyplot(plt)
    st.markdown("**On note que ceux qui donnes plus de pourboires sont les hommes non fumeur et le pourboire maximal donné est d'environs 3.13$.**")

# Pourboires en fonction du jour
with st.expander('Individus les plus généreux côté pourboire et les jours'):
    st.subheader('Individus les plus généreux côté pourboire et les jours')
    plt.figure(figsize=(10, 6))
    data.groupby(['sex', 'day'])['tip'].mean().plot(kind='line')
    plt.title('Moyenne des pourboires en fonction du sexe et du jour du repas')
    st.pyplot(plt)
    st.markdown("**On note que les pourboires les plus élevés sont donnés surtout en weekends et par les hommes.**")

# Conclusion
with st.expander('Conclusion'):
    st.header('Conclusion')
    st.markdown("On peut déduire que le lieu est plus fréquenté le weekend pour des dîners, que les tables prises sont principalement de taille 2, et que les hommes non fumeurs sont les plus généreux.")
