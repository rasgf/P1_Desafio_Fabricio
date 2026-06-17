import time
from strategies import AlertContext, ConsoleAlertStrategy
import os
import requests

# Este é um Microsserviço independente (Worker)
# Ele faz polling na API (Poderia ser RabbitMQ/Kafka, mas HTTP é viável para o deploy rápido)

API_URL = os.getenv("API_URL", "http://localhost:8000/leituras")

def monitor():
    strategy = ConsoleAlertStrategy()
    alert_context = AlertContext(strategy)
    
    print("Alert Worker Iniciado...")
    while True:
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                leituras = response.json()
                for leitura in leituras:
                    if not leitura.get('postura_correta'):
                        alert_context.execute_alert(leitura['dispositivo_id'], leitura['distancia_cm'])
        except Exception as e:
            print("Erro de conexão:", e)
        
        time.sleep(10) # Verifica a cada 10 segundos

if __name__ == "__main__":
    monitor()
