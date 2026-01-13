# model.py
import pandas as pd

# Load dataset
df = pd.read_csv("E:\Coding project\Movie_predic\imdb_top_1000.csv")

# Clean runtime column
df["Runtime"] = df["Runtime"].str.replace(" min", "").astype(int)

# Rename columns for consistency
df.rename(columns={
    "Series_Title": "title",
    "Released_Year": "year",
    "Overview": "overview",
    "Genre": "genre",
    "IMDB_Rating": "imdb_rating",
    "Certificate": "certificate"
}, inplace=True)

# Ensure numeric types
df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["Runtime"] = pd.to_numeric(df["Runtime"], errors="coerce")

# Drop rows with missing numeric values
df = df.dropna(subset=["year", "Runtime"])

# Save cleaned dataset for use in app.py
df.to_pickle("movies_clean.pkl")

print("✅ Cleaned dataset saved as movies_clean.pkl")


# --- Optional helper function for recommendations ---
def recommend_movies(genre: str, min_rating: float = 0.0, max_rating: float = 10.0, top_n: int = 5):
    results = df[
        (df["genre"].str.contains(genre, case=False, na=False)) &
        (df["imdb_rating"] >= min_rating) &
        (df["imdb_rating"] <= max_rating)
    ]
    return results[["title", "year", "overview", "certificate", "genre", "imdb_rating"]].head(top_n)


if __name__ == "__main__":
    # Example usage
    recs = recommend_movies("Drama", min_rating=8.5, top_n=10)
    print(recs)
