## tnote

[![GitHub license](https://img.shields.io/pypi/l/pyzipcode-cli.svg)](https://img.shields.io/pypi/l/pyzipcode-cli.svg) [![Supported python versions](https://img.shields.io/pypi/pyversions/Django.svg)]([![PyPI](https://img.shields.io/pypi/pyversions/Django.svg)]())

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


## Features
[:arrow_up: Back to top](#index)

- **Dead simple to use**: Even your granny would be able to use it. No seriously!
- **Feature rich** Add your precious note with it's _title_ , _content_ , _tags_

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

If poetry is on the system:

```
poetry install
```


#### Run it

Fire it up! :volcano:

`poetry run ./tnote_plus/tnote.py`

***


## Contributing
[:arrow_up: Back to top](#index)

This project was originally created in a few hours and utilizes [peewee (ORM)](https://github.com/coleifer/peewee). It
was then forked by acherrera to do more work. 

### Dependencies

Dependencies are managed with [Python Poetry](https://python-poetry.org/). This is also used to publish the package.

Install poetry with `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`

### Deployment

`poetry build` will build the project.

`poetry publish` will publish the package to a repository.

#### To-do
    
- [x] Convert color handling to Rich
- [x] Add initial tests
- [x] Add github actions for tests
- [ ] Make it pip installable
- [ ] Ability to edit the content of a note
- [ ] Add option to remove title for notes
- [ ] Add option to search for notes using title
- [ ] Add option to search for notes using timestamp
- [ ] List titles with number and open based on number

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

You can report the bugs at the [issue tracker](https://github.com/acherrera/tnote_plus/issues)

***

## License
[:arrow_up: Back to top](#index)

You can find a copy of the License at http://prodicus.mit-license.org/

