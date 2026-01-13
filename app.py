from fastapi import FastAPI
import uvicorn
import sys
import os
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.responses import Response
from fastapi.responses import JSONResponse
from textSummarizer.pipeline.prediction import PredictionPipeline



pipeline = PredictionPipeline() 
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
def predict(text: str, max_length: int = 128):
    try:
        summary = pipeline.predict(text, max_length)
        return JSONResponse({"summary": summary})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
            
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)