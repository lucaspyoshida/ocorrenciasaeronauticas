from partes.loop import loop
from partes.personas import investigador, revisor
from partes.inicio import inicio
from partes.fim import fim


from dotenv import load_dotenv
from openai import OpenAI

from pydantic import BaseModel, Field, model_validator
from guardrails import Guard


load_dotenv()


def gerar_chamada(ocorrencia):
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
    return chamada

client = OpenAI()



class Probs(BaseModel):
    acidente: float = Field(description="Probabilidade de ser um acidente", ge=0, le=100)
    incidente_grave: float = Field(description="Probabilidade de ser um incidente grave", ge=0, le=100)
    incidente: float = Field(description="Probabilidade de ser um incidente", ge=0, le=100)
    ocorrencia_solo: float = Field(description="Probabilidade de ser uma ocorrência de solo", ge=0, le=100)
    nao_ocorrencia: float = Field(description="Probabilidade de não ser uma ocorrência aeronáutica", ge=0, le=100)
    taxa_incerteza: float = Field(description="Taxa de incerteza na classificação", ge=0, le=100)
    loops: int = Field(description="Número de loops executados")
    ocorrencia: str = Field(description="Descreva apenas os fatos ocorridos, sem mencionar classificações ou análises. Foque em: o que aconteceu, quando, onde e como. Use entre 100 e 150 palavras para isso.")
    justificativa: str = Field(description="Explique usando entre 100 e 150 palavras como você chegou a essa classificação com base na NSCA 3-6")

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
 

def gerar_resposta(ocorrencia):
        chamada = gerar_chamada(ocorrencia)
        prompt = f"""
        {chamada}
        ${{gr.complete_json_suffix_v2}}
        """
        guard = Guard.for_pydantic(output_class=Probs)

        # resgpt = client.chat.completions.create(
        #         model="gpt-4o-mini-2024-07-18",
        #         messages=[{"role": "user", "content": chamada}]
        # )
        # resgpt = resgpt.choices[0].message.content
        # print(resgpt)
        # return
        
        res = guard(
            model="gpt-4o-mini-2024-07-18",
            messages=[{
                    "role": "user",
                    "content": prompt
                    # "content": f"{resgpt} ${{gr.complete_json_suffix_v2}}"
            }]
        )

        return f"{res.validated_output}"


# with open('ocorrencia.txt', 'r', encoding='utf-8') as arquivo:
#         ocorrencia = arquivo.read()
#         print(gerar_resposta(ocorrencia))