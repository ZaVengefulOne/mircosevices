import uvicorn
from fastapi import FastAPI
from app.database import engine
from app.routes import router
from app.models import Base

# Initialize Database
Base.metadata.create_all(bind=engine)

# FastAPI App
app = FastAPI()

# Include routes
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8800)