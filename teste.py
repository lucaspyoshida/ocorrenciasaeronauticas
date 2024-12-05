from app import gerar_resposta

with open('ocorrencia.txt', 'r', encoding='utf-8') as arquivo:
    ocorrencia = arquivo.read()
    print(gerar_resposta(ocorrencia))