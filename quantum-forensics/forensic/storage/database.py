from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


class ForensicDatabase:
    current_schema_version = 1

    def __init__(self, path: str = ":memory:"):
        self.path = path
        self.connection = sqlite3.connect(self.path, check_same_thread=False)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        cursor = self.connection.cursor()
        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS schema_info (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS cases (
                case_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                investigator TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                notes TEXT NOT NULL DEFAULT '[]'
            );

            CREATE TABLE IF NOT EXISTS evidences (
                evidence_id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                filename TEXT NOT NULL,
                original_path TEXT NOT NULL,
                sha256 TEXT NOT NULL,
                source TEXT NOT NULL,
                evidence_type TEXT NOT NULL,
                metadata TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(case_id) REFERENCES cases(case_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS artifacts (
                artifact_id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                evidence_id TEXT,
                artifact_type TEXT NOT NULL,
                name TEXT NOT NULL,
                metadata TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(case_id) REFERENCES cases(case_id) ON DELETE CASCADE,
                FOREIGN KEY(evidence_id) REFERENCES evidences(evidence_id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS iocs (
                ioc_id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                ioc_type TEXT NOT NULL,
                value TEXT NOT NULL,
                description TEXT,
                severity TEXT NOT NULL,
                confidence TEXT NOT NULL,
                metadata TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(case_id) REFERENCES cases(case_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS findings (
                finding_id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                severity TEXT NOT NULL,
                confidence TEXT NOT NULL,
                evidence_ids TEXT NOT NULL,
                metadata TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(case_id) REFERENCES cases(case_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS timeline_events (
                event_id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                timestamp_utc TEXT NOT NULL,
                metadata TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(case_id) REFERENCES cases(case_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS custody_records (
                record_id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                evidence_id TEXT NOT NULL,
                created_by TEXT NOT NULL,
                created_at TEXT NOT NULL,
                details TEXT NOT NULL,
                FOREIGN KEY(case_id) REFERENCES cases(case_id) ON DELETE CASCADE,
                FOREIGN KEY(evidence_id) REFERENCES evidences(evidence_id) ON DELETE CASCADE
            );
            """
        )
        self.connection.commit()
        self._apply_migrations()

    def _apply_migrations(self) -> None:
        schema_version = self._get_schema_version()
        if schema_version < self.current_schema_version:
            self._set_schema_version(self.current_schema_version)

    def _get_schema_version(self) -> int:
        row = self.connection.execute("SELECT value FROM schema_info WHERE key = 'schema_version'").fetchone()
        if row is None:
            self.connection.execute("INSERT INTO schema_info(key, value) VALUES ('schema_version', '0')")
            self.connection.commit()
            return 0
        return int(row[0])

    def _set_schema_version(self, version: int) -> None:
        self.connection.execute("INSERT INTO schema_info(key, value) VALUES ('schema_version', ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (str(version),))
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()

    def save_case(self, case: Dict[str, Any]) -> None:
        self.connection.execute(
            """
            INSERT INTO cases(case_id, title, description, investigator, status, created_at, updated_at, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(case_id) DO UPDATE SET
                title=excluded.title,
                description=excluded.description,
                investigator=excluded.investigator,
                status=excluded.status,
                updated_at=excluded.updated_at,
                notes=excluded.notes
            """,
            (
                case["case_id"],
                case["title"],
                case["description"],
                case["investigator"],
                case["status"],
                case["created_at"],
                case["updated_at"],
                json.dumps(case.get("notes", []), sort_keys=True),
            ),
        )
        self.connection.commit()

    def save_evidence(self, evidence: Dict[str, Any]) -> None:
        self.connection.execute(
            """
            INSERT INTO evidences(evidence_id, case_id, filename, original_path, sha256, source, evidence_type, metadata, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(evidence_id) DO UPDATE SET
                case_id=excluded.case_id,
                filename=excluded.filename,
                original_path=excluded.original_path,
                sha256=excluded.sha256,
                source=excluded.source,
                evidence_type=excluded.evidence_type,
                metadata=excluded.metadata,
                created_at=excluded.created_at
            """,
            (
                evidence["evidence_id"],
                evidence["case_id"],
                evidence["filename"],
                evidence["original_path"],
                evidence["sha256"],
                evidence["source"],
                evidence["evidence_type"],
                json.dumps(evidence.get("metadata", {}), sort_keys=True),
                evidence.get("created_at", _utc_timestamp()),
            ),
        )
        self.connection.commit()

    def save_artifact(self, artifact: Dict[str, Any]) -> None:
        self.connection.execute(
            """
            INSERT INTO artifacts(artifact_id, case_id, evidence_id, artifact_type, name, metadata, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(artifact_id) DO UPDATE SET
                case_id=excluded.case_id,
                evidence_id=excluded.evidence_id,
                artifact_type=excluded.artifact_type,
                name=excluded.name,
                metadata=excluded.metadata,
                created_at=excluded.created_at
            """,
            (
                artifact["artifact_id"],
                artifact["case_id"],
                artifact.get("evidence_id"),
                artifact["artifact_type"],
                artifact["name"],
                json.dumps(artifact.get("metadata", {}), sort_keys=True),
                artifact.get("created_at", _utc_timestamp()),
            ),
        )
        self.connection.commit()

    def save_ioc(self, ioc: Dict[str, Any]) -> None:
        self.connection.execute(
            """
            INSERT INTO iocs(ioc_id, case_id, ioc_type, value, description, severity, confidence, metadata, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(ioc_id) DO UPDATE SET
                case_id=excluded.case_id,
                ioc_type=excluded.ioc_type,
                value=excluded.value,
                description=excluded.description,
                severity=excluded.severity,
                confidence=excluded.confidence,
                metadata=excluded.metadata,
                created_at=excluded.created_at
            """,
            (
                ioc["ioc_id"],
                ioc["case_id"],
                ioc["ioc_type"],
                ioc["value"],
                ioc.get("description"),
                ioc["severity"],
                ioc["confidence"],
                json.dumps(ioc.get("metadata", {}), sort_keys=True),
                ioc.get("created_at", _utc_timestamp()),
            ),
        )
        self.connection.commit()

    def save_finding(self, finding: Dict[str, Any]) -> None:
        self.connection.execute(
            """
            INSERT INTO findings(finding_id, case_id, title, description, severity, confidence, evidence_ids, metadata, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(finding_id) DO UPDATE SET
                case_id=excluded.case_id,
                title=excluded.title,
                description=excluded.description,
                severity=excluded.severity,
                confidence=excluded.confidence,
                evidence_ids=excluded.evidence_ids,
                metadata=excluded.metadata,
                created_at=excluded.created_at
            """,
            (
                finding["finding_id"],
                finding["case_id"],
                finding["title"],
                finding["description"],
                finding["severity"],
                finding["confidence"],
                json.dumps(finding.get("evidence_ids", []), sort_keys=True),
                json.dumps(finding.get("metadata", {}), sort_keys=True),
                finding.get("created_at", _utc_timestamp()),
            ),
        )
        self.connection.commit()

    def save_timeline_event(self, event: Dict[str, Any]) -> None:
        self.connection.execute(
            """
            INSERT INTO timeline_events(event_id, case_id, event_type, title, description, timestamp_utc, metadata, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(event_id) DO UPDATE SET
                case_id=excluded.case_id,
                event_type=excluded.event_type,
                title=excluded.title,
                description=excluded.description,
                timestamp_utc=excluded.timestamp_utc,
                metadata=excluded.metadata,
                created_at=excluded.created_at
            """,
            (
                event["event_id"],
                event["case_id"],
                event["event_type"],
                event["title"],
                event["description"],
                event["timestamp_utc"],
                json.dumps(event.get("metadata", {}), sort_keys=True),
                event.get("created_at", _utc_timestamp()),
            ),
        )
        self.connection.commit()

    def save_custody_record(self, record: Dict[str, Any]) -> None:
        self.connection.execute(
            """
            INSERT INTO custody_records(record_id, case_id, evidence_id, created_by, created_at, details)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(record_id) DO UPDATE SET
                case_id=excluded.case_id,
                evidence_id=excluded.evidence_id,
                created_by=excluded.created_by,
                created_at=excluded.created_at,
                details=excluded.details
            """,
            (
                record["record_id"],
                record["case_id"],
                record["evidence_id"],
                record["created_by"],
                record.get("created_at", _utc_timestamp()),
                json.dumps(record.get("details", {}), sort_keys=True),
            ),
        )
        self.connection.commit()

    def load_case(self, case_id: str) -> Optional[Dict[str, Any]]:
        row = self.connection.execute(
            "SELECT case_id, title, description, investigator, status, created_at, updated_at, notes FROM cases WHERE case_id = ?",
            (case_id,),
        ).fetchone()
        if row is None:
            return None

        case = {
            "case_id": row[0],
            "title": row[1],
            "description": row[2],
            "investigator": row[3],
            "status": row[4],
            "created_at": row[5],
            "updated_at": row[6],
            "notes": json.loads(row[7] or "[]"),
        }

        case["evidences"] = [
            {
                "evidence_id": row[0],
                "case_id": case_id,
                "filename": row[1],
                "original_path": row[2],
                "sha256": row[3],
                "source": row[4],
                "evidence_type": row[5],
                "metadata": json.loads(row[6]),
                "created_at": row[7],
            }
            for row in self.connection.execute(
                "SELECT evidence_id, filename, original_path, sha256, source, evidence_type, metadata, created_at FROM evidences WHERE case_id = ?",
                (case_id,),
            ).fetchall()
        ]

        case["artifacts"] = [
            {
                "artifact_id": row[0],
                "case_id": case_id,
                "evidence_id": row[1],
                "artifact_type": row[2],
                "name": row[3],
                "metadata": json.loads(row[4]),
                "created_at": row[5],
            }
            for row in self.connection.execute(
                "SELECT artifact_id, evidence_id, artifact_type, name, metadata, created_at FROM artifacts WHERE case_id = ?",
                (case_id,),
            ).fetchall()
        ]

        case["iocs"] = [
            {
                "ioc_id": row[0],
                "case_id": case_id,
                "ioc_type": row[1],
                "value": row[2],
                "description": row[3],
                "severity": row[4],
                "confidence": row[5],
                "metadata": json.loads(row[6]),
                "created_at": row[7],
            }
            for row in self.connection.execute(
                "SELECT ioc_id, ioc_type, value, description, severity, confidence, metadata, created_at FROM iocs WHERE case_id = ?",
                (case_id,),
            ).fetchall()
        ]

        case["findings"] = [
            {
                "finding_id": row[0],
                "case_id": case_id,
                "title": row[1],
                "description": row[2],
                "severity": row[3],
                "confidence": row[4],
                "evidence_ids": json.loads(row[5]),
                "metadata": json.loads(row[6]),
                "created_at": row[7],
            }
            for row in self.connection.execute(
                "SELECT finding_id, title, description, severity, confidence, evidence_ids, metadata, created_at FROM findings WHERE case_id = ?",
                (case_id,),
            ).fetchall()
        ]

        case["timeline_events"] = [
            {
                "event_id": row[0],
                "case_id": case_id,
                "event_type": row[1],
                "title": row[2],
                "description": row[3],
                "timestamp_utc": row[4],
                "metadata": json.loads(row[5]),
                "created_at": row[6],
            }
            for row in self.connection.execute(
                "SELECT event_id, event_type, title, description, timestamp_utc, metadata, created_at FROM timeline_events WHERE case_id = ?",
                (case_id,),
            ).fetchall()
        ]

        case["custody_records"] = [
            {
                "record_id": row[0],
                "case_id": case_id,
                "evidence_id": row[1],
                "created_by": row[2],
                "created_at": row[3],
                "details": json.loads(row[4]),
            }
            for row in self.connection.execute(
                "SELECT record_id, evidence_id, created_by, created_at, details FROM custody_records WHERE case_id = ?",
                (case_id,),
            ).fetchall()
        ]

        return case
