from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from app.search import semantic_search, initialize_qdrant_client
import os
import logging
import traceback

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

static_dir = "app/static"
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

client = initialize_qdrant_client()

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/search")
async def search(request: Request, query: str = Form(...), num_results: int = Form(5)):
    logger.debug(f"Received search request: query='{query}', num_results={num_results}")
    try:
        results = semantic_search(query, client, top_k=num_results)
        logger.debug(f"Search completed. Found {len(results)} results.")
        return JSONResponse(content={"results": results, "query": query, "num_results": num_results})
    except Exception as e:
        logger.error(f"Error during search: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(content={"error": str(e)}, status_code=500)