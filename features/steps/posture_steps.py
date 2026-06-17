from behave import given, when, then
from sensor_api.domain.entities import LeituraPosturaEntity
from sensor_api.application.use_cases import RegistrarLeituraUseCase, ILeituraRepository
from alert_worker.strategies import ConsoleAlertStrategy

# Mock Repository para o BDD
class MockRepo(ILeituraRepository):
    def salvar(self, leitura):
        return leitura
    def buscar_todas(self):
        return []

@given('que a distância medida pelo sensor é de {distancia} centímetros')
def step_impl_given(context, distancia):
    context.leitura = LeituraPosturaEntity(dispositivo_id="BDD-TEST", distancia_cm=float(distancia))

@when('a leitura é processada pela regra de negócio')
def step_impl_when(context):
    use_case = RegistrarLeituraUseCase(MockRepo())
    context.resultado = use_case.executar(context.leitura)

@then('o sistema deve classificar a postura como incorreta')
def step_impl_then_posture(context):
    assert context.resultado.postura_correta is False

@then('a estratégia de alerta deve gerar a mensagem "{mensagem_esperada}"')
def step_impl_then_alert(context, mensagem_esperada):
    strategy = ConsoleAlertStrategy()
    msg = strategy.send_alert(context.resultado.dispositivo_id, context.resultado.distancia_cm)
    assert mensagem_esperada in msg
