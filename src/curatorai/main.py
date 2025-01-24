import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logfire

from curatorai.utils.clarifying_questions import Clarifyingrouter
from curatorai.utils.detail_extraction import detail_router
from curatorai.core.curator import Curator

app = FastAPI(title="Curator AI Backend")

# Enable CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(Curator)
# Include the router from clarifying_questions.py
app.include_router(Clarifyingrouter)
# Include the router from detail_extraction.py
app.include_router(detail_router)

logfire.instrument_fastapi(app)
logfire.configure(pydantic_plugin=logfire.PydanticPlugin(record="all"))

@app.get("/")
async def root():
    return {"message": "API Root"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", default=5000)), log_level="info")
