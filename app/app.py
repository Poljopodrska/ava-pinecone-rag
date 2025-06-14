print("✅ LOADING CORRECT app.py FROM:", __file__)

import sys, os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ✅ Import LangChain agent and embedding runner
from agent.agent import ask_agent
from scripts.embed_runner import run_fis_embedding

# ✅ Create FastAPI app
app = FastAPI()

# ✅ Setup templates and static
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ✅ GET route: show the form (browser)
@app.get("/", response_class=HTMLResponse)
def form_get(request: Request):
    print("✅ GET / triggered")
    return templates.TemplateResponse("form.html", {"request": request, "response": None})

# ✅ POST route: process form submission (browser)
@app.post("/", response_class=HTMLResponse)
async def form_post(request: Request, question: str = Form(...)):
    print("✅ POST / triggered — question:", question)
    response = ask_agent(question)
    return templates.TemplateResponse("form.html", {
        "request": request,
        "response": response,
        "question": question
    })

# ✅ API: JSON endpoint for chatbot or curl/Postman
class AskRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_api(request: AskRequest):
    print("✅ POST /ask triggered — question:", request.question)
    return {"answer": ask_agent(request.question)}

# ✅ Optional: trigger FIS embedding
@app.get("/embed-fis")
def embed_fis():
    try:
        run_fis_embedding()
        return {"status": "✅ FIS documents embedded successfully into Pinecone."}
    except Exception as e:
        return {"status": "❌ Failed to embed", "error": str(e)}

# ✅ Test endpoint
@app.get("/test123")
def test_route():
    return {"message": "✅ This is the REAL app.py!"}
