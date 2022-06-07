#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: acherrera
# @Email: Github username: @acherrera
# MIT License. You can find a copy of the License
# @http://prodicus.mit-license.org
# Follows a CRUD approach

from collections import OrderedDict
import sys
import datetime
import os
import re
from functools import reduce
from getkey import getkey, keys

import hashlib
from peewee import *
from rich.console import Console
from rich.style import Style

console = Console()

HEADER_COLOR = Style(color="deep_sky_blue3", bgcolor="black")
ACTION_COLOR = Style(color="orange_red1", bgcolor="black")
MENU_COLOR = Style(color="green_yellow", bgcolor="black")


ENV = os.environ.get("ENV")

__version__ = "0.1.0"
DB_PATH = os.getenv("HOME", os.path.expanduser("~")) + "/.tnote"

# Makes sure that the length of a string is a multiple of 32. Otherwise it
# is padded with the '^' character
pad_string = lambda s: s + (32 - len(s) % 32) * "^"

if ENV == "test":
    DB_PATH = "/tmp/tnote_testing/"
    db = SqliteDatabase(DB_PATH + "/diary.db")
else:
    db = SqliteDatabase(DB_PATH + "/diary.db")

finish_key = "<enter>"


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

    db.connect()
    db.create_tables([DiaryEntry], safe=True)


def get_keystroke():
    """
    Gets keystroke from user and remove casing
    """
    key = None
    while not key:
        key = getkey()
        if isinstance(key, str):
            return key.lower()
        else:
            return key


def menu_loop():
    """To display the diary menu"""

    choice = None
    while choice != "q":
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
        """
        tnote_banner += f"   version: {__version__} by acherrera"

        console.print(tnote_banner, style=HEADER_COLOR, highlight=False)
        console.print("\nEnter 'q' to quit", style=ACTION_COLOR)
        for key, value in MENU.items():
            console.print(
                "[green_yellow]{}[/green_yellow] : {}".format(key, value.__doc__)
            )
        console.print("Action: ", style=ACTION_COLOR)
        choice = get_keystroke()
        choice = choice.lower().strip()

        if choice in MENU:
            clear()
            MENU[choice]()
    clear()


def clear():
    """for removing the clutter from the screen when necessary"""
    os.system("cls" if os.name == "nt" else "clear")


def add_entry():
    """Adds an entry to the diary"""
    title_string = "Title: ".format(finish_key)
    console.print(title_string)
    console.print("=" * len(title_string))
    # title = sys.stdin.read().strip()
    title = input()
    if title:
        entry_string = "\nEnter your entry: ".format(finish_key)
        console.print(entry_string)
        console.print("=" * len(entry_string))
        # reads all the data entered from the user
        # data = sys.stdin.read().strip()
        data = input()
        while True:
            line_in = input()
            data = data + "\n" + line_in
            if not line_in:
                break

        if data:  # if something was actually entered
            console.print(
                "\nEnter comma separated tags(if any!): (press {} when finished) : ".format(
                    finish_key
                )
            )
            console.print("=" * (len(title_string) + 33))
            # tags = sys.stdin.read().strip()
            tags = input()
            tags = process_tags(tags)
            console.print("\n" + "=" * len(entry_string))
            # anything other than 'n'
            console.print("\nSave entry (y/n) : ")
            choice = get_keystroke()
            if choice != "n":
                DiaryEntry.create(content=data, tags=tags, title=title)
                console.print("Saved successfully")
    else:
        console.print("No title entered! Press Enter to return to main menu")
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
        console.print(
            "\nYour search had no results. Press enter to return to the main menu!"
        )
        get_keystroke()
        clear()
        return

    index = 0
    size = len(entries) - 1
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
        head = '"{title}" on "{timestamp}"'.format(
            title=entry.title, timestamp=timestamp
        )
        console.print(head)
        console.print("=" * len(head))

        if search_query and search_content:
            bits = re.compile("(%s)" % re.escape(search_query), re.IGNORECASE).split(
                entry.content
            )
            line = reduce(
                lambda x, y: x + y,
                [b if b.lower() == search_query.lower() else b for b in bits],
            )
            console.print(line)
        else:
            console.print(entry.content)

        console.print(
            ("\nTags: {}".format(entry.tags)) if entry.tags else "\nNo tags supplied"
        )
        console.print("\n\n" + "=" * len(head))
        console.print("Viewing note " + str(index + 1) + " of " + str(size + 1))

        menu_options = {
            "n": "next entry",
            "p": "previous entry",
            "d": "delete entry",
            "t": "add tag(s)",
            "r": "remove tag(s)",
            "q": "to return to main menu",
        }

        for key, value in menu_options.items():
            console.print(
                f"[green_yellow]{key}[/green_yellow] : {value}", highlight=False
            )

        console.print("Action: [n/p/q/d] : ")
        next_action = get_keystroke().strip()

        if next_action == "q":
            break
        elif next_action == "d":
            delete_entry(entry)
            size -= 1
            return
        elif next_action == "n":
            if (index + 1) <= size:
                index += 1
            else:
                index = size
        elif next_action == "p":
            if index <= 0:
                index = 0
            else:
                index -= 1
        elif next_action == "t":
            console.print("\nEnter tag(s): (press %s when finished) : " % finish_key)
            # new_tag = sys.stdin.read().strip()
            new_tag = input()
            add_tag(entry, new_tag)
        elif next_action == "r":
            console.print("\nEnter tag(s): (press %s when finished) : " % finish_key)
            # new_tag = sys.stdin.read().strip()
            new_tag = input()
            remove_tag(entry, new_tag)


def search_entries():
    """Let's us search through the diary entries"""
    while 1:
        clear()
        console.print("What do you want to search for?")
        console.print("c) Content")
        console.print("t) Tags")
        console.print("q) Return to the main menu")
        console.print("===============================")
        console.print("Action [c/t/q] : ", end="")

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
            console.print("Your input was not recognized, please try again!\n")
            input("")


def delete_entry(entry):
    """deletes a diary entry"""
    # It makes the most sense to me to delete the entry while I am
    # reading it in from the 'view_entry' method so here it is

    console.print("Are you sure (y/n) : ")
    choice = get_keystroke()
    choice = choice.strip()
    if choice.lower().strip() == "y":
        entry.delete_instance()
        console.print("Entry was deleted!")


def process_tags(tag: str) -> str:
    """
    Takes a string of comma separated tags, convert to a list of strings and removes leading and trailing spaces
    Args:
        tag: tag values to process. Example "todo  , later, new,"
    Returns:
        list of values with spaces removed. Example "todo,later,new"
    """
    cleaned_tags = tag.split(",")
    cleaned_tags = [tag.strip() for tag in cleaned_tags if tag]
    return ",".join(sorted(set(cleaned_tags)))


def add_tag(entry, tag):
    tagList = entry.tags.split(",")
    newTagList = process_tags(tag).split(",")
    for tag in newTagList:
        if tagList.count(tag) == 0:
            tagList.append(tag)
            entry.tags = ",".join(tagList)
            entry.save()
        else:
            console.print("Tag already present")


def remove_tag(entry: DiaryEntry, tag: str):
    """
    Removes the given tag from the given entry. This is accomplishbed by pulling the existing tags, converting them to a
    listand remove the value that matches "tag" above.
    Args:
        entry: Diary Entry object to modify
    Returns:
        None - updates the values
    """
    tagList = entry.tags.split(",")
    newTagList = process_tags(tag).split(",")
    for tag in newTagList:
        try:
            tagList.remove(tag)
            entry.tags = ",".join(tagList)
            entry.save()
            console.print("Tag deleted!")
        except ValueError:
            console.print("No such tag in this entry!")


MENU = OrderedDict([("a", add_entry), ("v", view_entry), ("s", search_entries)])


def main():
    initialize()

    try:
        menu_loop()
    except KeyboardInterrupt:
        clear()
        sys.exit(0)


if __name__ == "__main__":
    main()
