import os
from fastapi import FastAPI, File, Response, UploadFile, status, Form
import uvicorn
import aiofiles
from typing import List
from src.storage import MinioTransactions
from minio import Minio
from src.helpertools import Tools

description = """
This is a simple open source application that helps to store data securely on the server.

For suggestions and contributions, please visit [github.com/sagnik-sudo/Serverive](https://github.com/sagnik-sudo/Serverive/issues)

If you like my work, please star it on [github.com/sagnik-sudo/Serverive](https://github.com/sagnik-sudo/Serverive)
"""

app = FastAPI(
    title="Serverive",
    description=description,
    version="Beta",
    docs_url="/serverive",
    redoc_url="/serverive/redoc",
    contact={
        "name": "Developer - Sagnik Das",
        "email": "sagnikdas2305@gmail.com",
    },
)

tools = Tools()
minio = MinioTransactions()


@app.post("/upload", tags=["Serverive Transfers"], summary="Uploads multiple files to the server")
async def upload(directory: str, files: List[UploadFile] = File(...), response: Response = Response()):
    try:
        tempdir = tools.get_temp_dir()
        for file in files:
            destination_file_path = os.path.join(tempdir, file.filename)
            async with aiofiles.open(destination_file_path, 'wb') as out_file:
                # async read file chunk
                while content := await file.read(1024):
                    await out_file.write(content)  # async write file chunk
        paths = [os.path.join(tempdir, file.filename) for file in files]
        if minio.bucketExists(directory):
            for i in range(len(paths)):
                minio.uploadFile(directory, paths[i], files[i].filename)
                tools.delete_tempfile(paths[i])
            return {"Success": "Files uploaded successfully"}
        else:
            minio.createBucket(directory)
            for i in range(len(paths)):
                minio.uploadFile(directory, paths[i], files[i].filename)
                tools.delete_tempfile(paths[i])
            return {"Success": "Files uploaded successfully"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Error": str(e)}


@app.get("/download", tags=["Serverive Viewer"], summary="Downloads a file from the server")
async def download(directory: str, filename: str, response: Response = Response()):
    try:
        if minio.bucketExists(directory):
            obj = minio.downloadFile(directory, filename)
            if obj != None:
                response.status_code = status.HTTP_200_OK
                return obj
            else:
                response.status_code = status.HTTP_404_NOT_FOUND
                return {"Error": "File not found"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Error": str(e)}


@app.delete("/delete", tags=["Serverive Transfers"], summary="Deletes a file from the server")
async def delete(directory: str, filename: str, response: Response = Response()):
    try:
        if minio.bucketExists(directory):
            minio.deleteFile(directory, filename)
            response.status_code = status.HTTP_200_OK
            return {"Success": "File deleted successfully"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Error": str(e)}


@app.delete("/removedir", tags=["Serverive Transfers"], summary="Deletes a directory from the server")
async def delete_directory(directory: str, response: Response = Response()):
    try:
        if minio.bucketExists(directory):
            minio.deleteBucket(directory)
            response.status_code = status.HTTP_200_OK
            return {"Success": "Directory deleted successfully"}
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"Error": "Directory not found"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Error": str(e)}


@app.post("/create", tags=["Serverive Transfers"], summary="Creates a directory on the server")
async def create_directory(directory: str, response: Response = Response()):
    try:
        if minio.bucketExists(directory):
            response.status_code = status.HTTP_200_OK
            return {"Success": "Directory already exists"}
        else:
            minio.createBucket(directory)
            response.status_code = status.HTTP_200_OK
            return {"Success": "Directory created successfully"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Error": str(e)}


@app.get("/list", tags=["Serverive Viewer"], summary="Lists all the files in the server")
async def list_files(directory: str, response: Response = Response()):
    try:
        if minio.bucketExists(directory):
            response.status_code = status.HTTP_200_OK
            return minio.listObjects(directory)
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"Error": "Directory not found"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Error": str(e)}


@app.get("/listdir", tags=["Serverive Viewer"], summary="Lists all the directories in the server")
async def list_directories(response: Response = Response()):
    try:
        response.status_code = status.HTTP_200_OK
        return minio.listBuckets()
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Error": str(e)}


@app.put("/minioconfig", tags=["Configuration"], summary="Updates the minio configuration for this session")
async def update_minio_config(username: str = Form(), password: str = Form(), endpoint: str = Form(), response: Response = Response()):
    try:
        minio.minioClient = Minio(endpoint,
                                  access_key=username,
                                  secret_key=password,
                                  secure=False)
        response.status_code = status.HTTP_200_OK
        return {"Success": "Configuration updated successfully"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7777)
