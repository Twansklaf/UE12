# UE12
## Projet UE12 Extraction de l'information

lien du git :
https://github.com/Twansklaf/UE12

#### Requirements

__Dependencies__
* python 3.6.7
* tkinter (for note.py only)
* TwitterSearch
* keras
* pandas

#### Tools

* Jupyter

#### How to make a python kernel 3.6.7 for Jupyter

```bash
apt-get install python3.6
(python3.6 -m pip install venv)
python3.6 -m venv mypython36jupyter
cd mypython36jupyter
source bin/activate
pip install ipykernel
python -m ipykernel install --user

``` 

```python
pip install python-twitter
``` 

### Extraction 
skeleton.py utilise l'api twitter pour récupérer des tweets sur le sujet qui nous intéresse, en Français

parse.py contient des fonctions utiles pour manipuler les tweets extraites, et les formatter sur le format défini en cours.

word_toosl.py contient des fonctions qui sont utiles pour la préparation des données pour les modèles de ML

### Récupération de données

Pour récupérer les données, on lance 
```bash
python skeleton.py > output.txt
python parse.py --parse data.txt
```
### Entrainement des modèles
Divers modèle sont écrits dans les jupyter notebook. 
Deux sont basés sur LTSM, les autres sont des modèles "custom". Parmi ces custom, deux sont basés sur
une couche Embeddings, l'autre est constitué de simple couches. 

#################### RESTE #######################

Consumer API keys
P6OXKneDo1VgIsLaf7Hfz71pb (API key)

ggdOmpO0m6IMBDLal6CKijWWAc1nR6XoM9eA2jC1LcJ9yEaiRD (API secret key)

Access token & access token secret
4096983503-9GUudKy0I0E4mNENQDAvNwHvKvL2pujSERjYZcU (Access token)

dxxIXULVExrOy74EJ2UOZI8tmXytyo089h4TyliJ8AxQj (Access token secret)

Skeleton.py retrieves tweet and writes them to twitterdatax.txt

parse.py parse these tweets and write them to formatted data

note display tweets and stores their note.