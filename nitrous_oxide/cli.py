import argparse
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import print_formatted_text, radiolist_dialog
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import FormattedText
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from nitrous_oxi.api import NitrousOxiClient
from nitrous_oxi.utils import clean_phone

console = Console()
client = NitrousOxiClient()

# Define themes
themes = {
    'default': Style.from_dict({
        'banner': '#0000ff bold',
        'option': '#00ffff',
        'option-selected': '#ff0000 bold',
        'prompt': '#ffffff bold',
        'error': '#ff0000 bold'
    }),
    'dark': Style.from_dict({
        'banner': '#ffffff bold',
        'option': '#00ff00',
        'option-selected': '#ff00ff bold',
        'prompt': '#ffffff bold',
        'error': '#ff0000 bold'
    }),
}

# Set initial theme
current_theme = 'default'
style = themes[current_theme]

def display_banner():
    banner = r"""
 /$$   /$$ /$$$$$$ /$$$$$$$$ /$$$$$$$   /$$$$$$  /$$   /$$  /$$$$$$           /$$$$$$  /$$   /$$ /$$$$$$
| $$$ | $$|_  $$_/|__  $$__/| $$__  $$ /$$__  $$| $$  | $$ /$$__  $$         /$$__  $$| $$  / $$|_  $$_/
| $$$$| $$  | $$     | $$   | $$  \ $$| $$  \ $$| $$  | $$| $$  \__/        | $$  \ $$|  $$/ $$/  | $$  
| $$ $$ $$  | $$     | $$   | $$$$$$$/| $$  | $$| $$  | $$|  $$$$$$  /$$$$$$| $$  | $$ \  $$$$/   | $$  
| $$  $$$$  | $$     | $$   | $$__  $$| $$  | $$| $$  | $$ \____  $$|______/| $$  | $$  >$$  $$   | $$  
| $$\  $$$  | $$     | $$   | $$  \ $$| $$  | $$| $$  | $$ /$$  \ $$        | $$  | $$ /$$/\  $$  | $$  
| $$ \  $$ /$$$$$$   | $$   | $$  | $$|  $$$$$$/|  $$$$$$/|  $$$$$$/        |  $$$$$$/| $$  \ $$ /$$$$$$
|__/  \__/|______/   |__/   |__/  |__/ \______/  \______/  \______/          \______/ |__/  |__/|______/
    """
    print_formatted_text(FormattedText([("class:banner", banner)]), style=style)

def display_menu():
    options = [
        ('1', 'Search by Username'),
        ('2', 'Search by Domain'),
        ('3', 'Search by Email'),
        ('4', 'Search by Phone'),
        ('5', 'Search by IP'),
        ('t', 'Change Theme'),
        ('f', 'Change Result Format'),
        ('q', 'Quit')
    ]
    result = radiolist_dialog(
        title='NITROUS-OXI',
        text='Select an option:',
        values=options,
        style=style
    ).run()
    return result

def change_theme():
    global style, current_theme
    theme_options = [(key, key) for key in themes.keys()]
    theme_choice = radiolist_dialog(
        title='Change Theme',
        text='Select a theme:',
        values=theme_options,
        style=style
    ).run()
    if theme_choice:
        current_theme = theme_choice
        style = themes[current_theme]
        print_formatted_text(FormattedText([("class:prompt", f"Theme changed to {current_theme}")]), style=style)

def search_category(category, query=None):
    if query is None:
        query = prompt(f"Enter {category}: ", style=style)
    try:
        data = client.fetch_data(category, query)
        display_results(data)
    except ValueError as e:
        print_formatted_text(FormattedText([("class:error", str(e))]), style=style)

def display_results(data):
    if isinstance(data, list) and data:
        table = Table(box=box.ROUNDED)
        for key in data[0].keys():
            table.add_column(key)
        for item in data:
            table.add_row(*[str(value) for value in item.values()])
        console.print(Panel(table, title="Search Results"))
    else:
        console.print(Panel("No data found", title="Search Results", style="error"))

def change_result_format():
    print("Changing result format is currently a placeholder.")

def main():
    parser = argparse.ArgumentParser(description='Nitrous-Oxi CLI Tool')
    parser.add_argument('-s', '--search', help='Perform a search', action='store_true')
    parser.add_argument('-u', '--username', help='Search by username')
    parser.add_argument('-d', '--domain', help='Search by domain')
    parser.add_argument('-e', '--email', help='Search by email')
    parser.add_argument('-p', '--phone', help='Search by phone')
    parser.add_argument('-i', '--ip', help='Search by IP')

    args = parser.parse_args()

    if args.search:
        if args.username:
            search_category("username", args.username)
        elif args.domain:
            search_category("domain", args.domain)
        elif args.email:
            search_category("email", args.email)
        elif args.phone:
            search_category("phone", args.phone)
        elif args.ip:
            search_category("ip", args.ip)
        else:
            print("Please provide a valid search option with a value.")
    else:
        display_banner()
        while True:
            choice = display_menu()
            if choice == '1':
                search_category("username")
            elif choice == '2':
                search_category("domain")
            elif choice == '3':
                search_category("email")
            elif choice == '4':
                search_category("phone")
            elif choice == '5':
                search_category("ip")
            elif choice == 't':
                change_theme()
            elif choice == 'f':
                change_result_format()
            elif choice == 'q':
                print_formatted_text(FormattedText([("class:error", "Exiting...")]), style=style)
                break
            else:
                print_formatted_text(FormattedText([("class:error", "Invalid option. Try again.")]), style=style)

            if choice in {'1', '2', '3', '4', '5'}:
                prompt(FormattedText([("class:prompt", "Press Enter to return to main menu...")]), style=style)

if __name__ == "__main__":
    main()
