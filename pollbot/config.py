"""Config values for pollbot."""
import logging
import os
import sys

import toml
import shlex

default_config = {
    "telegram": {
        "bot_name": "your_bot_@_username",
        "api_key": "your_telegram_api_key",
        "worker_count": 20,
        "admin": "nukesor",
        "allow_private_vote": False,
        "max_user_votes_per_day": 200,
        "max_inline_shares": 20,
        "max_polls_per_user": 200,
    },
    "database": {
        "sql_uri": "postgresql://pollbot:localhost/pollbot",
        "connection_count": 20,
        "overflow_count": 10,
    },
    "logging": {
        "sentry_enabled": False,
        "sentry_token": "",
        "log_level": logging.INFO,
        "debug": False,
    },
    "webhook": {
        "enabled": False,
        "domain": "https://localhost",
        "token": "pollbot",
        "cert_path": "/path/to/cert.pem",
        "port": 7000,
    }
}

config_path = os.path.expanduser("~/.config/ultimate_pollbot.toml")
replacements_path = os.path.expanduser("~/.config/replacements.csv")

def load_replacements(config_file):
    replacements = {}
    if os.path.exists(config_path):
        with open(config_file, 'r', encoding='utf-8') as file:
            for line in file:
                if(len(line)>1):
                    
                    lexer = shlex.shlex(line, posix=True)
                    lexer.whitespace_split = True
                    lexer.whitespace = ' '
                    lexer = list(lexer)
                    #parts = line.strip().split(maxsplit=1)  # Разделение строки на 2 части
                    if len(lexer) == 2:
                        text_to_replace, new_text = lexer
                        replacements[text_to_replace] = new_text
    return replacements

if not os.path.exists(config_path):
    with open(config_path, "w") as file_descriptor:
        toml.dump(default_config, file_descriptor)
    print("Please adjust the configuration file at '~/.config/ultimate_pollbot.toml'")
    sys.exit(1)
else:
    config = toml.load(config_path)
    replacements = load_replacements(replacements_path)
    if(len(replacements)!=0):
        print("Replacements loaded")

    # Set default values for any missing keys in the loaded config
    for key, category in default_config.items():
        for option, value in category.items():
            if option not in config[key]:
                config[key][option] = value