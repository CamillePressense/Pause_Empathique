document.addEventListener("DOMContentLoaded", function() {
    let families = document.querySelectorAll("details");

    function isDesktop() {
        return window.innerWidth >= 768;
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
});
