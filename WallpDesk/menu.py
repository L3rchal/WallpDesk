"""Menu_bar

Menu bar module for setting menu bar setup for OSX
"""
__author__ = 'ales lerch'

import rumps
import desktop
import wallpaper
from wall import HOME
from os.path import isfile
from database import DB_lite
from subprocess import Popen, PIPE

class Bar(rumps.App):

    def __init__(self):
        super().__init__("WallpDesk")
        self.menu = ["About","Settings","Reset database", None,
                "Desktop daemon", "Wallpaper daemon", None
                ,"Next wallpaper", "Quit"]
        self.db = DB_lite()
        self.def_wallpaper = self.db.get_wall_path()
        self.quit_button = None
        self.template = True
        self.title = None
        if isfile("images/menu_bar.png"):
            self.icon = "images/menu_bar.png"
        else:
            self.title = "Icon not found"

        self.editor = wallpaper.Editor()
        self.desktop = desktop.Daemon()

    @rumps.clicked("About")
    def about(self, _):
        rumps.Window(message="\t   WallpDesk (0.0.4)", title="\tAbout WallpDesk",
                default_text="""\n\tVersion: 0.0.4\n\n\tLicence: MIT\n\n\tAuthor: Ales Lerch""",
            dimensions=(170, 130)).run()

    @rumps.clicked("Reset database")
    def reset_db(self, _):
        self.editor.reset_library()

    @rumps.clicked("Settings")
    def settings(self, _):
        cmd = b"""choose folder with prompt "Please select an output folder:" """
        proc = Popen(["osascript", '-'], stdin=PIPE, stdout=PIPE)
        file_path, _ = proc.communicate(cmd)
        file_path = file_path.decode("utf-8").replace("alias Macintosh HD",'').replace('\n','').replace(':','/')
        if self.def_wallpaper != file_path and proc.returncode == 0:
            print(file_path)
            self.def_wallpaper = file_path
            self.db.set_wall_path(file_path)
            self.editor.set_loading_dir(self.def_wallpaper)

    @rumps.clicked("Desktop daemon")
    def on_off_test(self, sender):
        """ notifications are so far broken in rumps
        rumps.notification(title='Hi', subtitle='There.', message='Friend!',
        sound=does_something.sound, data=my_data)"""
        sender.state = not sender.state
        if sender.state:
            rumps.alert(message='You are now running desktop daemon')
            self.desktop.interrupted = False
            self.desktop.run()
        else:
            self.desktop.interrupted = True

    @rumps.clicked("Wallpaper daemon")
    def wallpaper(self, sender):
        if self.def_wallpaper:
            sender.state = not sender.state
            if sender.state:
                rumps.alert(message='You are now running wallpaper daemon', ok='OK')
                print(self.def_wallpaper)
                self.editor.interrupted = False
                self.editor.run()
            else:
                self.editor.interrupted = True
        else:
            rumps.alert("No input path for images set!")

    @rumps.clicked("Next wallpaper")
    def next_wallpaper(self,_):
        self.editor.choose_random_image()

    @rumps.clicked("Quit")
    def clean_up_before_quit(self,_):
        print("Quit application")
        rumps.quit_application()

