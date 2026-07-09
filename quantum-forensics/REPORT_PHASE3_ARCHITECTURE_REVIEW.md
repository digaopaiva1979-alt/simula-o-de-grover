# REPORT PHASE 3 ARCHITECTURE REVIEW

## Objetivo
Avaliar a arquitetura da Fase 3 da branch `feature/quantum-forensics-simulator` antes da próxima evolução.

## 1) Separação de Camadas

### Camadas identificadas
- `Evidence`
  - `quantum-forensics/forensic/models/evidence.py`
  - Representa evidência forense com campos tipados.
- `Case`
  - `quantum-forensics/forensic/case.py`
  - Contém `ForensicCase` e `ForensicPipeline` como orquestradores do fluxo.
- `Intelligence`
  - `quantum-forensics/forensic/intelligence/ioc_correlation.py`
  - `quantum-forensics/forensic/intelligence/timeline.py`
  - `quantum-forensics/forensic/intelligence/risk_scoring.py`
  - Implementam correlação IOC, timeline e risco.
- `Quantum Interface`
  - `quantum-forensics/forensic/quantum_interface.py`
  - Adaptador para backend quântico abstrato.
- `Chain of Custody`
  - `quantum-forensics/forensic/chain_of_custody.py`
  - Registra eventos e produz hash de integridade.
- `Reports`
  - `examples/complete_investigation.py`
  - `reports/SAMPLE_FORENSIC_REPORT.md`
  - `quantum-forensics/REPORT_PHASE3_INTELLIGENCE.md`

### Avaliação de acoplamento
- A camada forense principal (`case.py`) orquestra todas as demais, o que é esperado.
- `ForensicPipeline` depende de `quantum_interface`, `chain_of_custody` e `intelligence` diretamente.
- `intelligence/ioc_correlation.py` depende de `sample_iocs()` e `sample_signatures()` concretos, o que representa acoplamento de dados estáticos e reduz flexibilidade.
- `timeline.py` e `risk_scoring.py` estão isolados logicamente, mas não usam uma interface comum para eventos.
- `quantum_interface.py` já delega a implementação quântica ao backend abstrato e não importa Qiskit diretamente.

### Conclusão sobre separação
A divisão em camadas é coerente e maior parte dos módulos está corretamente isolada. O principal acoplamento indevido está no uso de fontes de IOC/sinais hard-coded e na falta de uma camada de abstração para ingestão de inteligência externa.

## 2) Revisão do ForensicPipeline

### Ordem das etapas
- `collect_evidence()`
- `analyze_hashes()`
- `correlate_iocs()`
- `calculate_risk()`
- `run_quantum_search()`
- `generate_report()`

A ordem é lógica e segue o fluxo desejado.

### Observações de fluxo
- `analyze_hashes()` adiciona um passo ao timeline interno.
- `correlate_iocs()` substitui o `timeline` inteiro criado anteriormente por `build_forensic_timeline()`, apagando a entrada de `hash_analysis` e comprometendo a persistência completa do histórico.
- `run_quantum_search()` adiciona registro de cadeia de custódia somente quando um item é encontrado; pesquisas não encontradas não geram registro.

### Tratamento de erros
- O pipeline usa exceções simples (`RuntimeError`) para estados inválidos.
- Não há captura de exceções finas ou logging contextual no pipeline.

### Persistência dos resultados
- Todo estado é mantido em memória no objeto `ForensicCase`.
- Não existe persistência em disco nem exportação automática de estado de caso.

### Possibilidade de reexecução
- O pipeline pode ser reexecutado incrementalmente, mas a substituição de `timeline` e a mutação de `case` podem tornar reexecuções parciais menos previsíveis.
- A etapa `collect_evidence()` soma evidências, permitindo reexecução de coleta, mas sem controle de duplicação.

### Rastreabilidade
- Rastreabilidade é parcial: `ForensicCase` armazena evidências, timeline e resultados.
- O timeline simulado não guarda todos os passos transacionais com precisão de persistência.
- A cadeia de custódia registra eventos de busca, mas não registra automaticamente ações de coleta, hash ou correlação.

## 3) Revisão da Cadeia de Custódia

### Verificações
- Todos os eventos criados por `ChainOfCustodyRecord.add_event()` recebem `timestamp_utc` em formato `YYYY-MM-DDTHH:MM:SSZ`.
- Cada evento tem `event_id` gerado por SHA-256 de seus atributos.
- `record_hash` é calculado após a serialização canônica e não entra no cálculo de seu próprio hash.
- `previous_hash` está presente como campo de encadeamento, mas não é populado automaticamente na pipeline atual.

### Limitações
- A cadeia de custódia é criada apenas para eventos de busca quântica e, portanto, não preserva todo o histórico do caso.
- Não há um mecanismo explícito para armazenar versões anteriores de registros no caso de alterações.

### Conclusão sobre cadeias
O modelo técnico de cadeia de custódia é forte em formato e hash, mas o uso atual ainda carece de histórico completo e de encadeamento automático entre registros.

## 4) Revisão do Modelo de Dados

### Modelo Evidence
- Campos presentes: `id`, `filename`, `sha256`, `source`, `collected_at`, `metadata`.
- O modelo é adequado para o fluxo atual.

### Necessidade futura de modelos adicionais
- `Case`: formalizar metadados do caso, estado, autorizações e relacionamentos.
- `Evidence`: já existente, mas pode evoluir para `Artifact` se for necessária distinção entre arquivos, registros de memória, logs etc.
- `Artifact`: útil para diferenciar objetos coletados (arquivo, imagem, rede, memória).
- `IOC`: modelo formal para indicadores de compromisso com tipo, validade, fonte e confiança.
- `Finding`: resultado da análise com severidade, descrição, evidência vinculada e recomendação.
- `TimelineEvent`: modelo tipado para eventos de investigação, com categoria, actor, timestamp e contexto.
- `Report`: objeto estruturado para gerar saídas textuais, JSON e futuros PDFs.

### Conclusão sobre modelo de dados
O modelo de evidência é um bom ponto de partida, mas a arquitetura se beneficiará de uma família de modelos forenses mais formalizados antes da Fase 4.

## 5) Revisão de Segurança

### Validação de entrada
- Não há validação formal de `observed` em `correlate_ioc()`.
- O pipeline não valida os campos de evidência além das anotações de tipo Python.

### Exposição de dados sensíveis
- Relatórios e timelines expõem hashes, fontes e domínios sem qualquer mascaramento.
- A implementação atual não tem controles de proteção de dados sensíveis.

### Logs
- Não existem hooks de logging estruturado ou níveis de log no pipeline.
- Mensagens de erro são lançadas como exceções sem contexto de auditoria.

### Tratamento de exceções
- Exceções no pipeline são genéricas e não há captura por níveis.
- Falhas no backend quântico, na correlação ou nas etapas interdependentes podem derrubar o fluxo sem relatório de causa detalhada.

### Separação acadêmica vs operacional
- O projeto chama a simulação de "conceitual" em exemplos, mas não há mecanismo técnico para separar um modo de demonstração de um modo operacional.
- Isso é adequado para um protótipo, mas não suficiente para evitar confusão em um ambiente combinado.

## 6) Roadmap da Fase 4

### Recomendação de evolução
- `Phase 4`
  - Persistência de casos
  - Banco SQLite/PostgreSQL
  - Grafo de relacionamento
  - Exportação JSON/STIX
  - Assinatura digital
  - Dashboard investigativo

### Comentários de arquitetura
- Adicionar persistência é prioridade para rastreabilidade e reexecução controlada.
- Um grafo de relacionamento entre `Case`, `Evidence`, `IOC`, `Finding` e `TimelineEvent` é essencial para uma investigação mais próxima do real.
- Exportar JSON/STIX permite interoperabilidade com ferramentas de segurança.
- Assinatura digital e hash de relatório são necessários para a cadeia de custódia pericial.
- Dashboard investigativo deve ser construído sobre modelos e camadas de armazenamento claramente separadas.

## 7) Recomendações finais

### Alta prioridade
- Corrigir a perda de timeline entre `analyze_hashes()` e `correlate_iocs()`.
- Introduzir validação de entrada para `observed` e evidências.
- Formalizar o modelo `Report` e a persistência de caso.
- Separar claramente modo acadêmico de modo operacional no design da API.

### Média prioridade
- Refatorar `ioc_correlation` para depender de um provedor de IOC externo, não de dados hard-coded.
- Adicionar logs estruturados e tratamento de exceções mais granular.
- Estender `ChainOfCustodyRecord` para preencher `previous_hash` automaticamente e preservar histórico completo.

### Baixa prioridade
- Criar tipos formais `Artifact`, `IOC`, `Finding`, `TimelineEvent`, `Report`.
- Adicionar armazenamento de casos em banco de dados relacional.
- Gerar relatórios PDF e STIX como parte da Fase 4.

## 8) Conclusão
A Fase 3 entrega uma arquitetura de pipeline forense conceitual consistente e já separa bem as camadas principais. As principais fragilidades são a persistência do histórico, o acoplamento a dados estáticos de IOC e a falta de separação técnica entre simulação e operação. A Fase 4 deve focar em persistência, modelagem forense formal e controle de dados sensíveis.
