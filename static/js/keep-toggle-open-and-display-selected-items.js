document.addEventListener("DOMContentLoaded", function() {
    let families = document.querySelectorAll("details");
    let listOfItems = document.querySelector("#list-of-items");

    function isDesktop() {
        return window.innerWidth >= 768;
    }
    
    // Afficher les sentiments ou besoins sélectionnés
    function updateSelectedList() {
        listOfItems.innerHTML = "";
        
        const checkedBoxes = document.querySelectorAll("input[type=checkbox]:checked");
        const errorMessage = document.querySelector("#error-message");
        
        checkedBoxes.forEach(box => {
            const li = document.createElement("li");
            const label = box.closest("label");
            li.textContent = label.textContent;
            listOfItems.appendChild(li);
            if (isDesktop()){
                label.style.display = "block";
            }
        })

        // Masquer le message d'erreur s'il y a des cases cochées
        if (checkedBoxes.length > 0) {
            errorMessage.style.display = "none";
        }   
    }

    //Laisser les familles ouvertes sur desktop et sur mobile si elles ont des items sélectionnés
    families.forEach((family) => {
        let boxes = family.querySelectorAll("input[type=checkbox]");
        
        //Faire apparaître/disparaître les sentiments ou besoin au clic sur la famille sur desktop
        family.addEventListener("click", () => {
            if (isDesktop()) {
                const familyLabels = family.querySelectorAll("label");
                familyLabels.forEach(label => {
                    const checkbox = label.querySelector("input[type=checkbox]");
                    if(checkbox.checked){
                        label.style.display = "block";
                    }
                    
                    if (label.style.display === "block") {
                        // Ne cacher que si la checkbox n'est pas cochée
                        if (!checkbox.checked) {
                            label.style.display = "none";
                        }
                    } else {
                        label.style.display = "block";
                    }
                });
            }
        });

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
            
            // Réinitialiser les styles inline des labels
            const familyLabels = family.querySelectorAll("label");
            familyLabels.forEach(label => {
                label.style.display = "";
            });
            
            if (isDesktop() || hasCheckedBox()) {
                family.setAttribute("open", "");
                label.style.display = "block";
            } else {
                family.removeAttribute("open");
            }
        });
    });

    // Initialiser la liste et les labels cochés au chargement de la page
    updateSelectedList();

});
