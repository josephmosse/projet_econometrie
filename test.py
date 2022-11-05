import pandas as pd
import numpy as np
import streamlit as st

caracteristiques = pd.read_csv('data/carcteristiques-2021.csv', sep=';', index_col='Num_Acc')
usagers = pd.read_csv('data/usagers-2021.csv', sep=';', index_col='Num_Acc')
lieux = pd.read_csv('data/lieux-2021.csv', sep=';')
vehicules = pd.read_csv('data/vehicules-2021.csv', sep=';')

# Calcul de l'age des victimes de l'accident
usagers['age_moy'] = 2021 - usagers['an_nais']

# Calcul de la moyenne d'age par accidents
usagers = usagers.groupby('Num_Acc').mean()

# Transformation de agg en bool (0 : hors agglo 1 : en agglo)
caracteristiques['agg'] = caracteristiques['agg'] - 1

data = caracteristiques.join([usagers['age_moy'], lieux])
data.index = data.index - 202100000000

# Suppression des DOM

data = data[data['dep'].between('01', '95')]
display(data)


data = data.merge(df, on='dep')


data = data.drop(['Libellé'], axis=1)

#data['salaire_moy_dep'] = data['salaire_moy_dep']*35*4

display(data)

st.dataframe(caracteristiques.join(usagers))