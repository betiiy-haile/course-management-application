from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import supabase

router = APIRouter(tags=["courses"])


class Course(BaseModel):
    name: str
    description: str
    professor_id: str


@router.get("/courses/")
def get_courses():
    try:
        courses = supabase.table("courses").select("*, professors (name, surname)").execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return courses

@router.get("/courses/{course_id}")
def get_course(course_id: str):
    try:
        course = supabase.table("courses").select("*, professors (name, surname)").eq('id', course_id).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return course

@router.post("/courses/")
def create_course(course: Course):
    try:
        course = supabase.table("courses").insert(course.model_dump()).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return course

@router.put("/courses/{course_id}")
def update_course(course_id: str, course: Course):
    try:
        course = supabase.table("courses").update(course.model_dump()).eq('id', course_id).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return course

@router.delete("/courses/{course_id}")
def delete_course(course_id: str):
    try:
        supabase.table("courses").delete().eq('id', course_id).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return { "message": "Course deleted successfully" }

# Get courses for a student
@router.get("/courses/student/{student_id}")
def get_courses_for_student(student_id: str):
    try:
        students_courses = supabase.table("students_courses").select("*").eq('student_id', student_id).execute()
        courses = []
        for student_course in students_courses['data']:
            course = supabase.table("courses").select("*").eq('id', student_course['course_id']).execute()
            courses.append(course['data'][0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return courses

@router.get("/courses/professor/{professor_id}")
def get_courses_for_professor(professor_id: str):
    try:
        courses = supabase.table("courses").select("*").eq('professor_id', professor_id).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return courses

# ----------------------------
# STUDENTS COURSES

class StudentCourse(BaseModel):
    student_id: str
    course_id: str


@router.post("/students-courses/")
def create_student_course(student_course: StudentCourse):
    try:
        student_course = supabase.table("students_courses").insert(student_course.model_dump()).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return student_course

@router.delete("/students-courses/{student_id}/{course_id}")
def delete_student_course(student_id: str, course_id: str):
    try:
        supabase.table("students_courses").delete().eq('student_id', student_id).eq('course_id', course_id).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return { "message": "Student course deleted successfully" }
