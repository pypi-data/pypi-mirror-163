## PYTHON-TRAINING - TDD - PRACTICE
- Start date: 08-08-2022
- End date: 12-08-2022

## TEAM SIZE
- 1 dev

## DESCRIPTION AND TARGETS
- Description:
  - Create the Python CLI app send a request to a user-entered URL then get the title & h1 of that page.
- Targets:
  - Create the Python CLI send a request to a user-entered URL then get the title & h1 of that page.
  - Use argparse to build the python CLI.
  - Unittest for the code.

## REQUIREMENTS
- Install the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- Install the argparse: `pip install argparse`
- Install the validators: `pip install validators`
- Install the requests: `pip install requests`
- Install the beautifulsoup4: `pip install beautifulsoup4`

## ENVIRONMENT
- Ubuntu 18.04
- Visual Studio Code
- GitLab

## TECHNOLOGY
- Python 3.10.5

## GUIDELINE
- 1. Clone practice at [here](git@gitlab.asoft-python.com:cuong.doan/python-training.git)
- 2. Run `git checkout feature/dissect_site`
- 3. Run `cd dissect`
- 4. Run script:
  * Show the title and heading 1: `./dissect_site/dissect_site.py https://www.examples.com`
  * Show the title: `./dissect_site/dissect_site.py https://www.examples.com --title`
  * Show the heading 1: `./dissect_site/dissect_site.py https://www.examples.com --heading`
- 5. Run unittest: `python3 -m unittest discover -s dissect_site.tests`

*https://www.examples.com is a sample URL, can be replaced with another*

## AUTHOR
Cuong Doan
