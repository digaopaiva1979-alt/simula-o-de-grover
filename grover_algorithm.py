"""
Algoritmo de Grover em Qiskit
==============================
Implementação do algoritmo quântico de Grover para busca em banco de dados desordenado.
O algoritmo de Grover oferece aceleração quadrática O(√N) comparado aos algoritmos clássicos O(N).
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, circuit_drawer
import matplotlib.pyplot as plt
import numpy as np


def criar_grover_2qubits(elemento_procurado):
    """
    Implementa o algoritmo de Grover para 2 qubits.
    
    Parâmetros:
    - elemento_procurado: string binária (ex: '11') que representa o elemento a buscar
    
    Retorna:
    - QuantumCircuit: O circuito do algoritmo de Grover
    """
    
    # Criar registros quânticos
    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(2, 'c')
    
    # Criar circuito
    circuito = QuantumCircuit(qr, cr)
    
    # Passo 1: Inicialização com superposição uniforme
    print("=" * 60)
    print(f"Algoritmo de Grover - Procurando: {elemento_procurado}")
    print("=" * 60)
    print("\n1. Inicialização: Criar superposição uniforme")
    circuito.h(qr)  # Aplicar Hadamard em todos os qubits
    
    # Passo 2: Oracle (marca o estado procurado)
    print("2. Oracle: Marcar o estado procurado")
    aplicar_oracle(circuito, qr, elemento_procurado)
    
    # Passo 3: Difusão (amplificação de amplitude)
    print("3. Difusão (Amplificação de Amplitude)")
    aplicar_difusao(circuito, qr)
    
    # Passo 4: Medição
    print("4. Medição dos qubits\n")
    circuito.measure(qr, cr)
    
    return circuito


def aplicar_oracle(circuito, qr, elemento_procurado):
    """
    Implementa o Oracle que marca o estado procurado com uma fase -1.
    """
    # Converter elemento para lista de bits
    bits = [int(b) for b in elemento_procurado]
    
    # Aplicar X nos qubits que devem estar em |0⟩
    for i, bit in enumerate(bits):
        if bit == 0:
            circuito.x(qr[i])
    
    # Aplicar gate de fase (Z) controlado
    if len(qr) == 2:
        circuito.cz(qr[0], qr[1])
    
    # Desfazer o X
    for i, bit in enumerate(bits):
        if bit == 0:
            circuito.x(qr[i])


def aplicar_difusao(circuito, qr):
    """
    Implementa o operador de difusão (amplificação de amplitude).
    """
    # Aplicar Hadamard em todos os qubits
    for qubit in qr:
        circuito.h(qubit)
    
    # Aplicar X em todos os qubits
    for qubit in qr:
        circuito.x(qubit)
    
    # Aplicar gate CZ controlado
    circuito.cz(qr[0], qr[1])
    
    # Desfazer o X
    for qubit in qr:
        circuito.x(qubit)
    
    # Aplicar Hadamard novamente
    for qubit in qr:
        circuito.h(qubit)


def executar_grover(circuito, shots=1000):
    """
    Executa o circuito de Grover no simulador.
    """
    # Criar simulador
    simulador = AerSimulator()
    
    # Compilar e executar
    job = simulador.run(circuito, shots=shots)
    resultado = job.result()
    
    # Obter contagens
    contagens = resultado.get_counts(circuito)
    
    return contagens


def visualizar_resultado(contagens, elemento_procurado):
    """
    Visualiza os resultados em um gráfico.
    """
    # Criar figura
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Gráfico 1: Histograma dos resultados
    plot_histogram(contagens, ax=ax1)
    ax1.set_title('Resultados do Algoritmo de Grover', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Estado Quântico')
    ax1.set_ylabel('Ocorrências')
    
    # Gráfico 2: Probabilidades
    total = sum(contagens.values())
    probabilidades = {estado: count/total for estado, count in sorted(contagens.items())}
    
    estados = list(probabilidades.keys())
    probs = list(probabilidades.values())
    cores = ['green' if e == elemento_procurado else 'lightblue' for e in estados]
    
    ax2.bar(estados, probs, color=cores, edgecolor='black', linewidth=1.5)
    ax2.set_title(f'Probabilidades (Procurando: {elemento_procurado})', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Estado Quântico')
    ax2.set_ylabel('Probabilidade')
    ax2.set_ylim([0, 1])
    
    # Destacar elemento procurado
    for i, (estado, prob) in enumerate(probabilidades.items()):
        if estado == elemento_procurado:
            ax2.text(i, prob + 0.02, f'{prob:.1%}', ha='center', fontweight='bold', color='green')
        else:
            ax2.text(i, prob + 0.02, f'{prob:.1%}', ha='center')
    
    plt.tight_layout()
    # Salvar resultado em pasta do projeto (relativo)
    plt.savefig('docs/imagens/resultado.png', dpi=150)
    print(f"Gráfico salvo em: docs/imagens/resultado.png")
    plt.close()


def main():
    """
    Função principal.
    """
    # Elemento que queremos buscar
    elemento = '11'  # Pode ser: '00', '01', '10' ou '11'
    
    # Criar circuito de Grover
    print("\n" + "="*60)
    print("CRIANDO CIRCUITO DE GROVER")
    print("="*60 + "\n")
    
    circuito = criar_grover_2qubits(elemento)
    
    # Visualizar circuito
    print("\nVisualizando circuito...\n")
    print(circuito)
    
    # Desenhar circuito
    fig = circuit_drawer(circuito, output='mpl', fold=None)
    plt.savefig('docs/imagens/circuito.png', dpi=150, bbox_inches='tight')
    print("Circuito salvo em: docs/imagens/circuito.png\n")
    
    # Executar algoritmo
    print("="*60)
    print("EXECUTANDO ALGORITMO")
    print("="*60 + "\n")
    
    contagens = executar_grover(circuito, shots=1000)
    
    # Exibir resultados
    print("\nResultados (1000 shots):")
    print("-" * 40)
    total = sum(contagens.values())
    for estado in sorted(contagens.keys()):
        count = contagens[estado]
        percentual = (count / total) * 100
        marca = " ← PROCURADO" if estado == elemento else ""
        print(f"  {estado}: {count:4d} ({percentual:5.1f}%){marca}")
    print("-" * 40)
    
    # Visualizar resultados
    visualizar_resultado(contagens, elemento)
    
    # Análise de eficiência
    print("\n" + "="*60)
    print("ANÁLISE DE EFICIÊNCIA")
    print("="*60)
    if elemento in contagens:
        probabilidade = contagens[elemento] / total
        print(f"\nProbabilidade de encontrar {elemento}: {probabilidade:.1%}")
        print(f"Iterações de Grover usadas: 1")
        print(f"Speedup comparado a busca clássica: ~4x (2 qubits)")
    print("\nNota: Com mais qubits e mais iterações, o speedup cresce.")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
