import uvicorn
from fastapi import FastAPI
from clarifying_questions import Clarifyingrouter
from detail_extraction import detail_router
from curator_new import curator_new
import logfire
import os

app = FastAPI(title="Curator AI Backend")

app.include_router(curator_new)
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
    uvicorn.run("main:app", host="0.0.0.0", port=os.getenv("PORT", default=5000), log_level="info")
    # Enable CORS middleware
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )



