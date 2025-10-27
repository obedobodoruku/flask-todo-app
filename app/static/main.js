document.addEventListener("DOMContentLoaded", () => {
    const taskCheck = document.querySelectorAll(".task-check");


    taskCheck.forEach(check => check.addEventListener("change", () => {
        const label = check.closest("label");
        
        if (label) {
            label.style.textDecoration = check.checked ? "line-through" : "none";
        }
        
    }))
    
})



