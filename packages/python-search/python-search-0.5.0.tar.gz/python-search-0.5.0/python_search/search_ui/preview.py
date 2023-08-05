from datetime import datetime

from python_search.config import ConfigurationLoader


class Preview:
    def __init__(self):
        self.configuration = ConfigurationLoader()

    def display(self, entry_text):
        """
        Prints the entry in the preview window
        """
        key = entry_text.split(":")[0]
        from colorama import Fore, Style

        try:

            entry_data = self.configuration.load_entries()[key]
            print("")
            if "url" in entry_data:
                print(f"{Fore.BLUE}{entry_data['url']}{Style.RESET_ALL}")
                del entry_data["url"]
                type = "Url"

            if "snippet" in entry_data:
                print(f"{Fore.RED}{entry_data['snippet']}{Style.RESET_ALL}")
                del entry_data["snippet"]
                type = "Snippet"

            if "cmd" in entry_data:
                print(f"{Fore.GREEN}{entry_data['cmd']}{Style.RESET_ALL}")
                type = "Cmd"
                del entry_data["cmd"]

            if "cli_cmd" in entry_data:
                print(f"{Fore.GREEN}{entry_data['cli_cmd']}{Style.RESET_ALL}")
                type = "CliCmd"
                del entry_data["cli_cmd"]
            print("")

            print(f"Key: {Fore.YELLOW}{key}{Style.RESET_ALL}")
            print("Type: " + type)

            for key, value in entry_data.items():
                print(f"{key}: {value}")

            if "created_at" in entry_data:
                from dateutil import parser

                creation_date = parser.parse(entry_data["created_at"])
                today = datetime.now()
                print(f"Entry age: {today - creation_date}")

        except BaseException as e:
            print(entry_text)
            print(f"""Error while decoding: {e}""")
            raise e
