# Chess Tournament Helper

Logiciel servant à organiser des tournois d'échecs, avec un système de sauvegarde de données fonctionnant hors-ligne.

## **Installation**

1. Sur le dépôt GitHub, cliquer sur le bouton en vert '<> Code', puis sur Download ZIP.
2. Extraire le fichier ZIP obtenu dans le dossier de votre choix.
3. Ouvrir le dossier dans le terminal de votre choix (assurez-vous d'avoir Python installé).
4. Rentrer dans le terminal : 
- `python -m venv env` pour créer un environnement virtuel.
- `env\Scripts\activate.bat` pour activer l'environnement virtuel.
- `pip install -r requirements.txt` pour installer les librairies nécessaires/

## **Utilisation**

Pour lancer Chess Tournament Helper une fois l'installation terminée:  
1. Ouvrir le terminal de votre choix dans le dossier d'installation.
2. Rentrer `python chess_tournament_helper.py`.

### **Sauvegarde des données** 

Les données sont sauvegardées à l'intérieur du dossier d'installation, dans le dossier 'data'.
Elles peuvent être modifiées manuellement si besoin. Si les fichiers json sont supprimés, ils sont automatiquement recréés lors du démarrage du programme.

### **Exemple d'utilisation**

Dans le menu principal: 
`Rentrer le nombre indiqué pour exécuter la commande correspondante.
Rentrer 'Q' pour fermer le programme.

1: Ajouter un nouveau tournoi à la base de donnée.
2: Ajouter un joueur à la base de donnée.
3: Liste des tournois.
4: Liste des joueurs et joueuses.`  

1. Ajouter un nouveau tournoi, rentrer le nom et le lieu du tournoi.
2. Ajouter huit joueurs à la base de donnée. (Lorsque le nom de famille est demandé, vous pouvez rentrer `rand` pour remplir automatiquement les autres informations avec des données aléatoires.)
3. Afficher la liste des tournois pour afficher les commandes affectant sur les tournois.
4. Rentrer la commande pour ajouter des joueurs à un tournoi puis choisissez le tournoi que vous avez créé.
5. Ajouter au tournoi les huit joueurs précédemment ajoutés à la base de donnée.
6. Rouvrir la liste des tournois pour vérifier que les huit joueurs ont bien été ajoutés.
7. Rentrer la commande pour commencer le tournoi auquel les joueurs ont été assignés.
8. Commencer le premier round, et indiquer qui le résultat de chaque match.
9. Faire ainsi de suite pour les rounds restants. Il est possible d'interrompre le tournoi au début d'un round et de le reprendre plus tard, même après la fermeture du programme.  
10. Une fois le tournoi terminé, dans le menu liste des tournois, afficher les rounds du tournoi terminé pour voir les résultats des rounds et les résultats finaux du tournoi.

## **Génération du rapport flake-8**

1. Ouvrir le terminal de votre choix dans le dossier d'installation.
2. Rentrer `env\Scripts\activate.bat` pour activer l'environnement virtuel.
3. Rentrer `flake8 --format=html --htmldir=flake-report` pour générer le rapport.
4. Rentrer `.\flake-report\index.html` pour afficher le rapport dans votre navigateur par défaut.