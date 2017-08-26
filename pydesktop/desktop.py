"""Desktop daemon

This is desktop deamon for checking desktop files
"""
__author__ = 'ales lerch'

import os
import re
import wall
import time
import shutil
import threading
import subprocess
from enum import Enum


class Lexer_state(Enum):
    s = 1
    word = 2
    operation = 3

class Daemon(wall.Paper):

    def __init__(self, delay = 5):
        self.home = {os.path.expanduser('~')}
        super().__init__(f"{os.path.expanduser('~')}/Desktop/")

        def action():
            threading.Timer(9.0, action).start()
            super(Daemon,self).get_images_files()
            for file_ in self.img_files:
                if file_.startswith('@'):
                    o, t, c = self.lexer(file_)
                    self.evaluate(o,t,c)

        action()

    def lexer(self,text):
        """
        token stands for file name, commands are operations
        that should be done"""
        token = ""
        command = ""
        #commands = []
        state = Lexer_state.s
        identify = re.compile("[a-zA-Z0-9_\.-]+")
        orginal = text

        while text != "":
            if state == Lexer_state.s:
                if text[0] == ' ':
                    text = text[1:]
                elif text[0] == '@':
                    text = text[1:]
                    state = Lexer_state.operation
                elif identify.match(text[0]):
                    state = Lexer_state.word
                    token += text[0]
                    text = text[1:]
                else:
                    #print("[Error]Not valid charatect")
                    text = text[1:]

            elif state == Lexer_state.operation:
                if text[0] == '{':
                    text = text[1:]
                elif identify.match(text[0]):
                    command += text[0]
                    text = text[1:]
                elif text[0] == '}':
                    text = text[1:]
                    #commands.append(command.lower())
                    #command = ""
                    state = Lexer_state.s

            elif state == Lexer_state.word:
                if identify.match(text[0]):
                    token += text[0]
                    text = text[1:]
                else:
                    #should contiue? file_name should be done
                    state = Lexer_state.s

        return (orginal, token,[command])

    def evaluate(self,original, file_name,commands):

        def desktop(org, file_):
            subprocess.call(["mv", "-n", f"{os.path.expanduser('~')}/Desktop/{org}",f"{os.path.expanduser('~')}/Desktop/{file_}"])
            super(Daemon,self).set_wallpaper(
                    f"{os.path.expanduser('~')}/Desktop/{file_}")


        command_list = {
                "pixiv": lambda n :
                subprocess.call(["mv","-n",f"{os.path.expanduser('~')}/Desktop/{n[0]}",
                    f"{os.path.expanduser('~')}/Pictures/pix-girls/{n[1]}"]),
                "girls": lambda n :
                subprocess.call(["mv","-n",f"{os.path.expanduser('~')}/Desktop/{n[0]}",
                    f"{os.path.expanduser('~')}/Pictures/Madchen/{n[1]}"]),
                "img": lambda n :
                subprocess.call(["mv","-n",f"{os.path.expanduser('~')}/Desktop/{n[0]}",
                    f"{os.path.expanduser('~')}/Pictures/{n[1]}"]),
                "meme": lambda n : subprocess.call(["mv",
                    "-n",f"{os.path.expanduser('~')}/Desktop/{n[0]}",
                    f"{os.path.expanduser('~')}/Pictures/Meme/{n[1]}"]),
                "daytime" : lambda n :
                subprocess.call(["mv","-n",f"{os.path.expanduser('~')}/Desktop/{n[0]}",f"{os.path.expanduser('~')}/TimeDayWal/{n[1]}"]),
                "mv" : lambda f, t :
                subprocess.call(["mv","-n",f"{os.path.expanduser('~')}/Desktop/{f}",f"{os.path.abspath(t)}"]),
                "trash" : lambda n :
                subprocess.call(["mv",f"{os.path.expanduser('~')}/Desktop/{n[0]}",f"{os.path.expanduser('~')}/.Trash/{n[1]}"]),
                "wall" : lambda n : desktop(n[0], n[1]),
                }

        #control inputs
        try:
            if len(commands) > 1:
                #more commands
                if len(commands) == 2:
                    command_list[commands[0]](file_name,commands[1])
                else:
                    #so far there are no special tasks for more commands
                    command_list[commands[0]](file_name,commands)
            else:
                print("calling command",commands)
                command_list[commands[0]]((original,file_name))
        except KeyError:
            pass

if __name__ == "__main__":
    d = Daemon()

