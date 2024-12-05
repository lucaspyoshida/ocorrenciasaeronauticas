# Análise de Ocorrências Aeronáuticas com LLM e GuardRails AI

Este é um aplicativo em Python que analisa textos de notícias sobre ocorrências aeronáuticas e classifica a probabilidade de cada categoria de ocorrência. O projeto utiliza modelos de linguagem (LLMs) da OpenAI e a biblioteca GuardRails AI para garantir a consistência e a confiabilidade dos resultados.

## Sumário

- [Descrição do Projeto](#descrição-do-projeto)
- [Funcionalidades](#funcionalidades)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Exemplo de Uso](#exemplo-de-uso)

## Descrição do Projeto

O objetivo deste projeto é analisar textos referentes a ocorrências aeronáuticas e determinar a probabilidade de cada uma das seguintes categorias:

- **Acidente**
- **Incidente**
- **Incidente Grave**
- **Ocorrência de Solo**
- **Não é Aeronáutico**

Utilizando um modelo de linguagem da OpenAI, o aplicativo processa o texto fornecido e retorna as probabilidades em um formato JSON padronizado. A biblioteca GuardRails AI é empregada para garantir que a saída do modelo esteja no formato correto e que os valores numéricos sejam consistentes.

## Funcionalidades

- **Análise de Texto**: Processa textos de notícias e extrai probabilidades para cada categoria de ocorrência aeronáutica.
- **Validação de Saída**: Garante que a saída do LLM esteja em um formato JSON específico e que os valores numéricos atendam às restrições definidas.
- **Controle de Valores Numéricos**: Verifica se as probabilidades estão entre 0% e 100% e se a soma totaliza 100%.
- **Flexibilidade**: Permite ajustes no prompt e nas validações conforme necessário.

## Pré-requisitos

- Python 3.1 ou superior
- Conta na OpenAI com uma chave de API válida

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/lucaspyoshida/ocorrenciasaeronauticas
   cd ocorrenciasaeronauticas
   ```
2. **Instale as dependências:**

   ```bash
   uv sync
   ```

## Exemplo de uso
1. **Insira o texto que descreve uma ocorrência no arquivo `ocorrencia.txt`:**
2. **Execute o script:**

   ```bash
   uv run app.py
   ```


