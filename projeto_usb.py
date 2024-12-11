import json
from pydantic import BaseModel, Field, ValidationError
from typing import Dict
from decimal import Decimal
import openai



# Função para converter Decimal para float no JSON
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Type {obj._class.name_} not serializable")

# Configuração da API OpenAI
openai.api_key = "SUA_CHAVE_API"

# Função para anonimizar dados do paciente
def anonimizar_cpf(cpf):
    return f"anon-{hash(cpf) % 100000}"

# Definindo o modelo de validação de sinais vitais
class SinaisVitais(BaseModel):
    pressao_arterial: float = Field(ge=80, le=200)  # Entre 80 e 200
    temperatura: float = Field(ge=35, le=42)       # Entre 35 e 42
    oxigenacao: float = Field(ge=85, le=100)       # Entre 85 e 1001
    dor: int = Field(ge=1, le=5)                   # Escala de 1 a 5

# Função para validar sinais vitais com pydantic
def validar_sinais_vitais() -> Dict[str, float]:
    try:
        sinais = SinaisVitais(
            pressao_arterial=float(input("Pressão arterial: ")),
            temperatura=float(input("Temperatura corporal: ")),
            oxigenacao=float(input("Oxigenação: ")),
            dor=int(input("Escala de dor (1-5): ")),
        )
        return sinais.model_dump()  # Retorna os dados validados
    except ValidationError as e:
        print(f"Erro na validação dos sinais vitais:\n{e}")
        return validar_sinais_vitais()  # Repetir caso haja erro

# Persona 1: Administrativo
def administrativo():
    print("\n--- Administrativo ---")
    nome = input("Nome do paciente: ")
    data_nascimento = input("Data de nascimento (DD/MM/AAAA): ")
    sexo = input("Sexo (M/F): ")
    cep = input("CEP: ")
    sus = input("Número do cartão SUS: ")
    cpf = input("CPF: ")
    telefone = input("Número de telefone: ")
    codigo_paciente = anonimizar_cpf(cpf)
    return {
        "codigo_paciente": codigo_paciente,
        "dados_pessoais": {
            "nome": nome,
            "data_nascimento": data_nascimento,
            "sexo": sexo,
            "cep": cep,
            "sus": sus,
            "telefone": telefone,
        },
    }

# Persona 2: Triagem
def triagem(codigo_paciente):
    print("\n--- Triagem ---")
    queixa_principal = input("Queixa principal: ")
    sinais_vitais = validar_sinais_vitais()
    hipertenso = input("Paciente é hipertenso? (Sim/Não): ")
    diabetico = input("Paciente é diabético? (Sim/Não): ")
    alergias = input("Alergias: ")

    # Integração com ChatGPT para auxílio
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente médico."},
            {"role": "user", "content": f"Queixa principal: {queixa_principal}\nSinais vitais: {json.dumps(sinais_vitais, default=decimal_default)}\nHipertenso: {hipertenso}\nDiabético: {diabetico}\nAlergias: {alergias}"}
        ],
        max_tokens=150
    )
    sugestoes = response.choices[0].message['content'].strip()
    return {
        "codigo_paciente": codigo_paciente,
        "triagem": {
            "queixa_principal": queixa_principal,
            "sinais_vitais": sinais_vitais,
            "hipertenso": hipertenso,
            "diabetico": diabetico,
            "alergias": alergias,
            "sugestoes_ia": sugestoes,
        },
    }


# Persona 3: Especialista
def especialista(codigo_paciente):
    print("\n--- Especialista ---")
    sinais = input("Sinais observados: ")
    sintomas = input("Sintomas relatados: ")
    medicamentos = input("Transcrição de medicamentos: ")
    exames = input("Solicitação de exames: ")
    return {
        "codigo_paciente": codigo_paciente,
        "especialista": {
            "sinais": sinais,
            "sintomas": sintomas,
            "medicamentos": medicamentos,
            "exames": exames,
        },
    }

# Fluxo Principal
def fluxo_ubs():
    paciente = administrativo()
    triagem_dados = triagem(paciente["codigo_paciente"])
    especialista_dados = especialista(paciente["codigo_paciente"])

    # Exibindo o resumo do atendimento
    print("\n--- Resumo do Atendimento ---")
    resumo = {
        "administrativo": paciente,
        "triagem": triagem_dados,
        "especialista": especialista_dados,
    }

    # Usando o decimal_default para serializar corretamente os valores
    print(json.dumps(resumo, indent=4, ensure_ascii=False, default=decimal_default))

if _name_ == "_main_":
    fluxo_ubs()