from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.instructor_profile import InstructorProfileCreate, InstructorProfileUpdate, InstructorProfileResponse
from app.schemas.instructor_availability import InstructorAvailabilityCreate, InstructorAvailabilityUpdate, InstructorAvailabilityResponse
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentResponse
from app.schemas.instructor_time_off import InstructorTimeOffCreate, InstructorTimeOffUpdate, InstructorTimeOffResponse
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse, InstructorRatingStats
from app.schemas.instructor_document import InstructorDocumentCreate, InstructorDocumentResponse
from app.schemas.instructor_approval import InstructorApprovalUpdate

__all__ = [
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "InstructorProfileCreate",
    "InstructorProfileUpdate",
    "InstructorProfileResponse",
    "InstructorAvailabilityCreate",
    "InstructorAvailabilityUpdate",
    "InstructorAvailabilityResponse",
    "AppointmentCreate",
    "AppointmentUpdate",
    "AppointmentResponse",
    "InstructorTimeOffCreate",
    "InstructorTimeOffUpdate",
    "InstructorTimeOffResponse",
    "ReviewCreate",
    "ReviewUpdate",
    "ReviewResponse",
    "InstructorRatingStats",
    "InstructorDocumentCreate",
    "InstructorDocumentResponse",
    "InstructorApprovalUpdate"
]
