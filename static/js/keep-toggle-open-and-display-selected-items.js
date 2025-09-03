document.addEventListener("DOMContentLoaded", function() {
    let families = document.querySelectorAll("details");
    let listOfItems = document.querySelector("#list-of-items");

    function isDesktop() {
        return window.innerWidth >= 768;
    }

    function updateSelectedList() {
        listOfItems.innerHTML = "";
        
        const checkedBoxes = document.querySelectorAll("input[type=checkbox]:checked");
        
        checkedBoxes.forEach(box => {
            const li = document.createElement("li");
            // Récupérer le texte du label parent
            const label = box.closest("label");
            li.textContent = label.textContent;
            listOfItems.appendChild(li);
        });
    }

    families.forEach((family) => {
        let boxes = family.querySelectorAll("input[type=checkbox]");

        function hasCheckedBox() {
            return Array.from(boxes).some(b => b.checked);
        }
        
        // Ouvrir automatiquement sur desktop ou si des cases sont cochées
        if (isDesktop() || hasCheckedBox()) {
            family.setAttribute("open", "");
        }

        boxes.forEach((box) => {
            box.addEventListener("change", () => {
                if (hasCheckedBox()) {
                    family.setAttribute("open", "");
                }
                // Mettre à jour la liste des éléments sélectionnés
                updateSelectedList();
            });
        });

        family.addEventListener("toggle", (e) => {
            // Empêcher la fermeture sur desktop
            if (isDesktop()) {
                e.preventDefault();
                family.setAttribute("open", "");
            } else if (hasCheckedBox()) {
                // Sur mobile, garder ouvert si des cases sont cochées
                family.setAttribute("open", "");
            }
        });
    });

    // Réouvrir sur changement de taille d'écran
    window.addEventListener("resize", () => {
        if (isDesktop()) {
            families.forEach(family => {
                family.setAttribute("open", "");
            });
        }
    });

    // Initialiser la liste au chargement de la page
    updateSelectedList();
});
