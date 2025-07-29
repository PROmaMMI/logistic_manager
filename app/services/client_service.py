from app.db.models import Client
from app.schemas.client import ClientCreate, ClientUpdate
from app.services.base_crud import CRUDService

class ClientService(CRUDService[Client, ClientCreate, ClientUpdate]):
    def __init__(self):
        super().__init__(Client)