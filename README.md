# gerencia_fluxo_pacientes_ubs

# Título: Sistema de Gestão de Fluxo de Pacientes para UBS

Este projeto experimental é um tarefa da Disciplina de Prompts, ministrada pelo Profº Dr. Sanderson de Macedo, do Curso de Especialização de Sistemas e Agentes Inteligentes da Universidade Federal de Goiás. 
Ele foi concebido para auxiliar o fluxo de pacientes, em uma Unidade Básica de Saúde - U.B.S., que abrange as etapas de recepção, triagem e atendimento clínico.
O referido projeto usa como validação de dados e integração com a API da OpenAI para suporte dinâmico durante o atendimento.

## Equipe de desenvolvimento
   Billy Fádel.
   
   Edson Laranjeiras.
   
   Samantha Adiely.

## Funcionalidades
### 1. Administrativo (Recepção)

    Coleta dados pessoais do paciente, como:
        Nome, data de nascimento, sexo, CPF, telefone e número do cartão SUS.
    Anonimização: O CPF é anonimizado antes de ser armazenado, garantindo privacidade.
    Exemplo de anonimização:

anonimizar_cpf("123.456.789-00")  # Saída: anon-12345

### 2. Triagem

    Registra informações de saúde, incluindo:
        Queixa principal.
        Validação dos sinais vitais com o Pydantic, garantindo que os valores estejam dentro dos parâmetros clínicos aceitáveis:
            Pressão arterial (80 a 200 mmHg).
            Temperatura corporal (35 a 42 °C).
            Oxigenação (85% a 100%).
            Escala de dor (1 a 5).
    Integração com o modelo GPT-3.5-Turbo para análise da triagem e sugestões de conduta baseadas nos sinais vitais e informações do paciente.

### 3. Especialista

    Registra as observações do especialista, incluindo:
        Sinais observados.
        Sintomas relatados.
        Medicamentos prescritos.
        Exames solicitados.

### 4. Resumo do Atendimento

    Exibe um resumo completo das etapas realizadas, consolidando os dados de administrativo, triagem e especialista.


# Como Executar

    ## Clone o repositório:

git clone [https://github.com/elaranjeiras/sistema-fluxo-pacientes.git](https://github.com/elaranjeiras/gerencia_fluxo_pacientes_ubs)
cd sistema-fluxo-pacientes

    ## Renomear o Arquivo
    
Baixe o arquivo projeto_ubs.py e renomei para main.py

# Instale as dependências:

pip install -r requirements.txt

# Configure a chave da API da OpenAI:

Adicione sua chave de API como variável de ambiente:

export OPENAI_API_KEY="sua_chave_api"

# Ou substitua diretamente no código na linha:

openai.api_key = "sua_chave_api"

# Execute o sistema:

python main.py
