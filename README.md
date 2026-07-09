# Quantum Forensics Simulator

Projeto experimental que explora a integração entre **Computação Quântica**, **Algoritmo de Grover** e **Perícia Digital Computacional**.

O projeto iniciou como um simulador acadêmico do algoritmo de Grover e evoluiu para uma arquitetura experimental voltada à investigação digital, incorporando conceitos de:

- Busca quântica simulada;
- Análise de evidências digitais;
- Cadeia de custódia;
- Threat Intelligence;
- Correlação de indicadores de comprometimento (IOC);
- Linha do tempo investigativa;
- Pontuação de risco;
- Persistência de casos;
- Grafos de relacionamento;
- Exportação estruturada de dados.

> **Observação:** este projeto possui finalidade acadêmica e experimental. Não representa uma ferramenta pericial certificada e não substitui metodologias, normas ou softwares utilizados em investigações digitais reais.

---

# Arquitetura do Projeto

A arquitetura foi organizada em camadas independentes:


┌─────────────────────────────────────┐
│ Investigation Platform │
│ Cases | Storage | Reports | Export │
└─────────────────────────────────────┘
│
┌─────────────────────────────────────┐
│ Forensic Intelligence │
│ IOC | Timeline | Risk Analysis │
└─────────────────────────────────────┘
│
┌─────────────────────────────────────┐
│ Quantum Forensics │
│ Evidence | Artifact | Findings │
│ Chain of Custody │
└─────────────────────────────────────┘
│
┌─────────────────────────────────────┐
│ Quantum Core │
│ Grover Algorithm | Simulation │
└─────────────────────────────────────┘


---

# Quantum Core

Camada responsável pela simulação dos algoritmos quânticos.

Principais componentes:

### Grover Algorithm

Implementação do algoritmo de busca quântica de Grover.

Arquivos principais:

- `grover_algorithm.py`
- `grover_advanced.py`
- `grover_interactive.py`

Recursos:

- Construção de circuitos;
- Simulação de busca quântica;
- Manipulação de estados;
- Tratamento de convenções de bitstrings.

---

# Quantum Forensics Layer

Camada responsável pela representação e análise de evidências digitais.

## Evidence

Modelo de evidência contendo:

- Identificação;
- Hash SHA-256;
- Origem;
- Metadados;
- Informações de coleta.

## Artifact

Representação dos artefatos encontrados durante uma investigação:

Exemplos:

- Arquivos;
- Hashes;
- Registros;
- Indicadores técnicos.

## IOC

Indicadores de comprometimento:

- Hashes;
- Endereços IP;
- Domínios;
- Assinaturas.

## Chain of Custody

Implementação experimental de cadeia de custódia digital contendo:

- SHA-256;
- Versionamento de schema;
- Timestamp UTC;
- Encadeamento de registros;
- Integridade dos eventos.

---

# Forensic Intelligence

Camada de análise investigativa.

## IOC Correlation

Realiza correlação entre:

- Evidências;
- Indicadores;
- Hashes;
- Infraestrutura relacionada.

---

## Timeline Analysis

Construção de linha temporal investigativa:


Coleta da evidência
↓
Cálculo do hash
↓
Análise IOC
↓
Busca experimental com Grover
↓
Registro da cadeia de custódia


---

## Risk Scoring

Modelo experimental de avaliação de risco considerando:

- Hash associado a malware;
- IOC relacionado;
- Comportamento suspeito;
- Origem desconhecida.

---

# Investigation Platform

Camada de gerenciamento investigativo.

## Case Management

Gerenciamento de casos contendo:

- Evidências;
- Artefatos;
- Achados;
- Eventos.

## Storage

Persistência utilizando SQLite:

- Banco estruturado;
- Repositórios;
- Histórico investigativo.

## Relationship Graph

Modelo de relacionamento entre entidades:


Evidência
|
|
Hash
|
|
Malware
|
|
Domínio / IP


Permite visualizar conexões entre diferentes elementos da investigação.

---

# Exportação de Dados

Formatos experimentais:

- JSON;
- STIX 2.1.

Objetivo:

Facilitar integração futura com plataformas de Threat Intelligence.

---

# Estrutura do Projeto


.
├── grover_algorithm.py
├── grover_advanced.py
├── grover_interactive.py
│
├── quantum-forensics/
│ └── forensic/
│ ├── models/
│ ├── storage/
│ ├── graph/
│ ├── intelligence/
│ ├── export/
│ ├── backends/
│ └── chain_of_custody.py
│
├── examples/
├── reports/
├── docs/
├── tests/
└── requirements.txt


---

# Instalação

Requisitos:

- Python 3.8+
- Bibliotecas definidas em `requirements.txt`

Instalação:

```bash
pip install -r requirements.txt
Execução

Executar simulador de Grover:

python grover_interactive.py

Executar exemplo de investigação:

PYTHONPATH=.:quantum-forensics python examples/complete_investigation.py

Executar testes:

pytest
Evolução do Projeto
Fase 1 — Quantum Simulation
Implementação do algoritmo de Grover;
Simulação de circuitos;
Tratamento de estados quânticos.
Fase 2 — Quantum Forensics
Camada de evidências;
Cadeia de custódia;
Modelos forenses.
Fase 3 — Forensic Intelligence
Correlação IOC;
Timeline;
Risk scoring;
Pipeline investigativo.
Fase 4 — Investigation Platform
Casos;
Persistência;
Grafos;
Exportação estruturada.
Objetivo

Investigar como conceitos de Computação Quântica podem ser explorados em conjunto com técnicas de Forense Digital e Cyber Threat Intelligence.

O projeto busca criar uma ponte experimental entre:

Computação Quântica;
Segurança Cibernética;
Investigação Digital;
Análise automatizada de evidências.
Status

Quantum Forensics Simulator v0.4

Implementado:

✅ Algoritmo de Grover
✅ Simulação quântica
✅ Normalização de bitstrings
✅ Modelos de evidência
✅ Cadeia de custódia experimental
✅ Correlação IOC
✅ Pipeline investigativo
✅ Persistência de casos
✅ Grafo de relacionamentos
✅ Exportação JSON/STIX
