import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class LeituraModel(Base):
    __tablename__ = "leituras"
    id = Column(Integer, primary_key=True, index=True)
    dispositivo_id = Column(String, nullable=False)
    distancia_cm = Column(Float, nullable=False)
    tempo_duracao = Column(Integer, default=0)
    postura_correta = Column(Boolean, default=True)

# Singleton Pattern para a Engine do Banco
class DatabaseSingleton:
    _instance = None
    _engine = None
    _session_maker = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseSingleton, cls).__new__(cls)
            database_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/iotdb")
            cls._engine = create_engine(database_url)
            cls._session_maker = sessionmaker(autocommit=False, autoflush=False, bind=cls._engine)
        return cls._instance

    def get_session(self):
        db = self._session_maker()
        try:
            yield db
        finally:
            db.close()
    
    def create_tables(self):
        Base.metadata.create_all(bind=self._engine)
