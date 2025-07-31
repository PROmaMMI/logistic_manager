from fastapi import FastAPI
from app.api.users import router as users_router
from app.api.clients import router as clients_router
from app.api.tariff_zones import router as tariff_zones_router
from app.api.orders import router as orders_router
from app.api.routes import router as routes_router
from app.api.tasks import router as tasks_router
from app.api.task_comments import router as task_comments_router
from app.api import exception_handlers
from app.services.base_crud import (
    NotFoundException, ConflictException, DatabaseException
)
import uvicorn

app = FastAPI(title="Logistics Manager API")

app.add_exception_handler(NotFoundException, exception_handlers.not_found_exception_handler)
app.add_exception_handler(ConflictException, exception_handlers.conflict_exception_handler)
app.add_exception_handler(DatabaseException, exception_handlers.database_exception_handler)
app.add_exception_handler(Exception, exception_handlers.generic_exception_handler)

app.include_router(users_router)
app.include_router(clients_router)
app.include_router(tariff_zones_router)
app.include_router(orders_router)
app.include_router(routes_router)
app.include_router(tasks_router)
app.include_router(task_comments_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)