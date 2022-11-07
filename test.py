import math 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
import itertools
import time


caracteristiques = pd.read_csv('data/caracteristiques-2019.csv',
                                sep=';', index_col='Num_Acc', 
                                usecols=['Num_Acc','dep', 'lum', 'agg', 'atm','col'], 
                                dtype={'dep' : str})
usagers = pd.read_csv('data/usagers-2019.csv',
                        sep=';', index_col='Num_Acc',
                        usecols=['Num_Acc', 'sexe', 'an_nais', 'grav', 'secu1', 'secu2', 'secu3'])

lieux = pd.read_csv('data/lieux-2019.csv',
                    sep=';', index_col='Num_Acc',
                    usecols=['Num_Acc', 'catr','circ', 'nbv', 'plan', 'surf'])

vehicules = pd.read_csv('data/vehicules-2019.csv',
                        sep=';', index_col='Num_Acc',
                        usecols=['Num_Acc', 'catv' ])

donnes_brut = pd.read_csv('data/donnes.csv', index_col='dep')

# Variable agg (0 : Accident hors agglo, 1 : Accident en Agglo )
caracteristiques['agglo'] = caracteristiques['agg']-1
# Variable nuit (0 : Accident de jour, 1 : Accident de nuit)
caracteristiques['nuit'] = np.where(caracteristiques['lum'] == 1, 0, 1)
# Variable atm_extreme :
#   0 : atmosphère normale lors de l'accident = [normale, pluie légère, temps éblouissant, temps couvert]
#   1 : atmosphère extreme lors de l'accident = [pluie forte, neige/grele, brouillard/fumée, vent fort/tempete]
caracteristiques['atm_extreme'] = np.where((caracteristiques['atm'] < 2) | (caracteristiques['atm'] > 6),0, 1)
# Varriable col_front (0 : collision non frontale, 1: collision frontale)
caracteristiques['col_front'] = np.where(caracteristiques['col'] == 1,1,0)


# Variable auto : (0 : Accident hors autoroute, 1: Accident sur autouroute)
lieux['auto'] = np.where(lieux['catr'] == 1, 1, 0)
# Variable natio (0 : Accident hors nationale, 1: Accident sur nationale)
lieux['natio'] = np.where(lieux['catr'] == 2, 1, 0)
# Variable depart : (0 : Accident hors departementale, 1: Accident sur départementale)
lieux['depart'] = np.where(lieux['catr'] == 3, 1, 0)
# Variable bidirec (0 : Accident sur route non bidirectionnelle, 1 : Accident sur route bidirectionnelle)
lieux['bidirec'] = np.where(lieux['circ'] == 2, 1, 0)
# Variable virage (0 : Accident ayant eu lieu sur un plan rectiligne, 1 : Accident ayant eu lieu sur un plan non rectiligne)
lieux['virage'] = np.where(lieux['plan'] > 1, 1, 0)
# Variable surface_normale (0 : Etat de la surface normale, 1 : Etat de la surface non normale)
lieux ['surface_normale'] = np.where(lieux['surf'] == 1, 1, 0)




# Calcul age
usagers['age'] = 2019 - usagers['an_nais'] 
# 
usagers['femme'] = np.where(usagers['sexe'] == 2, 1, 0)
usagers['homme'] = np.where(usagers['sexe'] == 1, 1, 0)
# 0 : pas mort, 1 : mort
usagers['mort'] = np.where(usagers['grav'] == 2, 1, 0)


df = pd.DataFrame()
# Moyenne d'age par accidents
df['age_moy'] = usagers.age.groupby('Num_Acc').mean()
# Nombre de femmes et homme par accidents
df['femme'] = usagers.femme.groupby('Num_Acc').sum()
df['homme'] = usagers.homme.groupby('Num_Acc').sum()
df['usagers'] = usagers.groupby('Num_Acc').size()
# Nombre de morts par accidents
df['nb_mort'] = usagers.mort.groupby('Num_Acc').sum()


caracteristiques = caracteristiques.join([df, lieux])

data = pd.DataFrame()
# Nombre de morts par départements
data['morts'] = caracteristiques.groupby('dep')['nb_mort'].sum()
# Nombre d'accidents par départements
data['accidents'] = caracteristiques.groupby('dep').size()
# Nombre d'accidents qui ont eu lieu en agglomération
data['agglo'] = caracteristiques.groupby('dep')['agglo'].sum()
# Nombre d'accidents qui ont eu lieu pendant la nuit
data['nuit'] = caracteristiques.groupby('dep')['nuit'].sum()
# Nombre d'accidents ayant eu lieu sous conditions atmosphériques extremes
data['atm_extreme'] = caracteristiques.groupby('dep')['atm_extreme'].sum()
# Nombre d'accidents en collision frontale
data['col_front'] = caracteristiques.groupby('dep')['col_front'].sum()
# Nombre d'accidents impliquant des femmes
data['femme'] = caracteristiques.groupby('dep')['femme'].sum()
# Nombre d'accidents impliquant des hommes
data['homme'] = caracteristiques.groupby('dep')['homme'].sum()
# Nombre d'accidentés
data['usagers'] = caracteristiques.groupby('dep')['usagers'].sum()
# Nombre moyen d'accidentés par accidents
data['usagers_moy'] = caracteristiques.groupby('dep')['usagers'].mean()
# Age moyen des accidentés
data['age_moy'] = caracteristiques.groupby('dep')['age_moy'].mean()
# Nombre d'accidents sur l'autoroute
data['auto'] = caracteristiques.groupby('dep')['auto'].sum()
# Nombre d'accidents sur nationale
data['natio'] = caracteristiques.groupby('dep')['natio'].sum()
# Nombre d'accidents sur départementale
data['depart'] = caracteristiques.groupby('dep')['depart'].sum()
# Nombre d'accidents sur une voie bidirectionelle
data['bidirec'] = caracteristiques.groupby('dep')['bidirec'].sum()
# Nombre d'accidents ayant eu lieu dans des virages
data['virage'] = caracteristiques.groupby('dep')['virage'].sum()
# Nombre de voies moyen par accidents
data['nbv_moy'] = caracteristiques.groupby('dep')['nbv'].mean()
# Nombre d'accidents ayant eu lieu sur une route avec surface normale
data['surface_normale'] = caracteristiques.groupby('dep')['surface_normale'].sum()

data = data.drop(data.index[96:])


lachancla =[]
for i in data.iloc[:, 2:].columns:
    lachancla.append(i)

yatangaki=[]
for i in range(1,len(lachancla)+1):
   yatangaki.append(list(itertools.combinations(lachancla,i)))

issou=[]
for i in range(len(yatangaki)):
    for j in range(len(yatangaki[i])):
        issou.append('+'.join(yatangaki[i][j]))

print(f'{len(issou)} \n issou')

f = open('output.txt', 'w')

found = 0
for i in range(len(issou)):
    reg = smf.ols(formula = 'morts ~' + issou[i] , data=data).fit()
    if reg.rsquared_adj >= 0.75:
        #f.write(f'{issou[i]} R = {reg.rsquared} prob(F-stat) ={reg.f_pvalue} \n')
        f.write(f'{issou[i]} \n{reg.summary()} \n')
        found += 1

    print(f'loading : {round((i/65535) * 100,2)} %          Reg : {i}            Founded : {found}', end="\r")
    time.sleep(0.001)


