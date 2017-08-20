"""Desktop daemon

This is desktop deamon for checking desktop files
"""
__author__ = 'ales lerch'

import re
import time
import shutil
from enum import Enum

class Lexer_state(Enum):
    s = 1
    operation = 2
    word = 3

class Desk_deamon:

    def __init__(self,tosleep):
        self.files = []
        self.types = (".jpg",".png",".jpeg",".tiff")
        self.to_sleep = tosleep

        while True:
            time.sleep(self.to_sleep)
            self.get_dfiles()
            for file_ in self.files:
                self.evaluate(self.lexer(os.path.basename(file_)))

    def get_dfiles(self):
        for f in os.listdir("~/Desktop/"):
            if f.splitext[1] in self.types:
                self.files.append(f)

    def lexer(self,text):
        """
        token stands for file name, commands are operations
        that should be done"""
        token = ""
        command = ""
        commands = []
        state = Lexer_state.s
        identify = re.compitle("\w*\_*\(?\)?\.*-*")

        while text != "":
            if state == Lexer_state.s:
                if text[0] in [' ']:
                    text = text[1:]
                elif text[0] in ['@','{']:
                    text = text[1:]
                    state = Lexer_state.operation
                elif identify.match(text[0]):
                    state = Lexer_state.word
                    token += text[0]
                    text = text[1:]
                else:
                    print("[Error]Not valid charatect")

            elif state == Lexer_state.operation:
                if text[0] in ['@','{']:
                    text = text[1:]
                elif identify.match(text[0]):
                    command += text[0]
                    text = text[1:]
                elif text[0] == '}':
                    text = text[1:]
                    commands.append(command.lower())
                    command = ""
                    state = Lexer_state.s

            elif state == Lexer_state.word:
                if identify.match(text[0]):
                    token += text[0]
                    text = text[1:]
                else:
                    #should contiue? file_name should be done
                    state = Lexer_state.s

        return (token,commands)

    def evaluate(self,file_name,commands):

        def set_wallpaper(img):
            #same function is in wallpaper_changer
            db_file = "~/Library/Application Support/Dock/desktoppicture.db"
            subprocess.call(["sqlite3", db_file, f"update data set value = '{img}'"])
            subprocess.call(["killall", "Dock"])

        command_list = {
                "pixiv": lambda n : shutil.move(f"~/Desktop/{n}", "~/Pictures/pix-girls/"),
                "meme": lambda n : shutil.move(f"~/Desktop/{n}", "~/Pictures/Meme/"),
                "daytime" : lambda n : shutil.move(f"~/Desktop/{n}","~/TimeDayWal"),
                "mv" : lambda f, t : shutil.move(f"~/Desktop/{f}",f"{t}"),
                "trash" : lambda n : shutil.move(f"~/Desktop/{n}", "~/Pictures/pix-girls/"),
                "wall" : lambda n : set_wallpaper(n),
                }

        #control inputs
        if len(commands) > 1:
            #more commands
            if len(commands) == 2:
                command_list[commands[0]](file_name,commands[1])
            else:
                #so far there are no special tasks for more commands
                command_list[commands[0]](file_name,commands)
        else:
            command_list[commands[0]](file_name)

