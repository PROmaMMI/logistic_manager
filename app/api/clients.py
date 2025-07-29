from app.schemas.client import ClientRead, ClientCreate, ClientUpdate
from app.services.client_service import ClientService
from app.api.base_router import CRUDRouter
from app.db.models import Client
client_service = ClientService()

class ClientRouter(CRUDRouter[Client, ClientRead, ClientCreate, ClientUpdate, ClientService]):
    def __init__(self):
        super().__init__(
            prefix="/clients",
            tags=["Clients"],
            service=client_service,
            read_schema=ClientRead,
            create_schema=ClientCreate,
            update_schema=ClientUpdate,
        )

router = ClientRouter().router