from fastapi import APIRouter, File, HTTPException
from typing import Annotated
from db import supabase

router = APIRouter(tags=["files"])

@router.post("/files/")
def create_file(course_id: str, filename: str, file: Annotated[bytes, File()]):
    try:
        supabase.storage.from_("files").upload(path=course_id + "_" + filename + ".pdf", file=file, file_options={"content-type": "application/pdf"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return { "message": "File uploaded successfully" }

@router.get("/files/")
def get_files_course(course_id: str):
    try:
        files = supabase.storage.from_("files").list()
        urls = []
        for file in files:
            if file["name"].split("_")[0] != course_id:
                continue
            urls.append({
                "name": file["name"].split("_")[1].split(".")[0],
                "created_at": file["created_at"],
                "url": supabase.storage.from_('files').create_signed_url(file["name"], 3600)
            })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return urls

@router.get("/files/{filename}")
def get_file(course_id: str, filename: str):
    try:
        url = supabase.storage.from_('files').create_signed_url(course_id + "_" + filename + '.pdf', 3600)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return url

@router.delete("/files/{filename}")
def delete_file(filename: str):
    try:
        supabase.storage.from_("files").remove(filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return { "message": "File deleted successfully"}
