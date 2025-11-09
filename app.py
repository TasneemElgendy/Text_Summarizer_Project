from fastapi import FastAPI, Request
import uvicorn
import sys
import os
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.responses import Response, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from TextSummarizer.pipeline.prediction import PredictionPipeline

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=JSONResponse)
async def predict(request: Request):
    data = await request.json()
    text = data.get("text", "")
    length_percent = data.get("length_percent", 30)
    print(f"DEBUG: Received length_percent = {length_percent}")  # <<< Test

    if not text:
        return JSONResponse({"error": "No text provided"}, status_code=400)
    
    # try:
    #     # فقط للطباعة للتأكد من وصول القيمة
    #     return {"received_length_percent": length_percent, "text_length": len(text)}
    # except Exception as e:
    #     return JSONResponse({"error": str(e)}, status_code=500)
    
    try:
        pipeline = PredictionPipeline(length_percent=length_percent)
        summary = pipeline.predict(text)
        return {"summary": summary}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)    

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)

    # max_words = int(1024 * (length_percent / 100))
    # words = text.split()
    # if len(words) > max_words:
    #     text = " ".join(words[:max_words])
    # prompt = f"Summarize this text in a {tone} tone:\n{text}"
    # pipeline = PredictionPipeline()
    # summary = pipeline.predict(text)
    # return {"summary": summary}



#-----------------------------------------------------

# text:str = "What is Text Summarization? "

# app = FastAPI()

# @app.get("/", tags=["authentication"])
# async def index():
#     return RedirectResponse(url="/docs")


# @app.get("/train")
# async def training():
#     try:
#         os.system("python main.py")
#         return Response("Training successful !!")
#     except Exception as e:
#         return Response(f"Error Occurred! {e}")
    

# @app.post("/predict")
# async def predict_route(text):
#     try:
#         obj = PredictionPipeline()
#         text = obj.predict(text)
#         return text
#     except Exception as e:
#         raise e
    
