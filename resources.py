DEBUG = 0

class BgColors:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

CURRENCY_ID = {
    'mirror': 22,
    'divine': 3,
    'exalted': 2,
}

CURRENCY_ID = {
    'divine': 3,
    'alch': 4,
}

def debug(msg) -> None:
    if DEBUG:
        print(msg)