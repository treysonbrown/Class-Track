from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select

from database import get_db
from models import Course, Instructor, Student
from schemas import CreateCourseRequest, CreateInstructorRequest, CreateStudentRequest, AddStudentToCourseRequest

app = FastAPI()




### GET ###

@app.get("/students")
async def get_students(db: Session = Depends(get_db)) -> list[Student]:
    return db.exec(select(Student)).all()

@app.get("/instructors")
async def get_instructors(db: Session = Depends(get_db)) -> list[Instructor]:
    return db.exec(select(Instructor)).all()

@app.get("/courses")
async def get_courses(db: Session = Depends(get_db)) -> list[Course]:
    return db.exec(select(Course)).all()

@app.get("/courses/{course_id}/students")
async def get_course_student_list(course_id: int, db: Session = Depends(get_db)) -> list[Student]:
    course: Course | None = db.get(Course, course_id)
    if course == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with ID {course_id} was not found")
    return course.students



### POST ###

@app.post("/students", status_code=status.HTTP_201_CREATED)
async def create_student(create_student_request: CreateStudentRequest, db: Session = Depends(get_db)) -> int:
    student: Student = Student(name=create_student_request.name)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student.id

@app.post("/instructors", status_code=status.HTTP_201_CREATED)
async def create_instructor(create_instructor_request: CreateInstructorRequest, db: Session = Depends(get_db)) -> int:
    instructor: Instructor = Instructor(name=create_instructor_request.name)
    db.add(instructor)
    db.commit()
    db.refresh(instructor)
    return instructor.id


@app.post("/courses", status_code=status.HTTP_201_CREATED)
async def create_course(create_course_request: CreateCourseRequest, db: Session = Depends(get_db)) -> int:
    instructor: Instructor | None = db.get(Instructor, create_course_request.instructor_id)
    if instructor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Instructor with ID {create_course_request.instructor_id} was not found")

    course: Course = Course(**create_course_request.model_dump())

    db.add(course)
    db.commit()
    db.refresh(course)
    return course.id

@app.post("/courses/{course_id}/students")
async def add_student_to_course(course_id: int, request: AddStudentToCourseRequest, db: Session = Depends(get_db)) -> ???:

    student: Student | None = db.get(Student, request.student_id)

    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with ID {request.student_id} was not found")

    course: Course | None = db.get(Course, request.student_id)

    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with ID {course_id} was not found")
    

    if student in course.students:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Student with ID {request.student_id} is already in the course")

    course.students.append(student)
    db.commit()
    db.refresh(course)

    for student in course.students:
        print(student.name)








