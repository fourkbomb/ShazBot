import socket
import requests
import json
import re
import os

from bs4 import BeautifulSoup
from time import strftime

class ChallengeBot(object):
    def __init__(self, channel):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect(("irc.freenode.net", 6667))

        self.channel = channel
        self.owners = ["Shazer[2]"]
        self.user = re.compile(r'^:(.*)!')

        self.locked = True

        self.plugins = []
        self._load_plugins()

        if self.channel:
            self.join()
            self.idle()

    def join(self):
        self.connection.send("USER {nick} {nick} {nick} :{nick}\n".format(nick="ShazBot"))
        self.connection.send("NICK {}\n".format("ShazBot"))
        self.connection.send("JOIN {}\n".format(self.channel))

    def get_user(self, data):
        if self.user.match(data):
            return self.user.match(data).group(1)

    def send_message(self, message):
        self.connection.send("PRIVMSG {} :{}\n".format(self.channel, message))

    def _load_plugins(self):
        for plugin in os.listdir("./Plugins"):
            if plugin.endswith(".py") and not plugin.startswith("__init__"):
                plugin_import = __import__("Plugins." + plugin.split(".")[0], fromlist=['Plugin'])

                plugin_object = plugin_import.Plugin(self)

                if plugin_object.active:
                    self.plugins.append(plugin_object)

    def time(self):
        self.send_message(strftime("%d-%m-%Y %H:%M:%S"))

    def leave(self):
        self.connection.send("QUIT\n")

    def check_command(self, command, command_name, command_to_run, data, kwargs=None):
        if command.group(1) == command_name and not self.locked:
            if not kwargs:
                command_to_run()
            else:
                command_to_run(*kwargs)

        elif command.group(1) == command_name and self.locked:
            if self.get_user(data) not in self.owners:
                self.send_message("You are not the owner.")
            else:
                if not kwargs:
                    command_to_run()
                else:
                    command_to_run(*kwargs)

    def check_lock(self, command, data):
        if command.group(1) == "lock":
            if self.locked and self.get_user(data) in self.owners:
                self.send_message("Already locked.")
            if not self.locked and self.get_user(data) in self.owners:
                self.locked = True

        if command.group(1) == "unlock":
            if not self.locked and self.get_user(data) in self.owners:
                self.send_message("Already unlocked.")
            if self.locked and self.get_user(data) in self.owners:
                self.locked = False

    def add_owner(self, new_owner):
        if new_owner not in self.owners:
            self.owners.append(new_owner)
        else:
            self.send_message("Already an owner.")

    def remove_owner(self, owner):
        if owner not in self.owners:
            self.send_message("Not an owner.")
        else:
            self.owners.remove(owner)

    def plugin_respond(self, msg):
        for plugin in self.plugins:
            plugin.on_message(msg)

    def owners_list(self):
        self.send_message(self.owners)

    def idle(self):
        while True:
            data = self.connection.recv(2048)
            
            ping = re.match(r'^PING', data)
            if ping:
                self.connection.send("PONG\n")

            msg = re.match(r'^:([^:]+):([^:]+)', data)
            if msg:
                command = re.match(r'^--([\w]+)', msg.group(2))

                if command:
                    self.check_lock(command, data)
                    self.check_command(command, "time", self.time, data)
                    self.check_command(command, "leave", self.leave, data)
                    self.check_command(command, "owners", self.owners_list, data)

                    add_owner_regex = re.match(r'^--addowner ([\w]+)', msg.group(2))
                    if add_owner_regex:
                        self.check_command(command, "addowner", self.add_owner, data, kwargs=[add_owner_regex.group(1)])

                    remove_owner_regex = re.match(r'^--removeowner ([\w]+)', msg.group(2))
                    if remove_owner_regex:
                        self.check_command(command, "removeowner", self.remove_owner, data, kwargs=[remove_owner_regex.group(1)])

                self.plugin_respond(msg.group(2))

            if not data: break

            print data


if __name__ == "__main__":
    cb = ChallengeBot("#bot_test")