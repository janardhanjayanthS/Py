from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def home() -> dict[str, str]:
    """
    Home route

    Returns:
        dict[str, str]: json response
    """
    return {'hello': 'world'}
