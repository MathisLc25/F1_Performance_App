# Pitwall F1 - Ingénierie de Piste & Télémétrie Assistée par IA

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-F7931E.svg)](https://scikit-learn.org/)

**Pitwall F1** est une application web d'ingénierie de piste et de coaching automatisé développée dans le cadre de notre module de *Mise en Situation Professionnelle (MSP)* à l'ECE Bordeaux (Sujet n°4 : Sport). 

L'outil permet de transformer les flux de données télémétriques brutes de la FIA en cartographies décisionnelles claires et interactives grâce à un algorithme de Machine Learning non-supervisé.


##  Problématique Académique

> *Comment l'application d'un algorithme de Machine Learning non-supervisé peut-elle permettre d'identifier automatiquement les forces et faiblesses du style de pilotage d'un athlète sans intervention humaine préalable ?*


##  Notre Équipe (Groupe 2 - B2 Data & IA)

*   **Mathis LADINE-CALOC** (Chef de projet & Lead Developer) : Architecture globale, intégration de l'API de données, mise en cache et modélisation mathématique du clustering.
*   **Oscar LE CALONNEC** (UI/UX & Data Visualization) : Design de l'interface en Dark Mode, intégration du code CSS personnalisé et création des graphiques interactifs Plotly.
*   **Salah Eddine EL MANSOURY** (Data Mining & QA) : Nettoyage des bases de données brutes, ingénierie des variables (calcul d'accélération différentielle) et gestion de la portabilité.

---

##  Variante IA : Le Clustering K-Means

Plutôt que d'utiliser des conditions logiques statiques (`If/Else`), **Pitwall F1** embarque un modèle d'apprentissage non-supervisé **K-Means** (`Scikit-Learn`). 

L'algorithme analyse dynamiquement deux variables physiques (*features*) : la **vitesse instantanée** et l'**accélération longitudinale dérivée**. Sans connaissance préalable de la géométrie du circuit, il segmente le comportement de la monoplace en **3 clusters distincts** traduits sportivement :
1.  🔴 **Phase de Freinage Intense :** Vitesse en chute rapide, accélération fortement négative.
2.  🟡 **Phase de Transition / Virage :** Vitesse minimale stabilisée au point de corde (Apex).
3.  🟢 **Phase de Pleine Charge :** Vitesse élevée et ré-accélération (lignes droites et courbes rapides).

Ces clusters sont projetés en temps réel sur les coordonnées spatiales GPS (X, Y) du tracé pour offrir une mine d'or visuelle à l'ingénieur de piste.

---

## Architecture & Pipeline de Données

L'application est découpée en 3 couches logicielles strictes :
1.  **Acquisition (Ingestion) :** Requêtes synchrones vers l'API officielle via la bibliothèque `FastF1`. Optimisation majeure grâce au décorateur `@st.cache_data` de Streamlit permettant de stocker localement les sessions et de réduire le temps de chargement à **moins de 200ms**.
2.  **Traitement (Data Engineering & ML) :** Structuration matricielle sous `Pandas` / `NumPy`, calcul des deltas et exécution du modèle de clustering `KMeans`.
3.  **Restitution (UI) :** Rendu asynchrone et interactif sur navigateur via `Streamlit` et graphiques `Plotly`.

---

## Installation et Lancement Local

Suivez ces étapes pour exécuter le projet sur votre machine en moins de deux minutes :

### 1. Cloner le dépôt et se placer dans le dossier
```bash
git clone [https://github.com/MathisLc25/F1_Performance_App.git](https://github.com/MathisLc25/F1_Performance_App.git)
cd F1_Performance_App
