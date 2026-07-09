from forensic.storage import SqliteForensicStore


def test_storage_import():
    store = SqliteForensicStore(':memory:')
    store.close()
