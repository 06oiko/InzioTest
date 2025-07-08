document.addEventListener("DOMContentLoaded", () => {
  const searchButton = document.getElementById("search_button");
  const searchInput = document.getElementById("search_input");

  searchButton.addEventListener("click", async () => {
    const query = searchInput.value.trim();

    if (!query) {
      alert("Please type a request.");
      return;
    }

    await SearchPost(query);
  });
});

async function SearchPost(query) {
  const response = await fetch("/search", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });

  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "search_results.txt";
  a.click();
}
