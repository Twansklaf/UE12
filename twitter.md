## Machine Learning applied to twitter opinion analysis

### Data extraction



### Data processing

#### How to process words in a machine learning model ?

##### Standardized approach : Bag of words :

1st step : build dictionnary

2 step : for each sentence/tweet/group, build a standardized dictionnary vector reprensentation



##### (1100706823890452483,neg,collected by group 8)Heu... sérieux, il y a encore quelqu'un en France qui accorde de la crédibilité à Emmanuel #Macron et ses ministres godillots ???  #Ford #Blanquefort @BrunoLeMaire https://t.co/Jsz8CL61er





### Dans quel ordre procéder pour nettoyer correctement un tweet

Enlever complètemnt les @xxxxx

Retirer les hastags	



Si on construit un dictionnaire à partir du jeu de test, que le dictionnaire est de taille _n_, la dimension du vecteur d'entrée pour entrainer le modèle sera donc de _n_. Une fois le modèle entraîné, on voudra prédire pour un tweet dans quel classe il rentre. Comment créer un vecteur, pour un tweet qu'on voudra fournir au modèle, qui a la même typologie, même si ce tweet ne partage pas forcément le même dictionnaire ? Faut il fournir le dictionnaire en même temps que le modèle ? Que se passe-t-il quand des mots du tweet qu'on veut prédire ne sont pas le dictionnaire fourni ?

