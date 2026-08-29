from fastapi import APIRouter

from app.pets.pets_schemas import CreatePetDto, Pet, UpdatePetDto
from app.pets.pets_service import pets_service

router = APIRouter(
    prefix="/api/students/{studentId}/pets",
    tags=["Pets"],
)


@router.get("")
def find_all(studentId: str) -> list[Pet]:
    return pets_service.find_all_for_student(studentId)


@router.post("", status_code=201, response_model=ApiResponse[Pet])
def create(studentId: str, body: CreatePetDto) -> ApiResponse[Pet]:
    new_pet = pets_service.create(studentId, body)
    
    return ApiResponse(
        success=True,
        status_code=201,
        message=f"Mascota '{new_pet.name}' registrada exitosamente",
        data=new_pet,
    )

@router.patch("/{petId}")
def update(studentId: str, petId: str, body: UpdatePetDto) -> Pet:
    return pets_service.update(studentId, petId, body)


@router.delete("/{petId}")
def delete(studentId: str, petId: str) -> Pet:
    return pets_service.delete(studentId, petId)
