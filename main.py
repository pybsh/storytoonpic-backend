import asyncio
import os

from fastapi import FastAPI, UploadFile, WebSocket
from starlette.websockets import WebSocketDisconnect

import describe
import draw
import util
from exif import get_image_metadata

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.websocket("/ws/{id}")
async def websocket_endpoint(websocket: WebSocket, id: str):
    UPLOAD_DIR = f'./photo/{id}/'
    await websocket.accept()
    if not os.path.isdir(UPLOAD_DIR):
        await websocket.close(reason="please upload images first")
        return

    file_dirs = util.get_file_paths(UPLOAD_DIR)
    try:
        while True:
            data = await websocket.receive_text()
            if data == 'process':
                await websocket.send_text("start")
                metadata = get_image_metadata(file_dirs)
                await draw.draw(file_dirs)


                # describes = describe.get_info_from_image(UPLOAD_DIR)
                # print(describes)
                await websocket.send_text("done! please send 'GET /download_photo' request")




    except WebSocketDisconnect:
        pass


@app.post("/upload_photo")
async def upload_photo(files: list[UploadFile], id: str):
    UPLOAD_DIR = f"./photo/{id}/"  # 이미지를 저장할 서버 경로

    # 이미지 저장
    file_dirs = []
    for i, file in enumerate(files):
        if file.filename.split(".")[-1].lower() not in ["jpg", "jpeg", "png"]:
            continue
        content = await file.read()
        filename = f"{str(i)}.jpg"
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_dirs.append(os.path.join(UPLOAD_DIR, filename))
        with open(os.path.join(UPLOAD_DIR, filename), "wb") as fp:
            fp.write(content)

    return {"message": f"images uploaded at {UPLOAD_DIR}"}
