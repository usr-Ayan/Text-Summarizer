from fastapi import FastAPI
import uvicorn
import sys
import os
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.responses import Response
from textSummarizer.pipeline.prediction import PredictionPipeline


text:str= "What is Text Summarization? "
app = FastAPI()

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def training():
    try:
        os.system("python main.py")
        return Response(content="Training successful", media_type="text/plain")
    except Exception as e:
        return Response(content=f"Training failed due to {e}", media_type="text/plain")


@app.get("/predict")
async def predict(text: str):
    try:
        prediction_pipeline = PredictionPipeline()
        summary = prediction_pipeline.predict(text)
        return Response(content=summary, media_type="text/plain")
    except Exception as e:
        return Response(content=f"Prediction failed due to {e}", media_type="text/plain")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)