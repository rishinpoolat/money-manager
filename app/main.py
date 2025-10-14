from fastapi import FastAPI


app = FastAPI(title="Money Manager API")


@app.get("/")
def read_root():
    return {"message": "Money Manager API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


