import uvicorn, logging.config
from app.core.config import LOGGING_CONFIG
from app import create_app

app = create_app()

logging.config.dictConfig(LOGGING_CONFIG)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)