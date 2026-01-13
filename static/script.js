// Handle form submission
document.getElementById("recommendForm").addEventListener("submit", async function(e) {
  e.preventDefault();

  const genre = document.getElementById("genre").value;
  const min_rating = document.getElementById("min_rating").value;
  const max_rating = document.getElementById("max_rating").value;
  const top_n = document.getElementById("top_n").value;

  const payload = {
    genre: genre,
    min_rating: parseFloat(min_rating),
    max_rating: parseFloat(max_rating),
    top_n: parseInt(top_n)
  };

  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = "<p style='color:#e50914;'>Loading recommendations...</p>";

  try {
    const response = await fetch("/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    resultsDiv.innerHTML = "";

    if (data.error) {
      resultsDiv.innerHTML = `<p style="color:red;">Error: ${data.error}</p>`;
    } else if (data.length === 0) {
      resultsDiv.innerHTML = "<p>No movies found for your criteria.</p>";
    } else {
      data.forEach(movie => {
        const movieDiv = document.createElement("div");
        movieDiv.className = "movie";
        movieDiv.innerHTML = `
          <h3>${movie.title} (${movie.year})</h3>
          <p><strong>Genre:</strong> ${movie.genre}</p>
          <p><strong>IMDb Rating:</strong> ${movie.imdb_rating}</p>
          <p><strong>Certificate:</strong> ${movie.certificate}</p>
          <p><strong>Overview:</strong> ${movie.overview}</p>
        `;
        resultsDiv.appendChild(movieDiv);
      });
    }
  } catch (err) {
    resultsDiv.innerHTML = `<p style="color:red;">Request failed: ${err}</p>`;
  }
});

// Reset button handler
document.getElementById("resetBtn").addEventListener("click", function() {
  document.getElementById("recommendForm").reset(); // clears inputs
  document.getElementById("results").innerHTML = ""; // clears results
});
