## tnote

[![GitHub license](https://img.shields.io/pypi/l/pyzipcode-cli.svg)](https://img.shields.io/pypi/l/pyzipcode-cli.svg) [![Supported python versions](https://img.shields.io/pypi/pyversions/Django.svg)]([![PyPI](https://img.shields.io/pypi/pyversions/Django.svg)]()) [![Join the chat at https://gitter.im/prodicus/tnote](https://badges.gitter.im/prodicus/tnote.svg)](https://gitter.im/prodicus/tnote?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

```
                            _________ _        _______ _________ _______       _    
                            \__   __/( (    /|(  ___  )\__   __/(  ____ \     ( )   
                               ) (   |  \  ( || (   ) |   ) (   | (    \/     | |   
                               | |   |   \ | || |   | |   | |   | (__       __| |__ 
                               | |   | (\ \) || |   | |   | |   |  __)     (__   __)
                               | |   | | \   || |   | |   | |   | (           | |   
                               | |   | )  \  || (___) |   | |   | (____/\     | |   
                               )_(   |/    )_)(_______)   )_(   (_______/     (_)   
                                                                                    
```

A dead simple command line note taking app built for you! The original project lives here:
https://github.com/tasdikrahman/tnote

At the time of forking the project, there had been not updates in 4 years with 11 issues. I thought it was interesting
enough to at least fork it and give it a shot. 

## Index

- [Demo](#demo)
- [Features](#features)
- [Installation](#installation)
  - [Installing dependencies](#installing-dependencies)
  - [Clone it](#clone-it)
  - [Run it](#run-it)
- [Supported platforms](#supported-platforms)
- [Contributing](#contributing)
  - [To-do](#to-do)
  - [Contributers](#contributers)
- [Issues](#issues)
- [License](#license)

## Demo
[:arrow_up: Back to top](#index)

Watch a live demo of it working here

[![asciicast](https://asciinema.org/a/35557.png)](https://asciinema.org/a/35557)

*Here's the [link to previous version](https://asciinema.org/a/35378) if you are interested!*

***

## Features
[:arrow_up: Back to top](#index)

- **Dead simple to use**: Even your granny would be able to use it. No seriously!
- **Feature rich** Add your precious note with it's _title_ , _content_ , _tags_
- **Secure**: Encrypts your database using standard **AES-256 in CBC mode**. So even if anybody gets hand of your database file. He cannot make any sense of it. [A little demo of what I am doing using it](https://github.com/tasdikrahman/tnote/wiki/So-you-say-it-is-encrypted-eh%3F)

**NOTE**
  _This was built and testing in Linux - use on other OS's at your own risk_

- **Text Highlighting is cross platform** - Supports Linux, Windows, MAC for the terminal based highlighting.
- **Searching for notes is hassle free** in `tnote`: It supports full text search for notes based on _content_, _tags_
    - The search query if found in the database will be highlighted if found. Looks pleasing to the eyes
- Ability to add and remove tags for each note.
- Adds timestamp for each note which has been added.
- Written in uncomplicated python.

Need I say more?

***

## Installation
[:arrow_up: Back to top](#index)

#### Installing dependencies

**NOTE** 

On **linux** system, install `libsqlcipher-dev` 

```sh
$ sudo apt-get install libsqlcipher-dev
```

On **Mac OS** systems, you can install it by 

```sh
$ brew install sqlcipher
```

#### Clone it


```sh
$ git clone https://github.com/tasdikrahman/tnote
$ cd tnote && pip install -r requirements.txt
```

*Add a symbolic link to it*

```sh
$ chmod +x tnote
$ cd ~/bin/ 
$ ln -s ~/some/path/to/tnote
```

Replace `~/some/path/to/tnote` by the path where you have cloned the repo. For example if you have cloned it to `~/Downloads/tnote` folder than your command should look something like

`$ ln -s ~/Downloads/tnote/tnote`

#### Run it

Fire it up! :volcano:

`$ tnote`

***

## Supported platforms
[:arrow_up: Back to top](#index)

| OS | Support status |
| --- | --- |
| Linux | :white_check_mark: Full support |
| OS X | :white_check_mark: Full support  |
| Windows | :ballot_box_with_check: encrytion of the Database for windows not yet supported |

***

## Contributing
[:arrow_up: Back to top](#index)

This project was originally created in a few hours and utilizes [peewee (ORM)](https://github.com/coleifer/peewee). It
was then forked by acherrera to do more work. 

### Dependencies

Dependencies are managed with [Python Poetry](https://python-poetry.org/). This is also used to publish the package.

Install poetry with `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`

#### To-do
    
- [ ] Add **unit tests**. Like real quick!
- [ ] Make it pip installable
- [ ] Ability to edit the content of a note
- [x] Add python2 support
- [x] Add tags support for notes
- [x] Remove tahs for notes
- [x] Add option to add title for notes
- [ ] Add option to remove title for notes
- [x] Add option to search for notes using content
- [x] Add option to search for notes using tags
- [ ] Add option to search for notes using title
- [ ] Add option to search for notes using timestamp
- [x] Encrypt the `.db` file using **Sqlcipher**
- [x] Add colorized text to the notes for improved UI
- [ ] Add better UI using **urwid**

#### Contributers

A big shout out to all the contributers, more specifically to these guys

* OG contributers: 
- [@maxwellgerber](https://github.com/maxwellgerber)
- [@BrandtM](https://github.com/BrandtM)

## Motivation
[:arrow_up: Back to top](#index)

Original project had not had updates for 4 years, so I thought I would try my hand at understanding what was going on
and expanding upon the project.

***

## Issues
[:arrow_up: Back to top](#index)

You can report the bugs at the [issue tracker](https://github.com/tasdikrahman/tnote/issues)

***

## License
[:arrow_up: Back to top](#index)

You can find a copy of the License at http://prodicus.mit-license.org/

