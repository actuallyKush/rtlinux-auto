"""
Timing analysis module for automotive ECUs
Used at Hemeria internship for ARINC653 partition timing validation
"""

AUTOMOTIVE_MAX_JITTER_US = {
    "ASIL-D": 50,
    "ASIL-C": 100,
    "ASIL-B": 200,
    "ASIL-A": 500
}

def analyze_deadline_feasibility(ecu_config):
    timing = ecu_config["timing_requirements"]
    hw = ecu_config["hardware"]
    
    results = {
        "meets_deadline": timing["deadline_ms"] > 0,
        "jitter_ok": timing["jitter_us"] <= AUTOMOTIVE_MAX_JITTER_US.get(ecu_config["asili_level"], 500),
        "rt_kernel_required": timing["deadline_ms"] < 10,
        "memory_locking_needed": hw["memory_kb"] < 8192,
        "cpu_shielding_required": timing["periodicity_ms"] < 20
    }
    
    return results

def suggest_rt_patches(ecu_config):
    timing = ecu_config["timing_requirements"]
    suggestions = []
    
    if timing["deadline_ms"] < 5:
        suggestions.append("PREEMPT_RT_FULL")
    elif timing["deadline_ms"] < 10:
        suggestions.append("PREEMPT_RT_VOLUNTARY")
    
    if timing["jitter_us"] < 200:
        suggestions.extend(["RT_MUTEX", "NO_HZ_FULL", "CPU_ISOLATION"])
    
    return suggestions