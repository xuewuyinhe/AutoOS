# AutoOS
AutoOS is a framework designed to optimize specific OS distributions by automatically modifying Linux kernel configurations without human intervention using LLMs, primarily for AIoT scenarios.

Our work `AutoOS: Make Your OS More Powerful by Exploiting Large Language Models` has been published at ICML 2024. We welcome your attention.

## Requirements
- Linux kernel source code 
- Python 3.x
- `.config` file from your OS distribution for initial configuration

## Quick start

1. Inspect the Linux kernel version and .config file of the OS distribution that needs optimization.
2. Prepare the corresponding Linux version's source code repository. Then, clone and download this project, placing all files within the Linux kernel source repository.
   ```bash
   git clone [insert link to Linux kernel source repository]
   cd linux
   git clone [this project]
   mv AutoOS/* ./
   
3. Copy the .config file from the OS distribution to the Linux version's source code repository, then change the name  using the command below:
   ```bash
   cp .config .config_base
   
4. put your openai key in key.txt, then init the environment using the command below:
   ```bash
   source ./init_env.sh

5. Run AutoOS using the command below:
   ```bash
   python3 	AutoOS.py

   -The error message will appear as follows:
   ```bash
   kconfiglib.KconfigError: kernel/module/Kconfig:4: error: couldn't parse 'modules': unrecognized construct

   -To disable module functionality, delete the problematic code located under kernel/module/Kconfig(according to the message). The code to remove is as follows:
    ```bash
       menuconfig MODULES
              bool "Enable loadable module support"
              modules
              help
                Kernel modules are small pieces of compiled code which can
                be inserted in the running kernel, rather than being
                permanently built into the kernel.  You use the "modprobe"
                tool to add (and sometimes remove) them.  If you say Y here,
                many parts of the kernel can be built as modules (by
                answering M instead of Y where indicated): this is most
                useful for infrequently used options which are not required
                for booting.  For more information, see the man pages for
                modprobe, lsmod, modinfo, insmod and rmmod.
      
                If you say Y here, you will need to run "make
                modules_install" to put the modules under /lib/modules/
                where modprobe can find them (you may need to be root to do
                this).
      
                If unsure, say Y.
