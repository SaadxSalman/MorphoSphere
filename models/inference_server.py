from fastapi import FastAPI
app = FastAPI()

@app.post("/predict")
async def predict(image_data: dict):
    # Here you would call Gemma-3 or your Vision Model
    return {"action": "move_forward", "confidence": 0.98}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, ho st="0.0.0.0", port=8000)