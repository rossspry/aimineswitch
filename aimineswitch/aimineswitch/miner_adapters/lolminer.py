
import socket
import json
import psutil
from typing import Optional

class LolMiner:
    \"\"\"Adapter for lolMiner JSON TCP API. Fallback to process kill if API is unavailable.\"\"\"
    def __init__(self, host: str = "127.0.0.1", port: int = 4444, process_names: Optional[list[str]] = None):
        self.host = host
        self.port = int(port)
        self.process_names = [n.lower() for n in (process_names or ["lolMiner.exe", "lolMiner"])]

    def _rpc(self, method: str, params: dict | None = None, timeout: float = 1.5) -> bool:
        try:
            with socket.create_connection((self.host, self.port), timeout=timeout) as s:
                payload = {"id": 1, "method": method}
                if params:
                    payload["params"] = params
                data = (json.dumps(payload) + "\n").encode("utf-8")
                s.sendall(data)
                _ = s.recv(4096)
                return True
        except Exception:
            return False

    def _any_process(self) -> Optional[psutil.Process]:
        for p in psutil.process_iter(attrs=["name"]):
            try:
                nm = (p.info["name"] or "").lower()
                if nm in self.process_names:
                    return p
            except psutil.Error:
                pass
        return None

    def is_alive(self) -> bool:
        if self._rpc("summary"):
            return True
        return self._any_process() is not None

    def pause(self) -> bool:
        if self._rpc("pause"):
            return True
        proc = self._any_process()
        if proc:
            try:
                proc.terminate()
                proc.wait(timeout=3)
                return True
            except Exception:
                try:
                    proc.kill()
                    return True
                except Exception:
                    return False
        return False

    def resume(self) -> bool:
        return self._rpc("resume")
