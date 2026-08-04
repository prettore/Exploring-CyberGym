# Interface Cage 4
O cenário Cage Challenge 4 é uma simulação de rede multiagente que contém 5 agentes azuis diferentes e 5 agentes vermelhos diferentes. O objetivo do desafio é treinar agentes azuis capazes de impedir ataques na rede feitos pelos vermelhos. Demais detalhes podem ser consultados em https://cage-challenge.github.io/cage-challenge-4/pages/
A interface tem como objetivo facilitar o treinamento de agentes e a compreensão do que ocorre no cenário.

Essa interface usa o framework Dash. Ela utiliza callbacks para interagir com os arquivos train_agent.py e evaluate_agent.py em Cage4/Testing, recolher os respectivos outputs e exibi-los na interface.

## Executando o Dashboard

Para executar a interface web localmente, crie e ative um ambiente virtual, instale as dependências e inicie a aplicação:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python index.py
```

## Modo de Uso

Escolha o Cage4 como cenário. Para treinar, insira os parâmetros de taxa de aprendizagem, número de passos e tamanho do batch. Espere o treinamento terminar.
Para realizar a avaliação, escolha o arquivo de checkpoint de treinamento desejado e o número de passos.
Na área à direita, escolha entre a visualição do treinamento em tempo real ou dos resultados da avaliação.

Um teste a ser realizado é observar como a taxa de aprendizagem e o tamanho do batch afetam o tempo e a qualidade do treinamento. Uma alta taxa de aprendizagem leva a uma oscilação maior ao longo dos passos, porém pode auxiliar para convergir ao resultado rapidamente. O tamanho do batch é um parâmetro que depende da capacidade computacional da máquina. Valores mais altos podem permitir um treinamento que converge mais rapidamente, porém demanda mais capacidade computacional.
