# chat-hound
A tool that will hunt down telegram or discord channels based off keyword searching.

## Setup
- Install the version of [chromedriver](https://chromedriver.chromium.org/downloads) that matches the version of chrome installed on your computer and place the executable in `/usr/local/bin/`

- Run `./dev/setup.sh` to set up your virtual environment

## Usage

- Run `source env/bin/activate` to activate your virtual environment
- For more verbose output, you can change the logger mode from `INFO` to `DEBUG` on line 12.

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

### Examples

```
(env) user@host:~/chat-hound$ ./chathound.py telegram -k fun -n 50 -o fun-telegram.csv
[INFO] chathound.py: Searching for Telegram channels on Google using keyword fun
[INFO] chathound.py: Number of links found so far: 9
[INFO] chathound.py: Number of links found so far: 14
[INFO] chathound.py: Number of links found so far: 22
[INFO] chathound.py: Number of links found so far: 28
[INFO] chathound.py: Number of links found so far: 30
[INFO] chathound.py: Number of links found so far: 37
[INFO] chathound.py: Number of links found so far: 43
[INFO] chathound.py: Number of links found so far: 49
[INFO] chathound.py: Number of links found so far: 54
[INFO] chathound.py: Done finding links, now parsing info about each. Be patient, this takes time.
[INFO] chathound.py: Writing 54 links to fun-telegram.csv

```

## Future Development
- DuckDuckGo functionality (currently only Google)
- `-n , --number` option is currently approximate and will be fixed