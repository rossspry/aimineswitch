import psutil

def ai_running(process_names: list[str]) -> bool:
    names = set(n.lower() for n in process_names)
    for p in psutil.process_iter(attrs=["name"]):
        try:
            if p.info["name"] and p.info["name"].lower() in names:
                return True
        except psutil.Error:
            pass
    return False
