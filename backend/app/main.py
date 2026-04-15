from fastapi import FastAPI

app = FastAPI(title="PrimeTrade Backend API")


@app.get("/", tags=["Health"])
def read_root() -> dict:
    return {"message": "PrimeTrade backend is running"}
