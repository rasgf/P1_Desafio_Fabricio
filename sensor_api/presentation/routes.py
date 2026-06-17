from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from sensor_api.domain.entities import LeituraPosturaEntity
from sensor_api.infrastructure.database import DatabaseSingleton
from sensor_api.infrastructure.factories import UseCaseFactory

router = APIRouter()
db_singleton = DatabaseSingleton()

@router.post("/leituras", response_model=LeituraPosturaEntity, status_code=status.HTTP_201_CREATED)
def criar_leitura(leitura: LeituraPosturaEntity, db: Session = Depends(db_singleton.get_session)):
    use_case = UseCaseFactory.criar_registrar_leitura_use_case(db)
    return use_case.executar(leitura)

@router.get("/leituras", response_model=List[LeituraPosturaEntity])
def listar_leituras(db: Session = Depends(db_singleton.get_session)):
    from sensor_api.infrastructure.repositories import LeituraRepositoryPostgres
    repo = LeituraRepositoryPostgres(db)
    return repo.buscar_todas()
