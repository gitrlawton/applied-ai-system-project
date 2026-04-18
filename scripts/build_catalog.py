import pandas as pd
from pathlib import Path

GENRE_MOOD = {
    "acoustic": "peaceful", "folk": "peaceful", "singer-songwriter": "peaceful",
    "ambient": "chill", "sleep": "chill", "study": "chill",
    "blues": "melancholic", "soul": "melancholic", "gospel": "melancholic",
    "children": "happy", "disney": "happy", "kids": "happy",
    "classical": "focused", "piano": "focused",
    "comedy": "happy", "show-tunes": "happy",
    "country": "nostalgic", "honky-tonk": "nostalgic",
    "dance": "euphoric", "edm": "euphoric", "electro": "euphoric",
    "techno": "euphoric", "trance": "euphoric", "house": "euphoric",
    "dubstep": "euphoric",
    "death-metal": "intense", "metal": "intense", "black-metal": "intense",
    "grunge": "intense", "hardcore": "intense", "punk-rock": "intense",
    "punk": "intense", "emo": "intense",
    "hip-hop": "moody", "rap": "moody",
    "indie": "moody", "indie-pop": "moody", "alt-rock": "moody",
    "alternative": "moody",
    "jazz": "relaxed",
    "k-pop": "happy", "j-pop": "happy", "j-rock": "happy",
    "j-idol": "happy", "mandopop": "happy", "cantopop": "happy",
    "latin": "romantic", "reggaeton": "romantic", "samba": "romantic",
    "bossanova": "romantic", "salsa": "romantic", "tango": "romantic",
    "pagode": "romantic", "sertanejo": "romantic", "mpb": "romantic",
    "forro": "romantic", "axe": "romantic",
    "pop": "happy", "power-pop": "happy", "synth-pop": "happy",
    "r-n-b": "romantic", "romance": "romantic",
    "reggae": "peaceful", "ska": "peaceful",
    "rock": "intense", "psych-rock": "intense", "rockabilly": "intense",
    "new-age": "intense",
    "world-music": "nostalgic", "opera": "nostalgic", "afrobeat": "nostalgic",
    "iranian": "nostalgic", "turkish": "nostalgic", "swedish": "nostalgic",
    "spanish": "nostalgic", "french": "nostalgic", "german": "nostalgic",
    "british": "nostalgic", "malay": "nostalgic", "indian": "nostalgic",
}
DEFAULT_MOOD = "chill"

DROP_COLS = ["track_id", "key", "mode", "loudness", "duration_ms", "time_signature"]
RENAME_COLS = {"track_name": "title", "artist_name": "artist"}

REQUIRED_FIELDS = [
    "title", "artist", "genre", "energy", "valence", "acousticness",
    "tempo", "danceability", "speechiness", "instrumentalness",
    "liveness", "popularity", "year",
]

RAW_PATH        = Path("data/spotify_1m_raw.csv")
CATALOG_PATH    = Path("data/spotify_data.csv")
SONGS_PER_GENRE = 30
RANDOM_STATE    = 42


def build():
    print("Loading raw dataset...")
    df = pd.read_csv(RAW_PATH, index_col=0)

    df = df.drop(columns=[c for c in DROP_COLS if c in df.columns])
    df = df.rename(columns=RENAME_COLS)

    df["release_decade"] = (df["year"] // 10) * 10
    df["mood"] = df["genre"].map(GENRE_MOOD).fillna(DEFAULT_MOOD)

    before = len(df)
    df = df.dropna(subset=REQUIRED_FIELDS)
    dropped = before - len(df)
    print(f"Dropped {dropped} rows with missing values ({before} → {len(df)})")

    df = df.sort_values("popularity", ascending=False)

    catalog = pd.concat([
        g.sample(min(len(g), SONGS_PER_GENRE), random_state=RANDOM_STATE)
        for _, g in df.groupby("genre")
    ]).reset_index(drop=True)

    catalog.to_csv(CATALOG_PATH, index=False)

    print(f"Saved {len(catalog)} songs across {catalog['genre'].nunique()} genres")
    print(f"Avg popularity: {catalog['popularity'].mean():.1f}")
    print(f"Output: {CATALOG_PATH}")


if __name__ == "__main__":
    build()
