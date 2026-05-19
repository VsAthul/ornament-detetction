import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from database import initialize_db
from graph import detection_graph
from schemas import Agent_State
from database import get_db_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_db()
    yield


app = FastAPI(
    title = "Gold ornament detector",
    description="Upload an image to detect and count gold ornaments using a model via Groq",
    version="1.0.0",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory = "templates")

@app.get("/", response_class = HTMLResponse)
async def ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
        )


@app.post("/analyze")
async def analyse(file: UploadFile = File(...)):
    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(status_code=400, detail = "Uploaded file is empty")
    
    state :Agent_State={
        "image_bytes":image_bytes,
        "filename": file.filename,
        "content_type": file.content_type,
        "items": [],
    }

    try :
        result = detection_graph.invoke(state)
    except AssertionError as e:
        raise HTTPException(status_code=500, detail= str(e))
    except Exception as e :
        raise HTTPException(status_code=500, detail=f"Detection Failed : {str(e)}")
    
    return {
        "filename": file.filename,
        "total_types": len(result["items"]),
        "total_count": sum(i.quantity for i in result["items"]),
        "items": [i.model_dump() for i  in result["items"]],
    }

