# SAMPLE FORENSIC REPORT

## Case ID
CASE-001

## Investigator
Analista Silva

## Evidences
- EV-004 (malware.bin) source=isolated.img sha256=deadbeef

## IOC Correlation
- hash: deadbeef
- ip: 192.168.1.10
- domain: malware.test
- matched_signatures: ["FakeMal"]
- matched_iocs: ["hash:deadbeef"]
- related_evidence_ids: ["EV-004"]

## Risk Score
- total_score: 80
- level: high
- factors:
  - known_malware_hash: 40
  - related_ioc: 30
  - unknown_origin: 10

## Quantum Search Result
- probability: 100.00%
- found: EV-004

## Chain of Custody
- evidence_id: EV-004 record_hash: <hash>
  - event_id: <event_id> action: quantum_search timestamp: 2026-07-09T00:00:00Z
