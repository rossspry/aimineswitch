import pynvml as nvml

class GPUStats:
    def __init__(self, util, mem_total_gb, mem_used_gb, mem_free_gb, temp_c):
        self.util = util
        self.mem_total_gb = mem_total_gb
        self.mem_used_gb = mem_used_gb
        self.mem_free_gb = mem_free_gb
        self.temp_c = temp_c

def init():
    nvml.nvmlInit()

def shutdown():
    try:
        nvml.nvmlShutdown()
    except:  # noqa
        pass

def query(index: int) -> GPUStats:
    h = nvml.nvmlDeviceGetHandleByIndex(index)
    util = nvml.nvmlDeviceGetUtilizationRates(h).gpu
    mem = nvml.nvmlDeviceGetMemoryInfo(h)
    mem_total_gb = mem.total / (1024**3)
    mem_used_gb  = mem.used  / (1024**3)
    mem_free_gb  = mem.free  / (1024**3)
    temp_c = nvml.nvmlDeviceGetTemperature(h, nvml.NVML_TEMPERATURE_GPU)
    return GPUStats(util, mem_total_gb, mem_used_gb, mem_free_gb, temp_c)
