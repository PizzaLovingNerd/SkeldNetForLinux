# Simple skeld.net launcher for Linux made by PizzaLovingNerd.
# Code written under LGPL3

import gi, os, psutil, requests, subprocess, threading
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

HOME = os.getenv("HOME")

class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Skeld.net")

        # Box to put widgets in
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Main Label with Info
        self.label = Gtk.Label(
            label="\n\n\nWelcome to Skeld.net for Linux\n"
            "This is an unofficial installer for Linux users.\n"
            "Made by PizzaLovingNerd\n\n"
            "This only works for Among Us using Proton and Steam.\n"
            "Make sure Among Us is closed before patching.\n\n\n"
        )
        self.label.set_vexpand(True)
        self.label.set_justify(Gtk.Justification.CENTER)

        # 3 Buttons
        self.skeldButton = Gtk.Button(label="Use Skeld.net Servers")
        self.skeldButton.connect("clicked", self.skeld_clicked)
        self.officialButton = Gtk.Button(label="Switch back to official servers")
        self.officialButton.connect("clicked", self.official_clicked)
        self.launchButton = Gtk.Button(label="Launch Among Us")
        self.launchButton.connect("clicked", self.run_clicked)

        # Bottom Label
        # self.officialLabel = Gtk.Label(
        #     label="\n\n\nNote: you can also play on regular servers\n"
        #           "by selecting another server on the bottom right\n\n\n"
        #)

        # Adding everything to Box and Window
        self.box.add(self.label)
        self.box.add(self.skeldButton)
        self.box.add(self.officialButton)
        self.box.add(self.launchButton)
        # self.box.add(self.officialLabel)
        self.add(self.box)
        self.show_all()

    # Shows Dialog
    def error_dialog(self, text, secondtext):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=text,
        )
        dialog.format_secondary_text(secondtext)
        dialog.run()
        dialog.destroy()

    # Code that runs when you press the skeld.net button
    def skeld_clicked(self, button):
        if "Among Us.exe" in (p.name() for p in psutil.process_iter()): # Checks if Among Us is running
            self.error_dialog("Among Us is Running", "Please close Among Us")
        else:
            # Deletes regionInfo.dat
            if os.path.exists(HOME + "/.steam/steam/steamapps/compatdata/945360/pfx/drive_c/users/steamuser/AppData/LocalLow/Innersloth/Among Us/regionInfo.dat"):
                print("File Exists")
                os.remove(
                    HOME + "/.steam/steam/steamapps/compatdata/945360/pfx/"
                    "drive_c/users/steamuser/AppData/LocalLow/Innersloth/"
                    "Among Us/regionInfo.dat"
                )
            thread = threading.Thread(target=self.download_thread)
            thread.daemon = True
            thread.start()

    def official_clicked(self, button):
        self.error_dialog(
            "Go back to official servers",
            "If you ever want to go back to official servers\n"
            "simply open the region menu (the globe icon) and select a region.\n"
            "Among Us will replace your regionInfo.dat\n"
            "file with the official one."
        )

    def run_clicked(self, button):
        subprocess.Popen(["steam", "steam://rungameid/945360"], shell=True)

    def download_thread(self):
        try:  # Downloads skeld.net regionInfo
            regionfile = requests.get("https://skeld.net/setup/regionInfo.dat")
            with open(
                    HOME + "/.steam/steam/steamapps/compatdata/945360/pfx/"
                           "drive_c/users/steamuser/AppData/LocalLow/Innersloth/"
                           "Among Us/regionInfo.dat",
                    "wb"
            ) as f:
                f.write(regionfile.content)
            GLib.idle_add(self.error_dialog, "Among Us Patched Successfully", "You may now launch Among Us")
        except requests.exceptions.Timeout as e:
            GLib.idle_add(self.error_dialog, "Timeout", "regionInfo.dat must be unavailable :(\nCheck your internet")
        except requests.exceptions.TooManyRedirects as e:
            GLib.idle_add(self.error_dialog, "TooManyRedirects", "Must be a bad URL :/")
        except requests.exceptions.RequestException as e:
            GLib.idle_add(self.error_dialog, "RequestException", "Something bad happened.")

if __name__ == '__main__':
    window = Window()
    window.connect("delete-event", Gtk.main_quit)
    Gtk.main()

# Thanks to these resources
# https://stackabuse.com/download-files-with-python/
# https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module

# Notes:
# steam steam://rungameid/945360
# https://skeld.net/setup/regionInfo.dat
