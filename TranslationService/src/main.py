from typing import Union, Annotated

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
import translator

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home():
    html_content = """
        <body>
        <form action="/files/" enctype="multipart/form-data" method="post">
            <input name="files" type="file" multiple />
            <input type="submit" />
        </form>
        <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
            <input name="files" type="file" multiple />
            <input type="submit" />
        </form>
        </body>"""
    
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    for file in files:
        if file.content_type == "audio/wav":
            content = await file.read()
            translator.predict_S2ST(audio_input=content, target_language='English')
        else:
            raise HTTPException(status_code=415, detail="A audio/wav file is required, but a {} file was uploaded".format(file.content_type))
    return {"filename": file.filename}