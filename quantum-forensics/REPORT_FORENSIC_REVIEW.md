REPORT — Revisão Técnica: Quantum Forensic Search Simulator

Resumo executivo

Realizei uma revisão técnica da branch `feature/quantum-forensics-simulator`.
Em linhas gerais o pacote implementa uma prova de conceito bem organizada e
mantém separação razoável entre componentes forenses e a lógica quântica
existente. O projeto respeitou a restrição de não alterar o algoritmo de
Grover; os builders quânticos originais foram reaproveitados.

1) Arquitetura

Observações
- Estrutura: `quantum-forensics/forensic` contém módulos coerentes:
  - `evidencias.py`: modelo `Evidence` e gerador de amostras.
  - `ioc_database.py`: base simulada de IOCs.
  - `hash_search.py`: camada de integração que mapeia índice→bitstring e usa
    os builders do projeto para executar um fluxo conceitual de Grover.
  - `malware_signature.py`: objetos de assinatura simples e matcher.
  - `chain_of_custody.py`: registro básico de cadeia de custódia com cálculo
    de hash de integridade.

Avaliação
- Responsabilidades: estão bem separadas. Cada módulo tem responsabilidade
  única e limitada.
- Acoplamento: baixo a moderado. Pontos a notar:
  - `hash_search.py` importa diretamente `grover_algorithm` e (condicionalmente)
    `grover_3qubits` de `grover_advanced`. Isso cria dependência direta na
    API dos builders; para protótipo isso é aceitável, mas para escalabilidade
    recomenda-se uma interface adaptadora (ex.: `quantum_adapter`) que
    encapsule chamadas ao backend quântico.
- Expansibilidade: a estrutura facilita adição de novos IOCs, formatos de
  evidência e políticas de cadeia de custódia.

Recomendações arquiteturais rápidas
- Introduzir uma camada `quantum_interface` (adapter) que ofereça: `build_circuit(target_bitstring)`
  e `execute(circuit, shots)`; isso reduz o acoplamento e facilita testes.
- Padronizar representação de evidência (por ex. uso explícito de campos
  `hash_algo`, `hash_value`) para permitir múltiplos algoritmos de hash.

2) Integração com Grover

Observações
- O fluxo em `hash_search.simulate_grover_hash_search` segue o seguinte padrão:
  1. busca clássica para localizar o índice alvo (construir oráculo);
  2. calcula número mínimo de qubits (log2 do número de itens);
  3. converte índice → bitstring (MSB-left) e normaliza para Qiskit;
  4. usa os builders existentes (`criar_grover_2qubits` ou `grover_3qubits`);
  5. executa o circuito e formata resultados.
- Oráculo: a marcação do alvo é fornecida ao builder via o bitstring alvo. Isso
  espelha conceitualmente um oráculo que reconhece o índice desejado — suficiente
  para uma demonstração conceptual.

Avaliação
- Uso conceitual: sim — o pacote demonstra o conceito de Grover aplicado a um
  critério forense (hash correspondente ao IOC) sem alterar o algoritmo.
- Separação de camadas: existe uma separação clara:
  - camada forense: `forensic/*` (dados, IOCs, chain-of-custody, matchers);
  - camada quântica: `grover_algorithm.py` e `grover_advanced.py` (não modificados);
  - camada apresentação: `quantum-forensics/exemplos/caso_forense_simulado.py`.

Pontos de atenção
- Dependência direta nos builders: como mencionado, criar um adaptador ajudaria.
- Fallback para conjuntos grandes (>3 qubits): atualmente o código retorna
  a solução clássica com probabilidade 1.0. Isso é aceitável para demo, mas
  deveria ser documentado explicitamente no README da feature (já há docs, mas
  reforçar) e talvez exposto como comportamento configurável.

3) Validade científica e documentação

Observações
- `quantum-forensics/docs/QUANTUM_FORENSICS.md` já documenta que é uma demo
  acadêmica e menciona limitações de hardware.
- O README principal foi atualizado com link para a área experimental.

Avaliação
- A documentação deixa claro que é uma simulação acadêmica e que não é
  ferramenta pericial operacional. Bom nível mínimo de aviso.
- Recomenda-se adicionar explicitamente no README da feature:
  - a limitação de escala (n_qubits ≤ 3 demo completa; ≥4 fallback clássico);
  - explicitação de que a integridade das evidências aqui é simulação (hashes
    fictícios) e não substitui procedimentos forenses.

4) Segurança e requisitos de perícia digital

Observações
- `Evidence` contém identificador, nome do arquivo, campo `hash`, `origin`,
  `integrity` e `metadata` — cobre os itens básicos.
- `ChainOfCustodyRecord` mantém eventos e gera um `integrity_hash` por SHA-256
  de uma concatenação simples dos campos.

Avaliação
- Cobertura básica: identificação, hash e cadeia de custódia estão representados.
- Lacunas importantes para uso pericial real:
  - ausência de declaração do algoritmo de hash (ex.: SHA-256 vs MD5). O campo
    `hash` é livre; deve haver `hash_algo` e `hash_value`.
  - serialização canônica: a `finalize()` concatena strings para gerar hash de
    integridade; para robustez é preferível serializar em formato canônico
    (ex.: JSON com order consistente) antes de calcular o hash.
  - falta de assinaturas digitais ou mecanismos de stamp (ex.: assinatura do
    responsável ou uso de HSM para garantir não repúdio).
  - logs imutáveis e auditoria: eventos são mantidos em memória no objeto; para
    contexto forense real, eventos devem ser persistidos em repositório
    imutável (WORM) ou com trilha de auditoria.

Recomendações para aproximar de um uso pericial
- Registrar algoritmo de hash explicitamente: adicionar `hash_algo`.
- Usar serialização canônica (e.g., JSON sorted keys) antes de calcular
  `integrity_hash`.
- Adicionar assinaturas digitais (opcional para demo: simular assinatura).
- Adicionar mecanismos para exportar registros de cadeia de custódia em
  formato verificável (PDF/A + metadados, ou JSON+detached-signature).
- Incluir validação de formato/size/timestamps nas evidências.

5) Qualidade de código

Pontos positivos
- Uso de `dataclass` em `evidencias` e `chain_of_custody` é adequado.
- Módulos curtos e foco em responsabilidade única.
- Tipagem parcial presente (annotations em classes e funções públicas simples).
- Docstrings mínimos existem em diversos pontos (ex.: sample_evidences,
  simulate_grover_hash_search), o que facilita entendimento.

Pontos de melhoria
- Docstrings: alguns métodos (ex.: `MalwareSignature.matches`) têm docstring
  curta; recomenda-se padronizar docstrings estilo Google ou NumPy para todas
  funções públicas e classes.
- Tratamento de erros: atualmente funções levantam `ValueError`/`RuntimeError`
  indiretamente via utilitários. Recomenda-se definir exceções específicas
  do pacote (ex.: `forensic.errors.InvalidEvidenceError`) para tornar o
  fluxo mais previsível.
- Tipagem: adicionar tipos explícitos em todas as assinaturas públicas e
  retorno (`List[Dict]` -> `List[Mapping[str, Any]]`) e usar `typing` de forma
  consistente.
- Imports: estão organizados e simples; compatíveis com guidelines.
- Compatibilidade: código é compatível com Python 3.11+; não usa recursos
  experimentais, deve rodar em 3.12/3.13.

6) Sugestões e roadmap (priorizado)

Prioridade alta (antes de merge)
- Adicionar testes unitários para:
  - `simulate_grover_hash_search` (caminhos: target presente, target ausente,
    fallback clássico);
  - `ChainOfCustodyRecord.finalize()` (consistência de hash com serialização);
  - `MalwareSignature.matches` e `sample_signatures`.
- Definir e documentar `hash_algo` em `Evidence` (migrar `hash` para `hash_algo`+
  `hash_value` ou adicionar ambos).
- Padronizar serialização canônica antes do cálculo de `integrity_hash`.
- Adicionar um adaptador `quantum_interface` para encapsular chamadas a
  `grover_algorithm`/`grover_advanced` (reduz acoplamento e facilita testes).

Prioridade média (recomendado)
- Implementar logging estruturado (logger por módulo) em vez de prints.
- Persistência básica para cadeia de custódia (exportar JSON assinado).
- Melhorar docstrings e adicionar `__all__` nos módulos públicos.
- Criar fixture/test runner para executar `quantum-forensics` examples com
  PYTHONPATH controlado em CI.

Prioridade baixa (ideias futuras)
- Suporte para múltiplos algoritmos de hash e verificação automática de
  comprimento/algoritmo.
- Simulação de ruído e incerteza de hardware quântico (para educação).
- Interface web simples para demonstrar casos forenses em ambiente controlado.
- Integração com formatos forenses padrão (SANS/Autopsy artifacts export).

7) Conclusão

A implementação atual fornece uma prova de conceito bem organizada e correta
para demonstração acadêmica. A separação de responsabilidades é adequada,
embora eu recomende reduzir o acoplamento direto com os builders quânticos via
um adaptador. Antes de considerar merge para uma branch principal, implemente
os testes unitários e as melhorias de integridade/serialização descritas em
Prioridade alta.

-- Fim do relatório --
