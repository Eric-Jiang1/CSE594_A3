from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.utils.io_utils import load_json, save_json
from app.utils.random_utils import get_random_postings
import uuid
from typing import Optional


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load dataset and pre-generated AI outputs once at startup
POSTINGS = load_json("app/data/postings.json")
AI_OUTPUTS = load_json("app/data/ai_outputs.json")

# Create a lookup dictionary for faster access
AI_OUTPUTS_DICT = {entry["id"]: entry for entry in AI_OUTPUTS}


# -----------------------
# SCHEMAS
# -----------------------
class PredictionRequest(BaseModel):
    posting_id: str


class Submission(BaseModel):
    worker_id: str
    posting_id: str
    condition: str
    worker_label: str
    worker_confidence: int
    time_on_trial_ms: int
    ai_prediction: Optional[float] = None
    ai_confidence: Optional[float] = None


# -----------------------
# ROUTES
# -----------------------

@app.get("/postings/random")
def get_random(count: int = 10):
    """Return N random postings."""
    return get_random_postings(POSTINGS, count)


@app.post("/predict")
def predict(req: PredictionRequest):
    """Return pre-generated prediction from ai_outputs.json."""
    posting_id = req.posting_id
    
    if posting_id not in AI_OUTPUTS_DICT:
        return JSONResponse(
            status_code=404,
            content={"error": f"Prediction not found for posting_id: {posting_id}"}
        )
    
    ai_output = AI_OUTPUTS_DICT[posting_id]
    return {
        "prediction": ai_output["ai_prediction"],
        "confidence": ai_output["ai_confidence"],
        "reasoning": ai_output.get("ai_reasoning", [])
    }


@app.post("/submit")
def submit_data(sub: Submission):
    """Store submission in submissions.json"""
    submissions = load_json("app/data/submissions.json")

    entry = sub.dict()
    entry["submission_id"] = str(uuid.uuid4())

    submissions.append(entry)
    save_json("app/data/submissions.json", submissions)

    return {"status": "ok", "submission_id": entry["submission_id"]}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print("\nVALIDATION ERROR DETAILS:")
    for e in exc.errors():
        print(e)   # Print each field error clearly
    print("\nRAW BODY THAT CAUSED ERROR:")
    try:
        body = await request.json()
        print(body)
    except:
        print("Could not parse body")

    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )
