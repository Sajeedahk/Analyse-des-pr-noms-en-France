# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 09:22:24 2025

@author: sajee_4y670z6
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# nettoyage des données

def charger_donnees(fichier_path):
    df = pd.read_csv(fichier_path, sep=",")
    df.dropna(inplace=True)
    return df


# Compter les prénoms 

def compter_prenoms(df, sexe=None):
    compteur = {}
    for index, row in df.iterrows():
        prenom = row["ENFANT_PRENOM"]
        genre = row["ENFANT_SEXE"]
        if sexe is None or genre == sexe:
            compteur[prenom] = compteur.get(prenom, 0) + 1
    return compteur


#  Afficher un graphique en baton 
def afficher_top_prenoms(compteur, titre, couleur="pink"):
    top = sorted(compteur.items(), key=lambda x: x[1], reverse=True)[:20]
    prenoms = [x[0] for x in top]
    valeurs = [x[1] for x in top]

    plt.figure(figsize=(12, 6))
    plt.bar(prenoms, valeurs, color=couleur)
    plt.title(titre)
    plt.xlabel("Prénoms")
    plt.ylabel("Occurrences")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Évolution d’un prénom sur les années
def evolution_prenom_par_annee(df, prenom_cible):
    evolution = {}
    for index, row in df.iterrows():
        annee = row["ANNEE"]
        prenom = row["ENFANT_PRENOM"]
        if annee not in evolution:
            evolution[annee] = 0
        if prenom == prenom_cible:
            evolution[annee] += 1

    annees = sorted(evolution.keys())
    occurrences = [evolution[annee] for annee in annees]

    plt.figure(figsize=(12, 6))
    plt.plot(annees, occurrences, marker='o', label=prenom_cible)
    plt.title(f"Évolution du prénom {prenom_cible} au fil des années")
    plt.xlabel("Année")
    plt.ylabel("Occurrences")
    plt.grid(True)
    plt.tight_layout()
    plt.show()



def evolution_prenom_avec_tendance(df, prenom_cible):
    import numpy as np
    evolution = {}

    for index, row in df.iterrows():
        annee = row["ANNEE"]
        prenom = row["ENFANT_PRENOM"]
        if annee not in evolution:
            evolution[annee] = 0
        if prenom == prenom_cible:
            evolution[annee] += 1

    annees = sorted(evolution.keys())
    occurrences = [evolution[annee] for annee in annees]

    # Courbe
    plt.figure(figsize=(12, 6))
    plt.plot(annees, occurrences, marker='o', label=prenom_cible, color='green')

    # Ajout de la tendance linéaire
    annees_np = np.array(annees, dtype=int)
    occur_np = np.array(occurrences)
    coeffs = np.polyfit(annees_np, occur_np, 1)
    tendance = np.poly1d(coeffs)
    plt.plot(annees_np, tendance(annees_np), color='orange', linestyle='--', label='Tendance')

    plt.title(f"Évolution du prénom {prenom_cible} avec tendance")
    plt.xlabel("Année")
    plt.ylabel("Occurrences")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def statistiques_top_prenoms(compteur, top_n=20):
    import numpy as np
    top = sorted(compteur.items(), key=lambda x: x[1], reverse=True)[:top_n]
    valeurs = np.array([x[1] for x in top])
    
    moyenne = np.mean(valeurs)
    mediane = np.median(valeurs)
    ecart_type = np.std(valeurs)

    print(f"📊 Statistiques du Top {top_n} :")
    print(f"→ Moyenne : {moyenne:.2f}")
    print(f"→ Médiane : {mediane}")
    print(f"→ Écart-type : {ecart_type:.2f}\n")



# exécution des analyses
def main():
    # Charger le fichier
    df = charger_donnees("prenom.csv")

    # Top 20 tous genres confondus
    compteur = compter_prenoms(df)
    afficher_top_prenoms(compteur, "Top 20 des prénoms les plus fréquents", "purple")

    # Top 20 masculins
    compteur_m = compter_prenoms(df, sexe="M")
    afficher_top_prenoms(compteur_m, "Top 20 des prénoms masculins", "blue")

    # Top 20 féminins
    compteur_f = compter_prenoms(df, sexe="F")
    afficher_top_prenoms(compteur_f, "Top 20 des prénoms féminins", "hotpink")

    # Évolution dans le temps pour les deux prénoms les plus populaires
    evolution_prenom_par_annee(df, "Marie")
    evolution_prenom_par_annee(df, "Pierre")

    # Statistiques sur les prénoms
    statistiques_top_prenoms(compteur)
    statistiques_top_prenoms(compteur_m, top_n=10)
    statistiques_top_prenoms(compteur_f, top_n=10)

    # Évolution avec tendance
    evolution_prenom_avec_tendance(df, "Marie")
    evolution_prenom_avec_tendance(df, "Pierre")


if __name__ == "__main__":
    main()