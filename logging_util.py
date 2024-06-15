from colorama import Fore, Style, init

init(autoreset=True)


def log_info(message):
    print(Fore.GREEN + message + Style.RESET_ALL)


def log_warning(message):
    print(Fore.YELLOW + message + Style.RESET_ALL)


def log_error(message):
    print(Fore.RED + message + Style.RESET_ALL)
