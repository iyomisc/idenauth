
CONFIG = {"session_duration": -1, "db_path": "data/auth.db", "callback_url": "http://localhost", "nonce_endpoint": "http://localhost/auth/nonce/", "authentication_endpoint": "http://localhost/auth/authentication/", "favicon_url": ""}


with open("config.txt") as f:
    for line in f.read().split("\n"):
        if (not line) or ("=" not in line) or (line[0] == "#"):
            continue
        key, value = line.split("=")
        CONFIG[key] = value
CONFIG["session_duration"] = int(CONFIG["session_duration"])
print(CONFIG)
