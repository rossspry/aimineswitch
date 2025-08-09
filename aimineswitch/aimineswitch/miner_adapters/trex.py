import time
import requests

class TrexMiner:
    def __init__(self, api_url: str, resume_after_seconds: int = 2):
        self.url = api_url.rstrip("/")
        self.resume_delay = resume_after_seconds

    def _try(self, path: str, method="get", payload=None) -> bool:
        try:
            if method == "get":
                r = requests.get(self.url + path, timeout=2)
            else:
                r = requests.post(self.url + path, json=payload or {}, timeout=2)
            return r.status_code == 200
        except requests.RequestException:
            return False

    def pause(self) -> bool:
        return self._try("/pause") or self._try("/control", "post", {"method": "pause"})

    def resume(self) -> bool:
        ok = self._try("/resume") or self._try("/control", "post", {"method": "resume"})
        if ok:
            time.sleep(self.resume_delay)
        return ok

    def is_alive(self) -> bool:
        return self._try("/summary")
