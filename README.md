# Quantum Forensics Simulator

![Status](https://img.shields.io/badge/status-experimental-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![Quantum Computing](https://img.shields.io/badge/domain-quantum%20computing-purple)
![Digital Forensics](https://img.shields.io/badge/domain-digital%20forensics-red)

## Sobre o projeto

O **Quantum Forensics Simulator** é um projeto experimental que explora a integração entre:

- Computação Quântica;
- Algoritmo de Grover;
- Perícia Digital Computacional;
- Cyber Threat Intelligence;
- Análise automatizada de evidências.

O projeto iniciou como um simulador acadêmico do algoritmo de Grover e evoluiu para uma arquitetura experimental de investigação digital, incorporando conceitos utilizados em ambientes de pesquisa em segurança cibernética e computação forense.

> Este projeto possui finalidade acadêmica e experimental. Não representa uma ferramenta pericial certificada e não substitui metodologias, normas técnicas ou softwares profissionais utilizados em investigações digitais reais.

---

# Visão Geral da Arquitetura

A plataforma foi organizada em camadas independentes:


┌──────────────────────────────────────┐
│ Investigation Platform │
│ Cases | Storage | Reports | Export │
└──────────────────────────────────────┘
│
┌──────────────────────────────────────┐
│ Forensic Intelligence │
│ IOC | Timeline | Risk Analysis │
└──────────────────────────────────────┘
│
┌──────────────────────────────────────┐
│ Quantum Forensics │
│ Evidence | Artifact | Findings │
│ Chain of Custody │
└──────────────────────────────────────┘
│
┌──────────────────────────────────────┐
│ Quantum Core │
│ Grover Algorithm | Simulation │
└──────────────────────────────────────┘


---

# Quantum Core

Camada responsável pela simulação dos algoritmos quânticos.

## Componentes principais

### Grover Algorithm

Implementação experimental do algoritmo de busca quântica de Grover.

Arquivos:


grover_algorithm.py
grover_advanced.py
grover_interactive.py


Recursos:

- Construção de circuitos;
- Simulação de busca quântica;
- Manipulação de estados;
- Tratamento de bitstrings;
- Conversão de convenções MSB/LSB.

---

# Quantum Forensics Layer

Camada responsável pela representação de evidências digitais.

## Evidence Model

Modelo estruturado contendo:

- Identificação da evidência;
- Hash SHA-256;
- Origem;
- Metadados;
- Informações de coleta.

---

## Artifact Management

Representação de artefatos encontrados durante uma investigação.

Exemplos:

- Arquivos;
- Registros;
- Hashes;
- Indicadores técnicos.

---

## IOC Management

Representação de indicadores de comprometimento:

- Hashes maliciosos;
- Endereços IP;
- Domínios;
- Assinaturas.

---

## Chain of Custody

Implementação experimental de cadeia de custódia digital contendo:

- SHA-256;
- Timestamp UTC;
- Versionamento de schema;
- Encadeamento de eventos;
- Controle de integridade.

---

# Forensic Intelligence

Camada responsável pela análise investigativa.

## IOC Correlation

Correlação entre:

- Evidências;
- Indicadores;
- Infraestrutura relacionada;
- Eventos suspeitos.

---

## Timeline Analysis

Construção de linha temporal investigativa:


Coleta da evidência
│
▼
Cálculo do hash
│
▼
Análise IOC
│
▼
Busca experimental Grover
│
▼
Registro na cadeia de custódia


---

## Risk Scoring

Modelo experimental de classificação de risco baseado em:

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
- Eventos;
- Relacionamentos.

---

## Storage

Persistência utilizando SQLite:

- Banco estruturado;
- Repositórios;
- Histórico investigativo.

---

## Relationship Graph

Modelo experimental de relacionamento:


Evidence
│
▼
Hash
│
▼
Malware
│
▼
Domain / IP


Objetivo:

Visualizar conexões entre entidades relacionadas a uma investigação.

---

# Exportação

Formatos suportados:

- JSON;
- STIX 2.1.

Objetivo:

Permitir futura integração com plataformas de Threat Intelligence.

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

## Requisitos

- Python 3.8+
- Dependências definidas em:


requirements.txt


Instalação:

```bash
pip install -r requirements.txt
Execução
Simulador de Grover
python grover_interactive.py
Exemplo de investigação completa
PYTHONPATH=.:quantum-forensics python examples/complete_investigation.py
Testes
pytest
Evolução do Projeto
Fase 1 — Quantum Simulation

Implementado:

Algoritmo de Grover;
Simulação de circuitos;
Manipulação de estados quânticos.
Fase 2 — Quantum Forensics

Implementado:

Modelo de evidências;
Cadeia de custódia;
Hashing;
Representação forense.
Fase 3 — Forensic Intelligence

Implementado:

Correlação IOC;
Linha temporal investigativa;
Risk scoring;
Pipeline forense.
Fase 4 — Investigation Platform

Implementado:

Gerenciamento de casos;
Persistência SQLite;
Grafos de relacionamento;
Exportação JSON/STIX.
Objetivo da Pesquisa

Investigar como conceitos de Computação Quântica podem ser aplicados experimentalmente em conjunto com:

Forense Digital;
Cyber Threat Intelligence;
Análise automatizada de evidências;
Investigação computacional.

O projeto busca criar uma ponte experimental entre:

Computação Quântica
        +
Segurança Cibernética
        +
Perícia Digital
        +
Inteligência Artificial
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
