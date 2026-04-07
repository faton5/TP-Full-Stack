# Documentation de l'API

Le serveur tourne sur : `http://localhost:5000`

---

## 1. Récupérer toutes les suggestions

**GET** `/api/suggestions`

Dans le navigateur, ouvre simplement :
```
http://localhost:5000/api/suggestions
```

Réponse (exemple) :
```json
[
  { "id": 1, "titre": "Cinéma UGC", "categorie": "culture", "budget": "moyen", "description": "Soirée cinéma au tarif étudiant.", "note": 4 },
  { "id": 2, "titre": "Parc de la Villette", "categorie": "nature", "budget": "faible", "description": "Balade et pique-nique.", "note": 5 }
]
```

---

## 2. Filtrer les suggestions

**GET** `/api/suggestions?categorie=sport`
**GET** `/api/suggestions?budget=faible`
**GET** `/api/suggestions?categorie=food&budget=moyen`

Dans le navigateur :
```
http://localhost:5000/api/suggestions?categorie=sport
http://localhost:5000/api/suggestions?budget=faible
```

Les catégories disponibles : `culture`, `sport`, `food`, `nature`, `jeu`
Les budgets disponibles : `faible`, `moyen`, `élevé`

---

## 3. Ajouter une suggestion

**POST** `/api/suggestions`

Avec curl (terminal) :
```bash
curl -X POST http://localhost:5000/api/suggestions \
  -H "Content-Type: application/json" \
  -d '{
    "titre": "Bowling",
    "categorie": "jeu",
    "budget": "moyen",
    "description": "Soirée bowling avec les amis.",
    "note": 4
  }'
```

Réponse en cas de succès (code 201) :
```json
{ "id": 11, "titre": "Bowling", "categorie": "jeu", "budget": "moyen", "description": "Soirée bowling avec les amis.", "note": 4 }
```

Réponse en cas d'erreur (code 400) :
```json
{ "error": "Le champ 'titre' est manquant." }
```

Règles de validation :
- Tous les champs sont obligatoires
- `note` doit être un entier entre 1 et 5
- `budget` doit être `faible`, `moyen` ou `élevé`

---

## 4. Supprimer une suggestion

**DELETE** `/api/suggestions/<id>`

Avec curl (terminal) :
```bash
curl -X DELETE http://localhost:5000/api/suggestions/3
```

Réponse en cas de succès (code 200) :
```json
{ "message": "Suggestion supprimée." }
```

Réponse si l'id n'existe pas (code 404) :
```json
{ "error": "Suggestion introuvable." }
```

---

## 5. Statistiques

**GET** `/api/suggestions/stats`

Dans le navigateur :
```
http://localhost:5000/api/suggestions/stats
```

Réponse :
```json
{
  "count": 10,
  "note_moyenne": 4.4,
  "meilleure": { "id": 2, "titre": "Parc de la Villette", ... }
}
```

---

## Résumé des endpoints

| Méthode  | URL                          | Rôle                              |
|----------|------------------------------|-----------------------------------|
| GET      | /api/suggestions             | Toutes les suggestions            |
| GET      | /api/suggestions?categorie=X | Filtrer par catégorie             |
| GET      | /api/suggestions?budget=X    | Filtrer par budget                |
| POST     | /api/suggestions             | Ajouter une suggestion            |
| DELETE   | /api/suggestions/<id>        | Supprimer une suggestion par id   |
| GET      | /api/suggestions/stats       | Stats (count, moyenne, meilleure) |

---

## Lancer le serveur

```bash
cd Backend
venv/bin/python app.py
```
