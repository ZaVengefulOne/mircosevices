from app.database import engine
from app.routes import app
from app.models import Base
import uvicorn
# Initialize Database
Base.metadata.create_all(bind=engine)

# Main application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
