let families = document.querySelectorAll("details");

families.forEach((family) => {
    let boxes = family.querySelectorAll("input[type=checkbox]");

    function hasCheckedBox() {
        return Array.from(boxes).some(b => b.checked);
    }

    boxes.forEach((box) => {
        box.addEventListener("change", () => {
            if (hasCheckedBox()) {
                family.setAttribute("open", "");
            }
        });
    });

    family.addEventListener("toggle", () => {
        if (hasCheckedBox()) {
            family.setAttribute("open", "");
        }
    });
});
