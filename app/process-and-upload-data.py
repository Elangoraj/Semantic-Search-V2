import pandas as pd
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models
import ast
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_genres(genre_string):
    try:
        genre_dict = ast.literal_eval(genre_string)
        genres = ', '.join(genre_dict.values())
        return genres
    except:
        return ''

def clean_text(text):
    return text.lower().strip()

def process_data(movies_path, plots_path):
    logger.info("Processing movie metadata...")
    movies = pd.read_csv(movies_path, sep='\t', on_bad_lines='skip')
    movies.columns = ['movie_id', 'meta1', 'movie_name', 'release_date', 'meta2', 'meta3', 'language', 'country', 'genres']
    movies = movies.drop(columns=['meta1', 'meta2', 'meta3'])

    movies['language'] = movies['language'].apply(extract_genres)
    movies['country'] = movies['country'].apply(extract_genres)
    movies['genres'] = movies['genres'].apply(extract_genres)
    movies['language'] = movies['language'].str.replace('Language', '', regex=False)

    logger.info("Processing plot summaries...")
    plots = pd.read_csv(plots_path, sep='\t', names=['movie_id', 'summary'])
    
    df = movies.merge(plots, on='movie_id')
    df['clean_summary'] = df['summary'].apply(clean_text)

    df['release_year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year

    df['text'] = df.apply(lambda row: 
        f"movie name: {row['movie_name']}, " +
        (f"release year: {row['release_year']}, " if pd.notna(row['release_year']) else "") +
        f"movie language: {row['language']}, " +
        f"movie country: {row['country']}, " +
        f"movie genres: ({row['genres']}), " +
        f"movie summary: {row['clean_summary']}", 
        axis=1
    )

    return df

def create_and_upload_to_qdrant(df, client, collection_name="movies", encoder_model="all-MiniLM-L6-v2", batch_size=100):
    logger.info("Initializing SentenceTransformer...")
    encoder = SentenceTransformer(encoder_model)
    
    logger.info(f"Creating collection: {collection_name}")
    vector_size = len(encoder.encode("Sample text"))
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE)
    )
    
    logger.info("Preparing data for upload...")
    input_data = df[['movie_name', 'release_year', 'genres', 'language', 'country', 'text']].to_dict(orient='records')
    
    total_batches = (len(input_data) - 1) // batch_size + 1
    for i in range(0, len(input_data), batch_size):
        batch = input_data[i:i+batch_size]
        
        logger.info(f"Processing batch {i//batch_size + 1}/{total_batches}")
        
        points = [
            models.PointStruct(
                id=idx + i,
                vector=encoder.encode(doc["text"]).tolist(),
                payload=doc
            )
            for idx, doc in enumerate(batch)
        ]
        
        client.upsert(
            collection_name=collection_name,
            points=points
        )
    
    logger.info(f"Upload complete. Total points: {len(input_data)}")

if __name__ == "__main__":
    movies_path = "data/MovieSummaries/movie.metadata.tsv"
    plots_path = "data/MovieSummaries/plot_summaries.txt"
    
    logger.info("Starting data processing...")
    df = process_data(movies_path, plots_path)
    
    logger.info("Connecting to Qdrant...")
    client = QdrantClient(host="localhost", port=6333)
    
    logger.info("Starting data upload to Qdrant...")
    create_and_upload_to_qdrant(df, client)
    
    logger.info("Process completed successfully!")
