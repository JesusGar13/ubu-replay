document.getElementById("refresh").addEventListener("click", () => {
    chrome.runtime.sendMessage({ action: "getClosedSessions" }, (response) => {
        const list = document.getElementById("sessions-list");
        list.innerHTML = ""; // Limpiar la lista
        response.sessions.forEach((session, index) => {
            const li = document.createElement("li");
            li.textContent = `Sesión ${index + 1}: ${session}`;
            list.appendChild(li);
        });
    });
});
