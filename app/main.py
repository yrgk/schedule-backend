import uvicorn
from fastapi import FastAPI

from app.db import Base, engine
from app.score_router import router as score_router
from app.schedule_router import router as schedule_router


# Updating tables
Base.metadata.create_all(bind=engine)

# Implementing app
app = FastAPI()

# Including routers
app.include_router(schedule_router, prefix="/schedule", tags=["Schedule"])
app.include_router(score_router, prefix="/score", tags=["Score"])

# Launching app
if __name__ == '__main__':
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
