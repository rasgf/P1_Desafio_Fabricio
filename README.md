# HoGest - Enterprise IoT Posture Monitor (P1)

## 📖 Sobre o Projeto (O Problema)
Este projeto propõe uma solução de software avançada para o monitoramento de **Postural Creep** (degradação da postura) em ambientes de trabalho e estudo. Utilizando sensores IoT (simulados via script ou integrados fisicamente via ESP-01S/Arduino), o sistema capta a distância do usuário em relação à tela e processa em tempo real a qualidade ergonômica. Se a distância cair para níveis perigosos (ex: < 10cm), alertas são acionados automaticamente.

O objetivo desta entrega é demonstrar a evolução de um MVP monolítico para uma arquitetura distribuída, resiliente e escalável de alto nível, cumprindo estritamente os requisitos acadêmicos (P1).

---

## 🎯 Atendimento aos Requisitos do Edital

### 1. Divisão em Microsserviços
A solução foi segregada em dois contêineres Docker independentes:
- **Sensor API (`sensor_api/`)**: Responsável por alta vazão. Focada apenas em receber dados do IoT, validá-los e persistir no banco de dados.
- **Alert Worker (`alert_worker/`)**: Serviço *background* que realiza sondagem assíncrona. Analisa os dados persistidos para identificar posturas incorretas e triggar eventos (Desacoplamento do fluxo principal).

### 2. Organização em Clean Architecture
A base de código `sensor_api` foi rigorosamente estruturada em camadas concêntricas, isolando a regra de negócio do Framework Web (FastAPI) e do Banco de Dados:
- `domain/`: Entidades puras (ex: `LeituraPosturaEntity`).
- `application/`: Casos de Uso com a lógica central (ex: `RegistrarLeituraUseCase`).
- `infrastructure/`: Detalhes de implementação, persistência e frameworks (SQLAlchemy, Postgree).
- `presentation/`: Controladores e rotas (FastAPI).

### 3. Princípios SOLID Aplicados
- **SRP (Single Responsibility)**: Cada classe tem uma única razão para mudar. (O Controller não salva no banco, ele delega para o UseCase).
- **OCP (Open/Closed)**: Novas estratégias de alertas podem ser criadas estendendo `IAlertStrategy` sem modificar o Worker.
- **DIP (Dependency Inversion)**: Os Casos de Uso dependem de interfaces (`ILeituraRepository`) e não de implementações concretas (`LeituraRepositoryPostgres`).

### 4. Design Patterns (Padrões de Projeto)
Foram empregados **4 Design Patterns** fundamentais:
1. **Singleton** (`database.py`): Mantém uma única conexão com o banco PostgreSQL ativa, economizando memória no container.
2. **Repository** (`repositories.py`): Isola e padroniza as operações de acesso a dados (CRUD).
3. **Factory Method** (`factories.py`): Fabrica e monta as instâncias complexas injetando dependências, como a criação do `UseCase` com seu devido `Repository`.
4. **Strategy** (`strategies.py`): Permite a troca de algoritmos de alerta (Console, E-mail, SMS) de forma dinâmica em tempo de execução no *Worker*.

### 5. TDD e BDD (Qualidade)
- **TDD (Test-Driven Development)**: A pasta `tests/` possui scripts Pytest validando a integração dos endpoints da API, provando assertivamente que o banco de dados e as respostas 201 estão corretas.
- **BDD (Behavior-Driven Development)**: O arquivo `features/posture.feature` foi escrito em Gherkin, transformando requisitos de negócio ("Dado que a distância é 5cm...") em código Python automatizado na pasta `features/steps/`.

### 6. Docker e Deploy (IaC)
- A infraestrutura está declarada no `docker-compose.yml` para execução local completa.
- O Deploy em Nuvem (Produção) foi orquestrado utilizando **Infrastructure as Code (IaC)** através do arquivo `render.yaml`. O banco PostgreSQL e os dois microsserviços estão ativos publicamente na plataforma Render.com.

---

## 🚀 Como Executar o Projeto

### A) Demonstração do Projeto Online (Já Deploiado)
1. O backend está rodando em produção na URL pública fornecida na avaliação.
2. Acesse o **Frontend** hospedado na Vercel.
3. Cole a URL da API (ex: `https://.../leituras`) no Dashboard.
4. Para simular o IoT e ver a tela ganhar vida, execute localmente o script de simulação:
   ```bash
   python mock_sensor.py
   ```
   *O script irá perguntar a URL da API. Cole-a e acompanhe os gráficos!*

### B) Rodando Localmente com Docker Compose
Para testar a orquestração completa em sua máquina:
```bash
docker-compose up --build
```
Isso subirá o PostgreSQL na porta 5432, a Sensor API na porta 8000 e o Alert Worker silenciosamente em *background*.

### C) Rodando os Testes (TDD e BDD)
Com o ambiente Python configurado e ativado:
```bash
# Rodar os testes unitários da API (TDD)
pytest

# Rodar a validação de regras de negócio em Linguagem Natural (BDD)
behave
```
