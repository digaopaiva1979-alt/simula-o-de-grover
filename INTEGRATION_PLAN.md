INTEGRATION PLAN — normalize_bitstring (branch: investigate/endianness)

Objetivo

Descrever quais arquivos devem ser alterados e como integrar `normalize_bitstring()`
preservando a API pública e sem modificar a matemática do Algoritmo de Grover.

Arquivos que serão alterados

- `grover_interactive.py`
  - Motivo: interface interativa é ponto de entrada natural para normalizar a
    entrada do usuário antes de construir circuitos.

- `exemplos/exemplos_de_execucao.md` e eventuais scripts em `exemplos/`
  - Motivo: atualizar exemplos e snippets para usar a normalização e demonstrar
    entradas MSB-left e interpretação das saídas.

- `README.md`
  - Motivo: documentar convenção, mostrar snippet de uso de `normalize_bitstring()`
    e explicar como interpretar `get_counts`.

- `utils/bitstring.py` (já criado)
  - Motivo: local centralizado da utilidade; sem alterações estruturais previstas,
    mas possível refinamento da API (por ex. flags de conversão/strict mode).

- (opcional) pequenos wrappers ou helpers no projeto, p.ex. `cli.py` ou
  `examples/run_example.py`
  - Motivo: aplicar a normalização em pontos controlados, sem tocar nas funções
    internas responsáveis por construir circuitos.

Motivo de cada alteração

- Aplicar a normalização apenas na entrada (wrappers/exemplos/CLI/UI) evita
  tocar nas implementações fundamentais; isso reduz o risco e preserva a API pública.
- Atualizar documentação e exemplos garante que usuários compreendam convenção
  e vejam o comportamento corrigido.

Riscos

- Risco de regressão se a normalização for aplicada inadvertidamente dentro das
  funções centrais; mitigar mantendo `criar_grover_2qubits` e `grover_3qubits`
  inalteradas.
- Risco de duplicidade se múltiplos wrappers aplicarem normalização duas vezes;
  mitigar padronizando a responsabilidade (definir pontos únicos de normalização).
- Dependências de versão Qiskit (por exemplo, disponibilidade de `ccz`) não são
  afetadas pela normalização, mas devem ser documentadas e testadas separadamente.

Estratégia de compatibilidade

- Preservar `criar_grover_2qubits()` e `grover_3qubits()` sem alteração (API intacta).
- Normalizar exclusivamente nos pontos de entrada:
  - `grover_interactive.py`: chamar `normalize_bitstring(user_input, n_qubits)`
    antes de construir o circuito.
  - Exemplos: atualizar para sempre chamar `normalize_bitstring()`.
- Ao exibir resultados ao usuário (por ex. chaves de `get_counts`), converter
  novamente para a representação MSB-left (por ex. `key[::-1]`) para manter
  consistência da UX, a menos que a documentação explique explicitamente que
  as contagens são mostradas em notação Qiskit.
- Adicionar testes automatizados (já incluídos na branch) ao CI do PR para
  garantir regressão zero: `tests/run_endianness_tests.py`.

Plano de execução (passos)

1. Revisar e aprovar `INTEGRATION_PLAN.md` (este arquivo).
2. Implementar mudanças nos pontos de entrada: `grover_interactive.py` e exemplos.
3. Atualizar `README.md` e `exemplos/` para mostrar uso e resultados.
4. Executar testes locais e CI (usar `tests/run_endianness_tests.py`).
5. Abrir PR a partir de `investigate/endianness` com `PR_DESCRIPTION.md`/`PR_SUMMARY.md`.

Observações finais

- Não haverá merge automático; todas as alterações propostas ficarão na branch
  `investigate/endianness` para revisão.
- Este documento é um plano de integração — não implementei mudanças no código
  principal neste passo.
