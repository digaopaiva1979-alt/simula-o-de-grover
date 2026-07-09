"""grover_interactive.py

Wrapper de entrada/saída para executar exemplos do Algoritmo de Grover.

Responsabilidade desta camada:
- Validar e normalizar entradas (MSB-left) usando `normalize_bitstring()`.
- Executar circuitos via `grover_algorithm` (camada quântica, inalterada).
- Formatar contagens retornadas pelo simulador para MSB-left com
  `format_bitstring_output()` antes de exibir ao usuário.
"""

import argparse
from utils.bitstring import normalize_bitstring, format_bitstring_output
import grover_algorithm as ga


def run_interactive(element: str, shots: int = 1000):
    """Executa um fluxo completo: normaliza entrada, cria e executa circuito,
    formata e exibe resultados.
    """
    # Validar e normalizar (contrato: entrada MSB-left)
    n_qubits = len(element)
    elemento_normalizado = normalize_bitstring(element, n_qubits=n_qubits)

    # Mostrar conversão para o usuário (entrada é MSB-left, internamente usamos LSB-right)
    print(f"Entrada (MSB-left): {element}")
    print(f"Convertido para Qiskit (LSB-right): {elemento_normalizado}")

    # Construir e executar circuito (sem alterar lógica interna)
    circuito = ga.criar_grover_2qubits(elemento_normalizado)
    contagens = ga.executar_grover(circuito, shots=shots)

    # Formatar contagens para apresentação (MSB-left)
    contagens_formatadas = format_bitstring_output(contagens, n_qubits=n_qubits)

    # Exibir resumo simples
    total = sum(contagens_formatadas.values())
    print(f"\nResultados ({total} shots) — apresentado em MSB-left:")
    print("-" * 40)
    for estado in sorted(contagens_formatadas.keys()):
        count = contagens_formatadas[estado]
        percentual = (count / total) * 100 if total > 0 else 0
        marca = " ← PROCURADO" if estado == element else ""
        print(f"  {estado}: {count:4d} ({percentual:5.1f}%){marca}")
    print("-" * 40)


def main():
    parser = argparse.ArgumentParser(description='Wrapper interativo para Grover')
    parser.add_argument('--element', '-e', default='11', help='Elemento alvo (bitstring MSB-left, ex: 01, 101)')
    parser.add_argument('--shots', '-s', type=int, default=1000, help='Número de shots para execução')
    args = parser.parse_args()

    print('Executando fluxo interativo (entrada MSB-left)')
    run_interactive(args.element, shots=args.shots)


if __name__ == '__main__':
    main()
