# AutoOS
AutoOS is a framework designed to optimize specific OS distributions by automatically modifying Linux kernel configurations without human intervention using LLMs, primarily for AIoT scenarios.

Our work `AutoOS: Make Your OS More Powerful by Exploiting Large Language Models` has been published at ICML 2024. We welcome your attention.

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
3. **Configure the kernel using the command below:**
   ```bash
    make menuconfig ARCH=riscv (change riscv to the arch you use)
4. **Copy the .config file from the OS distribution to the Linux version's source code repository, then change the name  using the command below:**
   ```bash
   cp .config .config_base
5. **put your openai key in key.txt, then init the environment using the command below:**
   ```bash
   source ./init_env.sh
