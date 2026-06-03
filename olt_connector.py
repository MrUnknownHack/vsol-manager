import telnetlib
import time
from olt_config import OLT_CONFIG

class VSOLConnector:
    def __init__(self):
        self.conn = None
    
    def connect(self):
        try:
            self.conn = telnetlib.Telnet(
                OLT_CONFIG["ip"], 
                OLT_CONFIG["port"], 
                timeout=10
            )
            self.conn.read_until(b"Login: ", timeout=5)
            self.conn.write(OLT_CONFIG["username"].encode() + b"\n")
            self.conn.read_until(b"Password: ", timeout=5)
            self.conn.write(OLT_CONFIG["password"].encode() + b"\n")
            time.sleep(1)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def send_command(self, command):
        try:
            self.conn.write(command.encode() + b"\n")
            time.sleep(2)
            output = self.conn.read_very_eager().decode()
            return output
        except:
            return ""
    
    def close(self):
        if self.conn:
            self.conn.close()
