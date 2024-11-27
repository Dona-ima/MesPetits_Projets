import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import table

st.title("Analyse des données du dataset de Tips")

st.header('Importation des des données')
data = sns.load_dataset('tips')
data.head()

# Charger et afficher le fichier image
image = Image.open("/Images/data.png")
st.image(image, caption="Mon Graphique")
st.write(f"Le Dataset est constitué de {data.shape[0]} lignes et de {data.shape[1]} colonnes.")

x=st.header('Information sur les colonnes.')


st.write(
"- total_bill : Le montant total de la facture avant les pourboires. C'est la somme que le client doit payer pour la nourriture et les boissons, sans inclure le pourboire.\n\n",
"- tip : Le montant du pourboire donné par le client. Ce montant est généralement calculé en fonction du total de la facture.\n",
"- sex : Le sexe du client qui a payé la facture. Les valeurs possibles sont 'Male' (homme) et 'Female' (femme).\n\n",
"- smoker : Indique si la personne est fumeuse ou non. Les valeurs possibles sont 'Yes' (oui) et 'No' (non).\n\n",
"- day : Le jour de la semaine où le repas a été pris. Les valeurs possibles sont 'Thur' (jeudi), 'Fri' (vendredi), 'Sat' (samedi), et 'Sun' (dimanche).\n\n",
"- time : Le moment de la journée où le repas a été pris. Les valeurs possibles sont 'Lunch' (déjeuner) et 'Dinner' (dîner).\n\n",
"- size : Le nombre de personnes qui ont pris le repas (taille de la table). Cela peut être un nombre entier comme 1, 2, 3, etc.\n\n")

st.header('Visualisation des données')
st.write("Dans le dataset nous avons donc 7 variables dont **4 qualitatives** (sex, day, smoker, time) et **2 quantitatives continues** (total_bill, tip) et **1 quantitative discrète** (size). Aucune valeur du dataset n'est manquante et il n'y a pas de valeurs dupliquées")
st.subheader('Statistiques Descriptives')
data.describe(include = 'all').T
st.write("\n\n")
st.write("\n\n")

#camembert
st.subheader('Pie Chart')
var_qualitative= data[['sex', 'smoker', 'day' ,'time']]
fig,axs= plt.subplots(2,2, figsize=(10,12))
i=0
for var in var_qualitative:
    row= i // 2
    column= i % 2
    var_qualitative[var].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=axs[row, column])
    axs[row, column].set_title(f'Pie chart de {var}')
    i +=1
image = Image.open("/Images/camembert.png")
st.image(image, caption="Pie Chart")
st.markdown('**On note que le lieu est plus fréquenté le weekend principalement pour des dinnés, que les clients sont majoritairement non fumeurs et que les factures sont surtout réglés par des hommes.**\n\n\n\n\n\n')
st.write("\n\n")
st.write("\n\n")

#pairplot
st.subheader('Pairplot')
sns.pairplot(data, hue='day')
image = Image.open("/Images/pairplot1.png")
st.image(image, caption="Pairplot")
st.write("**On note que lorsque l'addition et la taille de la table augmente, le pourboir augmente. et aussi que l'addition augmente lorque la taille de la table augmante. On remarque aussi que les samedis et jeudi, le nombre de table réservées est élevé et ce sont en majorité des table de 2, et que l'addition et les pourboires sont élevés.Donc on peut dire que les samedis et jeudis il y a plus de clients et ce sont principalement des couples(duo) et vu que l'addition est élévé et que le pourboir aussi, il peut s'agir de rencard au cours desquels l'un essai d'impressionner l'autre.**")
st.write("\n\n")
st.write("\n\n")

#Boxplots
st.subheader('Boîtes à Moustaches')
fig,axs= plt.subplots(1,3, figsize=(18,8))
i=0
var_quantitativeCont= data[['total_bill', 'tip', 'size']]
for i, col in enumerate (var_quantitativeCont.columns): 
    sns.boxplot(data=var_quantitativeCont[col],ax=axs[i])
    axs[i].set_title(f'Boxplot de {col}')
    i +=1
image = Image.open("/Images/boxplots.png")
st.image(image, caption="Boîtes à Moustache")
st.write("\n\n")
st.write("\n\n")

#Matrice de Correlation
st.subheader('Matrixe de correlation')
image = Image.open("/Images/corr_matrix.png")
st.write("\n\n")
st.write("\n\n")

#Individus qui sont les plus généreux côté pourboir
st.subheader('Individus qui sont les plus généreux côté pourboire')
data.groupby(['sex', 'smoker'])['tip'].mean().plot(kind='line')
plt.title('Moyenne des pourboires en fonction du sexe et du moment du repas')
image = Image.open("/Images/moyenne_Pourboire_F(sex&smoker).png")
st.image(image, caption="Moyenne des pourboires en fonction du sexe et du status de l'individu")
st.write("\n\n")
st.write("\n\n")

#
st.subheader('Individus qui sont les plus généreux côté pourboire et les jours')
data.groupby(['sex', 'day'])['tip'].mean().plot(kind='line')
plt.title('Moyenne des pourboires en fonction du sexe et du jour du repas')
image = Image.open("/Images/moyenne_Pourboire_F(sex&day).png")

st.header('Conclusion')
st.markdown("On peut déduire que du fait que le lieu est plus fréquenté le weekend,pour des dînners, que les tables prises sont celles de 2 et que les les clients les plus généreux sont les hommes non fumeurs , alors le lieu a du succès du côté des dînners entre couple et pour maximiser son gain il pourrait proposer des services spéciaux ou faires des réductions pour de tels dînners")
