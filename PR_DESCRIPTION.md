# Título

Fix: normalize bitstring representation for Qiskit endianness compatibility

# Contexto

O Qiskit representa as chaves retornadas por `get_counts()` usando convenção
little-endian: o qubit de índice 0 corresponde ao bit menos significativo (direita)
na string de contagem. O projeto aceitava estados alvo em notação humana
(MSB à esquerda). Essa diferença de convenção causou divergências onde o
estado mais provável medido no simulador correspondia ao bit-reverse do estado
informado pelo usuário (ex.: usuário pede `"001"`, medido `"100"`).

Impacto:
- Confusão na interpretação dos resultados pelos usuários.
- Mesmo que o circuito e a matemática estejam corretos, a interface textual
  entre entrada e saída estava desalinhada.

# Alteração proposta

Adicionar a função utilitária `normalize_bitstring(bitstr, n_qubits=None)` em
`utils/bitstring.py` e utilizá-la nos pontos de entrada (wrappers/exemplos) para:

- validar o formato do bitstring;
- garantir que o bitstring passado para os construtores de circuito esteja na
  convenção esperada pelo Qiskit (LSB à direita);
- manter a experiência do usuário intuitiva (aceitar MSB-left externamente).

Observação: a alteração é aplicada somente na camada de representação/entrada.
Não há mudança nas funções centrais que constroem circuitos (`criar_grover_2qubits`,
`grover_3qubits`) nem nas implementações do Oracle ou do Difusor.

# Validação

Testes executados:

- `tests/endianness_investigation.py` — investigação inicial para mapear o comportamento.
- `tests/endianness_fix_validation.py` — validação rápida usando `target[::-1]`.
- `tests/test_endianness_2q.py` — teste automatizado cobrindo os 4 estados de 2 qubits.
- `tests/test_endianness_3q.py` — teste automatizado cobrindo os 8 estados de 3 qubits.
- `tests/run_endianness_tests.py` — runner independente (sem pytest) para CI/execução local.

Estados testados:
- 2 qubits: `00`, `01`, `10`, `11`.
- 3 qubits: `000`, `001`, `010`, `011`, `100`, `101`, `110`, `111`.

Resultado (resumo):
- Antes da normalização: alguns alvos resultavam no bit-reverse quando medidos.
- Após a normalização (entrada convertida para convenção Qiskit): todos os
  estados testados foram corretamente amplificados — o estado alvo informado
  pelo usuário passou a ser o estado com maior probabilidade medido.

Evidência: `REPORT_ENDIANNESS.md` contém os logs detalhados e os resultados dos
runners locais.

# Impacto

- Matemática do Algoritmo de Grover: nenhuma alteração.
- Gates (oráculo, difusor): inalterados.
- Implementação do oráculo/difusor: inalterada.
- Interface: melhora ergonômica — usuários podem fornecer bitstrings MSB-left
  e o adaptador normaliza para Qiskit.

# Checklist de revisão

- [ ] Código da utilidade revisado (`utils/bitstring.py`).
- [ ] Testes automatizados revisados e passing localmente (`tests/*`).
- [ ] Documentação atualizada (`README.md`, `REPORT_ENDIANNESS.md`).
- [ ] Alterações confinadas à camada de entrada/representação (nenhuma modificação
      em `grover_algorithm.py` ou `grover_advanced.py`).
- [ ] Compatibilidade com Qiskit validada localmente (notar que `pylatexenc`
      foi necessário para o drawer em ambiente de testes).

# Próximos passos recomendados

1. Integrar `normalize_bitstring()` nos pontos de entrada (ex.: `grover_interactive.py`,
   exemplos em `exemplos/`) — sem modificar funções centrais.
2. Atualizar `README.md` com instruções claras e exemplos de uso.
3. Atualizar exemplos em `exemplos/` para demonstrar a normalização e os outputs.
4. Adicionar `tests/run_endianness_tests.py` ao workflow do PR (CI).
5. Submeter PR a partir da branch `investigate/endianness` para revisão de pares.

---

**Observação:** Não fazer merge, não abrir Pull Request automaticamente e não
fazer push para a `main` até aprovação final da equipe. Este arquivo fornece o
corpo pronto do Pull Request quando for decidido abrir.
