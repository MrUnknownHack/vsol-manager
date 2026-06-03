import os
import subprocess
import re
import json
from datetime import datetime

class VSOLOLTConnector:
    def __init__(self):
        self.olt_ip = os.environ.get("OLT_IP", "192.168.8.100")
        self.snmp_community = os.environ.get("SNMP_COMMUNITY", "public")
        self.snmp_version = os.environ.get("SNMP_VERSION", "2c")
        self.snmp_enabled = os.environ.get("SNMP_ENABLED", "true") == "true"
        self.user_data = self.load_user_data()
    
    def load_user_data(self):
        """Load customer mapping from users.json"""
        try:
            with open('users.json', 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def run_snmp_get(self, oid):
        cmd = ["snmpget", f"-v{self.snmp_version}", "-c", self.snmp_community, self.olt_ip, oid]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return result.stdout
        except:
            return ""
    
    def get_onu_list(self):
        # Return ONU IDs 1-5 for now (from your working data)
        return [{"id": str(i)} for i in range(1, 6)]
    
    def get_onu_speed(self, onu_id):
        # Real-time speed (current bandwidth)
        rx_oid = f".1.3.6.1.4.1.3320.2.1.1.2.1.{onu_id}"
        tx_oid = f".1.3.6.1.4.1.3320.2.1.1.3.1.{onu_id}"
        
        rx_speed = 0
        tx_speed = 0
        
        rx_output = self.run_snmp_get(rx_oid)
        tx_output = self.run_snmp_get(tx_oid)
        
        numbers_rx = re.findall(r'(\d+)', rx_output)
        numbers_tx = re.findall(r'(\d+)', tx_output)
        
        if numbers_rx:
            rx_speed = int(numbers_rx[-1])
            if rx_speed > 1000000:
                rx_speed = rx_speed // 1000000
        
        if numbers_tx:
            tx_speed = int(numbers_tx[-1])
            if tx_speed > 1000000:
                tx_speed = tx_speed // 1000000
        
        return {"rx": rx_speed, "tx": tx_speed}
    
    def get_total_usage(self, onu_id):
        """Total data usage (bytes) - cumulative since ONU online"""
        # OIDs for total bytes (if available)
        rx_total_oid = f".1.3.6.1.4.1.3320.2.1.1.4.1.{onu_id}"
        tx_total_oid = f".1.3.6.1.4.1.3320.2.1.1.5.1.{onu_id}"
        
        rx_total = 0
        tx_total = 0
        
        rx_output = self.run_snmp_get(rx_total_oid)
        tx_output = self.run_snmp_get(tx_total_oid)
        
        numbers_rx = re.findall(r'(\d+)', rx_output)
        numbers_tx = re.findall(r'(\d+)', tx_output)
        
        if numbers_rx:
            rx_total = int(numbers_rx[-1]) // (1024**3)  # Convert to GB
        if numbers_tx:
            tx_total = int(numbers_tx[-1]) // (1024**3)  # Convert to GB
        
        return {"rx_gb": rx_total, "tx_gb": tx_total}
    
    def get_all_onu_speeds(self):
        onu_list = self.get_onu_list()
        results = []
        
        for onu in onu_list[:10]:
            onu_id = onu.get("id")
            speeds = self.get_onu_speed(onu_id)
            total = self.get_total_usage(onu_id)
            
            # Get user info from mapping
            user_info = self.user_data.get(onu_id, {
                "name": f"User {onu_id}",
                "address": "Unknown",
                "plan": "Unknown"
            })
            
            results.append({
                "onu_id": onu_id,
                "customer_name": user_info.get("name"),
                "address": user_info.get("address"),
                "plan": user_info.get("plan"),
                "rx_speed": speeds.get("rx", 0),
                "tx_speed": speeds.get("tx", 0),
                "total_download_gb": total.get("rx_gb", 0),
                "total_upload_gb": total.get("tx_gb", 0),
                "status": "online"
            })
        
        return results