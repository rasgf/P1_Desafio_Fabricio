from abc import ABC, abstractmethod

# Strategy Pattern (SOLID: Open/Closed Principle)
class IAlertStrategy(ABC):
    @abstractmethod
    def send_alert(self, dispositivo_id: str, distancia: float) -> str:
        pass

class EmailAlertStrategy(IAlertStrategy):
    def send_alert(self, dispositivo_id: str, distancia: float) -> str:
        # Lógica fingindo envio de e-mail
        return f"EMAIL ENVIADO: O dispositivo {dispositivo_id} está com postura perigosa ({distancia}cm)."

class ConsoleAlertStrategy(IAlertStrategy):
    def send_alert(self, dispositivo_id: str, distancia: float) -> str:
        msg = f"[ALERTA LOG] POSTURA RUIM DETECTADA: {dispositivo_id} a {distancia}cm."
        print(msg)
        return msg

class AlertContext:
    def __init__(self, strategy: IAlertStrategy):
        self._strategy = strategy

    def execute_alert(self, dispositivo_id: str, distancia: float):
        return self._strategy.send_alert(dispositivo_id, distancia)
