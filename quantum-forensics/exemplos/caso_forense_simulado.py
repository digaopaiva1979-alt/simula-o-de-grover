"""Simulated forensic case using the Quantum Forensic Search Simulator."""
from forensic.evidencias import sample_evidences, to_dict_list
from forensic.ioc_database import sample_iocs
from forensic.hash_search import simulate_grover_hash_search
from forensic.chain_of_custody import ChainOfCustodyRecord


def run_case():
    evidences = sample_evidences()
    evid_list = to_dict_list(evidences)

    iocs = sample_iocs()
    suspect_hash = iocs['hashes'][0]

    print('=== Caso Forense Simulado ===')
    print(f'Selecionado IOC (hash): {suspect_hash}')
    print('Evidências disponíveis:')
    for e in evidences:
        print(f" - {e.identifier}: {e.filename} (hash={e.hash}) origin={e.origin})")

    # Chain of custody for found evidence
    print('\nExecutando busca (simulada) com Grover...')
    found, prob = simulate_grover_hash_search(evid_list, suspect_hash, shots=500)
    if found:
        print(f'Encontrado: {found["identifier"]} (arquivo: {found["filename"]})')
        print(f'Probabilidade medida (simulada): {prob:.2%}')

        coc = ChainOfCustodyRecord(evidence_id=found['identifier'], created_by='analista')
        coc.add_event('analista', 'coleta', 'Evidência coletada para análise')
        coc.finalize()
        print(f'Chain-of-custody integrity hash: {coc.integrity_hash[:16]}...')
    else:
        print('Nenhuma evidência encontrada para o IOC selecionado.')


if __name__ == '__main__':
    run_case()
