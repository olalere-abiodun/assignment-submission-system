from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import schemas, model
from typing import Optional

#User CRUD
# ==========================================================
# Create User
def Sign_up(db: Session, user: schemas.UserCreate, hashed_password: str):
   db_user = model.Users (
        full_name = user.full_name,
        email = user.email,
        username = user.username,
        hashed_password = hashed_password,
        role = user.role
   )
   db.add(db_user)
   db.commit()
   db.refresh(db_user)
   return db_user

# Get User by Email
def check_email(db: Session, email:str):
   return db.query(model.Users).filter(model.Users.email == email).first()

# Check for Username Exist
def check_username(db: Session, username:str):
   return db.query(model.Users).filter(model.Users.username == username).first()

#Edit User Profile
def UpdateUser(db: Session, email:str, updateUser: schemas.UserUpdate):
   user = db.query(model.Users).filter(model.Users.email==email).first()
   if not user:
      raise HTTPException(status_code=404, detail="User Not Found")
   
   user.username = updateUser.username
   user.full_name = updateUser.full_name
   user.email = updateUser.email

   db.commit()
   db.refresh(user)

   return user

# Course Crud 
# =============================================================
# Create Course 
def create_new_course(db: Session, course: schemas.RegisterCourse, lecturer_id: int):
    db_course = model.Course(
        course_name=course.course_name,
        course_code=course.course_code,
        description=course.description,
        lecturer_id=lecturer_id
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

# Get All Courses
def get_all_courses(db: Session):
    return db.query(model.Course).all()
# Get Course by ID
def get_course_by_id(db: Session, course_id: int):
    return db.query(model.Course).filter(model.Course.course_id == course_id).first()
 
# Get course by course code 
def get_course_by_code(db: Session, course_code: str):
    return db.query(model.Course).filter(model.Course.course_code == course_code).first()

# Update Course by ID
def update_course(db: Session, course_id: int, course_update: schemas.CourseUpdate):
      db_course = db.query(model.Course).filter(model.Course.course_id == course_id).first()
      if not db_course:
         raise HTTPException(status_code=404, detail="Course not found")
      db_course.course_name = course_update.course_name if course_update.course_name else db_course.course_name
      db_course.course_code = course_update.course_code if course_update.course_code else db_course.course_code
      db_course.description = course_update.description if course_update.description else db_course.description
      
      db.commit()
      db.refresh(db_course)
      return db_course

# Update course by course code
def update_course_by_code(db: Session, course_code: str, course_update: schemas.CourseUpdate):
    db_course = db.query(model.Course).filter(model.Course.course_code == course_code).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    db_course.course_name = course_update.course_name if course_update.course_name else db_course.course_name
    db_course.course_code = course_update.course_code if course_update.course_code else db_course.course_code
    db_course.description = course_update.description if course_update.description else db_course.description
    
    db.commit()
    db.refresh(db_course)
    return db_course

#Enroll in a course
def new_enroll(db: Session, user_id: int, course_id: int):
   db_enroll = model.Enrollment (
      user_id = user_id,
      course_id = course_id

   )
   db.add(db_enroll)
   db.commit()
   db.refresh(db_enroll)
   return db_enroll

# Get Enrollments by User ID
def get_enrollments_by_user_id(db: Session, user_id: int):
    return db.query(model.Enrollment).filter(model.Enrollment.user_id == user_id).all()

# Unenroll from a course
def unenroll_from_course(db: Session, user_id: int, course_id: int):
    enrollment = db.query(model.Enrollment).filter(
        model.Enrollment.user_id == user_id,
        model.Enrollment.course_id == course_id
    ).first()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    db.delete(enrollment)
    db.commit()
    return {"message": "Unenrolled successfully"}

#Assignment CRUD
# =============================================================
# Create Assignment Instructor only
def create_assignment(db: Session, assignment: schemas.AssignmentCreate, lecturer_id: int):
      db_assignment = model.Assignment(
            course_id=assignment.course_id,
            lecturer_id=lecturer_id,
            assignment_title=assignment.assignment_title,
            description=assignment.description,
            due_date=assignment.due_date
      )
      db.add(db_assignment)
      db.commit()
      db.refresh(db_assignment)
      return db_assignment

# Get Assignment by ID
def get_assignment_by_id(db: Session, assignment_id: int):
    return db.query(model.Assignment).filter(model.Assignment.assignment_id == assignment_id).first()

def update_assignment(db: Session, assignment_id: int, assignment_update: schemas.AssignmentUpdate):
    db_assignment = db.query(model.Assignment).filter(model.Assignment.assignment_id == assignment_id).first()
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    db_assignment.assignment_title = assignment_update.assignment_title if assignment_update.assignment_title else db_assignment.assignment_title
    db_assignment.description = assignment_update.description if assignment_update.description else db_assignment.description
    db_assignment.due_date = assignment_update.due_date if assignment_update.due_date else db_assignment.due_date
    
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

# delete assignment 
def delete_assignment(db: Session, assignment_id: int):
    db_assignment = db.query(model.Assignment).filter(model.Assignment.assignment_id == assignment_id).first()
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found") 
    db.delete(db_assignment)
    db.commit()
    return {"message": "Assignment deleted successfully"}

# Get all assignments for a course
def get_assignments_by_course_id(db: Session, course_id: int):
    return db.query(model.Assignment).filter(model.Assignment.course_id == course_id).all()

# Submission CRUD
# =============================================================
# Check if student is enrolled in the course before submitting an assignment
def is_student_enrolled(db: Session, student_id: int, course_id: int):
    return db.query(model.Enrollment).filter(
        model.Enrollment.user_id == student_id,
        model.Enrollment.course_id == course_id
    ).first() is not None

# Check if student already submitted the assignment 
def has_student_submitted(db: Session, student_id: int, assignment_id: int):
    return db.query(model.Submission).filter(
        model.Submission.user_id == student_id,
        model.Submission.assignment_id == assignment_id
    ).first() is not None

# helper function to get course_id from assignment_id 
def get_course_id_by_assignment(db: Session, assignment_id: int) -> Optional[int]:
    assignment = db.query(model.Assignment).filter(model.Assignment.assignment_id == assignment_id).first()
    return assignment.course_id if assignment else None


# Submit an Submission

def create_submission(db: Session, submission: schemas.SubmissionCreate, student_id: int):
    db_submission = model.Submission(
        assignment_id=submission.assignment_id,
        user_id=student_id,
        content=submission.content,
        file_url=submission.file_url,
        submission_date=submission.submission_date
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission

# Get all submissions for an assignment
def get_all_assignment_submissions(db: Session, assignment_id: int):
    return db.query(model.Submission).filter(model.Submission.assignment_id == assignment_id).all() 

# Get submissions by student 
def get_submission_by_student(db: Session, student_id: int):
    return db.query(model.Submission).filter(model.Submission.user_id == student_id).all()

# Get submission by a student for a specific assignment 
def get_submission_by_student_and_assignment(db: Session, student_id: int, assignment_id: int):
    return db.query(model.Submission).filter(
        model.Submission.user_id == student_id,
        model.Submission.assignment_id == assignment_id
    ).first()
    