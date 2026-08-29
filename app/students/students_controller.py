from fastapi import APIRouter

from app.pets.pets_service import pets_service
from app.students.students_schemas import CreateStudentDto, Student, UpdateStudentDto
from app.students.students_service import students_service

router = APIRouter(prefix="/api/students", tags=["Students"])


@router.get("")
def find_all() -> list[Student]:
    return students_service.find_all()


@router.get("/{student_id}")
def find_by_id(student_id: str) -> Student:
    return students_service.find_by_id(student_id)


@router.post("", status_code=201)
def create(body: CreateStudentDto) -> Student:
    return students_service.create(body)


@router.patch("/{student_id}")
def update(student_id: str, body: UpdateStudentDto) -> Student:
    return students_service.update(student_id, body)


# Modificiación de funciones delete y assert_email_available
# Primero se define un endpoint en la ruta de student_id
@router.delete("/{student_id}") 
def delete(student_id: str) -> ApiResponse[Student]: # recibe como parametro student_id y se indica que se va a retornar un objeto ApiResponse  
    deleted = students_service.delete(student_id)    # servicio busca y elimina
    pets_service.delete_all_for_student(student_id)  # usa mismo id de estudiante para buscar mascotas vinculadas y eliminarlas

# Usamos estandarizadamente ApiResponse() para cada respuesta
# cada vez con exactamente cuatro atributos
    return ApiResponse(
        success     = True,
        status_code = status.HTTP_200_OK, # Todo ok
        message     = "Estudiante y mascopas vinculadas fueron eliminados correctamente",
        data        = deleted             # estudiante eliminado
    )

