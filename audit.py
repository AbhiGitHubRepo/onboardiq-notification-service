import json
from datetime import datetime, timezone
from pathlib import Path

from config import settings


def write_audit(event_name: str, payload: dict) -> None:
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event_name,
        "payload": payload,
    }
    with Path(settings.audit_log_file).open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
