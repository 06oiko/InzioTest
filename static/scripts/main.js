document.addEventListener("DOMContentLoaded", () => {
  const searchButton = document.getElementById("search_button");
  const searchInput = document.getElementById("search_input");

  searchButton.addEventListener("click", async () => {
    const query = searchInput.value.trim();

    if (!query) {
      alert("Please type a request.");
      return;
    }
  });
});
