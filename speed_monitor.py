from olt_connector import VSOLOLTConnector

def get_all_onu_speeds():
    connector = VSOLOLTConnector()
    
    if connector.snmp_enabled:
        return connector.get_all_onu_speeds()
    else:
        # Fallback mock data for testing
        return [
            {"onu_id": "1", "tx_speed": 1024000, "rx_speed": 512000, "status": "online"},
            {"onu_id": "2", "tx_speed": 512000, "rx_speed": 1024000, "status": "online"}
        ]
