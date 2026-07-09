"""Simulated forensic case using the Quantum Forensic Search Simulator.

This example builds a conceptual investigation scenario for malware analysis.
Grover is used as a model of quantum search and does not represent practical
acceleration in a classical workflow.
"""
from forensic.evidencias import sample_evidences
from forensic.ioc_database import sample_iocs
from forensic.hash_search import simulate_grover_hash_search
from forensic.chain_of_custody import ChainOfCustodyRecord
from forensic.models.evidence import Evidence


def run_case():
    evidences = sample_evidences()
    iocs = sample_iocs()
    suspect_hash = iocs['hashes'][0]

    print('=== Investigação de Malware (Simulada) ===')
    print(f'Selecionado IOC (hash): {suspect_hash}')
    print('\nEvidências disponíveis:')
    for e in evidences:
        print(f" - {e.id}: {e.filename} (sha256={e.sha256}) source={e.source}")

    print('\nExtraindo hashes SHA256 da imagem pericial simulada...')
    print('Usando base IOC para identificar possíveis correspondências.')

    print('\nExecutando busca Grover simulada...')
    found, prob = simulate_grover_hash_search(evidences, suspect_hash, shots=500)

    if found:
        if isinstance(found, Evidence):
            print(f'Encontrado: {found.id} (arquivo: {found.filename})')
        else:
            print(f'Encontrado: {found.get("id", "desconhecido")} (arquivo: {found.get("filename", "desconhecido")})')
        print(f'Probabilidade medida (simulada): {prob:.2%}')

        coc = ChainOfCustodyRecord(evidence_id=found.id if isinstance(found, Evidence) else found['id'], created_by='analista')
        coc.add_event('analista', 'collect', 'Evidence collected for analysis', tool_version='quantum-forensics-simulator/phase2')
        coc.finalize()
        print(f'Chain-of-custody record hash: {coc.record_hash[:16]}...')

        print('\nObservação: este é um cenário acadêmico. Grover é usado como modelo conceitual e não substitui ferramentas forenses reais.')
    else:
        print('Nenhuma evidência encontrada para o IOC selecionado.')


if __name__ == '__main__':
    run_case()
