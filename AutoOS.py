# -*- coding: utf-8 -*-
import openai
import os
import easygui as g
from menuconfig import MenuConfig
import re
import readline
import sys
import time
import fire

#os.environ["http_proxy"]="127.0.0.1:7890"
#os.environ["https_proxy"]="127.0.0.1:7890"


class Chat:
    def __init__(self,conversation_list=[]):
        self.conversation_list = [[],[],[],[],[],[],[]]  # initialize the dialogue list
        self.costs_list = [] 
        self.bre=False
            
    # print dialogue
    def show_conversation(self,msg_list):
        for msg in msg_list[-2:]:
            if msg['role'] == 'user': 
                message = msg['content']
                if msg['content']=="exit":
                     
                     self.bre=True
                     print("usr exit!")
            else: 
                   message = msg['content']
                   print(f"LLM: {message}")           
            print()

    def  last_step(self,ty,first):
            if first==1:
                        self.conversation_list[ty].pop(-3)
                        self.conversation_list[ty].pop(-3)
            else:
                        self.conversation_list[ty].pop(-1)
                        self.conversation_list[ty].pop(-1)

    def ask(self,prompt,ty=0):
        if ty==0 or ty==5:
                
                if len(self.conversation_list[ty])>5:
                    print('*****')
                    for j in range(6):
                            self.conversation_list[ty].pop(0)
                    print('*****/////')
                    print(self.conversation_list[ty])
        else:
                if len(self.conversation_list[ty])>3:
                    for j in range(2):
                            self.conversation_list[ty].pop(2)
            
        self.conversation_list[ty].append({"role":"user","content":prompt})
                
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo-0613",messages=self.conversation_list[ty])
        answer = response.choices[0].message['content']
        
        self.conversation_list[ty].append({"role":"assistant","content":answer})
        self.show_conversation(self.conversation_list[ty])
        

        if de==2:
                print("conversation_list after ask:")
                print(self.conversation_list[0])
                print(self.conversation_list[1])


        spend = total_counts(response)
        self.costs_list.append(spend)
        print()
        return answer

def total_counts(response):    
    
    tokens_nums = int(response['usage']['total_tokens']) 
    price = 0.002/1000 
    sp = '{:.5f}'.format(price * tokens_nums * 7.5)
    total = f"spend {tokens_nums} token,and spend {sp} yuan)"


    return float(sp)

class auto_counter:
        def __init__(self, max=8):
               self.max = max
        def create_file(self):
            # create counter
            with open('counter.txt', 'w') as file:
                file.write('0')

        def read_and_increment(self):
            try:       
                with open('counter.txt', 'r') as file:
                    number = int(file.read().strip())        
                t=number
                number += 1
                if number == self.max:
                    number=0
            
                with open('counter.txt', 'w') as file:
                    file.write(str(number))
                
                #print(f"The new value is: {number}")
                return t
            
            except FileNotFoundError:
                print("File not found. Creating a new counter with value 0.")
                self.create_file()
                return 0

#global var
mode = 2
de = 1
we = 300
save_cycle = 5

def main(mode = 2, de = 1, we = 300, save_cycle = 5):
    try: 
        with open('key.txt', 'r') as file:
                        line = file.readline().strip()
                        key = line.split()[0] 
                        #print(key)
                        openai.api_key = key
    except FileNotFoundError:
                print("key File not found. Creating a new counter with value 0.")
        
    if len(openai.api_key)==0:
           print('please set llm key')
           return
    
    de=de #Setting de=2 outputs more detailed information
    menu_config = MenuConfig("Kconfig")
    
    #target prompt
    target1="To enhance the Dhrystone and Whetstone  scores in UnixBench. The former represents integer processing capability, while the latter represents floating-point processing capability."
    target_object1="the  Dhrystone and Whetstone  scores in UnixBench"
    target2='to enhance the File Copy  score in Unixbench'
    target_object2=' the File Copy score in Unixbench, and  the file copy throughput '
    target3='to enhance the Execl Throughput  score in Unixbench .'
    target_object3=' the Execl Throughput score in Unixbench,The execl is a system call in Unix and Linux systems, used to execute a new program. '
    target4='to enhance the Pipe-based Context Switching score in Unixbench'
    target_object4=' the Pipe-based Context Switching score in Unixbench'

   # target5='to enhance the Dhrystone 2 using register variables,Double-Precision Whetstone,Execl Throughput,File Copy, Pipe Throughput,Pipe-based Context Switching,Process Creation Shell Scripts,and System Call Overhead scores in Unixbench'
   # target_object5='  the Dhrystone 2 using register variables,Double-Precision Whetstone,Execl Throughput,File Copy, Pipe Throughput,Pipe-based Context Switching,Process Creation Shell Scripts,and System Call Overhead scores in Unixbench'

    target5='to enhance the unixbench  total score'
    target_object5=' the unixbench total score'    
    target6='to enhance the Process Creation  score in Unixbench, improve the process creation ability for os'
    target_object6=' the Process Creation score in Unixbench and the process creation throughput' 
    target7='to enhance the System Call  score in Unixbench, improve the system call ability for os'
    target_object7=' the System Callscore in Unixbench and the system call throughput'    
    target8='to enhance the Shell Scripts  score in Unixbench'
    target_object8=' the Shell Scripts score in Unixbench and the Shell Script  throughput'
    
    target_list=[target1, target2, target3, target4, target5, target6, target7, target8]
    target_object_list=[target_object1, target_object2, target_object3, target_object4, target_object5, target_object6, target_object7, target_object8]
    prompt_cycle = len(target_list)
    a_counter = auto_counter(prompt_cycle)
    t=a_counter.read_and_increment()
    print(f"prompt_cycle = {prompt_cycle}")
    print(f"count number = {t}")
    
    target=target_list[t]
    target_object=target_object_list[t]

    talk = Chat()
    print()
    caidan_pool=[]
    caidan=dict([])
    xuanxiang=dict([])
    mul_xuanxiang=dict([])
    val_xuanxiang=dict([])
    bi_xuanxiang=dict([])
    tri_xuanxiang=dict([])
    sub_option=dict([])
    result=dict([]) #Result of the modified options
    result1=dict([])  #Invisible options because subtree is removed
    result2=dict([]) # Originel setting of the modified options
    result_notchange=dict([]) #Options are proposed but not actually modified, because the settings recommended  are the same as the original settings.
    inc=dict([]) #enabled options in proposal
    dec=dict([]) #disabled options in proposal
    pattern = r"^(\d+)\s+(\[\s+\]|\[\*\]|\(.*?\)|\<.*?\>|\({.*?}\)|\-\*\-|\-\-\>)?\s*([A-Za-z].*?)\s*($|\n)"
    pattern1 = r"(.*?)\s+([\[\(\<\{]?(?:on|off|M|\d+|\-\-\>)[\]\)\}\>]?)\s*($|\n)"
    pattern2 = r".*?\(([A-Za-z\_\d\.]+)\)$"
    pattern3 = r"\(\d+\)s*($|\n)" 
    pattern4 = r"\{M\}|\{\*\}"
    pattern5 = r"\<.*?\>"
    pattern6 = r".*?(\d)"
    pattern7 = r"\s*(\[\s+\]|\[\*\]|\(.*?\)|\<.*?\>|\({.*?}\)|\-\*\-|\-\-\>)?\s*([A-Za-z].*?)\s*($|\n)"
    pattern8 = r"\((\d+)\)" 
    pattern9 = r"(.*?)\s*($|\n)"
    pattern10 = r"^(\d+)\s+(\[\s+\]|\[\*\]|\(.*?\)|\<.*?\>|\({.*?}\)|\-\*\-|\-\-\>)?\s*(.*?)\s*($|\n)"
    pattern11 = r".*?\(([A-Za*--z\_\d\.]+)\)\s*\:\s*[\(\[\{\<]?([A-Za-z\_\d\.\-\>]+)[\)\]\}\>]?$"
    pattern12 = r"(\d+)\s+(\[\s+\]|\[\*\]|\(.*?\)|\<.*?\>|\({.*?}\)|\-\*\-|\-\-\>)?\s*([A-Za-z].*?)\s*($|\n)"
    pattern13 = r".*?\(([A-Za*--z\_\d\.]+)\)\s*$"
    caidan_pre=""
    caidan_prompt=f"I want to explore the configuration of the Linux kernel's 'config' to {target}. I will sequentially show you each level of menuconfig's directories, and I need you to tell me which directories are possibly related to {target}  based on your existing knowledge.\
    Here's how I'll show you the directories which is in some level in menuconfig:\n  [number] [directory name] \n  \
    Your response format: \n For relevant directories: [number] [directory name] \n \
    For example，when I give:0 memory setting(mem) \n  1 computer name(Name) \n   your answer :' 0 memory setting(mem) \n' because the memory setting is related to {target} but the name is not. \n  \
    No extra explanations needed. Do not recommend any directory related to Soc selection, device driver , cryptographic,file system, network ,platform type or architecture-depend directories.\
    Do not mention reason.Please obey the rules. Here are some directories,please  recommend:"

    caidan_prompt_first=f"I want to explore the configuration of the Linux kernel's 'config' to {target}. I will sequentially show you each level of menuconfig's directories, and I need you to recommend  directories related to target and filter any directory related to Soc selection, device driver , cryptographic,file system, network ,platform type or architecture-depend directories.\
    Here's how I'll show you the directories which is in some level in menuconfig:\n  [number] [directory name] \n  \
    Your response format: \n For relevant directories: [number] [directory name] \n \
    For example，when I give:0 memory setting(mem) \n  1 driver(d) \n   your answer :' 0 memory setting(mem) \n'   \
    No extra explanations needed. Do not recommend any directory related to Soc selection, device driver , cryptographic,file system, network ,platform type or architecture-depend directories.\
    Do not mention reason.Please obey the rules. Here are some directories,please  recommend:"

    xuanxing_pre1=f" For {target_object}  , analyze each of the following settings separately to determine whether they will increase or decrease {target_object} if the setting is enabled:"
    xuanxiang_pre2=f"Based on the analysis above, provide the options that could potentially affect {target_object} and analyse whether enabling the  settings will increase or decrease {target_object}"
    xuanxiang_prompt=f"According to the above analysis,for the options that could potentially impact {target_object} , determine whether each option will increase or decrease {target_object}, Output format: 'increase: \n Option Name1 \n Option Name2 \n  decrease: \n Option Name1 \n Option Name2'. No explation, no extra useless words. \
    For example，when related option is： IO Schedulers (IOS) \n  DYNAMIC_DEBUG(DD)   \n, the analysis is that IO Schedulers (IOS)   will increase the score and  DYNAMIC_DEBUG(DD)   will decrease the score   your answer : 'increase: \n IO Schedulers (IOS) \n  decrease: \n DYNAMIC_DEBUG(DD)  \n.Output complete name ,for example,output 'IO Schedulers (IOS) ',do not output 'IOS ' only! Complete name is important,you need attention. In the output, the assessment of enabling each option should align with the previous analysis, indicating whether it will increase or decrease {target_object}.\
    Do not mention reason.Do noy output options about network or Peripheral drives, just ignore.The option names should maintain consistent capitalization.  Please obey the rules. Output complete name as I said .please  output:"
   
    mul_xuanxiang_prompt=f"I'm exploring the Linux kernel's menuconfig for configurations to {target}. \
    Here are  multiple 'select one option' choices in menuconfig. Please select one suitable option at a time to potentially {target}. My format:\n [option1 name] \n  \ [option2 name] \n  ..  \n  Your response format: \n '[recommended option name]\n' \n \
    for example:  when I give: 'reveive buffer（rbuf）  \n log buffer(lbuf) \n /// \n  CPU schedule(cs) \n  CPU  default(cd) \n /// \n SLAB (SLAB) \n SLUB (Unqueued Allocator) (SLUB)'. This means there are three   'select one option' choices, and considering to {target} ,your answer is :receive buffer(rbuf)\n CPU schedule(cs) \n SLUB (Unqueued Allocator) (SLUB)\n  \
    Remember to choose the recommended setting to possibly {target} for each option: No extra explanations needed. Only suggest options which may be related. \
    Do not mention reason.Output complete name ,for example,output 'CPU schedule(cs)',do not optput 'cs' only! Complete name is important,you need attention.Please obey the rules. Here are some  'select one option' choices,please choose:"
    bi_xuanxiang_prompt=f"I'm exploring the Linux kernel's menuconfig for configurations that might {target}. \
    Here are  multiple binary choice options in menuconfig. There are two settings for an option: 'M' or 'on', which ‘M’ means configuring this option as a module and 'on' means compiling this option into the kernel image to make it a part of the kernel. .Please set the  options at a time to potentially {target}. My format:\n [option name]   \n  Your response format: \n [option name]  {{M or on}}\n \
    for example:  when I give: 'reveive buffer(rbuf) \n log buffer(lbuf)\n ',your answer is 'receive buffer(rbuf) {{on}} \n log buffer(lbuf) {{M}}' \n  \
    Remember to  recommend settings to possibly {target} for each option: No extra explanations needed. Only suggest options which may be related. \
    Do not mention reason. Please obey the rules. Here are some binary choice options ,please  recommend:"
    tri_xuanxiang_prompt=f"I'm exploring the Linux kernel's menuconfig for configurations that might {target}. \
    Here are  multiple ternary choice options in menuconfig. There are three settings for an option: 'M' ，'on' or 'off', which ‘M’ means configuring this option as a module , 'on' means compiling this option into the kernel image to make it a part of the kernel. and 'off' means disabling this option, not compiling it as a kernel component.Please set the  options at a time to potentially {target}. My format:\n [option name]   \n  Your response format: \n [option name]  <M or on or  off>\n \
    for example:  when I give: 'reveive buffer(rbuf)  \n log buffer(lbuf) \n Debug Filesystem(DFile) ',your answer is 'receive buffer(rbuf) <on> \n  log buffer(lbuf) <M> \n Debug Filesystem(DFile) <off>'   \n  \
    Remember to  recommend settings to possibly {target} for each option: No extra explanations needed. Only suggest options which may be tie to {target}. \
    Do not mention reason. Please obey the rules. Here are some ternary choice options ,please  recommend:"
    val_xuanxiang_prompt=f"I'm exploring the Linux kernel's menuconfig for configurations that might {target}. \
    Here are  multiple numeric  options in menuconfig.I have given you the range of each option value in the information above. Please set the  options at a time to potentially {target}. \
    If the option is not rellated to {target}, then remain the defalut value. \n My format:\n  [option name] (default value)  \n  Your response format: \n [option name] (recommended  value)   \n \
     for example:  when I give: 'maximum CPU number(1=>2 2=>4)  (cpunum) (1)',your answer is 'maximum CPU number(1=>2 2=>4)  (cpunum) (2)'   . Because  when the CPU number is more, the speed is usually better.\n \
    Remember to  recommend settings to possibly {target} for each option: No extra explanations needed. Only suggest options which maybe {target}. \
    Do not mention reason. Do not add units near number in the output.Please obey the rules. Here are some numeric options ,please  recommend: "
    prompt_set=[xuanxiang_prompt,mul_xuanxiang_prompt,val_xuanxiang_prompt,bi_xuanxiang_prompt,tri_xuanxiang_prompt,xuanxiang_prompt]
    next=["",[['root','']]]
    mode=mode #mode=2:Enter more subdirectories  within the first-level directory.
    wb=0 
    we=we #maximum expansion limit for leaf nodes  
    save_cycle=save_cycle

    br=False
    new = [] #save the one which exists newly: 0:option 1:mul_option 2:value_option 3:bi_option 4:tri_option
    for t in range(5):
        new.append(dict([]))
    count=1
    _,c=menu_config.run("load_config .config_base")
    if de==1:
           print('load config:')
           print(c)
         
    while True:
          count+=1                
       
          sta,words = menu_config.run("pwd")
          if de==1:
              print("pwd result")
              print(words)
          words_line=words.split('\n')
          for line_t in words_line:
             matches = re.findall(pattern,line_t)
             if len(matches)==0:
                   continue
             match=matches[0]
             if match[1] == '' :
                   caidan[match[2]] = match[0]
             elif match[1] == '-*-': 
                   menu_config.run(f"{match[0]}")
                   _,content = menu_config.run("pwd")
                   match_t=[]
                   lines = content.split("\n")
                   for t in lines:
                          c=re.findall(pattern10 ,t)
                          if len(c)!=0:
                                match_t.append(c.pop())    
                   is_mul_xuanxiang = False
                   sub_name=dict([])
                   for t in match_t:
                             if t[1] == "-->":
                                       is_mul_xuanxiang = True
                             sub_name[t[2]]=t[1]          
                   if is_mul_xuanxiang == True:
                             mul_xuanxiang[match[2]] = sub_name
                   else:
                             caidan[match[2]] = match[0]
                   menu_config.run("up")
                   menu_config.run("pwd")
             elif match[1] == '[ ]':
                   xuanxiang[match[2]] = '[off]'
             elif match[1] == '[*]': 
                   xuanxiang[match[2]] = '[on]'
                   menu_config.run(f"{match[0]}")
                   _,content=menu_config.run("pwd")
                   match_t = re.findall(pattern12,content)
                   dict_t=dict([])
                   if len(match_t)!=0:
                       is_all_option=True
                       for t in match_t:
                             if t[1] != '[ ]' and t[1] != '[*]':
                                       is_all_option=False                                
                             else:
                                       if t[1] == '[ ]':
                                               dict_t[t[2]] = '[off]'
                                       else:
                                               dict_t[t[2]] = '[on]' 

                       if is_all_option == False:
                              caidan[match[2]] = match[0]
                       else:
                              sub_option.update(dict_t)
                   menu_config.run("up")
                   menu_config.run("pwd")                         
             elif re.match(pattern3, match[1]):
                   val_xuanxiang[match[2]] = match[1]
             elif re.match(pattern4, match[1]):
                   bi_xuanxiang[match[2]] = match[1]
             elif re.match(pattern5, match[1]):
                   tri_xuanxiang[match[2]] = match[1]
             else:
                 print("unexpected match:")
                 print(match[1])
                   

          if len(caidan)!=0:
                   words_caidan = "\n".join([f"{index_t} {name_t}" for name_t,index_t in caidan.items()])
                   if de==1:
                           print("pwd directory")
                           print(words_caidan)
                   if count==2 and mode==2:
                       print("first level mode 2")                           
                       words_caidan = caidan_prompt_first +words_caidan
                   else:
                       words_caidan = caidan_prompt+words_caidan
                   if de==1:
                           print("directory answer:")
                   ans1=talk.ask(words_caidan,6)
  
                   caidan=dict([])
                   mem=next[1]

                   words_line= ans1.split('\n')
                   for line_t in words_line:
                        matches = re.findall(pattern,line_t)
                        if len(matches)==0 :
                               continue
                        match=matches[0]
                        mem_t=mem.copy()
                        mem_t.append([match[2],match[0]])
                        caidan_pool.append([match[2],mem_t])

          option_set=[xuanxiang, mul_xuanxiang, val_xuanxiang, bi_xuanxiang, tri_xuanxiang, sub_option]
          
          iter_number=-1          
          new=[dict([]), dict([]), dict([]), dict([]), dict([])]  #0:xuanxiang 1:mul 2:value 3:bi 4:tri
          while True:
                  if len(option_set[0])==0 and len(option_set[1])==0 and len(option_set[2])==0 and len(option_set[3])==0 and len(option_set[4])==0 and len(option_set[5])==0:
                            if len(new[0])==0 and len(new[1])==0 and len(new[2])==0 and len(new[3])==0 and len(new[4])==0:
                                 break
                            else:
                                  for t in range(5):
                                        option_set[t]=new[t]
                                  new=[dict([]), dict([]), dict([]), dict([]), dict([])]
                  iter_number += 1
                  if iter_number == 6:
                         iter_number = 0
                  if len(option_set[iter_number]) != 0:
                         if iter_number==3 or iter_number==4:
                                words_xuanxiang = "\n".join([name for name in option_set[iter_number].keys()])
                                if de==1:
                                               print('iter_number')
                                               print(iter_number)
                                               print("pwd bi/tri option:")
                                               print(words_xuanxiang)
                                words_xuanxiang = prompt_set[iter_number]+words_xuanxiang
                                if de==1:
                                               print("option answer:")
                                        
                                ans2=talk.ask(words_xuanxiang,iter_number)
                         if iter_number==0 or  iter_number==5:
                                 num=len(option_set[iter_number])//15
                                 if len(option_set[iter_number])%15!=0:
                                                num+=1
                                 dic=[]
                                 for i in range(num):
                                       dic.append({})
                                 t=0
                                 for key, value in option_set[iter_number].items():
                                          if len(dic[t])<15:
                                                dic[t][key]=value
                                          else:
                                                t+=1
                                                dic[t][key]=value
                                 ans2=""
                                
                                 for i in range(num):
                                          words_xuanxiang = "\n".join([f"{name}" for name,se in dic[i].items()])
                                          if de==1:
                                               print('iter_number')
                                               print(iter_number)
                                               print("pwd option:")
                                               print(words_xuanxiang)
                                          words_xuanxiang = xuanxing_pre1+words_xuanxiang
                                            
                                          if de==1:
                                               print("option answer:")
                                        
                                          talk.ask(words_xuanxiang,iter_number)
                                          talk.ask(xuanxiang_pre2,iter_number)
                                          ans_t=talk.ask(xuanxiang_prompt,iter_number)
                                          first_try=1
                                          while True:
                                                        
                                                        lines = ans_t.split('\n')

                                                        check=False
                                                        for line in lines:
                                                                if line == "increase:" or line == "Increase:" or line == "decrease:" or line == "Decrease:":
                                                                       pass
                                                                elif line:
                                                                       if line.startswith("- "):
                                                                                line = line[2:]
                                                                       res=re.findall(pattern13,line)
                                                                       if len(res)==1:
                                                                                 check=True

                                                        if check==False:
                                                               talk.last_step(iter_number,first_try)
                                                               if de==1:
                                                                   print(f'name is uncompleted, retry {first_try}')
                                                               ans_t=talk.ask('the name that your output is uncompleted,format:name(xx), please output complete name,retry:',iter_number)
                                                               first_try+=1
                                                               if first_try<5:
                                                                       continue

                                                        processing_increase = False
                                                        processing_decrease = False
                                                        inc_t=dict([])
                                                        dec_t=dict([])
                                                        for line in lines:
                                                                    line = line.strip()
                                                                    if line == "increase:" or line == "Increase:":
                                                                        processing_increase = True
                                                                        processing_decrease = False
                                                                    elif line == "decrease:" or line == "Decrease:":
                                                                        processing_increase = False
                                                                        processing_decrease = True
                                                                    elif line:
                                                                        if line.startswith("- "):
                                                                                line = line[2:]                                                                        
                                                                        res=re.findall(pattern13,line)
                                                                        if len(res)!=0:
                                                                                if processing_increase:
                                                                                                inc_t[line]='[on]'
                                                                                elif processing_decrease:
                                                                                                dec_t[line]='[off]'

                                                        if check==True or first_try>4:
                                                               break
                                                                        
                                          ans2+= "\n".join([f"{name} {se}" for name,se in inc_t.items()])
                                          ans2+="\n"
                                          ans2+= "\n".join([f"{name} {se}" for name,se in dec_t.items()])
                                          inc.update(inc_t)
                                          dec.update(dec_t)
                                          if  i!=num-1:
                                                ans2+="\n"
                                 if de==1:
                                       print("total option answer:")
                                 print(ans2)
                         if iter_number==1:
                                 words_xuanxiang=""
                    
                                 for name,item in option_set[iter_number].items():
                                         words_xuanxiang += "\n".join([name for name in item.keys()]) 
                                         words_xuanxiang +='\n///\n'
                                 words_xuanxiang=words_xuanxiang[:-5]
                                 if de==1:
                                        print('iter_number')
                                        print(iter_number)
                                        print("pwd option:")
                                        print(words_xuanxiang)
                                 words_xuanxiang = prompt_set[iter_number]+words_xuanxiang

                                 if de==1:
                                      print("option answer:")
                                 ans2=talk.ask(words_xuanxiang,iter_number)

                                 mat1=re.findall(pattern9,ans2)
                                 ans2=""
                                 for i, m in enumerate(mat1):
                                         if i != len(mat1) - 1:
                                              ans2+=f"{m[0]} -->\n"
                                         else :
                                              ans2+=m[0]
                                 print("mul answer")
                                 print(ans2)  
                         if iter_number==2:
                                words_xuanxiang = "\n".join([f"{name} {item}" for name,item in option_set[iter_number].items()])
                        
                                if de==1:
                                        print('iter_number')
                                        print(iter_number)
                                        print("pwd option:")
                                        print(words_xuanxiang)
                                help_info=""
                                for name,_ in option_set[iter_number].items():
                                         t = re.findall(pattern2, name)
                                         if len(t)==0:
                                                 continue
                                         name_t = t[0]                                  
                                         _,he=menu_config.run(f"{name_t}")
                                         help_info+=he+"\n"
                                words_xuanxiang = "Here is value options information:"+help_info+prompt_set[iter_number]+words_xuanxiang

                                if de==1:                                      
                                        print("option answer:")
                                ans2=talk.ask(words_xuanxiang,iter_number)
                               
                                

                         ans2_filter = re.findall(pattern1,ans2)
                         
                                                                           
                         remove=set({})
                         for match in ans2_filter:
                              if match[0] in remove:
                                  continue   
                              unchanged=False      
                                              
                              if iter_number in [0,2,3,4,5]:  #when the recommodation is similar to the origin
                                   if  match[0] not in option_set[iter_number]:
                                             print('key error:')
                                             print(option_set[iter_number])
                                             print(match[0])
                                             continue    
                                   if option_set[iter_number][match[0]]== match[1]:
                                                 result_notchange[match[0]] = match[1]
                                                 unchanged=True   
                                   else:
                                           result2[match[0]] = option_set[iter_number][match[0]]                 
                                              
                              elif  iter_number in [1] :
                                   for mul in option_set[iter_number].values():
                                          if match[0] in mul and mul[match[0]]==match[1]:
                                                unchanged=True   
                                                result_notchange[match[0]] = match[1]
                                          if match[0] in mul and mul[match[0]]!=match[1]:
                                                 result2[match[0]] = mul[match[0]]   

                              if unchanged==False:
                                  t = re.findall(pattern2, match[0])
                                  if len(t)==0:
                                      continue
                                  name_t = t[0]
                                  _, vis = menu_config.run(f"vis {name_t}")
                                  t = re.findall(pattern6, vis)    
                                  if len(t)==0:
                                      print('vis name error')
                                      continue
                                  visibility_t = t[0]
                                  if visibility_t == "1":
                                      print(f"visible is 1: {name_t}")

                                  if visibility_t == "0":
                                      print(f"visible is 0: {name_t}")
                                      result1[match[0]] = match[1]
                                    
                                  if visibility_t == "2" or visibility_t == "1":     #only when visible                     
                                       result[match[0]] = match[1]
                                       if iter_number in {0, 1, 3, 4, 5} and match[1] in {'[on]','-->'}:     
                                                 menu_config.run(f"write {name_t} y")
                                       elif iter_number in {0, 3, 4, 5} and match[1]=='[off]':     
                                                 menu_config.run(f"write {name_t} n")
                                       elif iter_number ==4 and match[1]=='M':     
                                                 menu_config.run(f"write {name_t} m")
                                       elif iter_number ==2:
                                                 t = re.findall(pattern8,match[1])  
                                                 menu_config.run(f"write {name_t} {t[0]}")
                                       _, option_state = menu_config.run("get_last_changes") #option_state:[0->2, 2->0]
                                      
                                       if de==2:
                                             print("option_state0")
                                             print(option_state[0])
                                             print("option_state1")
                                             print(option_state[1])
                                             print("option_state2")
                                             print(option_state[2])
                                             print("option_state3")
                                             print(option_state[3])

                                       if de==1:
                                             print("option_state2")
                                             print(option_state[2])
                                             print("option_state3")
                                             print(option_state[3])
                                       for option in option_state[0]:
                                           mat_t = re.findall(pattern7, option)
                                           mat_t = mat_t[0]
                                           if mat_t[0] == '[ ]':
                                                 new[0][mat_t[1]] = '[off]'
                                           elif mat_t[0] == '[*]':
                                                 new[0][mat_t[1]] = '[on]'                                      
                                           elif re.match(pattern3, mat_t[0]): #value
                                                 new[2][mat_t[1]] = mat_t[0]                                                 
                                           elif re.match(pattern4, mat_t[0]):
                                                 new[3][mat_t[1]] = mat_t[0]
                                           elif re.match(pattern5, mat_t[0]):
                                                 new[4][mat_t[1]] = mat_t[0]
                                           else:  
                                               pass     
                                       for option in option_state[1]:
                                           mat_t = re.findall(pattern7, option)
                                           mat_t = mat_t[0]
                                           remove.add(mat_t[1])
                                           if mat_t[0] == '[ ]' or mat_t[0] == '[*]':
                                                 if mat_t[1] in option_set[0]:
                                                     del option_set[0][mat_t[1]] 
                                                 if mat_t[1] in new[0]:
                                                     del new[0][mat_t[1]]
                                                 if mat_t[1] in option_set[5]:
                                                     del option_set[5][mat_t[1]]
                                           elif re.match(pattern3, mat_t[0]): #value
                                                 if mat_t[1] in option_set[2]:
                                                     del option_set[2][mat_t[1]]
                                                 if mat_t[1] in new[2]:
                                                     del new[2][mat_t[1]]
                                           elif re.match(pattern4, mat_t[0]):
                                                 if mat_t[1] in option_set[3]:  
                                                     del option_set[3][mat_t[1]]
                                                 if mat_t[1] in new[3]:
                                                     del new[3][mat_t[1]]
                                           elif re.match(pattern5, match[0]):
                                                 if mat_t[1] in option_set[4]:
                                                     del option_set[4][mat_t[1]]
                                                 if mat_t[1] in new[4]:
                                                     del new[4][mat_t[1]]
                                           else:
                                               pass  
                                                                          
                                       for option in option_state[2]:
                                                            mul_name=''
                                                            sub_name=dict([])
                                                            words_line= option.split('\n')
                                                            for line_t in words_line:
                                                                            matches = re.findall(pattern7,line_t)
                                                                            if len(matches)==0:
                                                                                continue
                                                                            match=matches[0]
                                                                            if match[0]=='-*-':
                                                                                   mul_name=match[1]
                                                                            else:
                                                                                   sub_name[match[1]]=match[0]
                                                            if len(sub_name)!=0:
                                                                      new[1][mul_name] = sub_name
                                                                      if de==1:
                                                                                    print('option_state2:subname')
                                                                                    print(sub_name)                                                   

                                       for t in option_state[3].keys():
                                                          t = re.findall(pattern7, t)
                                                          t=t[0]
                                                          if t in option_set[1]:
                                                                for j_t in option_state[3].values():
                                                                      j_t  = re.findall(pattern7, j_t)
                                                                      j_t =j_t[0]   
                                                                      if j_t in  option_set[1][t]:
                                                                                 del option_set[1][t][j_t]
                                                          if t in new[1]:
                                                                for j_t in option[t]:
                                                                      j_t  = re.findall(pattern7, j_t)
                                                                      j_t =j_t[0]  
                                                                      if j_t in new[1][t]:
                                                                                 del new[1][t][j_t]

                                                
                         option_set[iter_number]=dict([])                
                    

          if len(caidan_pool)==0:
              br=True
          else: 
              cond = True
              up_type=0
              while cond:              
                            if up_type==0:
                                        le=len(next[1])
                                        if le>1:
                                                for i in range(le-1):
                                                        menu_config.run("up")
                                        if de==1:
                                            print("up finish")
                            else:
                                      for j in range(i):
                                            print(next[1][j])
                                      for j in range(i-1):
                                            menu_config.run("up")
                                      if de==1:
                                              print("not exit: up finish")
                                      up_type=0
                            next=caidan_pool.pop()
                            if de==1:
                                print("go into next directory")
                                print(next)
                            i=0
                            leng=len(next[1])
                            for action in next[1]:
                                i+=1
                                if action[0]=="root":
                                            continue
                                _,con=menu_config.run("pwd")
                               
                                t=[]
                                ok=False
                                
                                words_line=con.split('\n')
                                for line_t in words_line:
                                       matches = re.findall(pattern,line_t)
                                       if len(matches)==0:
                                              continue
                                       match=matches[0]                                
                                       if match[2]==action[0]:  
                                                sta,_=menu_config.run(match[0])
                                                if de==1:
                                                    print("actual number")
                                                    print(match[0])
                                                    print("mem number")
                                                    print(action[1])
                                                    
                                                if sta==False:
                                                    print("error")
                                                    print(_)
                                                    break
                                                else:
                                                    ok=True                                                
                                                    break
                                
                                if ok==False:
                                        break
                            if ok== True and i==leng:
                                        cond = False
                            if ok==False:
                                    print("option does not exit anymore:")
                                    _,con=menu_config.run("pwd")
                                    print(con)
                                    up_type=1


          if sta==False:
                print("error,exit!")
                break

          wb+=1

          if wb%save_cycle==0 or br==True or wb==we:
                 with open("output.txt", "w") as file:     #Result of the modified options
                         for key, value in result.items():
                                    file.write(f"{key}: {value}\n")
                 file.close()
                 with open("output1.txt", "w") as file:    
                           for key, value in result_notchange.items():
                                    file.write(f"{key}: {value}\n")
                 file.close()
                 with open("output2.txt", "w") as file:
                           for key, value in result2.items():
                                    file.write(f"{key}: {value}\n")
                 file.close()
                 with open("inc.txt", "w") as file:
                           for key, value in inc.items():
                                    file.write(f"{key}: {value}\n")
                 file.close()
                 with open("dec.txt", "w") as file:
                           for key, value in dec.items():
                                    file.write(f"{key}: {value}\n")
                 file.close()

          if wb==we:
              print("up to iteration limit")
              break

          if br==True:
              print("finish iteration ")
              break

          xuanxiang=dict([])
          mul_xuanxiang=dict([])
          val_xuanxiang=dict([])
          bi_xuanxiang=dict([])
          tri_xuanxiang=dict([])
          sub_option=dict([])

          time.sleep(1)
    
       
if __name__ == '__main__':
    fire.Fire(main)
