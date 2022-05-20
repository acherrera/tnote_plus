#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: acherrera
# @Email: Github username: @acherrera
# MIT License. You can find a copy of the License
# @http://prodicus.mit-license.org
# Follows a CRUD approach

from __future__ import print_function
from collections import OrderedDict
import sys
import datetime
import os
import re
import getpass
from functools import reduce
from getkey import getkey, keys


import hashlib
from peewee import *
from clint.textui import colored, puts
if os.name != 'nt':
    from playhouse.sqlcipher_ext import SqlCipherDatabase
    from Crypto.Cipher import AES

ENV = os.environ.get("ENV")

__version__ = '0.0.2'
DB_PATH = os.getenv('HOME', os.path.expanduser('~')) + '/.tnote'

# Makes sure that the length of a string is a multiple of 32. Otherwise it
# is padded with the '^' character
pad_string = lambda s: s + (32 - len(s) % 32) * '^'

if ENV == "test":
    DB_PATH = "/tmp/tnote_testing/"
    db = SqliteDatabase(DB_PATH + '/diary.db')
else:
    password = getpass.getpass("Please enter your key: ")
    key = hashlib.sha256(password.encode('utf-8')).digest()
    cryptor = AES.new(key)
    passphrase = getpass.getpass("Please enter your passphrase: ")
    crypted_pass = cryptor.encrypt(pad_string(passphrase))
    db = SqlCipherDatabase(DB_PATH + '/diary.db', passphrase=str(crypted_pass))

finish_key = "ctrl+Z" if os.name == 'nt' else "ctrl+D"


class DiaryEntry(Model):

    """The main Diray Model"""
    title = CharField()
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    tags = CharField()

    class Meta:
        database = db

def initialize():
    """Load the database and creates it if it doesn't exist"""


    if not os.path.exists(DB_PATH):
        os.makedirs(DB_PATH)
    try:
        db.connect()
        db.create_tables([DiaryEntry], safe=True)
    except DatabaseError:
        print(
            'Your key and/or passphrase were incorrect.\n \
            Please restart the application and try again!')
        exit(0)


def get_keystroke():
    """
    Gets keystroke from user and remove casing
    """
    key = None
    while not key:
        key=getkey()
        if isinstance(key, str):
            return key.lower()
        else:
            return key

def menu_loop():
    """To display the diary menu"""

    choice = None
    while choice != 'q':
        clear()
        tnote_banner = r"""

        _________ _        _______ _________ _______       _    
        \__   __/( (    /|(  ___  )\__   __/(  ____ \     ( )   
           ) (   |  \  ( || (   ) |   ) (   | (    \/     | |   
           | |   |   \ | || |   | |   | |   | (__       __| |__ 
           | |   | (\ \) || |   | |   | |   |  __)     (__   __)
           | |   | | \   || |   | |   | |   | (           | |   
           | |   | )  \  || (___) |   | |   | (____/\     | |   
           )_(   |/    )_)(_______)   )_(   (_______/     (_)   
                                        - By acherrera(@acherrera)
        """

        puts(colored.yellow(tnote_banner))
        puts(colored.red("\nEnter 'q' to quit"))
        for key, value in menu.items():
            puts(colored.green('{}) {} : '.format(key, value.__doc__)))
        print("Action: ")
        choice = get_keystroke()
        choice = choice.lower().strip()

        if choice in menu:
            clear()
            menu[choice]()
    clear()


def clear():
    """for removing the clutter from the screen when necessary"""
    os.system('cls' if os.name == 'nt' else 'clear')


def add_entry():
    """Adds an entry to the diary"""
    title_string = "Title (press {} when finished)".format(finish_key)
    puts(colored.yellow(title_string))
    puts(colored.green("="*len(title_string)))
    title = sys.stdin.read().strip()
    if title:
        entry_string = "\nEnter your entry: (press {} when finished)".format(finish_key)
        puts(colored.yellow(entry_string))
        puts(colored.green("="*len(entry_string)))
        # reads all the data entered from the user
        data = sys.stdin.read().strip()
        if data:    # if something was actually entered
            puts(colored.yellow("\nEnter comma separated tags(if any!): (press {} when finished) : ".format(finish_key)))
            puts(colored.green("="*(len(title_string)+33)))
            tags = sys.stdin.read().strip()
            tags = process_tags(tags)
            puts(colored.green("\n"+"="*len(entry_string)))
            # anything other than 'n'
            print("\nSave entry (y/n) : ").lower() 
            choice = get_keystroke()
            if choice != 'n':
                DiaryEntry.create(content=data, tags=tags, title=title)
                puts(colored.green("Saved successfully"))
    else:
        puts(
            colored.red("No title entered! Press Enter to return to main menu"))
        get_keystroke()
        clear()
        return


def view_entry(search_query=None, search_content=True):
    """Views a diary entry"""
    entries = DiaryEntry.select().order_by(DiaryEntry.timestamp.desc())

    if search_query and search_content:
        entries = entries.where(DiaryEntry.content.contains(search_query))
    elif search_query and not search_content:
        entries = entries.where(DiaryEntry.tags.contains(search_query))

    entries = list(entries)
    if not entries:
        puts(colored.red(
            "\nYour search had no results. Press enter to return to the main menu!"))
        get_keystroke()
        clear()
        return

    index = 0
    size = len(entries)-1
    while 1:
        entry = entries[index]
        timestamp = entry.timestamp.strftime("%A %B %d, %Y %I:%M%p ")
        clear()
        """
        A: weekeday name
        B: month name
        D: day number
        Y: year
        I: hour(12hr clock)
        M: minute
        p: am or pm
        """
        head = "\"{title}\" on \"{timestamp}\"".format(
            title=entry.title, timestamp=timestamp)
        puts(colored.red(head))
        puts(colored.green('='*len(head)))

        if search_query and search_content:
            bits = re.compile("(%s)" % re.escape(search_query), re.IGNORECASE).split(entry.content)
            line = reduce(lambda x,y : x+y, [colored.cyan(b) if b.lower() == search_query.lower()
                else colored.yellow(b) for b in bits])
            puts(line)
        else:
            puts(colored.yellow(entry.content))

        puts(colored.magenta(
            ('\nTags: {}'.format(entry.tags)) if entry.tags else '\nNo tags supplied'))
        puts(colored.green('\n\n'+'='*len(head)))
        puts(
            colored.yellow("Viewing note " + str(index+1) + " of " + str(size+1)))

        print('n) next entry')
        print('p) previous entry')
        print('d) delete entry')
        print('t) add tag(s)')
        print('r) remove tag(s)')
        print('q) to return to main menu')

        print('Action: [n/p/q/d] : ')
        next_action = get_keystroke().strip()

        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)
            size -= 1
            return
        elif next_action == 'n':
            if (index + 1) <= size:
                index += 1
            else: 
                index = size
        elif next_action == 'p':
            if index <= 0:
                index = 0
            else: 
                index -= 1
        elif next_action == 't':
            puts(
                colored.yellow("\nEnter tag(s): (press %s when finished) : " % finish_key))
            new_tag = sys.stdin.read().strip()
            add_tag(entry, new_tag)
        elif next_action == 'r':
            puts(
                colored.yellow("\nEnter tag(s): (press %s when finished) : " % finish_key))
            new_tag = sys.stdin.read().strip()
            remove_tag(entry, new_tag)


def search_entries():
    """Let's us search through the diary entries"""
    while 1:
        clear()
        print("What do you want to search for?")
        puts(colored.green("c) Content"))
        puts(colored.green("t) Tags"))
        puts(colored.green("q) Return to the main menu"))
        puts(colored.yellow("==============================="))
        print("Action [c/t/q] : ", end="")

        query_selector = get_keystroke()
        if query_selector == "t":

            view_entry(input("Enter a search Query: "), search_content=False)
            break
        elif query_selector == "c":
            view_entry(input("Enter a search Query: "), search_content=True)
            break
        elif query_selector == "q":
            break
        else:
            print("Your input was not recognized, please try again!\n")
            input('')


def delete_entry(entry):
    """deletes a diary entry"""
    # It makes the most sense to me to delete the entry while I am
    # reading it in from the 'view_entry' method so here it is
    
    puts(colored.red("Are you sure (y/n) : "))
    choice = get_keystroke()
    choice = choice.strip()
    if choice.lower().strip() == 'y':
        entry.delete_instance()
        puts(colored.green("Entry was deleted!"))


def process_tags(tag: str)->str:
    """
    Takes a string of comma separated tags, convert to a list of strings and removes leading and trailing spaces
    Args:
        tag: tag values to process. Example "todo  , later, new,"
    Returns:
        list of values with spaces removed. Example "todo,later,new"
    """
    cleaned_tags = tag.split(',')
    cleaned_tags = [tag.strip() for tag in cleaned_tags if tag]
    return ','.join(sorted(set(cleaned_tags)))


def add_tag(entry, tag):
    tagList = entry.tags.split(',')
    newTagList = process_tags(tag).split(',')
    for tag in newTagList:
        if(tagList.count(tag) == 0):
            tagList.append(tag)
            entry.tags = ",".join(tagList)
            entry.save()
        else:
            puts(colored.red("Tag already present"))


def remove_tag(entry, tag):
    tagList = entry.tags.split(',')
    newTagList = process_tags(tag).split(',')
    for tag in newTagList:
        try:
            tagList.remove(tag)
            entry.tags = ','.join(tagList)
            entry.save()
            puts(colored.green("Tag deleted!"))
        except ValueError:
            puts(colored.red("No such tag in this entry!"))


menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entry),
    ('s', search_entries)
])

if __name__ == "__main__":
    initialize()

    try:
        menu_loop()
    except KeyboardInterrupt:
        clear()
        sys.exit(0)
