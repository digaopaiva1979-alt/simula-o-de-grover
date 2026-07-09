# Endianness Investigation Report

2-qubit results
{'target': '00', 'measured': '00', 'reversed_target': '00', 'match': True, 'match_reversed': True, 'top_count': 2000, 'total_shots': 2000}
{'target': '01', 'measured': '10', 'reversed_target': '10', 'match': False, 'match_reversed': True, 'top_count': 2000, 'total_shots': 2000}
{'target': '10', 'measured': '01', 'reversed_target': '01', 'match': False, 'match_reversed': True, 'top_count': 2000, 'total_shots': 2000}
{'target': '11', 'measured': '11', 'reversed_target': '11', 'match': True, 'match_reversed': True, 'top_count': 2000, 'total_shots': 2000}

3-qubit results
{'target': '000', 'measured': '000', 'reversed_target': '000', 'match': True, 'match_reversed': True, 'top_count': 1888, 'total_shots': 2000}
{'target': '001', 'measured': '100', 'reversed_target': '100', 'match': False, 'match_reversed': True, 'top_count': 1890, 'total_shots': 2000}
{'target': '010', 'measured': '010', 'reversed_target': '010', 'match': True, 'match_reversed': True, 'top_count': 1900, 'total_shots': 2000}
{'target': '011', 'measured': '110', 'reversed_target': '110', 'match': False, 'match_reversed': True, 'top_count': 1895, 'total_shots': 2000}
{'target': '100', 'measured': '001', 'reversed_target': '001', 'match': False, 'match_reversed': True, 'top_count': 1897, 'total_shots': 2000}
{'target': '101', 'measured': '101', 'reversed_target': '101', 'match': True, 'match_reversed': True, 'top_count': 1886, 'total_shots': 2000}
{'target': '110', 'measured': '011', 'reversed_target': '011', 'match': False, 'match_reversed': True, 'top_count': 1898, 'total_shots': 2000}
{'target': '111', 'measured': '111', 'reversed_target': '111', 'match': True, 'match_reversed': True, 'top_count': 1871, 'total_shots': 2000}

## Analysis

- Observação principal: quando o circuito é construído pedindo o estado alvo como
	string na convenção atual do projeto (por exemplo, `'101'`), alguns alvos
	aparecem invertidos no resultado (por exemplo, `'110'` → medido `'011'`).
- Em todos os casos onde houve discrepância, o estado medido corresponde exatamente
	ao bit-reverse do `target` (ou seja, `measured == target[::-1]`). Isso indica
	que a ordem de mapeamento entre qubits e caracteres da string alvo está invertida
	entre a expectativa do código e a convenção usada na representação de resultados
	do Qiskit.

## Convenção do Qiskit (endianness)

- O Qiskit mapeia qubits para bits clássicos de forma que o qubit de índice 0 é o
	menos significativo (LSB) quando as contagens são representadas como strings.
	Na prática, quando você mede e recebe um estado como `'abc'`, o caractere mais
	à direita corresponde ao qubit 0. Isso é frequentemente descrito como
	"little-endian" na representação dos bitstrings de contagem.
- Consequência: se o código assume que o primeiro caractere da string de entrada
	corresponde ao qubit 0, a interpretação fica trocada; o efeito prático é um
	bit-reverse entre o estado alvo fornecido ao construtor do circuito e a saída
	mostrada pelo simulador.

## Comparação com definição padrão do Algoritmo de Grover

- A definição matemática do Algoritmo de Grover define estados como vetores
	binários sem uma convenção textual intrínseca sobre qual qubit corresponde ao
	bit mais à esquerda ou direita. A convenção escolhida deve ser consistente
	entre a construção do Oracle/difusor e a interpretação do resultado.
- No código atual, a construção do Oracle assume uma ordem (indexação de
	qubits nos registradores) que difere da ordem usada na string de saída do
	`get_counts`. Portanto o algoritmo em si está correto, mas a interface textual
	entre `elemento_procurado` e `get_counts` exige alinhamento.

## Solução proposta (preservando corretude matemática)

Opções não intrusivas (recomendadas):

1. Documentar explicitamente a convenção adotada (Qiskit little-endian) e exigir
	 que os `elemento_procurado` sejam fornecidos nessa ordem (ou seja, LSB à direita).

2. For melhor ergonomia, implementar uma pequena função utilitária que converta
	 entre a notação humana (MSB à esquerda) e a notação do Qiskit, por exemplo:

	 - ao criar o circuito: `circuito = criar_grover_2qubits(elemento[::-1])`
	 - ao interpretar resultados: mapear cada key de `get_counts` com `[::-1]`.

3. Alternativa de baixo nível: ajustar explicitamente os mapeamentos de medição
	 (`circuit.measure(qr, cr)`) com a ordem de `cr` para corresponder à string de
	 entrada; porém, isso é mais intrusivo e pode gerar confusão se não bem documentado.

Recomendação: aplicar a opção 2 em wrappers/na documentação — é a solução mais
simples e minimamente invasiva.

## Validação da solução proposta

- Executei um teste que inverte o `elemento_procurado` antes de construir o
	circuito (implementado em `tests/endianness_fix_validation.py`). Resultados:

	- Para 2 qubits: todos os estados (`00`..`11`) foram medidos corretamente após
		reverter o input. Ex.: target `01` → passamos `10` ao construtor → medimos `01`.
	- Para 3 qubits: mesma observação; todos os estados testados (`000`..`111`) foram
		medidos corretamente quando o input foi reverso.

	Os resultados detalhados foram anexados ao final deste relatório (arquivo
	`REPORT_ENDIANNESS.md`).

## Impacto e próximos passos

- Impacto mínimo na lógica: a correção proposta é uma conversão/adapter de
	convenção de string; não há alteração matemática do Oracle ou do Difusor.
- Próximo passo recomendado: criar uma função utilitária `normalize_bitstring`
	no branch de investigação que faça a conversão entre notações e integrar aos
	scripts de exemplo (sem alterar funções centrais) — depois submeter para
	revisão.

## Conclusão

- A diferença observada é de convenção de ordenação (endianness) entre a forma
	como o projeto nomeia estados alvo e a representação textual das contagens do
	Qiskit. A solução mais segura é introduzir um adaptador/normalizador de
	bitstrings e documentar claramente a convenção adotada.


---

Validation of reversed-input fix:

2-qubit validation:
('00', '00', '00', True)
('01', '10', '01', True)
('10', '01', '10', True)
('11', '11', '11', True)

3-qubit validation:
('000', '000', '000', True)
('001', '100', '001', True)
('010', '010', '010', True)
('011', '110', '011', True)
('100', '001', '100', True)
('101', '101', '101', True)
('110', '011', '110', True)
('111', '111', '111', True)
