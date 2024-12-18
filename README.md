# Movie Search App

## Description
This Movie Search App is a semantic search engine for movies. It uses natural language processing to find movies based on plot summaries, genres, and other metadata. The app leverages FastAPI for the backend, Qdrant for vector search, and Sentence Transformers for generating embeddings.

## App

![App](images/movie_search.gif)

## Features
- Semantic search for movies based on plot summaries and metadata
- Customizable number of search results
- Interactive web interface
- Fast and efficient vector search using Qdrant

## Installation

### Prerequisites
- Python 3.7+
- Docker (for running Qdrant)

### Steps
1. Clone the repository:
   ```
   git clone https://github.com/Elangoraj/Semantic-Search-V2.git
   ```

2. Create a conda environment and activate it:
   ```
   conda create --name your_env_name python=3.11
   conda activate your_env_name
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Start the Qdrant server using Docker:
   ```
   docker run -p 6333:6333 qdrant/qdrant
   ```

5. Ensure the dataset is [downloaded](http://www.cs.cmu.edu/~ark/personas/) and put in the path (data/MovieSummaries/*) as shown below. 

6. Next we can run the script below to embed text, and upload the movies to Qdrant database:
   ```
   python -m app.process-and-upload-data
   ```

## Usage

1. Start the FastAPI server:
   ```
   python -m run
   ```

2. Open your web browser and go to `http://localhost:8000`

3. Enter your search query and the desired number of results in the form.

4. Click "Search" to see the results.

## Project Structure
```
movie-search-app/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── search.py
│   └── templates/
│       ├── base.html
│       └── index.html
├── data/
│   └── MovieSummaries/
│       ├── movie.metadata.tsv
│       └── plot_summaries.txt
├── notebooks/
│   └── semantic_search.ipynb
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

## Acknowledgements
- [FastAPI](https://fastapi.tiangolo.com/)
- [Qdrant](https://qdrant.tech/)
- [Sentence Transformers](https://www.sbert.net/)
- [CMU Movie Summary Corpus](http://www.cs.cmu.edu/~ark/personas/)
