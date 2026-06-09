#!/usr/bin/env python3
"""
CAN bus simulation for automotive testing
"""

import struct
import time

class CANMessage:
    def __init__(self, can_id: int, data: bytes, timestamp: float = 0):
        self.can_id = can_id
        self.data = data
        self.timestamp = timestamp or time.time()

class CANSimulator:
    def __init__(self, interface: str = "can0"):
        self.interface = interface
        self.messages = []
    
    def add_message(self, can_id: int, data: bytes, period_ms: int = 100):
        """Add periodic message to simulation"""
        self.messages.append({
            "id": can_id,
            "data": data,
            "period": period_ms,
            "last_sent": 0
        })
    
    def simulate_ecu_traffic(self, ecu_type: str) -> list:
        """Generate typical automotive message patterns"""
        
        if ecu_type == "engine":
            return [
                {"id": 0x123, "data": b'\x01\x02\x03\x04', "desc": "RPM"},
                {"id": 0x124, "data": b'\x10\x20', "desc": "Temperature"},
                {"id": 0x125, "data": b'\x00', "desc": "Status"}
            ]
        elif ecu_type == "brake":
            return [
                {"id": 0x201, "data": b'\x00\x00', "desc": "Pressure"},
                {"id": 0x202, "data": b'\x01', "desc": "Pedal position"},
                {"id": 0x203, "data": b'\x00', "desc": "Fault status"}
            ]
        elif ecu_type == "steering":
            return [
                {"id": 0x301, "data": b'\x00\x00', "desc": "Angle"},
                {"id": 0x302, "data": b'\x02', "desc": "Torque"}
            ]
        return []

def parse_can_log(log_path: str) -> list:
    """Parse candump log files"""
    messages = []
    try:
        with open(log_path, 'r') as f:
            for line in f:
                if ' ' in line:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        try:
                            can_id = int(parts[0].split(':')[0], 16)
                            data_bytes = bytes.fromhex(parts[1].replace(' ', ''))
                            messages.append(CANMessage(can_id, data_bytes))
                        except (ValueError, IndexError):
                            continue
    except FileNotFoundError:
        pass
    return messages