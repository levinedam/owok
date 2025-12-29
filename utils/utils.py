import time

def format_seconds(seconds):
    """
    Formats total seconds into 'Xh Ym Zs'
    """
    if not seconds or seconds < 0:
        return "0s"
        
    seconds = int(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    
    parts = []
    if h > 0: parts.append(f"{h}h")
    if m > 0: parts.append(f"{m}m")
    if s > 0 or not parts: parts.append(f"{s}s")
    
    return " ".join(parts)
