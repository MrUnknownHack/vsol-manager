import os

OLT_CONFIG = {
    "ip": os.environ.get("OLT_IP", "myolt.duckdns.org"),
    "username": os.environ.get("OLT_USERNAME", "admin"),
    "password": os.environ.get("OLT_PASSWORD", "Xpon@Olt9417#"),
    "port": int(os.environ.get("OLT_PORT", 23))
}

PON_PORTS = [1, 2, 3, 4]
ONU_IDS = [1, 2, 3, 4, 5, 6, 7, 8]