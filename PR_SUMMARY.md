# Fix: normalize bitstring representation for Qiskit endianness compatibility

## Resumo

Este PR propõe adicionar uma utilidade para normalizar a representação de bitstrings
fornecidas pelo usuário de forma que sejam compatíveis com a convenção de
endianness do Qiskit (little-endian nas strings retornadas por `get_counts`).

**Objetivo:** evitar divergências entre o estado informado pelo usuário e o
estado efetivamente amplificado pelo circuito, sem alterar a matemática do
Algoritmo de Grover.

---

## Contexto do problema

- O projeto recebe estados alvo como strings binárias (por exemplo, `"101"`).
- O Qiskit representa as chaves de `get_counts` em little-endian: o qubit 0
  corresponde ao bit menos significativo (direito) da string retornada.
- Quando a convenção de entrada do usuário (MSB à esquerda) difere da
  convenção de saída do simulador (LSB à direita), observa-se um `bit-reverse`
  nos estados medidos (ex.: usuário pede `"001"` e o simulador retorna `"100"`).

## Comportamento observado

- Em diversos testes, o estado de maior ocorrência (`most probable`) correspondia
  ao bit-reverse do `elemento_procurado` fornecido pelo usuário.
- Exemplo: para 3 qubits, ao buscar `"001"` foi medido `"100"` como top state.

## Causa identificada

- Diferença de convenção (endianness) entre a representação textual usada pelo
  usuário e a representação das chaves de contagem do Qiskit (little-endian).
- A construção do Oracle e do difusor está correta; o problema está na camada de
  entrada/representação dos estados alvo.

## Solução proposta

- Adicionar `normalize_bitstring(bitstr, n_qubits=None)` em `utils/bitstring.py`.
  - Valida caracteres e tamanho.
  - Converte (reverte) a string para a convenção esperada pelo Qiskit.
- Usar a função em pontos de entrada (wrappers/exemplos/CLI) antes de construir o
  circuito. Não alterar funções internas do algoritmo (`criar_grover_2qubits`,
  `grover_3qubits`).
- Documentar a conversão no `README.md` e em `REPORT_ENDIANNESS.md`.

## Impacto técnico

- Circuitos (gates, oráculo, difusor) permanecem idênticos — nenhuma mudança
  matemática aplicada ao Algoritmo de Grover.
- Interface de entrada passa a ser mais ergonômica: usuário informa bitstrings no
  formato natural (MSB-left) e a função normaliza para Qiskit.
- Baixo risco de regressão quando aplicada apenas em camadas de entrada.

## Garantia de não-alteração da matemática

- A alteração trata apenas transformação de representação (string reversal e
  validação). Não houve modificação nos oráculos, difusores ou no número de
  iterações. Implementações matemáticas permanecem intactas.

---

## Technical Validation

### Testes realizados

- `tests/endianness_investigation.py` — investigação inicial que detectou o
  comportamento e gerou `REPORT_ENDIANNESS.md`.
- `tests/endianness_fix_validation.py` — validação que demonstrou que passar o
  `elemento_procurado[::-1]` ao construtor corrige o mapeamento.
- Nova utilidade: `utils/bitstring.py` com `normalize_bitstring()` adicionada.
- Testes automatizados adicionados:
  - `tests/test_endianness_2q.py` — verifica todos os 4 estados de 2 qubits.
  - `tests/test_endianness_3q.py` — verifica todos os 8 estados de 3 qubits.
  - `tests/run_endianness_tests.py` — runner independente (sem pytest) para CI local.

### Estados testados

- 2 qubits: `00`, `01`, `10`, `11`.
- 3 qubits: `000`, `001`, `010`, `011`, `100`, `101`, `110`, `111`.

### Resultado dos testes

- Antes da correção: alguns alvos retornavam o estado invertido (bit-reverse).
- Após usar `normalize_bitstring()` como entrada para os construtores de
  circuito, todos os estados testados foram corretamente amplificados (testes
  passaram localmente).
- Runner `tests/run_endianness_tests.py` executado com sucesso: "All endianness
  normalization tests passed.".

### Confirmação

- Confirma-se que, após normalização, o estado alvo informado pelo usuário é o
  estado com maior probabilidade medido no simulador.

---

## Checklist antes do merge (para revisão)

- [ ] Algoritmo de Grover preservado
- [ ] Oráculo não alterado
- [ ] Difusor não alterado
- [ ] Testes de 2 qubits executados
- [ ] Testes de 3 qubits executados
- [ ] Documentação atualizada (`README.md`, `REPORT_ENDIANNESS.md`)
- [ ] Compatibilidade Qiskit validada (testes localmente e nota sobre `ccz`)

---

## Próximos passos propostos

1. Integrar `normalize_bitstring()` nos pontos de entrada (ex.: `grover_interactive.py`,
   exemplos em `exemplos/`) — sem tocar funções centrais.
2. Atualizar `README.md` com instrução clara e exemplo de uso.
3. Atualizar exemplos em `exemplos/` para usar a função e demonstrar saída.
4. Garantir CI: adicionar `tests/run_endianness_tests.py` ao workflow do PR.
5. Abrir Pull Request a partir de `investigate/endianness` para revisão de pares.

---

**Nota:** Não fazer merge, push ou abrir PR automático. Este arquivo é um resumo
pronto para ser usado como descrição de Pull Request quando desejar.
