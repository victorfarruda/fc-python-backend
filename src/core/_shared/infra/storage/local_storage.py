from pathlib import Path

from src.core._shared.infra.storage.abstract_storage_service import AbstractStorageService


class LocalStorage(AbstractStorageService):
    TMP_BUCKET = "/tmp/code-fix-storage"

    def __init__(self, bucket: str = TMP_BUCKET) -> None:
        self.bucket = Path(bucket)

        if not self.bucket.exists():
            self.bucket.mkdir(parents=True, exist_ok=True)

    def store(self, file_path: str, content: bytes, content_type: str) -> None:
        full_path = self.bucket / file_path

        if not full_path.parent.exists():
            full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, "wb") as f:
            f.write(content)
