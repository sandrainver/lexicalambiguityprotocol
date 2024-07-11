import pandas as pd
import os
import re

# Chemins des fichiers CSV à fusionner
dossier_path = "C:\\Users\\535607\\OneDrive - UMONS\\Données testable et codes\\priming"

df = pd.read_excel(os.path.join(dossier_path, "Expe2_priming_all.xlsx"))

# Convertir la colonne "version_hand" en chaînes de caractères
df['version_hand'] = df['version_hand'].astype(str)

# Créer la colonne 'pair' en concaténant les valeurs des colonnes "version_hand" et "rowNo" avec le séparateur "_"
df['pair'] = df['version_hand'] + '_' + df['rowNo'].astype(str)

# Retirer tous les ".0" de la colonne "pair"
df['pair'] = df['pair'].str.replace('.0', '', regex=False)

# Affichage du DataFrame résultant
print(df)

# Affichage des valeurs de la colonne 'pair'
print("Valeurs de la colonne 'pair':")
for val in df['pair']:
    print(val)

###  2  ### supprimer les lignes et colonnes superflues

## supprimer les lignes de trial d'entrainement
trialexclu= "training"
nouveau_df = df[df["condition"] != trialexclu]

## supprimer les colonnes superflues
colonnes_a_supprimer = ['filename', 'browser', 'version', 'screenWidth', 'screenHeight', 'OS',
                        'OS_lang', 'GMT_timestamp', 'local_timestamp', 'trial_file_version',
                        'link', 'calibration', 'duration_s', 'duration', 'duration_m'
                        , 'type', 'stim1', 'stim2', 'stim3', 'random',
                        'stimFormat', 'keyboard', 'feedback', 'presTime', 'ISI',
                        'condition_trial', 'condition_pair', 'presTime_ms', 'presTime_f',
                        'condition', 'timestamp']
df.drop(colonnes_a_supprimer, axis=1, inplace=True)

## importer le fichier contenant les données psycholinguistiques des paires pour fusionner
df2 = pd.read_excel(os.path.join(dossier_path, "Authors2023_LDT_stimOSF.xlsx"))

## fusionner df et df2 pour que le tableau de réponses des participants inclue les données psycholinguistiques
df3 = pd.merge(df, df2, on='pair') ## attention selon version de l'expérience


###  3  ###  exporter le fichier de données pour analyses statistiques

# Chemin complet pour le fichier de sortie
output_folder_path = "C:\\Users\\535607\\OneDrive - UMONS\\Données testable et codes\\newfile"
output_file_path = os.path.join(output_folder_path, 'Expe2_priming_allclean.xlsx')

# Écrire le DataFrame nettoyé dans un nouveau fichier CSV
df3.to_excel(output_file_path, index=False)

print(f"le nouveau tableau se trouve dans {output_file_path}.")


## trouver les lignes qui n'ont pas fusionné

# Fusionner les DataFrames par la colonne "matricule" en utilisant l'indicateur "_merge"
df3 = pd.merge(df, df2, on='pair', how="outer", indicator=True)

# Filtrer les lignes qui n'ont pas pu être fusionnées
df3 = df3[df3["_merge"] == "left_only"]

# Afficher le DataFrame des lignes non fusionnées
print("DataFrame des lignes non fusionnées:")
print(df3)

# Écrire les données non fusionnées dans un df excel
output_file_path = os.path.join(output_folder_path, 'NON FUSIONNE_Expe2_priming_allclean.xlsx')
df3.to_excel(output_file_path, index=False)

print(f"Exporté les donnees non fusionnees vers {output_file_path} à vérifier car ne doit contenir que les essais de training")