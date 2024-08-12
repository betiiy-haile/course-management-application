from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import students, professors, courses, files

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def test():
    return {"Hello": "World"}

app.include_router(students.router)
app.include_router(professors.router)
app.include_router(courses.router)
app.include_router(files.router)
