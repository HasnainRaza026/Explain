const socket = io(); // Ensure this runs without errors

socket.on("connect", () => {
    console.log("WebSocket connected!");
});

document.getElementById("movieInput").addEventListener("input", function () {
    let query = this.value.trim();
    if (query.length > 0) {
        socket.emit("search_query", query);
        console.log("Query sent to server:", query);
    }
});

socket.on("search_results", function (data) {
    console.log("Received data from server:", data);
    let suggestions = document.getElementById("suggestions");
    suggestions.innerHTML = "";

    if (data.length > 0) {
        data.forEach(movie => {
            let item = document.createElement("li");
            item.textContent = `${movie.title} (${movie.year})`;
            item.classList.add("list-group-item");
            suggestions.appendChild(item);
        });
        suggestions.style.display = "block";
    } else {
        suggestions.style.display = "none";
    }
});
