import time
from .config import Config
from .telemetry import nvml
from .miner_adapters.trex import TrexMiner
from .arbiter import Arbiter

def main():
    cfg = Config()
    nvml.init()
    try:
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
