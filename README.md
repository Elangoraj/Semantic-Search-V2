# Movie Search App

## Description
This Movie Search App is a semantic search engine for movies. It uses natural language processing to find movies based on plot summaries, genres, and other metadata. The app leverages FastAPI for the backend, Qdrant for vector search, and Sentence Transformers for generating embeddings.

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
   git clone https://github.com/your-username/movie-search-app.git
   cd movie-search-app
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Start the Qdrant server using Docker:
   ```
   docker run -p 6333:6333 qdrant/qdrant
   ```

5. Need to ensure the dataset is downloaded and put in the path (data/MovieSummaries/*) as shown below. Now we can run the process and upload script below to upload the movies to Qdrant database(you may need to modify the data processing script):
   ```
   python -m app.process-and-upload-data
   ```

## Usage

1. Start the FastAPI server:
   ```
   python run.py
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

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- [FastAPI](https://fastapi.tiangolo.com/)
- [Qdrant](https://qdrant.tech/)
- [Sentence Transformers](https://www.sbert.net/)
- [CMU Movie Summary Corpus](http://www.cs.cmu.edu/~ark/personas/)
