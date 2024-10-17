from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

encoder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def generate_embedding(text):
    logger.debug(f"Generating embedding for text: '{text}'")
    return encoder.encode(text)

def initialize_qdrant_client():
    try:
        logger.debug("Initializing Qdrant client")
        client = QdrantClient(host="localhost", port=6333)
        collections = client.get_collections()
        logger.debug(f"Available collections: {collections}")
        if "movies" not in [c.name for c in collections.collections]:
            logger.info("Creating 'movies' collection")
            client.create_collection(
                collection_name="movies",
                vectors_config=VectorParams(size=encoder.get_sentence_embedding_dimension(), distance=Distance.COSINE),
            )
        logger.info("Qdrant client initialized successfully")
        return client
    except Exception as e:
        logger.error(f"Error initializing Qdrant client: {e}")
        raise

def semantic_search(query, client, top_k=5):
    if client is None:
        logger.error("Qdrant client is None")
        raise ValueError("Qdrant client is not initialized")
    
    logger.debug(f"Generating embedding for query: '{query}'")
    query_vector = generate_embedding(query)
    
    try:
        logger.debug(f"Performing search with top_k={top_k}")
        results = client.search(
            collection_name="movies",
            query_vector=query_vector,
            limit=top_k
        )
        logger.debug(f"Search completed. Found {len(results)} results.")
        return [
            {
                'movie_name': result.payload['movie_name'],
                'release_year': result.payload['release_year'],
                'genres': result.payload['genres'],
                'summary': result.payload['text'].split('movie summary: ')[1],
                'score': result.score
            } for result in results
        ]
    except Exception as e:
        logger.error(f"Error performing semantic search: {e}")
        raise