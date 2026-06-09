#!/usr/bin/env python3
"""
Kernel config generator for automotive RT Linux
"""

def generate_rt_config(target: str, asil_level: str) -> dict:
    """Generate RT-Preempt kernel config for automotive"""
    
    base_config = {
        "CONFIG_EMBEDDED": "y",
        "CONFIG_EXPERT": "y",
        "CONFIG_EXPERT_CORE": "y"
    }
    
    # ASIL-specific configs
    if asil_level in ["B", "C", "D"]:
        base_config.update({
            "CONFIG_PREEMPT_RT": "y",
            "CONFIG_PREEMPT_RT_NO_FREEZE": "y",
            "CONFIG_PREEMPT_RT_TRACE": "y"
        })
    
    if asil_level in ["C", "D"]:
        base_config.update({
            "CONFIG_LOCKDEP": "y",
            "CONFIG_LOCK_STAT": "y",
            "CONFIG_DEBUG_PREEMPT": "y"
        })
    
    # Memory locking
    base_config["CONFIG_MLOCK_LIMIT"] = "131072"  # 128KB default mlock
    
    # Target-specific
    if target.upper() == "TC3XX":
        base_config.update({
            "CONFIG_X86_RT_PRIO": "y",
            "CONFIG_NO_HZ_FULL": "y",
            "CONFIG_RCU_NOCB": "y"
        })
    elif target.upper() == "R-CAR":
        base_config.update({
            "CONFIG_ARM64_RT_PRIO": "y",
            "CONFIG_NO_HZ_FULL": "y"
        })
    elif target.upper() == "IMX6":
        base_config.update({
            "CONFIG_ARM_RT_PRIO": "y",
            "CONFIG_NO_HZ": "y",
            "CONFIG_HIGH_RES_TIMERS": "y"
        })
    
    return base_config

def write_config_file(config: dict, output_path: str):
    """Write kernel config to file"""
    with open(output_path, 'w') as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")