from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CRITICAL: This allows the exam server to fetch your data without getting blocked
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ⚠️ WARNING: Replace this mock data with the EXACT JSON structure the exam asks for!
EXAM_JSON_RESPONSE = {
    "audio_1": {"text": "안녕하세요", "speaker": "A"},
    "audio_2": {"text": "감사합니다", "speaker": "B"}
}

# The root endpoint (good for checking if the server is alive)
@app.get("/")
def read_root():
    return {"status": "Korean Audio API is running!"}

# The endpoint you will submit (Make sure to check if the exam wants a specific route name!)
@app.get("/dataset") 
def get_dataset():
    return EXAM_JSON_RESPONSE
