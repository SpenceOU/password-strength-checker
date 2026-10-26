const input = document.getElementById("passwordInput");
const bar = document.getElementById("strengthBar");
const label = document.getElementById("strengthLabel");
const crackTimeBox = document.getElementById("crackTimeBox");
const crackTimeEl = document.getElementById("crackTime");
const feedbackList = document.getElementById("feedbackList");

const strengthColors = {
    "Very Weak": "#ef4444",
    "Weak": "#f97316",
    "Moderate": "#eab308",
    "Strong": "#84cc16",
    "Very Strong": "#22c55e"
};

let debounceTimer;

input.addEventListener("input", () => {
    clearTimeout(debounceTimer);
    const password = input.value;

    if (!password) {
        bar.style.width = "0%";
        label.textContent = "";
        crackTimeBox.classList.add("hidden");
        feedbackList.innerHTML = "";
        return;
    }

    debounceTimer = setTimeout(() => {
        fetch("/check", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ password: password })
        })
        .then(res => res.json())
        .then(data => {
            bar.style.width = data.score + "%";
            bar.style.background = strengthColors[data.strength];
            label.textContent = data.strength;
            label.style.color = strengthColors[data.strength];

            crackTimeBox.classList.remove("hidden");
            crackTimeEl.textContent = data.crack_time;

            feedbackList.innerHTML = "";
            data.feedback.forEach(msg => {
                const li = document.createElement("li");
                li.textContent = msg;
                feedbackList.appendChild(li);
            });
        });
    }, 200);
});