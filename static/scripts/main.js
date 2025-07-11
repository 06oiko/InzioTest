document.addEventListener("DOMContentLoaded", () => {
  const searchButton = document.getElementById("search_button");
  const searchInput = document.getElementById("search_input");
  const format = document.getElementById("format_select").value;

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
  try {
    const response = await fetch("/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, format }),
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "search_results.txt";
    a.click();
    URL.revokeObjectURL(url);
  } catch (error) {
    console.error("SearchPost error:", error);
    alert("Failed to fetch search results. Please try again.");
  }
}
