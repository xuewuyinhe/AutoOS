#!/usr/bin/env python3

from __future__ import print_function
from itertools import chain
from kconfiglib import Kconfig, Symbol, MENU, COMMENT, BOOL, TRISTATE, STRING, INT, HEX, UNKNOWN, expr_value, TRI_TO_STR

class MenuConfig:
    def __init__(self, kconfig_file):
        self.kconf = Kconfig(kconfig_file)
        self.current_node = self.kconf.top_node
        self.stack = []
        self.my_list = []
        self.last_changes=""
        self.to_visible=[]
        self.to_invisible=[]
        self.choices_to_vis=[]
        self.choices_to_invis={}
        self.parent_name=[]


    def indent_print(self, s, indent):
        save = (indent * " " + s)
        return save

    def value_str(self,sc):
        """
        Returns the value part ("[*]", "<M>", "(foo)" etc.) of a menu entry.

        sc: Symbol or Choice.
        """
        if sc.type in (STRING, INT, HEX):
            return "({})".format(sc.str_value)

        # BOOL or TRISTATE

        # The choice mode is an upper bound on the visibility of choice symbols, so
        # we can check the choice symbols' own visibility to see if the choice is
        # in y mode
        if isinstance(sc, Symbol) and sc.choice and sc.visibility == 2:
            # For choices in y mode, print '-->' next to the selected symbol
            return "-->" if sc.choice.selection is sc else "   "

        tri_val_str = (" ", "M", "*")[sc.tri_value]

        if len(sc.assignable) == 1:
            # Pinned to a single value
            return "-{}-".format(tri_val_str)

        if sc.type == BOOL:
            return "[{}]".format(tri_val_str)

        if sc.type == TRISTATE:
            if sc.assignable == (1, 2):
                # m and y available
                return "{" + tri_val_str + "}"  # Gets a bit confusing with .format()
            return "<{}>".format(tri_val_str)

    def sub_choice(self,sc):
        res=""
        for node in sc.nodes:
            if node.prompt:
                    prompt, prompt_cond = node.prompt
                    ans =1
                    if self.get_type(sc)=="CHOICE":
                        for tmp in self.parent_name:
                            if tmp ==node.parent:
                                ans=0
                        if ans==0:
                            continue;
                        self.parent_name.append(node.parent)
                        res+=self.show_menuconfig(node.parent)
                        print(res)


    def add_choice(self,sc):
        res=""
        for node in sc.nodes:
            if node.prompt:
                    #print(self.node_str(node))
                    #print("    "+self.node_str(node.parent))
                    prompt, prompt_cond = node.prompt
                    ans =1
                    if self.get_type(sc)=="CHOICE":
                        for tmp in self.parent_name:
                            if tmp ==node.parent:
                                ans=0
                        if ans==0:
                            continue;
                        self.parent_name.append(node.parent)
                        res+=self.show_menuconfig(node.parent)
        return res

    def add_sub_choice(self,sc):
        for node in sc.nodes:
            if node.prompt:
                    #print(self.node_str(node))
                    #print("    "+self.node_str(node.parent))
                    prompt, prompt_cond = node.prompt
                    if self.get_type(sc)=="CHOICE":
                        value = self.choices_to_invis.get(self.invis_node_str(node.parent))
                        if value is not None:
                            value.append(self.sc_str(sc))
                        else:
                            self.choices_to_invis[self.invis_node_str(node.parent)]=[self.sc_str(sc)]

    def invis_node_str(self,node):
        """
        Returns the complete menu entry text for a menu node, or "" for invisible
        menu nodes. Invisible menu nodes are those that lack a prompt or that do
        not have a satisfied prompt condition.

        Example return value: "[*] Bool symbol (BOOL)"

        The symbol name is printed in parentheses to the right of the prompt. This
        is so that symbols can easily be referred to in the configuration
        interface.
        """
        if not node.prompt:
            return ""

        # Even for menu nodes for symbols and choices, it's wrong to check
        # Symbol.visibility / Choice.visibility here. The reason is that a symbol
        # (and a choice, in theory) can be defined in multiple locations, giving it
        # multiple menu nodes, which do not necessarily all have the same prompt
        # visibility. Symbol.visibility / Choice.visibility is calculated as the OR
        # of the visibility of all the prompts.
        prompt, prompt_cond = node.prompt

        if node.item == MENU:
            return "    " + prompt

        if node.item == COMMENT:
            return "    *** {} ***".format(prompt)

        # Symbol or Choice

        sc = node.item

        if sc.type == UNKNOWN:
            # Skip symbols defined without a type (these are obscure and generate
            # a warning)

            return ""
        # {:3} sets the field width to three. Gives nice alignment for empty string
        # values.
        res = "{:3} {}".format(self.value_str(sc), prompt)

        # Don't print the name for unnamed choices (the normal kind)
        if sc.name is not None:
            res += " ({})".format(sc.name)

        return res
    def sc_str(self,sc):
        for node in sc.nodes:
            if node.prompt:
                    #print(self.node_str(node))
                    #print("    "+self.node_str(node.parent))
                    prompt, prompt_cond = node.prompt
        if sc.type == UNKNOWN:
            # Skip symbols defined without a type (these are obscure and generate
            # a warning)

            return ""
        res =""
        # {:3} sets the field width to three. Gives nice alignment for empty string
        # values.
        res = "{:3} {}".format(self.value_str(sc), prompt)

        # Don't print the name for unnamed choices (the normal kind)
        if sc.name is not None:
            res += " ({})".format(sc.name)
        return res


    def node_str(self,node):
        """
        Returns the complete menu entry text for a menu node, or "" for invisible
        menu nodes. Invisible menu nodes are those that lack a prompt or that do
        not have a satisfied prompt condition.

        Example return value: "[*] Bool symbol (BOOL)"

        The symbol name is printed in parentheses to the right of the prompt. This
        is so that symbols can easily be referred to in the configuration
        interface.
        """
        if not node.prompt:
            return ""

        # Even for menu nodes for symbols and choices, it's wrong to check
        # Symbol.visibility / Choice.visibility here. The reason is that a symbol
        # (and a choice, in theory) can be defined in multiple locations, giving it
        # multiple menu nodes, which do not necessarily all have the same prompt
        # visibility. Symbol.visibility / Choice.visibility is calculated as the OR
        # of the visibility of all the prompts.
        prompt, prompt_cond = node.prompt
        if not expr_value(prompt_cond):
            return ""

        if node.item == MENU:
            return "    " + prompt

        if node.item == COMMENT:
            return "    *** {} ***".format(prompt)

        # Symbol or Choice

        sc = node.item

        if sc.type == UNKNOWN:
            # Skip symbols defined without a type (these are obscure and generate
            # a warning)

            return ""
        # {:3} sets the field width to three. Gives nice alignment for empty string
        # values.
        res = "{:3} {}".format(self.value_str(sc), prompt)

        # Don't print the name for unnamed choices (the normal kind)
        if sc.name is not None:
            res += " ({})".format(sc.name)

        return res

    def is_visible(self,node):
        str=self.node_str(node)
        if str=="":
            return False
        return True

    def print_menuconfig_nodes(self,node, indent):
        save =""
        while node:
            string = self.node_str(node)
            if string:
                save+="\n"+self.indent_print(string, indent)

            if node.list:
                save+="\n"+self.print_menuconfig_nodes(node.list, indent + 8)

            node = node.next
        return save

    def show_menuconfig_top_node(self, node, indent):
        """
        Prints a tree with all the menu entries rooted at 'node'. Child menu
        entries are indented.
        """
        save=""
        while node:
            string = self.node_str(node)
            if string:
                save +="\n"+self.indent_print(string, indent)
            node = node.next
        return save

    def print_menuconfig_top_node(self, node, indent):
        """
        Prints a tree with all the menu entries rooted at 'node'. Child menu
        entries are indented.
        """
        self.my_list.clear()
        index = 0;
        index_real = 0;
        save=""
        while node:
            string = self.node_str(node)
            if string:
                prefix = str(index)+"    "
                index = index+1
                save +="\n"+self.indent_print(prefix+string, indent)
                self.my_list.append(index_real)
            index_real=index_real+1
            node = node.next
        return save

    def show_menuconfig(self,node):
        """
        Prints all menu entries for the configuration.
        """
        # Print the expanded mainmenu text at the top. This is the same as
        # kconf.top_node.prompt[0], but with variable references expanded.
        string = self.node_str(node)
        save=""
        if string:
            save += "\n"+ self.indent_print(string, 0)
        save += "\n"+ self.show_menuconfig_top_node(node.list, 8) + "\n"
        return save

    def print_menuconfig(self,node):
        """
        Prints all menu entries for the configuration.
        """
        # Print the expanded mainmenu text at the top. This is the same as
        # kconf.top_node.prompt[0], but with variable references expanded.
        save = ("\n======== {} ========\n".format(self.kconf.mainmenu_text))
        string = self.node_str(node)
        if string:
            save += "\n"+ self.indent_print(string, 0)
        save += "\n"+ self.print_menuconfig_top_node(node.list, 0) + "\n"
        return save

    def get_type(self,sc):
        _BOOL_TRISTATE=frozenset({
            BOOL,
            TRISTATE,
        })
        type_name={
            BOOL : "BOOL",
            STRING:"STRING",
            TRISTATE:"TRISTATE",
            _BOOL_TRISTATE:"BOOL and TRISTATE",
            HEX:"HEX",
            INT:"INT",
            999:"CHOICE"
        }
        if isinstance(sc, Symbol) and sc.choice :
            return "CHOICE"
        return  type_name.get(sc.type,"UNKNOWN")
    def get_visibility(self,sc):
        return True, "config "+sc.name+" has visibility: "+str(sc.visibility)

    def set_value(self,sc,val):
        if sc.type == HEX and not val.startswith(("0x", "0X")):
            val = "0x" + val

        # Let Kconfiglib itself print a warning here if the value is invalid. We
        # could also disable warnings temporarily with 'kconf.warn = False' and
        # print our own warning.

        # Create a dictionary to store the visibility status of options (where True means visible and False means invisible)
        visibility_before = {option: option.visibility for option in chain(self.kconf.syms.values(),self.kconf.named_choices.values())}

       
        res=sc.set_value(val)

        
        visibility_after = {option: option.visibility for option in self.kconf.syms.values()}


        self.last_changes=""
        dic={}
        #Compare the changes in visibility status before and after
        for option_name, is_visible_before in visibility_before.items():
            is_visible_after = visibility_after[option_name]
            if is_visible_before != is_visible_after:
                dic[option_name]=is_visible_after*is_visible_after-is_visible_before*is_visible_before
                #self.last_changes+= (f"Option {option_name}: Visibility changed from {is_visible_before} to {is_visible_after}")
                #self.last_changes+="\n"
        _BOOL_TRISTATE=frozenset({
            BOOL,
            TRISTATE,
        })
        type_name={
            BOOL : "BOOL",
            STRING:"STRING",
            TRISTATE:"TRISTATE",
            _BOOL_TRISTATE:"BOOL and TRISTATE",
            HEX:"HEX",
            INT:"INT",
            999:"CHOICE"
        }
        from02=""
        from20=""
        from10=""
        from01=""
        from12=""
        from21=""
        self.to_visible=[]
        self.to_invisible=[]
        self.parent_name.clear()
        self.choices_to_invis.clear()
        self.choices_to_vis.clear()
        for _type in type_name.values():
            for key1,value in dic.items():
                if self.get_type(key1)!=_type:
                    continue
                key=" "+self.get_type(key1)+"  "+self.sc_str(key1)
                #print(self.value_str(key1))
                #print(key1.config_string)

                if self.get_type(key1)=="CHOICE" :
                    if value>0:
                        str=self.add_choice(key1)
                        if str:
                            self.choices_to_vis.append(str)
                    else :
                        self.add_sub_choice(key1)
                    continue

                if value==-4:
                    from20+=key+"\n"
                    self.to_invisible.append(self.sc_str(key1))
                elif value==4:
                    from02+=key+"\n"
                    self.to_visible.append(self.sc_str(key1))
                elif value ==-1:
                    from10+=key+"\n"
                    self.to_invisible.append(self.sc_str(key1))
                elif value==1:
                    from01+=key+"\n"
                    self.to_visible.append(self.sc_str(key1))
                elif value==3:
                    from12=key+"\n"
                elif value==-3:
                    from21=key+"\n"
        if from20!="":
            self.last_changes+="change from 2 to 0"+"\n"+from20
        if from02!="":
            self.last_changes+="change from 0 to 2"+"\n"+from02
        if from10!="":
            self.last_changes+="change from 1 to 0"+"\n"+from10
        if from01!="":
            self.last_changes+="change from 0 to 1"+"\n"+from01
        if from12!="":
            self.last_changes+="change from 1 to 2"+"\n"+from12
        if from21!="":
            self.last_changes+="change from 2 to 1"+"\n"+from21
        return  res


    def get_last_changes(self):
        return self.last_changes

    def get_value_from_user(self, sc):
        """
        Prompts the user for a value for the symbol or choice 'sc'. For
        bool/tristate symbols and choices, provides a list of all the assignable
        values.
        """
        save = ""
        # if not sc.visibility:
        #     save = (sc.name + " is not currently visible")
        #     return False,save

        prompt = "Value for {}".format(sc.name)
        if sc.type in (BOOL, TRISTATE):
            prompt += " (available: {})" \
            .format(", ".join(TRI_TO_STR[val] for val in sc.assignable))
        prompt += ": "

        save = (sc)
        save=str(save)+"\n"+str(prompt)

        #save +="\n"+ ("value = " +sc.str_value)
        #save +="\n"+("visibility = "+TRI_TO_STR[sc.visibility])
        #save +="\n"+("currently assignable vaulus : " +
        #        ", ".join([TRI_TO_STR[v] for v in sc.assignable]))

        # Let Kconfiglib itself print a warning here if the value is invalid. We
        # could also disable warnings temporarily with 'kconf.warn = False' and
        # print our own warning.
        return True,save

    def run(self,cmd):
        #self.print_menuconfig(self.current_node)
        save = ""
        state = True
        if cmd:
            cmd_list = cmd.split()
            if cmd == "help" :
                save+="\nusage:\n"
                save+="help                     #help\n"
                save+="up                       \n"
                save+="pwd                      \n"
                save+="0                        \n"
                save+="config_name              #Return detailed information and instructions on how to set it.\n"
                save+="write config_name y      #write \n"
                save+="load_config  file_name   #file_name is the name you want to load, for example, .config (added: load .config file)\n"
                save+="write_config file_name   #Save the current file as file_name\n"
                save+="last_changes             #Return the nodes that have changed since the most recent config modification.\n"
                save+="vis config_name          #config_name is the name of the node whose visibility you want to check.\n"
                state=True
            elif cmd == "up":  #go to upper node
                if len(self.stack) == 0:
                    save +=("Already at the top layer")
                    state = False
                else:
                    self.current_node = self.stack.pop()
                    state = True
                    save ="Return up-node successfully"
            elif cmd == "ls": #print all nodes
                save+=self.print_menuconfig_nodes(self.current_node, 0)
            elif cmd =="pwd": #pwd subnodes
                save+=self.print_menuconfig(self.current_node)
            elif cmd=="last_changes":
                save+=self.get_last_changes()
            elif cmd=="get_last_changes":
                save=[self.to_visible,self.to_invisible,self.choices_to_vis,self.choices_to_invis]
            elif cmd.isdigit(): 
                node = self.current_node.list
                if not node:
                    save = ("Error: no child node")
                    state = False
                    return state,save
                index = self.my_list[int(cmd)]
                while index > 0:
                    node = node.next
                    index = index - 1
                if node:
                    self.stack.append(self.current_node)
                    self.current_node = node
                else:
                    save = ("Error: Wrong number,Please enter again!")
                    state = False
                if state == True:
                    save = "Enter sub-node suscessfully"
            elif cmd_list[0] == "load_config":
                config_filename=cmd_list[1]
                try:
                        # Returns a message telling which file got loaded
                    save=(self.kconf.load_config(config_filename))
                    state=True
                except EnvironmentError as e:
                    save=e
                    state=False
            elif cmd_list[0] =="write_config": 
                config_filename=cmd_list[1]
                try:
                    # Returns a message telling which file got saved
                    save=(self.kconf.write_config(config_filename))
                    state = True
                except EnvironmentError as e:
                    save=e
                    state = False
            elif cmd in self.kconf.syms: 
                state,save=self.get_value_from_user(self.kconf.syms[cmd])
            elif cmd in self.kconf.named_choices:
                state,save=self.get_value_from_user(self.kconf.named_choices[cmd])
            elif cmd_list[0] == "write": 
                if len(cmd_list) != 3:
                    save+= "CHECK write-commline-line "
                    return False,save
                if cmd_list[1] in self.kconf.syms:
                    state=self.set_value(self.kconf.syms[cmd_list[1]],cmd_list[2])
                    save="write ok"
                elif cmd_list[1] in self.kconf.named_choices:
                    state=self.set_value(self.kconf.named_choices[cmd_list[1]],cmd_list[2])
                    save ="write ok"
                else:
                    state=False
                    save = "No such symbol/choice to write"
            elif cmd_list[0] =="vis": #check the visibility of nodes (or options) 
                if cmd_list[1] in self.kconf.syms:
                    state,save=self.get_visibility(self.kconf.syms[cmd_list[1]])
                elif cmd_list[1] in self.kconf.named_choices:
                    state,save=self.set_value(self.kconf.named_choices[cmd_list[1]],cmd_list[2])
                else:
                    state=False
                    save="No symbol/choice named '{}' in the configuration".format(cmd_list[1])
            else:
                state = False
                save = ("No symbol/choice named '{}' in the configuration".format(cmd))
            return state,save
