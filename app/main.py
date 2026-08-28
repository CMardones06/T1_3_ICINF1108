from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.shared.schemas import ApiResponse

from app.pets.pets_controller import router as pets_router
from app.students.students_controller import router as students_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI CRUD Students & Pets",
        description=(
            "API de un CRUD en memoria para la entidad Student y sus mascotas (Pet)"
        ),
        version="1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(students_router)
    app.include_router(pets_router)

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        mensajes_traduc = {
            400: "Solicitud incorrecta",
            401: "No autorizado",
            403: "Acceso denegado",
            404: "Recurso no encontrado",
            405: "Método no permitido",
            409: "Conflicto (el recurso ya existe)"
        }

        mensaje_traducido = mensajes_traduc.get(exc.status_code, str(exc.detail))
        return JSONResponse(
            status_code=exc.status_code,
            content=ApiResponse(
                success=False,
                status_code=exc.status_code,
                message=exc.detail,
                data=None
            ).model_dump()
        )

    # @app.exception_handler(RequestValidationError)
    # async def validation_exception_handler(request: Request, exc: RequestValidationError):
    #     return JSONResponse(
    #         status_code=422,
    #         content=ApiResponse(
    #             success=False,
    #             status_code=422,
    #             message="Error de validación en los datos enviados",
    #             data=exc.errors()
    #         ).model_dump()
    #     )

    # @app.exception_handler(StarletteHTTPException)
    # async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    #     api_response = ApiResponse(
    #         success=False,
    #         status_code=exc.status_code,
    #         message=str(exc.detail),
    #         data=None
    #     )
    #     return JSONResponse(
    #         status_code=exc.status_code,
    #         content=api_response.model_dump()
    #     )

    # @app.exception_handler(RequestValidationError)
    # async def validation_exception_handler(request: Request, exc: RequestValidationError):
    #     api_response = ApiResponse(
    #         success=False,
    #         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #         message="Error de validación en los datos enviados",
    #         data=exc.errors()
    #     )
    #     return JSONResponse(
    #         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #         content=api_response.model_dump()
    #     )

    # @app.exception_handler(Exception)
    # async def global_exception_handler(request: Request, exc: Exception):
    #         return JSONResponse(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             content=ApiResponse(
    #                 success=False,
    #                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #                 message="Error interno del servidor",
    #                 data=str(exc)
    #             ).model_dump()
    #         )
    return app
app = create_app()
