from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


# ==============================================================================
# DONNÉES — stockage en mémoire (une simple liste Python)
# ==============================================================================
suggestions = [
    {"id": 1,  "titre": "Cinéma UGC",          "categorie": "culture", "budget": "moyen",  "description": "Soirée cinéma au tarif étudiant.",              "note": 4},
    {"id": 2,  "titre": "Parc de la Villette",  "categorie": "nature",  "budget": "faible", "description": "Balade et pique-nique au bord du canal.",        "note": 5},
    {"id": 3,  "titre": "Laser Game",           "categorie": "jeu",     "budget": "moyen",  "description": "Une session laser game entre amis.",             "note": 3},
    {"id": 4,  "titre": "Match de basket",      "categorie": "sport",   "budget": "faible", "description": "Match ouvert au gymnase municipal.",             "note": 4},
    {"id": 5,  "titre": "Resto japonais",       "categorie": "food",    "budget": "moyen",  "description": "Déjeuner dans un ramen bar du quartier.",        "note": 5},
    {"id": 6,  "titre": "Musée d'Orsay",        "categorie": "culture", "budget": "faible", "description": "Entrée gratuite le premier dimanche du mois.",  "note": 5},
    {"id": 7,  "titre": "Escape Game",          "categorie": "jeu",     "budget": "élevé",  "description": "60 minutes pour s'échapper d'une salle thème.", "note": 4},
    {"id": 8,  "titre": "Randonnée en forêt",   "categorie": "nature",  "budget": "faible", "description": "Journée de randonnée dans les bois.",            "note": 5},
    {"id": 9,  "titre": "Cours de cuisine",     "categorie": "food",    "budget": "élevé",  "description": "Atelier pour apprendre à faire des sushis.",     "note": 4},
    {"id": 10, "titre": "Concert en plein air", "categorie": "culture", "budget": "moyen",  "description": "Concert gratuit dans le parc.",                  "note": 5},
    {"id": 11, "titre": "Bowling",              "categorie": "jeu",     "budget": "moyen",  "description": "Soirée bowling entre amis.",                     "note": 3},
    {"id": 12, "titre": "Vélo en ville",        "categorie": "sport",   "budget": "faible", "description": "Tour à vélo sur les pistes cyclables de Paris.", "note": 4},
    {"id": 13, "titre": "Marché bio",           "categorie": "food",    "budget": "faible", "description": "Flâner et goûter au marché bio du quartier.",    "note": 4},
    {"id": 14, "titre": "Exposition photo",     "categorie": "culture", "budget": "faible", "description": "Expo photo gratuite à la Mairie.",               "note": 4},
    {"id": 15, "titre": "Karting",              "categorie": "sport",   "budget": "élevé",  "description": "Session karting en circuit indoor.",             "note": 5},
    {"id": 16, "titre": "Piscine municipale",   "categorie": "sport",   "budget": "faible", "description": "Nage libre à la piscine du quartier.",           "note": 3},
    {"id": 17, "titre": "Brunch dominical",     "categorie": "food",    "budget": "moyen",  "description": "Brunch copieux dans un café branché.",           "note": 5},
    {"id": 18, "titre": "Jeu de société café",  "categorie": "jeu",     "budget": "faible", "description": "Après-midi jeux de société dans un café ludique.","note": 5},
    {"id": 19, "titre": "Visite du Louvre",     "categorie": "culture", "budget": "moyen",  "description": "Visite guidée des galeries égyptiennes.",        "note": 4},
    {"id": 20, "titre": "Kayak sur la Marne",       "categorie": "nature",  "budget": "moyen",  "description": "Location de kayak pour une balade fluviale.",             "note": 5},
    {"id": 21, "titre": "McDo après les cours",     "categorie": "food",    "budget": "faible", "description": "Classique mais efficace après une longue journée.",       "note": 2},
    {"id": 22, "titre": "Soirée karaoké",           "categorie": "jeu",     "budget": "moyen",  "description": "Karaoké en groupe, ambiance garantie mais oreilles en danger.", "note": 3},
    {"id": 23, "titre": "Musée Grévin",             "categorie": "culture", "budget": "élevé",  "description": "Les statues de cire valent-elles vraiment ce prix ?",     "note": 2},
    {"id": 24, "titre": "Balade à Montmartre",      "categorie": "nature",  "budget": "faible", "description": "Grimper la butte et profiter de la vue sur Paris.",       "note": 5},
    {"id": 25, "titre": "Accrobranche",             "categorie": "sport",   "budget": "élevé",  "description": "Parcours dans les arbres, adrénaline assurée.",           "note": 4},
    {"id": 26, "titre": "Vieux films au ciné-club", "categorie": "culture", "budget": "faible", "description": "Séance de cinéma old-school, pas forcément pour tout le monde.", "note": 2},
    {"id": 27, "titre": "Poker entre amis",         "categorie": "jeu",     "budget": "faible", "description": "Soirée poker à la maison, attention aux mauvais perdants.", "note": 4},
    {"id": 28, "titre": "Restaurant étoilé",        "categorie": "food",    "budget": "élevé",  "description": "Expérience gastronomique exceptionnelle, budget serré après.", "note": 5},
    {"id": 29, "titre": "Salle de sport discount",  "categorie": "sport",   "budget": "faible", "description": "Machines vieillissantes mais le prix fait oublier le reste.", "note": 2},
    {"id": 30, "titre": "Pique-nique au Trocadéro", "categorie": "nature",  "budget": "faible", "description": "Vue sur la Tour Eiffel, sandwich et bonne humeur.",       "note": 5},
    {"id": 31, "titre": "Escape Game budget",       "categorie": "jeu",     "budget": "moyen",  "description": "Version moins chère mais scénario un peu décevant.",      "note": 2},
    {"id": 32, "titre": "Cours de salsa",           "categorie": "sport",   "budget": "moyen",  "description": "Premier cours offert, ensuite on accroche ou pas.",       "note": 3},
    {"id": 33, "titre": "Food truck festival",      "categorie": "food",    "budget": "moyen",  "description": "Large choix de cuisine du monde dans un même endroit.",    "note": 4},
    {"id": 34, "titre": "Visite catacombes",        "categorie": "culture", "budget": "faible", "description": "Impressionnant mais claustrophobes s'abstenir.",          "note": 4},
    {"id": 35, "titre": "Billard américain",        "categorie": "jeu",     "budget": "faible", "description": "Bar avec billard, ambiance cool mais tables parfois prises.", "note": 3},
    {"id": 36, "titre": "Zumba en plein air",       "categorie": "sport",   "budget": "faible", "description": "Cours gratuit dans le parc le samedi matin.",            "note": 3},
    {"id": 37, "titre": "Brunch hors de prix",      "categorie": "food",    "budget": "élevé",  "description": "Joli cadre mais l'addition pique vraiment.",             "note": 1},
    {"id": 38, "titre": "Opéra Bastille",           "categorie": "culture", "budget": "élevé",  "description": "Expérience unique, tarif réduit étudiant disponible.",    "note": 5},
    {"id": 39, "titre": "Ping-pong au parc",        "categorie": "sport",   "budget": "faible", "description": "Tables en libre accès, juste ramener ses raquettes.",    "note": 4},
    {"id": 40, "titre": "Musée en travaux",         "categorie": "culture", "budget": "moyen",  "description": "La moitié des salles fermées, vraiment décevant.",        "note": 1},
]

# "next_id" est un compteur pour attribuer un ID unique à chaque nouvelle suggestion.
next_id = 41


# ==============================================================================
# ENDPOINT 1 — GET /api/suggestions
# ==============================================================================
# Cette route répond aux requêtes GET sur /api/suggestions.
# Elle renvoie toutes les suggestions au format JSON.
#
# Paramètres optionnels dans l'URL (query string) :
#   ?categorie=sport          → filtre par catégorie
#   ?budget=faible            → filtre par niveau de budget
#   ?search=cinema            → recherche dans le titre ET la description
#   ?sort=note                → trie par note (décroissant, les meilleures en premier)
#   ?sort=titre               → trie par titre (ordre alphabétique)
#
# On peut combiner tous ces paramètres :
#   /api/suggestions?categorie=food&sort=note
#   /api/suggestions?search=parc&budget=faible
@app.route("/api/suggestions", methods=["GET"])
def get_suggestions():
    # request.args.get("x") lit le paramètre ?x= dans l'URL.
    # Si le paramètre est absent, get() renvoie None par défaut.
    categorie = request.args.get("categorie")
    budget    = request.args.get("budget")
    search    = request.args.get("search")
    sort      = request.args.get("sort")

    # On commence avec la liste complète.
    # On copie la liste avec list() pour ne pas modifier l'originale lors du tri.
    result = list(suggestions)

    # --- Filtre par catégorie ---
    # Si le paramètre ?categorie= est fourni, on ne garde que les suggestions
    # dont la catégorie correspond exactement à la valeur demandée.
    if categorie:
        result = [s for s in result if s["categorie"] == categorie]

    # --- Filtre par budget ---
    # Même logique : on filtre sur la valeur exacte du budget.
    if budget:
        result = [s for s in result if s["budget"] == budget]

    # --- Recherche par mot-clé ---
    # Si le paramètre ?search= est fourni, on garde uniquement les suggestions
    # dont le titre OU la description contient le mot-clé (sans tenir compte
    # des majuscules grâce à .lower()).
    # Exemple : ?search=parc  trouvera "Parc de la Villette" et "Concert dans le parc"
    if search:
        mot = search.lower()
        result = [
            s for s in result
            if mot in s["titre"].lower() or mot in s["description"].lower()
        ]

    # --- Tri ---
    # Si le paramètre ?sort= est fourni, on trie la liste résultante.
    # sorted() renvoie une NOUVELLE liste triée sans modifier l'originale.
    if sort == "note":
        # Tri par note décroissante : la suggestion avec la meilleure note apparaît en premier.
        # reverse=True inverse l'ordre (de grand à petit).
        result = sorted(result, key=lambda s: s["note"], reverse=True)
    elif sort == "titre":
        # Tri alphabétique croissant sur le titre.
        # .lower() garantit que les majuscules ne faussent pas l'ordre.
        result = sorted(result, key=lambda s: s["titre"].lower())

    # jsonify() transforme la liste Python en JSON et l'envoie au client.
    return jsonify(result), 200


# ==============================================================================
# ENDPOINT 2 — POST /api/suggestions
# ==============================================================================
# Cette route répond aux requêtes POST sur /api/suggestions.
# Le front-end envoie une nouvelle suggestion en JSON dans le corps de la
# requête, et on l'ajoute à notre liste.
@app.route("/api/suggestions", methods=["POST"])
def add_suggestion():
    # "global" indique qu'on veut modifier la variable next_id
    # définie en dehors de la fonction (sinon Python en crée une locale).
    global next_id

    # On lit le JSON envoyé par le front-end dans le corps de la requête.
    # Si le corps est vide ou mal formé, get_json() renvoie None.
    data = request.get_json()

    # Sécurité : si aucune donnée n'a été envoyée, on refuse et on répond 400.
    # 400 = "Bad Request" (la requête est incorrecte).
    if not data:
        return jsonify({"error": "Données manquantes."}), 400

    # On liste tous les champs qu'une suggestion doit obligatoirement avoir.
    champs_requis = ["titre", "categorie", "budget", "description", "note"]

    # On parcourt chaque champ requis et on vérifie qu'il est bien présent
    # et non vide dans les données reçues.
    # str(...).strip() supprime les espaces au début/fin et convertit en texte.
    for champ in champs_requis:
        if not str(data.get(champ, "")).strip():
            # Si un champ manque, on renvoie une erreur 400 avec le nom du champ.
            return jsonify({"error": f"Le champ '{champ}' est manquant."}), 400

    # La note doit être un entier entre 1 et 5.
    # On utilise try/except pour attraper les erreurs si la valeur n'est pas
    # convertible en entier (ex: "abc" → ValueError).
    try:
        note = int(data["note"])
        if not 1 <= note <= 5:
            raise ValueError  # on force l'erreur si hors de la plage 1–5
    except (ValueError, TypeError):
        return jsonify({"error": "La note doit être un entier entre 1 et 5."}), 400

    # Le budget doit être exactement l'une de ces trois valeurs.
    # L'opérateur "not in" vérifie que la valeur n'est pas dans le tuple.
    if data["budget"] not in ("faible", "moyen", "élevé"):
        return jsonify({"error": "Budget invalide. Valeurs acceptées : faible, moyen, élevé"}), 400

    # Toutes les vérifications sont passées : on crée la nouvelle suggestion.
    # .strip() supprime les espaces inutiles au début et à la fin du texte.
    nouvelle = {
        "id":          next_id,               # ID unique généré automatiquement
        "titre":       data["titre"].strip(),
        "categorie":   data["categorie"].strip(),
        "budget":      data["budget"],
        "description": data["description"].strip(),
        "note":        note,
    }

    # On incrémente le compteur pour que le prochain ID soit différent.
    next_id += 1

    # On ajoute la nouvelle suggestion à la liste.
    suggestions.append(nouvelle)

    # On renvoie la suggestion créée avec le code 201 ("Created").
    # 201 signifie qu'une ressource a bien été créée côté serveur.
    return jsonify(nouvelle), 201


# ==============================================================================
# ENDPOINT 3 — PUT /api/suggestions/<id>
# ==============================================================================
# Cette route permet de MODIFIER une suggestion existante.
# Le front-end envoie les nouveaux champs en JSON, et on met à jour la suggestion
# dont l'ID est passé dans l'URL.
# Exemple : PUT /api/suggestions/3  avec {"note": 5} → met la note de la suggestion 3 à 5
#
# On n'est pas obligé d'envoyer tous les champs : seuls ceux présents dans la
# requête seront mis à jour (modification partielle).
@app.route("/api/suggestions/<int:suggestion_id>", methods=["PUT"])
def update_suggestion(suggestion_id):
    # On lit le JSON envoyé dans le corps de la requête.
    data = request.get_json()

    # Si le corps est vide ou absent, on refuse avec une erreur 400.
    if not data:
        return jsonify({"error": "Données manquantes."}), 400

    # On cherche la suggestion correspondant à l'ID dans la liste.
    cible = None
    for s in suggestions:
        if s["id"] == suggestion_id:
            cible = s
            break  # inutile de continuer une fois trouvé

    # Si aucune suggestion ne correspond à cet ID, on renvoie 404 ("Not Found").
    if cible is None:
        return jsonify({"error": "Suggestion introuvable."}), 404

    # --- Mise à jour champ par champ ---
    # Pour chaque champ autorisé à être modifié, on vérifie si le front-end
    # l'a envoyé. Si oui, on valide sa valeur avant de l'appliquer.

    # Titre : on accepte tout texte non vide
    if "titre" in data:
        if not str(data["titre"]).strip():
            return jsonify({"error": "Le titre ne peut pas être vide."}), 400
        cible["titre"] = data["titre"].strip()

    # Catégorie : on accepte tout texte non vide
    if "categorie" in data:
        if not str(data["categorie"]).strip():
            return jsonify({"error": "La catégorie ne peut pas être vide."}), 400
        cible["categorie"] = data["categorie"].strip()

    # Budget : doit être l'une des trois valeurs autorisées
    if "budget" in data:
        if data["budget"] not in ("faible", "moyen", "élevé"):
            return jsonify({"error": "Budget invalide. Valeurs acceptées : faible, moyen, élevé"}), 400
        cible["budget"] = data["budget"]

    # Description : on accepte tout texte non vide
    if "description" in data:
        if not str(data["description"]).strip():
            return jsonify({"error": "La description ne peut pas être vide."}), 400
        cible["description"] = data["description"].strip()

    # Note : doit rester un entier entre 1 et 5
    if "note" in data:
        try:
            note = int(data["note"])
            if not 1 <= note <= 5:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "La note doit être un entier entre 1 et 5."}), 400
        cible["note"] = note

    # On renvoie la suggestion mise à jour avec le code 200 ("OK").
    return jsonify(cible), 200


# ==============================================================================
# ENDPOINT 4 — DELETE /api/suggestions/<id>
# ==============================================================================
# Cette route supprime la suggestion dont l'ID est passé dans l'URL.
# Exemple : DELETE /api/suggestions/3  → supprime la suggestion avec id=3
#
# Flask convertit automatiquement <int:suggestion_id> en entier Python.
@app.route("/api/suggestions/<int:suggestion_id>", methods=["DELETE"])
def delete_suggestion(suggestion_id):
    # On parcourt la liste pour trouver la suggestion avec l'ID demandé.
    cible = None
    for s in suggestions:
        if s["id"] == suggestion_id:
            cible = s
            break  # on arrête la boucle dès qu'on a trouvé

    # Si on n'a rien trouvé, on renvoie 404 ("Not Found").
    if cible is None:
        return jsonify({"error": "Suggestion introuvable."}), 404

    # On supprime la suggestion trouvée de la liste.
    suggestions.remove(cible)

    # On confirme la suppression avec un message et le code 200.
    return jsonify({"message": "Suggestion supprimée."}), 200


# ==============================================================================
# ENDPOINT 5 — GET /api/suggestions/stats  (bonus)
# ==============================================================================
# Renvoie des statistiques globales sur les suggestions :
#   - count        : nombre total de suggestions
#   - note_moyenne : moyenne des notes (arrondie à 2 décimales)
#   - meilleure    : la suggestion avec la note la plus haute
@app.route("/api/suggestions/stats", methods=["GET"])
def get_stats():
    # Cas particulier : si la liste est vide, on évite une division par zéro.
    if not suggestions:
        return jsonify({"count": 0, "note_moyenne": None, "meilleure": None}), 200

    total = len(suggestions)

    # sum() additionne toutes les notes, on divise par le total pour la moyenne.
    # round(..., 2) arrondit à 2 chiffres après la virgule.
    note_moyenne = round(sum(s["note"] for s in suggestions) / total, 2)

    # max() parcourt la liste et renvoie l'élément avec la note la plus haute.
    # "key=lambda s: s["note"]" indique à max() sur quel critère comparer.
    meilleure = max(suggestions, key=lambda s: s["note"])

    return jsonify({
        "count":        total,
        "note_moyenne": note_moyenne,
        "meilleure":    meilleure,
    }), 200


# ==============================================================================
# LANCEMENT DU SERVEUR
# ==============================================================================
# Ce bloc ne s'exécute que si on lance directement ce fichier avec :
#   python app.py
# (et non pas si le fichier est importé dans un autre script)
if __name__ == "__main__":
    # debug=True : Flask redémarre automatiquement quand on modifie le code
    # port=5000  : le serveur écoute sur http://localhost:5000
    app.run(debug=True, port=5000)
