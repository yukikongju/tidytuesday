# Bixi - Historique de déplacements et emprunts de tous les utilisateurs de Montreal

Analyse de l'usage et des déplacements des utilisateurs de Bixi de Montréal

Les données utilisées peuvent être trouvées [ici](https://bixi.com/fr/donnees-ouvertes)

## Lignes directrices

1. Quelle capacité devrait avoir chacune des stations BIXI? doit-on ajouter ou 
   enlever des vélos/spots?
    - Lorsqu'un utilisateur se pointe à une station, y-a-t-il un vélo disponible? 
      Inversement, y-a-t-il de la place pour que celui-ci puisse ranger son 
      vélo? Nous allons étudier la capacité de chaque station à travers le 
      temps, puis modéliser le temps entre chaque emprunt avec un processus 
      de Poisson. Idéalement, on voudrait choisir une capacité tel qu'il y 
      ait toujours de la place pour placer un vélo ou pour en emprunter un.
    - On doit aussi considérer la demande grandissante des BIXIs au fil des 
      années. On veut donc faire une projection du nombre d'utilisateur par 
      station pour les prochains 5 ans à l'aide d'une régression linéaire ou 
      d'une OLS au besoin.
2. Quel impact l'utilisation du Bixi a-t-elle sur le traffic à Montréal?
    - comment peut-on mesurer le traffic à Montréal? Nombre de voitures sur 
      les routes, temps d'attente, ...
    - le Bixi a-t-il un impact significatif sur le traffic? et s'il pleut/vente? 
      On tentera de répondre à cette question avec un test d'hypothèse

## Conclusion

## Ressources

- [Bixi Station Information JSON](https://gbfs.velobixi.com/gbfs/en/station_information.json)
- [Bixi Future Trip Predictions](https://github.com/chaoyangzhengnash/BIXI-future-trip-prediction)


