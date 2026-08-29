from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException, status

from icinf1108.app.shared.in_memory_store import InMemoryStore
from icinf1108.app.students.students_schemas import CreateStudentDto, Student, UpdateStudentDto


class StudentsService:
    def __init__(self) -> None:
        self.store: InMemoryStore[Student] = InMemoryStore()

    def find_all(self) -> list[Student]:
        return sorted(self.store.find_all(), key=lambda s: s.createdAt, reverse=True)

    def find_by_id(self, student_id: str) -> Student:
        student = self.store.get(student_id)

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estudiante no encontrado",
            )

        return student

    def create(self, data: CreateStudentDto) -> Student:
        self.assert_email_available(data.email)

        now = datetime.now()
        student = Student(
            id=str(uuid4()),
            name=data.name,
            email=data.email,
            age=data.age,
            createdAt=now,
            updatedAt=now,
        )

        self.store.set(student)
        return student

    def update(self, student_id: str, data: UpdateStudentDto) -> Student:
        existing = self.find_by_id(student_id)

        if data.email and data.email != existing.email:
            self.assert_email_available(data.email)

        updated = existing.model_copy(
            update={
                **data.model_dump(exclude_none=True),
                "updatedAt": datetime.now(),
            }
        )

        self.store.set(updated)
        return updated

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


