### GeoBAN 🐋
Cette application permet de rechercher une adresse dans la BAN, d'obtenir des suggestions d'adresses avec un score de similarité, puis de visualiser les coordonnées géographiques sur une carte.
    
### Comment ça marche ?
1. **Saisir une adresse** : la présence d'un code postal impact grandement la qualité des résultats. Les fautes d'orthographes sont permises tant qu'il y a un code postal.
2. **Sélectionner une adresse** : après avoir saisi une adresse, une liste de suggestions apparaîtra. Choisissez celle qui possède le meilleur score.
3. **Afficher la carte** : une fois l'adresse sélectionnée, une carte interactive s'affichera avec la position géographique de l'adresse. Vous pouvez choisir parmi plusieurs styles de carte.

![screenshot](assets/images/mon_image.png)

### Questions :
- **Que faire si l'adresse n'est pas trouvée ?**  
  Si l'adresse saisie n'est pas trouvée, assurez-vous qu'elle est correctement orthographiée ou essayez d'ajouter plus d'informations (ex. : le code postal).
- **Comment fonctionne la géolocalisation ?**  
  La géolocalisation utilise l'API **Nominatim** de **OpenStreetMap** pour obtenir les coordonnées de l'adresse saisie.
