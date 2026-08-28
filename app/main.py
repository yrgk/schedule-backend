import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI

# Allow this file to be launched directly as well as imported as ``app.main``.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db import Base, engine
from app.schedule_router import router as schedule_router


# Updating tables
Base.metadata.create_all(bind=engine)

# Implementing app
app = FastAPI()

# Including router
app.include_router(schedule_router, prefix="/schedule", tags=["Schedule"])

# Launching app
if __name__ == '__main__':
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
