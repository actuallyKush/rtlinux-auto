# rtlinux-auto
Real-time Linux toolkit for automotive ECUs

## What this is
CLI tools exploring aerospace RTOS concepts for automotive real-time Linux. Built while studying embedded systems for consumer electronics and automotive applications.

## Why this project exists
Targeted at roles in:
- Automotive (BMW, Porsche, Audi - embedded software engineer positions)
- Consumer electronics with real-time requirements (infotainment systems)

These industries need Linux that meets automotive safety deadlines. Most candidates know QNX/VxWorks. I'm applying aerospace RTOS experience (partitioning, timing) to solve Linux real-time problems - a crossover skill most don't have.

## How to use

### 1. Check timing feasibility
```bash
python3 bin/rtlinux-auto analyze --ecu-config config/ecu.json
```
Outputs RT-Preempt patch recommendations based on deadline/jitter.

### 2. Generate Yocto structure
```bash
python3 bin/rtlinux-auto generate --target TC3XX --output ./meta-auto
```
Creates automotive-focused Yocto layer structure.

### 3. Validate safety compliance  
```bash
python3 bin/rtlinux-auto verify --iso26262 --asil-level B
```
Checks ISO 26262 ASIL-B requirements.

## What the code does

### timing_analysis.py
Maps ECU timing requirements to Linux kernel patches. Knows that:
- ASIL-D = 50us max jitter (brake/steering)
- ASIL-C = 100us max jitter (engine)
- ASIL-B = 200us max jitter (body control)

### yocto_generator.py
Generates Yocto meta-layer configs for automotive MCUs:
- TC3XX (Infineon) - brake ECUs
- R-CAR (Renesas) - infotainment  
- i.MX (NXP) - gateway/body

### compliance_checker.py
Validates ISO 26262 compliance. Catches missing:
- RT kernel (required ASIL-B+)
- Memory locking (required ASIL-B+)
- CPU shielding (required ASIL-C+)

## Test configs

- `config/ecu.json` - ASIL-B body control ECU
- `config/brake_control.json` - ASIL-D brake system
- `config/steering_control_no_rt.json` - Broken config for testing

## Potential extensions
- Actual bitbake recipe generation
- CAN/LIN protocol simulation
- Integration with automotive debugging tools