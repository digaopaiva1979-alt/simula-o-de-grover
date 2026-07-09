# Evolução do projeto

Este documento consolida a evolução do projeto desde a implementação inicial do simulador de Grover até a plataforma de gestão de casos forenses da Fase 4.

## Fase 1 — Simulador Grover

A primeira fase concentrou-se na implementação do algoritmo de Grover como uma ferramenta de demonstração quântica. A base do projeto incluiu:

- Algoritmo de Grover
- Tratamento de endianness
- Normalização de bitstrings
- Simulação de buscas com foco em estruturas de dados e interpretação de resultados

Essa fase estabeleceu a base computacional e a lógica de busca quântica simulada que passou a sustentar as abordagens forenses posteriores.

## Fase 2 — Arquitetura Forense

A segunda fase expandiu o projeto para um contexto investigativo, introduzindo componentes de arquitetura forense e rastreabilidade:

- Quantum interface
- Backend abstrato
- Chain of custody
- Modelo Evidence
- Estrutura inicial de casos e evidências

O foco passou a ser a associação entre dados de entrada, análise e rastreio da procedência das evidências.

## Fase 3 — Inteligência Forense

A terceira fase promoveu a evolução do simulador para um fluxo de análise investigativa mais completo:

- IOC correlation
- Timeline
- Risk scoring
- Forensic pipeline

Nesse estágio, o sistema passou a reunir sinais, relacionamentos e métricas de risco, permitindo uma leitura mais próxima de um processo forense automatizado.

## Fase 4 — Plataforma de Casos

A quarta fase consolidou a proposta em uma plataforma de gestão de casos forenses, com foco em persistência e organização estruturada:

- Case management
- SQLite persistence
- Models
- Relationship graph
- JSON/STIX export

A arquitetura passou a incorporar um fluxo mais formal de armazenamento, recuperação e exportação de dados forenses, preparando o projeto para cenários mais próximos de sistemas de investigação.

## Arquitetura atual resumida

A arquitetura atual combina três pilares principais:

1. Simulação quântica, baseada no algoritmo de Grover e em sua interface para execução simulada.
2. Camada forense, com modelos de caso, evidências, artefatos, IOC, achados e eventos de timeline.
3. Plataforma de gestão, com persistência em SQLite, grafo de relacionamento e exportação estruturada para JSON e STIX.

Essa composição permite uma visão integrada entre execução quântica simulada, análise forense e organização de casos.

## Limitações acadêmicas

O projeto permanece um protótipo acadêmico e experimental. Entre as principais limitações, destacam-se:

- Uso de simulação em vez de execução em hardware quântico real
- Persistência simples baseada em SQLite, sem multilayer ou escalabilidade enterprise
- Modelo inicial de exportação STIX, com foco em compatibilidade conceitual e não em interoperabilidade completa
- Estrutura ainda limitada para uso operacional em larga escala

## Próximos passos possíveis

Os próximos passos naturais incluem:

- Integrar autenticação, permissões e controle de acesso
- Expandir a modelagem para múltiplos tipos de evidência e artefatos
- Melhorar a integração com fontes externas e pipelines de ingestão
- Ampliar a interoperabilidade com padrões forenses e de troca de inteligência
- Evoluir a camada de persistência para mecanismos mais robustos e distribuídos
