document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("/onboard", {
      method: "POST",
      body: formData,
      headers: {
        Authorization: "Bearer {self.api_key}",
      },
    });
    const data = await response.json();
    document.getElementById("message").textContent = data.message;
    document.getElementById("results").textContent = JSON.stringify(
      data.results,
      null,
      2
    );
  } catch (error) {
    document.getElementById("message").textContent =
      "An error occurred: " + error.message;
  }
});
