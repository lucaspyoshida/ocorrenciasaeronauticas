from partes.loop import loop
from partes.personas import investigador, revisor
from partes.inicio import inicio
from partes.fim import fim


from dotenv import load_dotenv
from openai import OpenAI

from pydantic import BaseModel, Field, model_validator
from guardrails import Guard


load_dotenv()


with open('ocorrencia.txt', 'r', encoding='utf-8') as arquivo:
        ocorrencia = arquivo.read()
        chamada = f""""
{inicio}

{investigador}

{revisor}

<ocorrencia>
{ocorrencia}
</ocorrencia>

{loop}

{fim}
"""

client = OpenAI()


class Probs(BaseModel):
    acidente: float = Field(description="Probabilidade de ser um acidente", ge=0, le=100)
    incidente_grave: float = Field(description="Probabilidade de ser um incidente grave", ge=0, le=100)
    incidente: float = Field(description="Probabilidade de ser um incidente", ge=0, le=100)
    ocorrencia_solo: float = Field(description="Probabilidade de ser uma ocorrência de solo", ge=0, le=100)
    nao_ocorrencia: float = Field(description="Probabilidade de não ser uma ocorrência aeronáutica", ge=0, le=100)
    taxa_incerteza: float = Field(description="Taxa de incerteza na classificação", ge=0, le=100)
    loops: int = Field(description="Número de loops executados")

    @model_validator(mode='after')
    def check_sum_of_probabilities(cls, values):
        total = sum([
            values.acidente,
            values.incidente_grave,
            values.incidente,
            values.ocorrencia_solo,
            values.nao_ocorrencia
        ])
        if not abs(total - 100) < 1e-6:
            raise ValueError('A soma das probabilidades deve ser exatamente 100%.')
        return values
    

prompt = f"""
    {chamada}
    ${{gr.complete_json_suffix_v2}}
"""
guard = Guard.for_pydantic(output_class=Probs)

res = guard(
    model="gpt-4o-mini",
    messages=[{
        "role": "user",
        "content": prompt
    }]
)

print(f"{res.validated_output}")