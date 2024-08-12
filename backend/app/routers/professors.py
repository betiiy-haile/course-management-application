from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import supabase

router = APIRouter(tags=["professors"])

class Professor(BaseModel):
    name: str
    surname: str


@router.get("/professors/")
def get_professors():
    try:
        professors = supabase.table("professors").select("*").execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return professors

@router.post("/professors/")
def create_professor(professor: Professor):
    try:
        professor = supabase.table("professors").insert(professor.model_dump()).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return professor

@router.put("/professors/{professor_id}")
def update_professor(professor_id: str, professor: Professor):
    try:
        professor = supabase.table("professors").update(professor.model_dump()).eq('id', professor_id).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return professor

@router.delete("/professors/{professor_id}")
def delete_professor(professor_id: str):
    try:
        supabase.table("professors").delete().eq('id', professor_id).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return { "message": "Professor deleted successfully" }
