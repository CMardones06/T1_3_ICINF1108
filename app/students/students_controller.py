from fastapi import APIRouter
from fastapi import status

from app.pets.pets_service import pets_service
from app.students.students_schemas import CreateStudentDto, Student, UpdateStudentDto
from app.students.students_service import students_service
#Clase estandarizada
from app.shared.schemas import ApiResponse

router = APIRouter(prefix="/api/students", tags=["Students"])


@router.get("")
def find_all() -> ApiResponse[list[Student]]:
    data = students_service.find_all()
    return ApiResponse(
        success=True,
        status_code=status.HTTP_200_OK,
        message="Lista de estudiantes obtenida exitosamente!",
        data=data
    )

@router.get("/{student_id}")
def find_by_id(student_id: str) -> ApiResponse[Student]:
    data=students_service.find_by_id(student_id)
    return ApiResponse(
        success=True,
        status_code=status.HTTP_200_OK,
        message="Estudiante encontrado!",
        data=data
    )

@router.post("", status_code=status.HTTP_201_CREATED)
def create(body: CreateStudentDto) -> ApiResponse[Student]:
    data=students_service.create(body)
    return ApiResponse(
        success=True,
        status_code=status.HTTP_201_CREATED,
        message="Estudiante creado exitosamente!!",
        data=data
    )

@router.patch("/{student_id}")
def update(student_id: str, body: UpdateStudentDto) -> ApiResponse[Student]:
    data=students_service.update(student_id, body)
    return ApiResponse(
        success=True,
        status_code=status.HTTP_200_OK,
        message="Estudiante fue actualizado correctamente",
        data=data
    )


@router.delete("/{student_id}")
def delete(student_id: str) -> ApiResponse[Student]:
    deleted = students_service.delete(student_id)
    pets_service.delete_all_for_student(student_id)

    return ApiResponse(
        success=True,
        status_code=status.HTTP_200_OK,
        message="Estudiante y mascotas vinculadas fueron eliminadas correctamente",
        data=deleted
    )
