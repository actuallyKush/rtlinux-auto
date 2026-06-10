# Architecture: Aerospace RTOS to Automotive Linux

## ARINC653 vs AUTOSAR Partitioning

```
AEROSPACE (ARINC653/XtratuM)    →    AUTOMOTIVE (Mixed-Criticality Linux)
───────────────────────────────────────────────────────────────────────────

Partition 1 (Time/Space Isolated)        core0 (safety_critical)
  - Hard real-time deadlines             - RT kernel + PREEMPT_RT_FULL
  - Memory protection                    - Memory locking
  - Scheduled slots                      - CPU shielding
  
Partition 2 (Time/Space Isolated)        core1 (best_effort)  
  - Periodic tasks                       - Event-triggered scheduling
  - Fault isolation                      - Partitioned isolation
  - Health monitoring                    - Isolated from core0

Partition 3 (Time/Space Isolated)        core2 (infotainment)
  - Non-critical tasks                   - Time-triggered infotainment
  - Best-effort deadlines                - Isolated execution
  - Media processing                     - No safety requirements
```

## Key Transformations

### Timing Requirements
- **Space**: Satellite control loops (1-10ms) → **Automotive**: Brake control (1ms)
- **Jitter**: <50us in both domains
- **Partition isolation**: ARINC653 blackboard pattern → Linux cgroups + namespaces

### Safety Patterns  
- **DO-178C** → **ISO 26262**
  - Both require deterministic timing
  - Both require fault isolation
  - Both require traceability (requirements → code → test)

### Build Systems
- **PetaLinux** (Xilinx) → **Yocto** (Automotive)
  - Same bitbake syntax
  - Same kernel patching mechanism
  - Different target configurations (Zynq vs TC3xx)