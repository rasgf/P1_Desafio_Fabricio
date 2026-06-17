Feature: Avaliação da Postura do Usuário

  Scenario: Usuário está muito perto da tela
    Given que a distância medida pelo sensor é de 5 centímetros
    When a leitura é processada pela regra de negócio
    Then o sistema deve classificar a postura como incorreta
    And a estratégia de alerta deve gerar a mensagem "POSTURA RUIM DETECTADA"
