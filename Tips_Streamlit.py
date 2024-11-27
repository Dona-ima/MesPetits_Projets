import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

st.title("Analyse des données du dataset de Tips")

# Charger les données
st.header('Importation des données')
data = sns.load_dataset('tips')
st.write(data.head())



# Afficher la taille du dataset
st.write(f"Le Dataset est constitué de {data.shape[0]} lignes et de {data.shape[1]} colonnes.")

# Description des colonnes
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

# Visualisation
st.header('Visualisation des données')
st.write("Dans le dataset, nous avons 7 variables : 4 qualitatives, 2 quantitatives continues, et 1 discrète.")

# Statistiques descriptives
st.subheader('Statistiques Descriptives')
st.write(data.describe(include='all').T)

# Camemberts
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

# Pairplot
st.subheader('Pairplot')
sns.pairplot(data, hue='day')
st.pyplot(plt)

# Boxplots
st.subheader('Boîtes à Moustaches')
fig, axs = plt.subplots(1, 3, figsize=(18, 8))
var_quantitativeCont = data[['total_bill', 'tip', 'size']]
for i, col in enumerate(var_quantitativeCont.columns):
    sns.boxplot(data=var_quantitativeCont[col], ax=axs[i])
    axs[i].set_title(f'Boxplot de {col}')
st.pyplot(fig)

# Matrice de Corrélation
st.subheader('Matrice de corrélation')
corr_matrix = var_quantitativeCont.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='crest', fmt='.2f', center=0)
st.pyplot(plt)

# Pourboires par sexe et statut de fumeur
st.subheader('Individus les plus généreux côté pourboire')
plt.figure(figsize=(10, 6))
data.groupby(['sex', 'smoker'])['tip'].mean().plot(kind='line')
plt.title('Moyenne des pourboires en fonction du sexe et du moment du repas')
st.pyplot(plt)

# Pourboires en fonction du jour
st.subheader('Individus les plus généreux côté pourboire et les jours')
plt.figure(figsize=(10, 6))
data.groupby(['sex', 'day'])['tip'].mean().plot(kind='line')
plt.title('Moyenne des pourboires en fonction du sexe et du jour du repas')
st.pyplot(plt)

# Conclusion
st.header('Conclusion')
st.markdown("On peut déduire que le lieu est plus fréquenté le weekend pour des dîners, que les tables prises sont principalement de taille 2, et que les hommes non fumeurs sont les plus généreux.")
