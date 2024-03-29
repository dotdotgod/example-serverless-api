from fastapi import FastAPI
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware

from api.v1.auth.auth_router import auth

docs_url = "/docs"

app = FastAPI(
    title="API",
    description="API for my Example data",
    version="1.0",
    terms_of_service="/",
    docs_url=docs_url,
    redoc_url=None,
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

prefix_v1 = "/api/v1"

# auth router
app.include_router(auth, prefix=prefix_v1)


@app.get("/", include_in_schema=False)
def hello_world():
    return {"body": "hello_world"}


handler = Mangum(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
