from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse, Response
import uvicorn
import os
from textSummarizer.pipeline.prediction import PredictionPipeline

# Initialize model once at startup
pipeline = PredictionPipeline()

app = FastAPI()


@app.get("/")
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def training():
    try:
        os.system("python main.py")
        return Response(content="Training successful", media_type="text/plain")
    except Exception as e:
        return Response(content=f"Training failed: {e}", media_type="text/plain")


@app.get("/predict")
def predict(text: str, max_length: int = 150):
    try:
        # Hard safety caps to protect the model
        MAX_UI_WORDS = 250
        max_length = min(max_length, MAX_UI_WORDS)

        summary = pipeline.predict(text, max_length)
        return JSONResponse({"summary": summary})

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
