#!/usr/bin/python
'''
DUI's management of CLI commands and navigation tree

Author: Luis Fuentes-Montero (Luiso)
With strong help from DIALS and CCP4 teams

copyright (c) CCP4 - DLS
'''

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import os
import sys
import pickle
from cli_utils import print_list, TreeShow, DialsCommand, \
     generate_report, build_command_lst, get_next_step

class UniStep(object):
    dials_com_lst = [
    'import',
    'find_spots',
    'index',
    'refine_bravais_settings',
    'reindex',
    'refine',
    'integrate',
    'export',
    ]

    def __init__(self, prev_step = None):
        self.lin_num = 0
        self.next_step_list = []
        self.prev_step = prev_step
        self.command_lst = [None]
        self.success = None
        self.pickle_file_out = None
        self.json_file_out = None
        self.phil_file_out = None
        self.report_out = None
        self.dials_comand = DialsCommand()

        self.work_dir = os.getcwd()


    def __call__(self, cmd_lst, ref_to_class):
        self.command_lst = cmd_lst
        if(cmd_lst[0] == "fail"):
            #testing virtual failed step
            print "\n intentionally FAILED for testing \n"
            self.success = False

        else:
            if(cmd_lst[0] in self.dials_com_lst):
                self.build_command(cmd_lst)
                self.success = self.dials_comand( lst_cmd_to_run = self.cmd_lst_to_run,
                                                 ref_to_class = ref_to_class)

                if(self.success == True):
                    #print "#generate_report(self)"
                    self.report_out = generate_report(self)

            else:
                print "NOT dials command"
                self.success = False

    def edit_list(self, cmd_lst):
        self.command_lst = cmd_lst

    def build_command(self, cmd_lst):

        self.cmd_lst_to_run = build_command_lst(self, cmd_lst)
        print "\n cmd_lst_to_run =", self.cmd_lst_to_run, "\n"

    def get_next_step(self):
        return get_next_step(self)

class Runner(object):

    def __init__(self):
        root_node = UniStep(prev_step = None)
        root_node.success = True
        root_node.command_lst = ["Root"]
        self.step_list = [root_node]
        self.bigger_lin = 0
        self.current_line = self.bigger_lin
        self.create_step(root_node)

    def run(self, command, ref_to_class, mk_nxt = True):

        if(type(command) is str):
            cmd_lst = command.split()
        else:
            cmd_lst = command

        if(cmd_lst[0] == "goto"):
            self.goto(int(cmd_lst[1]))

        elif(cmd_lst[0] == "slist"):
            self.slist()

        elif(cmd_lst[0] == "clean"):
            self.clean()

        elif(cmd_lst[0] == "mkchi"):
            self.create_step(self.step_list[self.current_line])

        elif(cmd_lst[0] == "mksib"):
            old_command_lst = self.step_list[self.current_line].command_lst
            self.goto_prev()
            print "forking"
            self.create_step(self.step_list[self.current_line])
            self.step_list[self.current_line].edit_list(old_command_lst)

        else:
            if(self.step_list[self.current_line].success == True):
                self.goto_prev()
                print "forking"
                self.create_step(self.step_list[self.current_line])

            self.step_list[self.current_line](cmd_lst, ref_to_class)
            if(self.step_list[self.current_line].success == True and mk_nxt == True):
                self.create_step(self.step_list[self.current_line])

            else:
                print "failed step"

    def clean(self):
        print "\n Cleaning"
        print "self.current_line =", self.current_line

        lst_to_rm = []

        for node in self.step_list:
            if(node != self.step_list[self.current_line] and node.success == None):
                lst_to_rm.append(node.lin_num)

        print "lst_to_rm:\n", lst_to_rm

        for n_lin in lst_to_rm:
            self.step_list[n_lin].prev_step.next_step_list.remove(self.step_list[n_lin])
            self.step_list.remove(self.step_list[n_lin])

        print "self.current_line =", self.current_line, "\n"

    def create_step(self, prev_step):
        new_step = UniStep(prev_step = prev_step)
        self.bigger_lin += 1
        new_step.lin_num = self.bigger_lin
        prev_step.next_step_list.append(new_step)
        self.step_list.append(new_step)
        self.goto(self.bigger_lin)

    def goto_prev(self):
        try:
            self.goto(self.step_list[self.current_line].prev_step.lin_num)

        except:
            print "can NOT fork <None> node "

    def goto(self, new_lin):
        self.current_line = new_lin

    def get_html_report(self):
        if(self.step_list[self.current_line].success == True):
            html_rep = self.step_list[self.current_line].report_out

        else:
            try:
                html_rep = self.step_list[self.current_line].prev_step.report_out

            except:
                html_rep = None

        return html_rep

    def get_datablock_path(self):

        tmp_cur = self.step_list[self.current_line]
        path_to_json = None

        while True:
            if(tmp_cur.command_lst == [None]):
                tmp_cur = tmp_cur.prev_step

            elif(tmp_cur.success == True and tmp_cur.command_lst[0] == "import"):
                path_to_json = tmp_cur.json_file_out
                break

            elif(tmp_cur.command_lst[0] == "Root" or tmp_cur.success == False):
                break

            else:
                tmp_cur = tmp_cur.prev_step


        return path_to_json

    def get_experiment_path(self):
        path_to_json = None
        tmp_cur = self.step_list[self.current_line]
        if(tmp_cur.command_lst == [None]):
           tmp_cur = tmp_cur.prev_step

        if(tmp_cur.command_lst[0] != "Root" and
          tmp_cur.command_lst[0] != "import" and
          tmp_cur.command_lst[0] != "find_spots" and
          tmp_cur.success == True):

            try:
                path_to_json = tmp_cur.json_file_out

            except:
                print "no experimet json file available"

        return path_to_json



    def get_reflections_path(self):
        tmp_cur = self.step_list[self.current_line]
        if(tmp_cur.command_lst == [None]):
           tmp_cur = tmp_cur.prev_step

        if(tmp_cur.command_lst[0] == "Root" or
             tmp_cur.command_lst[0] == "import" or
             tmp_cur.success == False):

            path_to_pickle = None

        try:
            path_to_pickle = tmp_cur.pickle_file_out

        except:
            path_to_pickle = None
            print "no pickle file available"

        return path_to_pickle

    def get_next_from_here(self):
        return self.step_list[self.current_line].get_next_step()

    def slist(self):
        print "printing in steps list mode: \n"
        print_list(self.step_list, self.current_line)

if(__name__ == "__main__"):
    tree_output = TreeShow()

    try:
        with open ('bkp.pickle', 'rb') as bkp_in:
            uni_controler = pickle.load(bkp_in)

    except:
        uni_controler = Runner()

    tree_output(uni_controler)

    command = ""
    while(command.strip() != 'exit' and command.strip() != 'quit'):
        try:
            inp_str = "lin [" + str(uni_controler.current_line) + "] >>> "
            command = str(raw_input(inp_str))
            if(command == ""):
                print "converting empty line in self.slist()"
                command = "slist"

        except:
            print " ... interrupting"
            sys.exit(0)

        uni_controler.run(command, None, mk_nxt = True)
        tree_output(uni_controler)
        nxt_str = uni_controler.get_next_from_here()
        print "\n next to run:\n ", nxt_str

        with open('bkp.pickle', 'wb') as bkp_out:
            pickle.dump(uni_controler, bkp_out)

