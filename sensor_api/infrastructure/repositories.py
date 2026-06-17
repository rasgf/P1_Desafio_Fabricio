from typing import List
from sqlalchemy.orm import Session
from sensor_api.domain.entities import LeituraPosturaEntity
from sensor_api.application.use_cases import ILeituraRepository
from sensor_api.infrastructure.database import LeituraModel

# Repository Pattern
class LeituraRepositoryPostgres(ILeituraRepository):
    def __init__(self, session: Session):
        self.session = session
        
    def salvar(self, leitura: LeituraPosturaEntity) -> LeituraPosturaEntity:
        db_leitura = LeituraModel(
            dispositivo_id=leitura.dispositivo_id,
            distancia_cm=leitura.distancia_cm,
            tempo_duracao=leitura.tempo_duracao,
            postura_correta=leitura.postura_correta
        )
        self.session.add(db_leitura)
        self.session.commit()
        self.session.refresh(db_leitura)
        return leitura
        
    def buscar_todas(self) -> List[LeituraPosturaEntity]:
        db_leituras = self.session.query(LeituraModel).all()
        return [
            LeituraPosturaEntity(
                dispositivo_id=l.dispositivo_id,
                distancia_cm=l.distancia_cm,
                tempo_duracao=l.tempo_duracao,
                postura_correta=l.postura_correta
            ) for l in db_leituras
        ]
