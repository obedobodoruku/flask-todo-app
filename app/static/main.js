document.addEventListener("DOMContentLoaded", () => {
    const taskCheck = document.querySelectorAll(".task-check");

    taskCheck.forEach(check => check.addEventListener("change", () => {
        const label = check.closest("label");
        const taskItem = check.closest(".task-list");
        const taskId = taskItem.dataset.id;
        const completed = check.checked
        if (label) {
            label.style.textDecoration = completed ? "line-through" : "none";
        }
        
        fetch(`http://127.0.0.1:5000/complete/${taskId}`, {
        method: "POST",
        headers: {"Content-type": "application/json"},
        body: JSON.stringify({ completed: completed })
    })
    .then(res => res.json())
    .then(data => console.log(`Updated: ${data}`))
    .catch(err => console.log(`Eror: ${err}`));
    }))
})


    




