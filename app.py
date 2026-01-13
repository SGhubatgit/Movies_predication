# app.py
import pandas as pd
from flask import Flask, render_template, request, jsonify
import os


app = Flask(__name__)

# Load cleaned dataset
df = pd.read_pickle("movies_clean.pkl")

def recommend_movies(genre: str, min_rating: float = 0.0, max_rating: float = 10.0, top_n: int = 5):
    results = df[
        (df["genre"].str.contains(genre, case=False, na=False)) &
        (df["imdb_rating"] >= min_rating) &
        (df["imdb_rating"] <= max_rating)
    ]
    return results[["title", "year", "overview", "certificate", "genre", "imdb_rating"]].head(top_n)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")  # serves your frontend


@app.route("/recommend", methods=["POST"])
def recommend():
    """Return movie details based on genre + rating filter"""
    payload = request.get_json(force=True)
    genre = payload.get("genre", "")
    min_rating = float(payload.get("min_rating", 0))
    max_rating = float(payload.get("max_rating", 10))
    top_n = int(payload.get("top_n", 5))

    try:
        results = recommend_movies(genre, min_rating, max_rating, top_n)
        return results.to_json(orient="records")
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

