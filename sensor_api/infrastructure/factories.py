from sqlalchemy.orm import Session
from sensor_api.infrastructure.repositories import LeituraRepositoryPostgres
from sensor_api.application.use_cases import RegistrarLeituraUseCase

# Factory Pattern
class UseCaseFactory:
    @staticmethod
    def criar_registrar_leitura_use_case(session: Session) -> RegistrarLeituraUseCase:
        # Injeção de dependência manual (Factory)
        repository = LeituraRepositoryPostgres(session)
        return RegistrarLeituraUseCase(repository)
