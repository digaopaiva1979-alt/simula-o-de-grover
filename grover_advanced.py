"""
Exemplos Avançados do Algoritmo de Grover
==========================================
Implementações com 3 qubits, múltiplas iterações e análise de complexidade.
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, pi, sin, cos, asin


def grover_3qubits(elemento_procurado, num_iteracoes=1):
    """
    Implementa Grover com 3 qubits e múltiplas iterações.
    
    Para N = 2^n estados, o número ótimo de iterações é aproximadamente:
    iterações_ótimas ≈ π/4 * sqrt(N)
    """
    qr = QuantumRegister(3, 'q')
    cr = ClassicalRegister(3, 'c')
    circuito = QuantumCircuit(qr, cr)
    
    # Inicialização - superposição uniforme
    circuito.h(qr)
    
    # Aplicar iterações de Grover
    for _ in range(num_iteracoes):
        # Oracle
        aplicar_oracle_3qubits(circuito, qr, elemento_procurado)
        
        # Difusão
        aplicar_difusao_3qubits(circuito, qr)
    
    # Medição
    circuito.measure(qr, cr)
    
    return circuito


def aplicar_oracle_3qubits(circuito, qr, elemento_procurado):
    """
    Oracle para 3 qubits - marca o estado com fase -1.
    """
    bits = [int(b) for b in elemento_procurado]
    
    # Aplicar X nos qubits que devem estar em |0⟩
    for i, bit in enumerate(bits):
        if bit == 0:
            circuito.x(qr[i])
    
    # Aplicar CZ com 3 qubits controladores
    circuito.ccz(qr[0], qr[1], qr[2])
    
    # Desfazer o X
    for i, bit in enumerate(bits):
        if bit == 0:
            circuito.x(qr[i])


def aplicar_difusao_3qubits(circuito, qr):
    """
    Operador de difusão para 3 qubits.
    """
    # Hadamard em todos
    for qubit in qr:
        circuito.h(qubit)
    
    # X em todos
    for qubit in qr:
        circuito.x(qubit)
    
    # CZ com 3 qubits controladores
    circuito.ccz(qr[0], qr[1], qr[2])
    
    # X em todos
    for qubit in qr:
        circuito.x(qubit)
    
    # Hadamard em todos
    for qubit in qr:
        circuito.h(qubit)


def analisar_numero_iteracoes():
    """
    Analisa o efeito do número de iterações.
    """
    print("\n" + "="*70)
    print("ANÁLISE: EFEITO DO NÚMERO DE ITERAÇÕES")
    print("="*70 + "\n")
    
    elemento = '101'
    simulador = AerSimulator()
    
    iteracoes_teste = [1, 2, 3, 4, 5]
    probabilidades = {}
    
    for iters in iteracoes_teste:
        circuito = grover_3qubits(elemento, num_iteracoes=iters)
        job = simulador.run(circuito, shots=1000)
        resultado = job.result()
        contagens = resultado.get_counts(circuito)
        
        if elemento in contagens:
            prob = contagens[elemento] / 1000
        else:
            prob = 0
        
        probabilidades[iters] = prob
        print(f"Iterações: {iters} → Probabilidade: {prob:6.1%}")
    
    # Gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    iters_list = list(probabilidades.keys())
    probs_list = list(probabilidades.values())
    
    ax.plot(iters_list, probs_list, 'o-', linewidth=2, markersize=10, color='darkblue')
    ax.axhline(y=1.0, color='red', linestyle='--', label='Probabilidade ideal')
    ax.set_xlabel('Número de Iterações', fontsize=12, fontweight='bold')
    ax.set_ylabel('Probabilidade de Sucesso', fontsize=12, fontweight='bold')
    ax.set_title(f'Algoritmo de Grover: Efeito do Número de Iterações (procurando {elemento})', 
                 fontsize=13, fontweight='bold')
    ax.set_ylim([0, 1.1])
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('/home/rodrigo/Documentos/Novo Site/grover_iteracoes.png', dpi=150)
    print("\nGráfico salvo em: grover_iteracoes.png")
    plt.close()


def comparar_elementos():
    """
    Compara a busca de diferentes elementos.
    """
    print("\n" + "="*70)
    print("ANÁLISE: COMPARAÇÃO DE ELEMENTOS DIFERENTES")
    print("="*70 + "\n")
    
    elementos = ['000', '101', '110', '111']
    simulador = AerSimulator()
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, elemento in enumerate(elementos):
        circuito = grover_3qubits(elemento, num_iteracoes=2)
        job = simulador.run(circuito, shots=1000)
        resultado = job.result()
        contagens = resultado.get_counts(circuito)
        
        # Ordenar para visualização
        contagens_ordenadas = dict(sorted(contagens.items()))
        
        # Gráfico individual
        estados = list(contagens_ordenadas.keys())
        counts = list(contagens_ordenadas.values())
        cores = ['green' if e == elemento else 'lightblue' for e in estados]
        
        axes[idx].bar(estados, counts, color=cores, edgecolor='black')
        axes[idx].set_title(f'Procurando: {elemento}', fontsize=12, fontweight='bold')
        axes[idx].set_xlabel('Estado')
        axes[idx].set_ylabel('Contagens')
        
        # Probabilidade do elemento procurado
        if elemento in contagens:
            prob = contagens[elemento] / 1000
            axes[idx].text(0.5, 0.95, f'P({elemento}) = {prob:.1%}', 
                          transform=axes[idx].transAxes, 
                          ha='center', va='top',
                          bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8),
                          fontsize=11, fontweight='bold')
        
        print(f"Elemento {elemento}: Contagens mais frequentes:")
        for estado, count in sorted(contagens.items(), key=lambda x: x[1], reverse=True)[:3]:
            print(f"  {estado}: {count} ({count/10:.1f}%)")
        print()
    
    plt.tight_layout()
    plt.savefig('/home/rodrigo/Documentos/Novo Site/grover_comparacao.png', dpi=150)
    print("Gráfico salvo em: grover_comparacao.png\n")
    plt.close()


def calcular_complexidade_teorica():
    """
    Calcula e exibe a complexidade teórica do algoritmo.
    """
    print("\n" + "="*70)
    print("COMPLEXIDADE TEÓRICA DO ALGORITMO DE GROVER")
    print("="*70 + "\n")
    
    print("Fórmula: T = O(√N)")
    print("onde N = 2^n é o número total de estados\n")
    
    print("Comparação Clássica vs Quantum:")
    print("-" * 50)
    print(f"{'Qubits':<10} {'N':<15} {'Clássico O(N)':<20} {'Quantum O(√N)':<15}")
    print("-" * 50)
    
    for n in range(1, 11):
        N = 2 ** n
        classico = N
        quantum = int(sqrt(N))
        speedup = classico / quantum if quantum > 0 else 0
        
        print(f"{n:<10} {N:<15} {classico:<20} {quantum:<15} (speedup: {speedup:.1f}x)")
    
    print("-" * 50)
    print("\nNota: Para 10 qubits (1024 estados):")
    print("  - Busca clássica: até 1024 operações")
    print("  - Algoritmo de Grover: apenas 32 operações (√1024)")
    print("="*70 + "\n")


def main():
    """
    Executa todas as análises.
    """
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  ALGORITMO DE GROVER - EXEMPLOS AVANÇADOS".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    
    # 1. Análise de iterações
    analisar_numero_iteracoes()
    
    # 2. Comparação de elementos
    comparar_elementos()
    
    # 3. Complexidade teórica
    calcular_complexidade_teorica()
    
    print("\n" + "█" * 70)
    print("█" + "  EXECUÇÃO CONCLUÍDA".center(68) + "█")
    print("█" * 70 + "\n")


if __name__ == '__main__':
    main()
