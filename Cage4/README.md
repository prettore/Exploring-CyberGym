# Instalação do CybORG

Estas etapas diferem do guia original porque corrigem um problema de dependência com o **NumPy**. Além disso, é **altamente recomendável** criar um ambiente virtual.

Inicialize os submódulos após clonar o repositório:

```bash
git submodule update --init --recursive
```

Utilize o **pyenv** para gerenciar versões do Python e instale o Python 3.10. Caso prefira, também é possível utilizar o **Anaconda**, embora essa abordagem seja mais lenta. Certifique-se de estar no diretório raiz do projeto.

```bash
pyenv install 3.10
pyenv local 3.10
```

Crie um ambiente virtual e instale as dependências:

```bash
python -m venv .venv &&
echo 'export PYTHONPATH=$PYTHONPATH:/caminho/para/o/repositorio/Exploring-CyberGym/Cage4/cage-challenge-4' >> .venv/bin/activate
source .venv/bin/activate &&
pip install -U pip &&
cd cage-challenge-4 &&
pip install -e .
```

Teste se tudo foi instalado corretamente:

```bash
pytest
```

As instruções originais podem ser encontradas em:
https://github.com/cage-challenge/CybORG/blob/2742b5e0ce4330c9b14006b38acd3b5ebe00d6fd/CybORG/Tutorial/0.%20Installation.

# Funcionamento

Os scripts estão localizados na pasta Testing. Os principais são train_agent.py e evaluate_agent.py.
Em evaluate_agent.py o primeiro passo é criar uma função para instanciar uma classe EnterpriseMAE (MAE = Multi Agent Environment).
No main, são definidos argumentos (agent_path é o caminho do arquivo dos dados de treinamento do agente e steps é o número de passos para realizar na avaliação). Após a instanciação do cenário usando a função criada, o loop da linha 55 dá um passo no cenário a cada iteração e atualiza a instância de VisualizeRedExpansionMod (modificação feita para permitir a avaliação de agentes feitos pelo usuário). 
