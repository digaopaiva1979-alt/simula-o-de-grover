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

-- Novas seções adicionadas abaixo --

1) Contrato de representação de bitstrings

- Convenção de entrada (contrato): todas as interfaces públicas (CLI, exemplos,
  `grover_interactive.py`) aceitam bitstrings no formato MSB-left. Exemplo: para
  três qubits, o estado `"101"` corresponde ao MSB 1 à esquerda.
- Conversão interna: antes de construir circuitos para Qiskit, aplicar
  `normalize_bitstring(bitstr, n_qubits)` que valida o comprimento e transforma
  a string para a convenção esperada pelo Qiskit (LSB-right). Internamente isso
  normalmente equivale a `bitstr[::-1]` após validação, mas a função encapsula
  o comportamento e validações.
- Responsabilidades por camada:
  - Camada de entrada: validação do input, chamada a `normalize_bitstring()` e
    garantia do contrato (MSB-left). Também é responsável por mensagens de
    erro claras quando o `n_qubits` não corresponde ao comprimento fornecido.
  - Camada quântica (processing): funções como `criar_grover_2qubits`,
    `grover_3qubits` recebem bitstrings já normalizados (LSB-right) e NÃO devem
    aplicar conversões. Essa camada permanece inalterada logicamente.
  - Camada de apresentação: responsável por formatar a saída em convenção
    MSB-left para o usuário final usando `format_bitstring_output()`.

2) Idempotência e controle de fluxo

- Regra geral: a normalização de entrada deve ocorrer UMA ÚNICA VEZ por fluxo de
  execução (ex.: do momento em que o usuário fornece a entrada até a construção
  do circuito).
- Ponto de normalização único: o fluxo de execução deve possuir UM ÚNICO ponto
  autorizado para normalização; wrappers/CLI/exemplos são responsáveis por
  essa chamada. Builders e bibliotecas internas NUNCA devem chamar
  `normalize_bitstring()`.
- Contrato explícito para `normalize_bitstring()`:
  - `normalize_bitstring()` aceita somente entradas no formato MSB-left.
  - A conversão para a convenção Qiskit (LSB-right) ocorre UMA ÚNICA VEZ nos
    pontos de entrada autorizados.
  - A função NÃO tentará identificar automaticamente se uma string já foi
    normalizada; não deve haver detecção automática de estado normalizado.
  - Evitar dupla conversão por controle arquitetural (pontos de chamada
    autorizados), não por detecção automática.
- Validação e erros: a função deve validar o comprimento (`n_qubits`) e os
  caracteres; em caso de inconsistência, lançar erro com mensagem orientadora.
- Documentação: explicar o "fluxo seguro" no `README.md` e em `exemplos/`.

3) Utilitário de saída — `format_bitstring_output()`

- Função proposta: `format_bitstring_output(counts: dict, n_qubits: int) -> dict`
  - Responsabilidade: converter as chaves do `get_counts()` (Qiskit LSB-right)
    para a representação MSB-left usada pela interface do projeto.
  - Contrato UX: as contagens exibidas e os relatórios devem usar MSB-left para
    favorecer legibilidade e consistência com a entrada do usuário.
  - Garantia de preservação de shots: a transformação deve preservar a soma
    total dos shots (por ex., sum(counts.values()) permanece igual após a
    conversão).
  - Exemplo conceitual (conteúdos, não código):
    - Entrada `counts` do Qiskit: `{'00': 10, '01': 5}` (LSB-right)
    - Após `format_bitstring_output(counts, 2)` → `{'00': 10, '10': 5}` (MSB-left)
    - Total de shots: 15 antes e depois.
  - Implementation note (documentar, não codificar aqui): a função fará a
    transformação de cada chave via `key[::-1]` e preservará os contadores.
  - Local sugerido: `utils/bitstring.py` como parceira de
    `normalize_bitstring()` para manter coesão.

4) Plano de testes (adicional ao existente)

-- Testes unitários:
  - `test_normalize_bitstring_contract`: garantir que `normalize_bitstring()`
    exige entradas MSB-left, valida comprimento e caracteres, e lança erro em
    entradas inválidas.
  - `test_normalize_bitstring_validation`: comprimento e caracteres válidos.
  - `test_format_bitstring_output`: conversão de `get_counts()` preservando
    somas e contagens.

- Testes de integração:
  - Fluxo completo: entrada MSB-left → `normalize_bitstring()` → construir
    circuito → executar → `format_bitstring_output()` → comparação com target.
  - Testes para 2-qubits e 3-qubits (já presentes como base na branch).

- Testes de regressão:
  - Garantir que exemplos existentes que não usam wrappers explicitamente
    continuem executando (documentar recomendação de atualização dos exemplos).

-- CI:
  - Incluir `tests/run_endianness_tests.py` no workflow do PR (apenas no PR,
    não alterar `main` diretamente).
  - Incluir atualização do `README.md` e `exemplos/` no mesmo PR para evitar
    divergência entre código e documentação.
  - Exigir que o PR passe com esses testes antes de aprovação.

5) Segurança da alteração

- Garantia: funções centrais do algoritmo (oráculo, difusor, builders de
  circuito) permanecem inalteradas. O plano exige revisão obrigatória caso
  qualquer patch modifique `grover_algorithm.py` ou `grover_advanced.py`.
- Política proposta:
  - Commits que alterem `grover_algorithm.py` ou `grover_advanced.py` devem
    incluir justificativa técnica e revisão dedicada (PR separado se houver
    mudanças lógicas).
  - Alterações de normalização devem ser confinadas a wrappers, exemplos e
    `utils/bitstring.py`.

Seção: Checklist de revisão rápida (pré-merge do PR)

- Verificar que `normalize_bitstring()` é chamado apenas nos pontos autorizados
  (wrappers/exemplos/CLI/UI).
- Verificar que `format_bitstring_output()` é usado para apresentar resultados
  ao usuário final.
- Confirmar que testes unitários e de integração foram adicionados e passam
  localmente e no CI do PR.
- Confirmar que o README e exemplos foram atualizados para explicar o contrato
  MSB-left.

Conclusão / Parecer

- O plano original já era sólido; as adições aqui clarificam o contrato de
  bitstrings, garantem idempotência, provêm um utilitário de saída e ampliam a
  cobertura de testes. Com essas mudanças documentadas, o plano está pronto
  para implementação. Implementação deve seguir a regra de uma única normalização
  por fluxo e preservar a camada quântica inalterada.
