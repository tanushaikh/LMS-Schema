from datetime import datetime
from typing import Optional

user_logs = []

def create_log(user: str, action: str, ip: Optional[str] = None):
    log = {
        "user": user,
        "action": action,
        "timestamp": str(datetime.now()),
        "ip_address": ip
    }
    user_logs.append(log)
    print(log)  # You can also store this in a database
