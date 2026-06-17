from pydantic import BaseModel, Field

# Entity (Clean Architecture)
class LeituraPosturaEntity(BaseModel):
    dispositivo_id: str = Field(..., min_length=1)
    distancia_cm: float = Field(..., gt=0)
    tempo_duracao: int = 0
    postura_correta: bool = True
