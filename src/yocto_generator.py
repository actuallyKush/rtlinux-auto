"""
Yocto layer generator for automotive real-time Linux
ESIGELEC internship project - automotive adaptation of PetaLinux builds
"""

TARGET_CONFIGS = {
    "TC3XX": {
        "defconfig": "TC3XX_RT_DEFCONFIG",
        "recommended": ["CONFIG_PREEMPT_RT", "CONFIG_NO_HZ", "CONFIG_RCU_NOCB"]
    },
    "R-CAR": {
        "defconfig": "R8A779XX_RT",
        "recommended": ["CONFIG_PREEMPT_RT", "CONFIG_EMBEDDED_CFG", "CONFIG_EXPERT"]
    },
    "IMX6": {
        "defconfig": "IMX6_RT_DEFAULT",
        "recommended": ["CONFIG_PREEMPT", "CONFIG_NO_HZ", "CONFIG_HIGH_RES_TIMERS"]
    }
}

def generate_rt_layer(target, output_dir):
    target_upper = target.upper()
    if target_upper not in TARGET_CONFIGS:
        return {"error": f"Unknown target: {target}"}
    
    config = TARGET_CONFIGS[target_upper]
    
    layer = {
        "name": f"meta-automotive-rt-{target.lower()}",
        "version": "1.0",
        "kernel_config": config["defconfig"],
        "patches": config["recommended"],
        "recipes": [
            "recipes-kernel/linux/linux-rt_%.bbappend",
            "recipes-core/rt-tests/rt-tests_%.bbappend"
        ]
    }
    
    return layer

def generate_autosar_partitions(target):
    partitions = {
        "core0": {
            "purpose": "safety_critical",
            "isolation": "full",
            "schedule": "time_triggered"
        },
        "core1": {
            "purpose": "best_effort",
            "isolation": "partitioned",
            "schedule": "event_triggered"
        },
        "core2": {
            "purpose": "infotainment",
            "isolation": "isolated",
            "schedule": "time_triggered"
        }
    }
    
    return partitions