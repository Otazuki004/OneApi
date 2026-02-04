from . import app


@app.get("/")
async def home():
    return {"status": "ok", "message": "Welcome to OneApi!"}

if __name__ == "__main__":
    from OneApi.routes import loader
    loader.load_modules_from_folder("OneApi/routes")
