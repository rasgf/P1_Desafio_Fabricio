import time
import os
import requests
import threading
from strategies import AlertContext, ConsoleAlertStrategy
from http.server import BaseHTTPRequestHandler, HTTPServer

API_URL = os.getenv("API_URL", "http://localhost:8000/leituras")
PORT = int(os.getenv("PORT", 8080))

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
        time.sleep(10)

class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Worker is alive")

if __name__ == "__main__":
    # Roda o monitor em uma thread separada
    t = threading.Thread(target=monitor, daemon=True)
    t.start()
    
    # Roda um servidor web fake apenas para o Render achar que e um Web Service e dar o plano Gratis
    server = HTTPServer(("0.0.0.0", PORT), DummyHandler)
    server.serve_forever()
