# Fase 4 - Plataforma de Gestão de Casos Forenses

## Arquitetura
A Fase 4 introduz uma camada de persistência baseada em SQLite, com modelos separados para caso, evidência, artefato, IOC, achado e evento de timeline.

## Fluxo de dados
1. Criação/atualização de um caso.
2. Persistência em banco SQLite versionado.
3. Recuperação do caso via repositório.
4. Geração de relacionamento e exportação para JSON/STIX.

## Limitações acadêmicas
- O fluxo é um protótipo acadêmico.
- A integração com backends quânticos reais permanece simulada.
- O grafo inicial usa NetworkX apenas como estrutura abstrata.

## Próximos passos
- Adicionar autenticação e permissões.
- Suportar múltiplos formatos de evidência.
- Integrar com pipelines de ingestão automatizada.
