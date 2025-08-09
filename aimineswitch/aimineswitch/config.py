import yaml
from pathlib import Path

class Config:
    def __init__(self, path: str | None = None):
        cfg_path = Path(path or Path(__file__).resolve().parents[1] / "config.yaml")
        with open(cfg_path, "r", encoding="utf-8") as f:
            d = yaml.safe_load(f)

        self.gpu_index = d.get("gpu_index", 0)
        thr = d.get("thresholds", {})
        self.enter_ai_gpu_util = thr.get("enter_ai_gpu_util", 25)
        self.enter_ai_mem_free_gb = thr.get("enter_ai_mem_free_gb", 6)
        self.exit_ai_gpu_util = thr.get("exit_ai_gpu_util", 15)
        self.hysteresis_seconds = thr.get("hysteresis_seconds", 15)

        therm = d.get("thermals", {})
        self.max_gpu_temp_c = therm.get("max_gpu_temp_c", 85)
        self.cooloff_seconds = therm.get("cooloff_seconds", 20)

        miner = d.get("miner", {})
        self.miner_kind = miner.get("kind", "trex")
        self.miner_api_url = miner.get("api_url", "http://127.0.0.1:4067")
        self.resume_after_seconds = miner.get("resume_after_seconds", 2)

        ai = d.get("ai", {})
        self.ai_process_names = ai.get("process_names", ["ollama.exe", "ollama"])


        # lolMiner extras
        lol = d.get("miner_lolminer", {})
        self.lol_host = lol.get("host", "127.0.0.1")
        self.lol_port = lol.get("port", 4444)
        self.lol_process_names = lol.get("process_names", ["lolMiner.exe", "lolMiner"])
