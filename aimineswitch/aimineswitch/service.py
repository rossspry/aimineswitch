import time
from .config import Config
from .telemetry import nvml
from .miner_adapters.trex import TrexMiner
from .miner_adapters.lolminer import LolMiner
from .arbiter import Arbiter

def main():
    cfg = Config()
    nvml.init()
    try:
        if cfg.miner_kind.lower() == 'lolminer':
            miner = LolMiner(
                host=getattr(cfg, 'lol_host', '127.0.0.1'),
                port=getattr(cfg, 'lol_port', 4444),
                process_names=getattr(cfg, 'lol_process_names', ['lolMiner.exe','lolMiner'])
            )
        else:
            miner = TrexMiner(cfg.miner_api_url, cfg.resume_after_seconds)
        arb = Arbiter(cfg, miner)
        print("AIMineSwitch running. Ctrl+C to quit.")
        while True:
            arb.step()
            time.sleep(1)
    finally:
        nvml.shutdown()

if __name__ == "__main__":
    main()
