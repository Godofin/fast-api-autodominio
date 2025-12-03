from app.routes.users import router as users_router
from app.routes.instructor_profiles import router as instructor_profiles_router
from app.routes.instructor_availability import router as instructor_availability_router
from app.routes.appointments import router as appointments_router
from app.routes.instructor_time_off import router as instructor_time_off_router
from app.routes.reviews import router as reviews_router
from app.routes.instructor_approval import router as instructor_approval_router
from app.routes.uploads import router as uploads_router

__all__ = [
    "users_router",
    "instructor_profiles_router",
    "instructor_availability_router",
    "appointments_router",
    "instructor_time_off_router",
    "reviews_router",
    "instructor_approval_router",
    "uploads_router"
]
