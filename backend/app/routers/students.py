from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import supabase

router = APIRouter(tags=["students"])


class Student(BaseModel):
    name: str
    surname: str


@router.get("/students/")
def get_students():
    try:
        students = supabase.table("students").select("*").execute()
        print(students)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return students

@router.post("/students/")
def create_student(student: Student):
    try:
        student = supabase.table("students").insert(student.model_dump()).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return student

@router.put("/students/{student_id}")
def update_student(student_id: str, student: Student):
    try:
        student = supabase.table("students").update(student.model_dump()).eq('id', student_id).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return student

@router.delete("/students/{student_id}")
def delete_student(student_id: str):
    try:
        supabase.table("students").delete().eq('id', student_id).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return { "message": "Student deleted successfully" }

# Get students for a course
@router.get("/students/course/{course_id}")
def get_students_for_course(course_id: str):
    try:
        students_courses = supabase.table("students_courses").select("*, students (name, surname)").eq('course_id', course_id).execute()
        # students = [student_course['students'] for student_course in students_courses.data]]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return students_courses

# Get students that are not in a course
@router.get("/students/not-in-course/{course_id}")
def get_students_not_in_course(course_id: str):
    try:
        students_courses = supabase.table("students_courses").select("student_id").eq('course_id', course_id).execute()
        students_ids = [student_course['student_id'] for student_course in students_courses.data]
        students = supabase.table("students").select("*").not_.in_('id', students_ids).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return students
