from fastapi import FastAPI

app = FastAPI(type)


@app.post("/login")
def login():
    pass


@app.get("/activities")
def activities():
    pass
