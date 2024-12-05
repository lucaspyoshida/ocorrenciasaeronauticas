
from pydantic import BaseModel, Field, model_validator,ValidationError
import json


invalid_json = {
    "acidente": 30.0,
    "incidente_grave": 20.0,
    "incidente": 25.0,
    "ocorrencia_solo": 15.0,
    "nao_ocorrencia": 5.0,  # Soma é 95, não 100
    "taxa_incerteza": 5.0,
    "loops": 1
}


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

try:
    result = Probs(**invalid_json)
    print("Resultado Válido")
except ValidationError as e:
    error = json.loads(e.json())
    print(error[0]["msg"])
