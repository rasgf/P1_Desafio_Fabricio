from abc import ABC, abstractmethod
from typing import List
from sensor_api.domain.entities import LeituraPosturaEntity

# Interface do Repositório (Princípio de Inversão de Dependência do SOLID)
class ILeituraRepository(ABC):
    @abstractmethod
    def salvar(self, leitura: LeituraPosturaEntity) -> LeituraPosturaEntity:
        pass
    
    @abstractmethod
    def buscar_todas(self) -> List[LeituraPosturaEntity]:
        pass

# Caso de Uso (Application Layer)
class RegistrarLeituraUseCase:
    def __init__(self, repository: ILeituraRepository):
        self.repository = repository
        
    def executar(self, leitura: LeituraPosturaEntity) -> LeituraPosturaEntity:
        # Regra de negócio: Se a distância for menor que 10cm, postura incorreta
        if leitura.distancia_cm < 10.0:
            leitura.postura_correta = False
        else:
            leitura.postura_correta = True
            
        return self.repository.salvar(leitura)
