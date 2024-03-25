from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

docs_url = "/docs"

# app instance
app = FastAPI(
    title="API",
    description="API for my Link-tue data",
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
# app.include_router(auth, prefix=prefix_v1)


@app.get(
    "/",
    include_in_schema=False,
)
def hello_world():
    return {"body": "hello_worldå"}


handler = Mangum(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
