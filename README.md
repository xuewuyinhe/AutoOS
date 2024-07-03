# AutoOS
AutoOS is the first framework designed to optimize the Linux kernel configurations of specific OS distributions on certain hardware without human intervention using LLMs, primarily for AIoT scenarios.

Our work `AutoOS: Make Your OS More Powerful by Exploiting Large Language Models` has been published at ICML 2024. We welcome your attention.

Don't forget to give a star if you like.

## Requirements
- Linux kernel source code 
- Python 3.x
- `.config` file from your OS distribution for initial configuration
- LLM API key: The specific version of the LLM we use in the exeriment is gpt-3.5-turbo-0613 of openai (2023.6.13 - 2024.9). You can use the latest gpt-3.5-turbo version after 2024.9.
## Quick start
0. Make sure you can replace the configuration of the OS by mannual in your environment. 
1. Inspect the Linux kernel version and .config file of the OS distribution that needs optimization.
2. Prepare the corresponding Linux version's source code repository. Then, clone and download this project, placing all files within the Linux kernel source repository.
   ```bash
   git clone [insert link to Linux kernel source repository]
   cd linux
   git clone [this project]
   mv AutoOS/* ./
   
3. Copy the .config file from the OS distribution that needs optimization to the Linux version's source code repository, then change the name  using the command below:
   ```bash
   cp .config .config_base
   
4. Init the environment
   
   The init_env.sh is as follows:
   ~~~bash
   export srctree=.
   export CC=gcc
   export LD=ld
   export ARCH=x86
   export SRCARCH=x86
   ~~~
   Modify the ARCH and SRCARCH variable to your architecture name. Make sure that your architecture name matches the architecture name in the Linux source code. You can use the following command to view all supported architecture names in the Linux source code
   ~~~bash
   ls arch/
   ~~~
   put your openai key in key.txt, then init the environment using the command below:
   ~~~bash
   source ./init_env.sh
   ~~~
5. Run AutoOS:
   Use the command below
   ~~~bash
   python3 AutoOS.py
   ~~~
   When first run it, the error message will appear as follows:
   ~~~bash
   kconfiglib.KconfigError: kernel/module/Kconfig:4: error: couldn't parse 'modules': unrecognized construct
   ~~~
   To disable module functionality, delete the problematic code located under kernel/module/Kconfig (The place is according to the message). The code to remove is as follows:
   ~~~bash
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
    ~~~
    Then use  the command below again to start one search:
    ~~~bash
    python3 AutoOS.py
    ~~~
6. Generate new config files using the command below:
    ~~~bash
    python3 append.py
    ~~~
    The newly generated configuration file is located at ./files/config

    If the program runtime is too short (<1min) or too long (>15min), it is often due to LLM hallucinations causing incorrect output formats in the initial attempts or getting stuck searching in subtrees containing extensive hardware-related configurations. You can interrupt the program and rerun the command immediately for quicker search.

8. Using the following command, load the newly generated ./files/config file, and then save it as ./.config in the current directory.
    ~~~bash
    menuconfig ARCH=x86 (change riscv to the arch you use) 
    ~~~
9. Compile and install a new OS with the new config， then evaluate it using unixbench total score.
10. Steps 5-8 constitute a single search, with 24-48 searches recommended. If the generated OS fails to boot, you can return the errors and modified options to your LLM for identification. If not successful, use a binary search to identify the problematic option . Remember the previously identified options and filter out those in subsequent generated configurations. The modified options in one search is in ./output.txt  generated after running AutoOS.py. Remove the the problematic options in output.txt and run append.py again to generated a viable OS configuration.

You can use the above commands according to your own compiled OS environment to write a shell script that automates the process of searching, compiling, and installing.
## Citation
If you are using AutoOS framework or code for your project , please cite the following paper:
~~~
@inproceedings{chenautoos,
  title={AutoOS: Make Your OS More Powerful by Exploiting Large Language Models},
  author={Chen, Huilai and Wen, Yuanbo and Cheng, Limin and Kuang, Shouxu and Liu, Yumeng and Li, Weijia and Li, Ling and Zhang, Rui and Song, Xinkai and Li, Wei and others},
  booktitle={Forty-first International Conference on Machine Learning}
}
~~~
