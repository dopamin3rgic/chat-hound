# chat-hound
A tool that will help you find telegram or discord channels based off keyword searching.

## Setup
- install the version of [chromedriver](https://chromedriver.chromium.org/downloads) that matches the version of chrome installed on your computer and place the executable in `/usr/local/bin/`

- run ./dev/setup.sh

## Usage

- run `source env/bin/activate` to activate your virtual environment

### Telegram
```
(env) user@host:~/chat-hound$ ./chathound.py telegram --help
usage: chathound.py telegram [-h] [-o <filename>] [-n <number>]
                             [-s <search-engine>] -k <keyword>

Find telegram invites using keyword searching.

optional arguments:
  -h, --help            show this help message and exit
  -o <filename>, --output <filename>
                        Name of the output file (CSV)
  -n <number>, --number <number>
                        Number of links to find (default 100)
  -s <search-engine>, --search-engine <search-engine>
                        Search engine to use (default Google)
  -k <keyword>, --key-word <keyword>
                        keyword to use when searching for links

```

### Discord

```

(env) user@host:~/chat-hound$ ./chathound.py discord --help
usage: chathound.py discord [-h] [-o <file>] [-n <number>] -k <keyword>
                            [-s <search-engine>]

Find discord invites using keyword searching.

optional arguments:
  -h, --help            show this help message and exit
  -o <file>, --output <file>
                        Name of the output file (CSV)
  -n <number>, --number <number>
                        Number of links to find (default 100)
  -k <keyword>, --key-word <keyword>
                        keyword to use when searching for links
  -s <search-engine>, --search-engine <search-engine>
                        Search engine to use (default Google)

```