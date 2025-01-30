from fastapi import FastAPI


app = FastAPI()

match_logs = []

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/match_log")
def add_match_log(match_log):
    match_logs.append(match_log)
    return match_logs

@app.post("/reset_match_log")
def add_match_log():
    match_logs.clear()
    return match_logs