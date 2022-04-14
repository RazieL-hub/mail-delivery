from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {'message': 'hello world'}


@app.get("/")
async def test_mailer_delivery():
    return {'message': 'Mailer delivery started'}
