document.getElementById("form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = document.getElementById("text").value;
  const res = await fetch("/classify", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  const data = await res.json();
  const output = document.getElementById("output");
  if (data.error) {
    output.style.display = "block";
    output.innerHTML = `<p>${data.error}</p>`;
    return;
  }

  output.style.display = "block";
  output.innerHTML = `
    <strong>Predicho:</strong> ${data.predicted}<br>
    <div class="prob">🇪🇸 Español: ${(data.probabilities.ESPAÑOL * 100).toFixed(2)}%</div>
    <div class="prob">🇬🇧 Inglés: ${(data.probabilities.INGLES * 100).toFixed(2)}%</div>
    <div class="prob">🇫🇷 Francés: ${(data.probabilities.FRANCES * 100).toFixed(2)}%</div>
  `;
});
