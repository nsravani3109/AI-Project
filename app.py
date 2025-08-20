from fastapi import FastAPI

app = FastAPI()

@app.get("/validate_mc/{mcid}")
def validate_mc(mcid: str):
    if mcid.isdigit():
        return {"mcid": mcid, "valid": True}
    else:
        return {"mcid": mcid, "valid": False}