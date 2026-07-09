# Simula-o-de-Grover

Simulação didática e evolução do algoritmo de Grover para um contexto de pesquisa forense quântica. O projeto combina uma base de computação quântica simulada com uma arquitetura forense progressiva para análise de evidências, relacionamento entre artefatos e exportação de inteligência.

## Descrição atual do projeto

O projeto começou como um estudo didático sobre o algoritmo de Grover e evoluiu para uma plataforma acadêmica de referência que integra:

- simulação quântica de busca;
- modelos forenses para evidências e casos;
- persistência em SQLite;
- grafo investigativo;
- exportação para JSON e STIX.

Este repositório é um protótipo acadêmico para explorar conceitos de computação quântica aplicada ao contexto forense, sem substituir ferramentas operacionais de investigação.

## Arquitetura atual

### Forensic Layer

Responsável por representar casos, evidências, artefatos, achados, IOC e eventos de timeline.

### Intelligence Layer

Encapsula correlação de IOC, construção de timelines, cálculo de risk score e execução do pipeline forense.

### Quantum Layer

Contém a lógica do algoritmo de Grover, a interface quântica e os backends abstratos usados para simulação.

### Persistence Layer

Fornece persistência estruturada em SQLite com modelos e repositórios para leitura e gravação de casos e evidências.

### Reporting Layer

Gera relatórios, exportações e representações estruturadas para documentação e troca de inteligência.

## Fases da evolução

### Fase 1 — Simulador Grover

- algoritmo de Grover;
- correção de endianness;
- normalização de bitstrings.

### Fase 2 — Arquitetura Forense

- quantum interface;
- backend abstrato;
- chain of custody;
- modelo Evidence.

### Fase 3 — Inteligência Forense

- IOC correlation;
- timeline;
- risk scoring;
- forensic pipeline.

### Fase 4 — Plataforma Forense

- gerenciamento de casos;
- persistência SQLite;
- modelos Case/Evidence/Artifact/Finding;
- grafo investigativo;
- exportação JSON/STIX.

## Fluxo investigativo de exemplo

1. Um caso forense é criado com metadados e investigador responsável.
2. Evidências são adicionadas e armazenadas com hash e origem.
3. O pipeline realiza correlação de IOC, construção de timeline e cálculo de risco.
4. O relacionamento entre evidências, IOC e achados é representado em um grafo.
5. O resultado é exportado para JSON/STIX e pode ser documentado em um relatório.

## Instalação

1. Clone o repositório:

```bash
git clone <repo-url>
cd simula-o-de-grover
```

2. Crie um ambiente virtual e ative-o:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução

- Script principal (2 qubits):

```bash
python3 grover_algorithm.py
```

- Exemplos avançados (3 qubits, iterações, comparações):

```bash
python3 grover_advanced.py
```

- Interface leve / placeholder:

```bash
python3 grover_interactive.py
```

## Testes

Os testes disponíveis podem ser executados com:

```bash
pytest -q
```

## Estrutura de diretórios

```text
simula-o-de-grover/
├── README.md
├── REPORT_PROJECT_EVOLUTION.md
├── LICENSE
├── requirements.txt
├── grover_algorithm.py
├── grover_advanced.py
├── grover_interactive.py
├── quantum-forensics/
│   └── forensic/
│       ├── models/
│       ├── storage/
│       ├── graph/
│       └── export/
├── reports/
└── tests/
```

## Aviso acadêmico

Este projeto é um protótipo acadêmico e de simulação. Ele não substitui soluções forenses comerciais ou infraestruturas operacionais reais.

## Tecnologias utilizadas

- Qiskit
- Qiskit Aer (simulador)
- NumPy
- Matplotlib

## Referências

- L. K. Grover, "A fast quantum mechanical algorithm for database search", Proceedings of the 28th Annual ACM Symposium on the Theory of Computing (STOC), 1996.
- Nielsen, M. A., & Chuang, I. L. (2010). Quantum Computation and Quantum Information.

## Licença

Este projeto está licenciado sob a MIT License — veja o arquivo LICENSE para detalhes.
