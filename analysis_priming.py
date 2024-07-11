### ce script reprend le fichier résultant du script clean_priming_file.py
#C:\\Users\\535607\\PycharmProjects\\test1\\newfile\\Expe2_priming_TCD.csv

## ce script transforme le fichier en :
# supprimant les colonnes inutiles
# fusionne avec le fichier table1 pour avoir les groupes
# ne garde que les conditions d'intérêt
# exlue les réponses incorrectes
# exclue les outliers temps sur base de la méthode MAD (écart de 3 MAD)
#


import pandas as pd
import os
import numpy as np

# Chemins des fichiers CSV à fusionner
dossier_path = "C:\\Users\\535607\\OneDrive - UMONS\\Données testable et codes\\newfile"

df = pd.read_excel(os.path.join(dossier_path, "Expe2_priming_allclean.xlsx"))

#########################################################################################################################

## supprimer les colonnes superflues
colonnes_a_supprimer = ['age', 'gender', 'handedness',
      'key', 'response',
       'version_hand',  'VERSION', 'construction' ]
df.drop(colonnes_a_supprimer, axis=1, inplace=True)
df = df.rename(columns={"nombre du participant": "participant"})

### in column "pair" retrieval of lines  1_40 / 2_36 / 3_23 / 3_33 / 3_36 / 4_36 /4_40 / 4_46 to ensure PL and LSA balance of the analysis

# Define the values to be removed
values_to_remove = ['1_40', '2_36', '3_23', '3_33', '3_36', '4_36', '4_40', '4_46']

# Filter out rows where 'pair' column matches the values to remove
df = df[~df['pair'].isin(values_to_remove)]

print(df)

print(df.columns)
## ##### importer les données '"groupes" pour les fusionner avec le df

# Chemin vers le fichier Excel
chemin_fichier = "C:\\Users\\535607\\OneDrive - UMONS\\A. Etudes\\DAS 2021 Recherche dépression Alzheimer sémantique\\Expérience 2_2022_2023\\DAS_EXPE2_table1_ALLgroups - après juin 2024.xlsx"

# Nom de la feuille
nom_feuille = 'tab.1'

# Importer la feuille en tant que DataFrame
df2 = pd.read_excel(chemin_fichier, sheet_name=nom_feuille,decimal=',')

# Liste des noms de colonnes que vous voulez conserver
colonnes_a_garder = ['participant', 'GROUP', 'age']  # Remplacez par les noms de vos colonnes

# Sélectionner les colonnes à garder
df2 = df2[colonnes_a_garder]

# Fusionner les DataFrames par la colonne "participant"
merged_df = df.merge(df2, on='participant', how='inner')

print(merged_df.columns)


# Fusionner les DataFrames par la colonne "matricule" en utilisant l'indicateur "_merge"

df_fusionne = pd.merge(df, df2, on="participant", how="outer", indicator=True)
# Filtrer les lignes qui n'ont pas pu être fusionnées
df_non_fusionne = df_fusionne[df_fusionne["_merge"] == "left_only"]

# Afficher le DataFrame des lignes non fusionnées
print("DataFrame des lignes non fusionnées:")
print(df_non_fusionne)

# Chemin complet pour le fichier de sortie : fichier de récupération des données non fusionnées pour contrôle
output_folder_path = "C:\\Users\\535607\\OneDrive - UMONS\\Données testable et codes\\newfile"
output_file_path = os.path.join(output_folder_path, 'Expe2_priming_DONNEES NON FUSIONNEES.xlsx')

# Écrire le DataFrame nettoyé dans un nouveau fichier CSV
df_non_fusionne.to_excel(output_file_path, index=True)

# Chemin complet pour le fichier de sortie
output_folder_path = "C:\\Users\\535607\\OneDrive - UMONS\\Données testable et codes\\newfile"
output_file_path = os.path.join(output_folder_path, 'Expe2_priming_analyses.xlsx')

# Écrire le DataFrame nettoyé dans un nouveau fichier CSV
merged_df.to_excel(output_file_path, index=True)

print("Le fichier Expe2_priming_analyses contenant l'ensemble des données a été exporté dans C:\\Users\\535607\\OneDrive - UMONS\\Données testable et codes\\newfile")


#########################################################################################################################

# Filtrer les lignes selon la condition
filtered_df = merged_df[merged_df['condition'].isin(['HD', 'HS','AS', 'NR'])]

print("Le df filtered_df représente les données bruts, uniquement pour les conditions d'intêréts HD, HS, AS, NR")

#########################################################################################################################

#### créer le tableau excluant les mauvaises réponses et les outliers de temps pour les analyses sur les temps de réponse

# Chemin complet pour le fichier de sortie
output_folder_path = "C:\\Users\\535607\\OneDrive - UMONS\\Données testable et codes\\newfile"
output_file_path = os.path.join(output_folder_path, 'Expe2_priming_analyses_MADok.xlsx')

# Nombre total de lignes dans filtered_df
lignes_totales_filtrees = len(filtered_df)

# Éliminer les lignes où "correct" est égal à 0
df = filtered_df[filtered_df['correct'] != 0]

# Calculer le pourcentage de perte après cette étape
pourcentage_perte_correct_zero = ((lignes_totales_filtrees - len(df)) / lignes_totales_filtrees) * 100
print(f"Pourcentage de perte après élimination des réponses incorrectes : {pourcentage_perte_correct_zero:.2f}%")

# Nombre total de lignes dans df après première étape de filtrage
lignes_totales = len(df)

# Filtrer les lignes où la valeur de la colonne "RT" est aberrante : inférieure à 100 ou supérieure à 10000
df = df[(df['RT'] >= 100) & (df['RT'] <= 10000)]

# Calculer le pourcentage de perte après cette étape
pourcentage_perte_aberrantes = ((lignes_totales - len(df)) / lignes_totales) * 100
print(f"Pourcentage de perte après élimination des valeurs aberrantes de RT : {pourcentage_perte_aberrantes:.2f}%")


# Paramètres pour la méthode MAD
k = 1.4826  # Facteur pour déterminer la plage d'outliers

# Calculer la médiane et le MAD pour chaque groupe "participant"
grouped = df.groupby("participant")["RT"]
medians = grouped.transform("median")
mad = grouped.transform(lambda x: k * np.median(np.abs(x - np.median(x))))

# Identifier les valeurs outliers en dehors de la plage [median - k * MAD, median + k * MAD]
outliers_mask = (df["RT"] < medians - 3 * mad) | (df["RT"] > medians + 3 * mad)

# Éliminer les lignes correspondantes
df_filtered2 = df[~outliers_mask]

# Nombre de lignes éliminées par rapport à l'ensemble des réponses correctes
nombre_lignes_eliminees = len(df) - len(df_filtered2)
nombre_total_lignes_correctes = len(filtered_df[filtered_df['correct'] != 0])

# Calculer le pourcentage de lignes éliminées
pourcentage_eliminees = (nombre_lignes_eliminees / nombre_total_lignes_correctes) * 100

print(f"Pourcentage de lignes éliminées : {pourcentage_eliminees:.2f}%")

# Écrire le DataFrame nettoyé dans un nouveau fichier Excel
df_filtered2.to_excel(output_file_path, index=False)

print(f"Le nouveau tableau contenant les données nettoyées est enregistré dans : {output_file_path}")
###  3  ### montrer un tableau croisé des données principales de ce fichier "clea"
# Créer un tableau croisé dynamique
# Définition des fonctions d'agrégation souhaitées
aggregation_functions = {
    'RT': ['mean', 'std']
}

# Création du tableau pivot avec moyenne et écart type
pivot_table = pd.pivot_table(df_filtered2,
                             values='RT',
                             index=['participant','GROUP'],
                             columns='condition',
                             aggfunc=aggregation_functions)

# Renommer les colonnes pour refléter les fonctions d'agrégation
pivot_table.columns = [f'{col}_{agg}' for col, agg in pivot_table.columns]

# Créer colonne SPE
print(pivot_table.columns)

pivot_table['SPE_HD'] = ((pivot_table['mean_NR']-pivot_table['mean_HD'])/pivot_table['mean_NR']*100)
pivot_table['SPE_HS'] = ((pivot_table['mean_NR']-pivot_table['mean_HS'])/pivot_table['mean_NR']*100)
pivot_table['SPE_AS'] = ((pivot_table['mean_NR']-pivot_table['mean_AS'])/pivot_table['mean_NR']*100)

# Chemin complet pour le fichier de sortie
output_folder_path = "C:\\Users\\535607\\OneDrive - UMONS\\Données testable et codes\\newfile"
output_file_path = os.path.join(output_folder_path, 'Expe2_priming_TCD.xlsx')

# Écrire le DataFrame nettoyé dans un nouveau fichier CSV
pivot_table.to_excel(output_file_path, index=True)

print(f"le nouveau TCD basé sur les données de priming, uniquement réponses correctes, sur conditions d'intérêt et après retrait des outliers MAD se trouve dans {output_file_path}.")

