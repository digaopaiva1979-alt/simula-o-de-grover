# Exemplos de Execução

Este arquivo descreve exemplos rápidos de execução dos scripts deste projeto.

1) Executar a simulação interativa (placeholder):

```bash
python3 grover_interactive.py
```

2) Executar o script principal (cria circuito, executa e salva imagens):

```bash
python3 grover_algorithm.py
```

3) Executar exemplos avançados (gera gráficos de iterações e comparações):

```bash
python3 grover_advanced.py
```

Observações:
- As imagens geradas são salvas em `docs/imagens/`.
- Para executar os scripts é necessário ter o Qiskit instalado.

Nota sobre entradas de bitstrings

- As interfaces públicas (CLI, `grover_interactive.py` e exemplos) aceitam
	bitstrings no formato MSB-left (ex.: `01`, `101`). Essas entradas serão
	convertidas automaticamente para a convenção do Qiskit (LSB-right) UMA
	ÚNICA VEZ pelos wrappers antes da construção do circuito.
