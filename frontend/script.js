const API_URL = "http://127.0.0.1:5000/api/suggestions";

// Cibler les éléments du DOM
const form = document.getElementById("addForm");
const suggestionsList = document.getElementById("suggestionsList");
const counter = document.getElementById("counter");
const searchInput = document.getElementById("searchInput");
const sortSelect = document.getElementById("sortSelect");
const editModal = document.getElementById("editModal");
const editForm = document.getElementById("editForm");
const message = document.getElementById("message");

// Filtres actifs
let currentCategory = "toutes";
let currentBudget = "tous";

// Afficher un message de retour sous le formulaire
function showMessage(texte, type) {
    message.textContent = texte;
    message.className = type; // "success" ou "error"
    setTimeout(function() {
        message.textContent = "";
        message.className = "hidden";
    }, 3000);
}

// GET — Récupérer et afficher les suggestions
function fetchSuggestions() {
    // Construction de l'URL avec les filtres actifs
    let url = API_URL;
    const params = [];
    if (currentCategory !== "toutes") params.push("categorie=" + currentCategory);
    if (currentBudget !== "tous")     params.push("budget=" + currentBudget);
    if (searchInput.value.trim())     params.push("search=" + searchInput.value.trim());
    if (sortSelect.value)             params.push("sort=" + sortSelect.value);
    if (params.length > 0) url += "?" + params.join("&");

    fetch(url)
        .then(function(response) { return response.json(); })
        .then(function(data) {
            suggestionsList.innerHTML = "";

            if (data.length === 0) {
            suggestionsList.innerHTML = "<p class='empty-state'>Aucune sortie ne correspond à votre recherche.</p>";
            return;
        }

        data.forEach(function(s) {
                const article = document.createElement("article");
                article.innerHTML = `
                    <div class="card-img-wrap">
                        <img src="https://picsum.photos/400/200?random=${s.id}" alt="Image illustrant la sortie"/>
                        <span class="card-category">${s.categorie}</span>
                        <button class="card-delete" title="Supprimer">
                            <span class="material-symbols-outlined">delete</span>
                        </button>
                    </div>
                    <div class="card-body">
                        <div class="card-top">
                            <h4>${s.titre}</h4>
                            <span class="card-note">
                                <span class="material-symbols-outlined">star</span>${s.note}/5
                            </span>
                        </div>
                        <p>${s.description}</p>
                        <div class="card-footer">
                            <p class="card-budget">Budget : ${s.budget}</p>
                            <button class="card-edit" title="Modifier">
                                <span class="material-symbols-outlined">edit</span>
                            </button>
                        </div>
                    </div>
                `;
                article.querySelector(".card-delete").addEventListener("click", function() { deleteSuggestion(s.id); });
                article.querySelector(".card-edit").addEventListener("click", function() { openEditModal(s); });
                suggestionsList.appendChild(article);
            });

            counter.textContent = "Total : " + data.length + " suggestion(s)";
            updateStats(data);
        })
        .catch(function(err) { console.error("Erreur fetch :", err); });
}

// Calcul des stats depuis les données déjà filtrées
function updateStats(data) {
    if (data.length === 0) {
        document.getElementById("statCount").textContent = "0 sortie(s)";
        document.getElementById("statAvg").textContent = "Note moy. : —";
        document.getElementById("statBest").textContent = "Meilleure : —";
        return;
    }
    var total = data.length;
    var somme = data.reduce(function(acc, s) { return acc + s.note; }, 0);
    var moyenne = (somme / total).toFixed(2);
    var meilleure = data.reduce(function(best, s) { return s.note > best.note ? s : best; }, data[0]);

    document.getElementById("statCount").textContent = total + " sortie(s)";
    document.getElementById("statAvg").textContent = "Note moy. : " + moyenne + "/5";
    document.getElementById("statBest").textContent = "Meilleure : " + meilleure.titre;
}

// POST — Ajouter une suggestion
form.addEventListener("submit", function(event) {
    event.preventDefault();

    const newSuggestion = {
        titre:       document.getElementById("titre").value,
        categorie:   document.getElementById("categorie").value,
        budget:      document.getElementById("budget").value,
        description: document.getElementById("description").value,
        note:        parseInt(document.getElementById("note").value)
    };

    fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newSuggestion)
    })
    .then(function(response) { return response.json(); })
    .then(function(data) {
        if (data.error) {
            showMessage("Erreur : " + data.error, "error");
        } else {
            form.reset();
            showMessage("Sortie ajoutée avec succès !", "success");
            fetchSuggestions();
        }
    })
    .catch(function(err) {
        showMessage("Impossible de contacter le serveur.", "error");
        console.error("Erreur ajout :", err);
    });
});

// DELETE — Supprimer une suggestion
function deleteSuggestion(id) {
    fetch(API_URL + "/" + id, { method: "DELETE" })
        .then(function() { fetchSuggestions(); })
        .catch(function(err) { console.error("Erreur suppression :", err); });
}

// PUT — Ouvrir le modal et pré-remplir les champs
function openEditModal(s) {
    document.getElementById("editId").value          = s.id;
    document.getElementById("editTitre").value       = s.titre;
    document.getElementById("editCategorie").value   = s.categorie;
    document.getElementById("editBudget").value      = s.budget;
    document.getElementById("editDescription").value = s.description;
    document.getElementById("editNote").value        = s.note;
    editModal.classList.remove("hidden");
}

function closeEditModal() {
    editModal.classList.add("hidden");
    editForm.reset();
}

document.getElementById("cancelEdit").addEventListener("click", closeEditModal);
editModal.addEventListener("click", function(e) {
    if (e.target === editModal) closeEditModal();
});

// PUT — Envoyer les modifications
editForm.addEventListener("submit", function(e) {
    e.preventDefault();

    const id = document.getElementById("editId").value;
    const updated = {
        titre:       document.getElementById("editTitre").value,
        categorie:   document.getElementById("editCategorie").value,
        budget:      document.getElementById("editBudget").value,
        description: document.getElementById("editDescription").value,
        note:        parseInt(document.getElementById("editNote").value)
    };

    fetch(API_URL + "/" + id, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updated)
    })
    .then(function(response) { return response.json(); })
    .then(function() {
        closeEditModal();
        fetchSuggestions();
    })
    .catch(function(err) { console.error("Erreur édition :", err); });
});

// Filtres catégorie
document.querySelectorAll(".filter-btn[data-category]").forEach(function(btn) {
    btn.addEventListener("click", function() {
        document.querySelectorAll(".filter-btn[data-category]").forEach(function(b) { b.classList.remove("active"); });
        btn.classList.add("active");
        currentCategory = btn.getAttribute("data-category");
        fetchSuggestions();
    });
});

// Filtres budget
document.querySelectorAll(".filter-btn[data-budget]").forEach(function(btn) {
    btn.addEventListener("click", function() {
        document.querySelectorAll(".filter-btn[data-budget]").forEach(function(b) { b.classList.remove("active"); });
        btn.classList.add("active");
        currentBudget = btn.getAttribute("data-budget");
        fetchSuggestions();
    });
});

// Recherche et tri
searchInput.addEventListener("input", function() { fetchSuggestions(); });
sortSelect.addEventListener("change", function() { fetchSuggestions(); });

// Chargement initial
fetchSuggestions();
