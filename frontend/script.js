const API_URL = "http://127.0.0.1:5000/api/suggestions";

// DOM
const form = document.getElementById("addForm");
const suggestionsList = document.getElementById("suggestionsList");
const counter = document.getElementById("counter");
const searchInput = document.getElementById("searchInput");
const sortSelect = document.getElementById("sortSelect");
const editModal = document.getElementById("editModal");
const editForm = document.getElementById("editForm");
const cancelEditBtn = document.getElementById("cancelEdit");

// État actif des filtres
let currentCategory = "toutes";
let currentBudget = "tous";

// --- Construction de l'URL avec tous les paramètres actifs ---
function buildUrl() {
    const params = new URLSearchParams();
    if (currentCategory !== "toutes") params.set("categorie", currentCategory);
    if (currentBudget !== "tous") params.set("budget", currentBudget);
    const search = searchInput.value.trim();
    if (search) params.set("search", search);
    const sort = sortSelect.value;
    if (sort) params.set("sort", sort);
    const qs = params.toString();
    return qs ? `${API_URL}?${qs}` : API_URL;
}

// --- GET : récupérer et afficher les suggestions ---
function fetchSuggestions() {
    fetch(buildUrl())
        .then(r => r.json())
        .then(data => {
            renderSuggestions(data);
            counter.textContent = `Total : ${data.length} suggestion(s)`;
        })
        .catch(err => console.error("Erreur fetch:", err));
}

function renderSuggestions(data) {
    suggestionsList.innerHTML = "";
    data.forEach(s => {
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
        article.querySelector(".card-delete").addEventListener("click", () => deleteSuggestion(s.id));
        article.querySelector(".card-edit").addEventListener("click", () => openEditModal(s));
        suggestionsList.appendChild(article);
    });
}

// --- GET stats ---
function fetchStats() {
    fetch(`${API_URL}/stats`)
        .then(r => r.json())
        .then(data => {
            document.getElementById("statCount").textContent = `${data.count} sortie(s)`;
            document.getElementById("statAvg").textContent = `Note moy. : ${data.note_moyenne ?? "—"}/5`;
            document.getElementById("statBest").textContent = data.meilleure
                ? `Meilleure : ${data.meilleure.titre}`
                : "—";
        })
        .catch(err => console.error("Erreur stats:", err));
}

// --- POST : ajouter une suggestion ---
form.addEventListener("submit", function(event) {
    event.preventDefault();
    const newSuggestion = {
        titre: document.getElementById("titre").value,
        categorie: document.getElementById("categorie").value,
        budget: document.getElementById("budget").value,
        description: document.getElementById("description").value,
        note: parseInt(document.getElementById("note").value)
    };
    fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newSuggestion)
    })
    .then(r => r.json())
    .then(() => {
        form.reset();
        fetchSuggestions();
        fetchStats();
    })
    .catch(err => console.error("Erreur ajout:", err));
});

// --- DELETE : supprimer une suggestion ---
function deleteSuggestion(id) {
    fetch(`${API_URL}/${id}`, { method: "DELETE" })
        .then(() => {
            fetchSuggestions();
            fetchStats();
        })
        .catch(err => console.error("Erreur suppression:", err));
}

// --- PUT : modifier une suggestion (modal) ---
function openEditModal(s) {
    document.getElementById("editId").value = s.id;
    document.getElementById("editTitre").value = s.titre;
    document.getElementById("editCategorie").value = s.categorie;
    document.getElementById("editBudget").value = s.budget;
    document.getElementById("editDescription").value = s.description;
    document.getElementById("editNote").value = s.note;
    editModal.classList.remove("hidden");
}

function closeEditModal() {
    editModal.classList.add("hidden");
    editForm.reset();
}

cancelEditBtn.addEventListener("click", closeEditModal);
editModal.addEventListener("click", function(e) {
    if (e.target === editModal) closeEditModal();
});

editForm.addEventListener("submit", function(e) {
    e.preventDefault();
    const id = document.getElementById("editId").value;
    const updated = {
        titre: document.getElementById("editTitre").value,
        categorie: document.getElementById("editCategorie").value,
        budget: document.getElementById("editBudget").value,
        description: document.getElementById("editDescription").value,
        note: parseInt(document.getElementById("editNote").value)
    };
    fetch(`${API_URL}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updated)
    })
    .then(r => r.json())
    .then(() => {
        closeEditModal();
        fetchSuggestions();
        fetchStats();
    })
    .catch(err => console.error("Erreur édition:", err));
});

// --- Filtres catégorie ---
document.querySelectorAll(".filter-btn[data-category]").forEach(btn => {
    btn.addEventListener("click", function() {
        document.querySelectorAll(".filter-btn[data-category]").forEach(b => b.classList.remove("active"));
        this.classList.add("active");
        currentCategory = this.getAttribute("data-category");
        fetchSuggestions();
    });
});

// --- Filtres budget ---
document.querySelectorAll(".filter-btn[data-budget]").forEach(btn => {
    btn.addEventListener("click", function() {
        document.querySelectorAll(".filter-btn[data-budget]").forEach(b => b.classList.remove("active"));
        this.classList.add("active");
        currentBudget = this.getAttribute("data-budget");
        fetchSuggestions();
    });
});

// --- Recherche et tri ---
searchInput.addEventListener("input", () => fetchSuggestions());
sortSelect.addEventListener("change", () => fetchSuggestions());

// --- Chargement initial ---
fetchSuggestions();
fetchStats();
