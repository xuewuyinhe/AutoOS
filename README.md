# AutoOS source code (ICML2024)

## Overview
AutoOS is a framework designed for optimizing specific OS distributions through modifying the Linux kernel configurations automatically without human efforts,  which is mainly for AIoT scenarios.  

## Requirements
- Linux kernel source code 
- Python 3.x
- `.config` file from your OS distribution for initial configuration

## Quick start

1. **Inspect the Linux kernel version and .config file of the OS distribution that needs optimization.**
2. **Prepare the corresponding Linux version's source code repository.**
   ```bash
   git clone [insert link to Linux kernel source repository]
   cd linux
