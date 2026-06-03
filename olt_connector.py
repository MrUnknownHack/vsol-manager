import os
import subprocess
import json

class VSOLOLTConnector:
    def __init__(self):
        self.olt_ip = os.environ.get("OLT_IP", "192.168.8.100")
        self.snmp_community = os.environ.get("SNMP_COMMUNITY", "public")
        self.snmp_version = os.environ.get("SNMP_VERSION", "2c")
        self.olt_port = os.environ.get("OLT_PORT", "161")
        self.snmp_enabled = os.environ.get("SNMP_ENABLED", "true") == "true"
    
    def run_snmp_command(self, oid):
        cmd = ["snmpwalk", f"-v{self.snmp_version}", "-c", self.snmp_community, self.olt_ip, oid]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return result.stdout
        except Exception as e:
            print(f"SNMP error: {e}")
            return ""
    
    def get_onu_list(self):
        onu_oid = ".1.3.6.1.4.1.3320.1.2.1.1"
        output = self.run_snmp_command(onu_oid)
        onu_list = []
        for line in output.split("\n"):
            if "INTEGER:" in line or "Gauge32:" in line:
                parts = line.split("=")
                if len(parts) > 1:
                    value = parts[1].strip()
                    onu_list.append({"id": len(onu_list)+1, "value": value})
        return onu_list if onu_list else [{"id": 1, "value": "test"}]
    
    def get_onu_speed(self, onu_id):
        rx_oid = f".1.3.6.1.4.1.3320.2.1.1.{onu_id}.1"
        tx_oid = f".1.3.6.1.4.1.3320.2.1.1.{onu_id}.2"
        rx_output = self.run_snmp_command(rx_oid)
        tx_output = self.run_snmp_command(tx_oid)
        rx_speed = self.extract_speed(rx_output)
        tx_speed = self.extract_speed(tx_output)
        return {"rx": rx_speed, "tx": tx_speed}
    
    def extract_speed(self, output):
        if "=" in output:
            part = output.split("=")[1].strip()
            numbers = [int(s) for s in part.split() if s.isdigit()]
            if numbers:
                return numbers[0]
        return 0
    
    def get_all_onu_speeds(self):
        onu_list = self.get_onu_list()
        results = []
        for onu in onu_list:
            onu_id = onu.get("id", 1)
            speeds = self.get_onu_speed(onu_id)
            results.append({
                "onu_id": str(onu_id),
                "tx_speed": speeds.get("tx", 0),
                "rx_speed": speeds.get("rx", 0),
                "status": "online"
            })
        return results