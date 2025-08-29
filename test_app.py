from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="Test API",
    description="测试API",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def test():
    return {"message": "Test endpoint"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
