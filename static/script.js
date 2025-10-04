document.getElementById("generateBtn").addEventListener("click", async () => {
  const code = document.getElementById("codeInput").value;
  const errorOutput = document.getElementById("errorOutput");
  const diagram = document.getElementById("diagram");
  const downloadBtn = document.getElementById("downloadBtn");

  errorOutput.textContent = "";
  diagram.style.display = "none";
  downloadBtn.style.display = "none";

  try {
    const response = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code })
    });

    const data = await response.json();

    if (!data.success) {
      errorOutput.textContent = "Error: " + data.error;
    } else {
      diagram.src = "data:image/png;base64," + data.image;
      diagram.style.display = "block";
      downloadBtn.style.display = "inline-block";

      downloadBtn.onclick = () => {
        const link = document.createElement("a");
        link.href = diagram.src;
        link.download = "diagram.png";
        link.click();
      };
    }
  } catch (err) {
    errorOutput.textContent = "Error: " + err.message;
  }
});

document.getElementById("themeToggle").addEventListener("click", () => {
  document.body.classList.toggle("light-mode");
  const isLight = document.body.classList.contains("light-mode");
  document.getElementById("themeToggle").textContent = isLight
    ? "🌞 Light Mode"
    : "🌙 Dark Mode";
});
