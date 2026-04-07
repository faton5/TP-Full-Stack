// URL de l'API (à adapter avec le port Flask)
const API_URL = "http://127.0.0.1:5000/api/suggestions";

// Étape 1 : Cibler les éléments du DOM
const form = document.getElementById("addForm");
const suggestionsList = document.getElementById("suggestionsList");
const counter = document.getElementById("counter");
const filterButtons = document.querySelectorAll(".filter-btn");

function setActiveFilter(activeButton) {
    filterButtons.forEach(button => button.classList.remove("active"));
    activeButton.classList.add("active");
}

function getActiveCategory() {
    const activeButton = document.querySelector(".filter-btn.active");
    return activeButton ? activeButton.getAttribute("data-category") : "toutes";
}

// Étape 2 : Récupérer et afficher les données (GET)
function fetchSuggestions(category = "toutes") {
    let url = API_URL;
    if (category !== "toutes") {
        url += `?categorie=${category}`;
    }

    // Syntaxe exacte de la slide "API Rest"
    fetch(url)
        .then(response => response.json())
        .then(data => {
            suggestionsList.innerHTML = ""; // On vide la liste

            // On boucle sur chaque objet JSON
            data.forEach(suggestion => {
                // Création de l'article HTML (Slide TD1)
                const article = document.createElement("article");
                article.className = "bg-surface-container-lowest rounded-[2rem] overflow-hidden shadow-md hover:translate-y-[-4px] transition-transform duration-300";
                
                // Injection des données dans le design Tailwind
                article.innerHTML = `
                    <div class="relative h-32 w-full bg-slate-200">
                        <img class="w-full h-full object-cover" src="https://picsum.photos/400/200?random=${suggestion.id}" alt="Image illustrant la sortie"/>
                        <div class="absolute top-4 left-4 flex gap-2">
                            <span class="bg-white/80 backdrop-blur-md text-primary text-[10px] font-extrabold px-3 py-1 rounded-full uppercase">${suggestion.categorie}</span>
                        </div>
                        <div class="absolute bottom-4 right-4">
                            <button onclick="deleteSuggestion(${suggestion.id})" class="w-10 h-10 bg-error/10 text-error rounded-full flex items-center justify-center hover:bg-error hover:text-white transition-colors">
                                <span class="material-symbols-outlined text-xl">delete</span>
                            </button>
                        </div>
                    </div>
                    <div class="p-6">
                        <div class="flex justify-between items-start mb-2">
                            <h4 class="text-xl font-bold leading-tight text-on-surface">${suggestion.titre}</h4>
                            <div class="flex items-center gap-1 bg-surface-container-high px-2 py-1 rounded-lg">
                                <span class="material-symbols-outlined text-sm">star</span>
                                <span class="text-xs font-bold">${suggestion.note}/5</span>
                            </div>
                        </div>
                        <p class="text-sm text-on-surface-variant mb-4">${suggestion.description}</p>
                        <div class="flex items-center gap-2">
                            <span class="text-xs font-semibold uppercase tracking-wide">Budget : ${suggestion.budget}</span>
                        </div>
                    </div>
                `;
                // On ajoute l'élément au DOM
                suggestionsList.appendChild(article);
            });

            if (counter) {
                counter.textContent = `Total : ${data.length} suggestion(s)`;
            }
        })
        .catch(error => {
            console.error("Erreur lors de la récupération :", error);
        });
}

// Étape 3 : Ajouter une suggestion (POST)
form.addEventListener("submit", function(event) {
    event.preventDefault(); // Annule le rechargement par défaut

    const newSuggestion = {
        titre: document.getElementById("titre").value,
        categorie: document.getElementById("categorie").value,
        budget: document.getElementById("budget").value,
        description: document.getElementById("description").value,
        note: parseInt(document.getElementById("note").value)
    };

    // Requête POST vue en TD1
    fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(newSuggestion)
    })
    .then(response => response.json())
    .then(data => {
        form.reset(); // Vider les champs
        fetchSuggestions(getActiveCategory()); // Recharger la liste sans perdre le filtre actif
    })
    .catch(error => {
        console.error("Erreur lors de l'ajout :", error);
    });
});

// Étape Bonus : Supprimer un élément (Niveau Avancé)
function deleteSuggestion(id) {
    fetch(`${API_URL}/${id}`, {
        method: "DELETE"
    })
    .then(() => {
        fetchSuggestions(getActiveCategory()); // Mise à jour de l'affichage sans changer le filtre
    })
    .catch(error => {
        console.error("Erreur de suppression :", error);
    });
}

// Écouteur pour les boutons de filtrage
filterButtons.forEach(button => {
    button.addEventListener("click", function() {
        setActiveFilter(this);
        const category = this.getAttribute("data-category");
        fetchSuggestions(category);
    });
});

// Chargement initial des données au démarrage
fetchSuggestions();