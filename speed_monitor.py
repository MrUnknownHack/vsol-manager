import time
import re
from olt_connector import VSOLConnector
from olt_config import ONU_IDS

def get_all_onu_speeds():
    results = []
    conn = VSOLConnector()
    
    if not conn.connect():
        return [{"error": "Cannot connect to OLT"}]
    
    conn.send_command("enable")
    time.sleep(1)
    
    for onu_id in ONU_IDS:
        output = conn.send_command(f"show epon statistics onu 0/1:{onu_id}")
        
        tx_speed = 0
        rx_speed = 0
        
        tx_match = re.search(r"Tx[\s_]*Speed[\s:]*(\d+)", output, re.IGNORECASE)
        if tx_match:
            tx_speed = int(tx_match.group(1))
        
        rx_match = re.search(r"Rx[\s_]*Speed[\s:]*(\d+)", output, re.IGNORECASE)
        if rx_match:
            rx_speed = int(rx_match.group(1))
        
        results.append({
            "onu_id": onu_id,
            "tx_speed": tx_speed,
            "rx_speed": rx_speed,
            "status": "online"
        })
    
    conn.close()
    return results