document.addEventListener("DOMContentLoaded", function() {
    let families = document.querySelectorAll("details");
    let listOfItems = document.querySelector("#list-of-items");

    function isDesktop() {
        return window.innerWidth >= 768;
    }

    function updateSelectedList() {
        listOfItems.innerHTML = "";
        
        const checkedBoxes = document.querySelectorAll("input[type=checkbox]:checked");
        const errorMessage = document.querySelector("#error-message");
        
        checkedBoxes.forEach(box => {
            const li = document.createElement("li");
            const label = box.closest("label");
            li.textContent = label.textContent;
            listOfItems.appendChild(li);
        });
        
        // Masquer le message d'erreur s'il y a des cases cochées
        if (checkedBoxes.length > 0) {
            errorMessage.style.display = "none";
        } 
        
        
    }

    families.forEach((family) => {
        let boxes = family.querySelectorAll("input[type=checkbox]");

        function hasCheckedBox() {
            return Array.from(boxes).some(b => b.checked);
        }
        
        if (isDesktop() || hasCheckedBox()) {
            family.setAttribute("open", "");
        } else {
            // Sur mobile, fermer par défaut si aucune case cochée
            family.removeAttribute("open");
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
        families.forEach(family => {
            let boxes = family.querySelectorAll("input[type=checkbox]");
            function hasCheckedBox() {
                return Array.from(boxes).some(b => b.checked);
            }
            
            if (isDesktop() || hasCheckedBox()) {
                family.setAttribute("open", "");
            } else {
                family.removeAttribute("open");
            }
        });
    });

    // Initialiser la liste au chargement de la page
    updateSelectedList();
});
