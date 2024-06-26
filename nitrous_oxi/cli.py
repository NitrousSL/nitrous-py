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

style = Style.from_dict({
    'banner': '#0000ff bold',
    'option': '#00ffff',
    'option-selected': '#ff0000 bold',
    'prompt': '#ffffff bold',
    'error': '#ff0000 bold'
})

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
        ('q', 'Quit')
    ]
    result = radiolist_dialog(
        title='NITROUS-OXI',
        text='Select an option:',
        values=options,
        style=style
    ).run()
    return result

def search_category(category):
    query = prompt(FormattedText([("class:prompt", f"Enter the {category} to search: ")]), style=style)
    if category == "phone":
        query = clean_phone(query)
    data = client.fetch_data(category, query)
    if data:
        display_data(category, data)

def display_data(category, data):
    for item in data:
        if 'name' in item and 'data' in item:
            table = Table(title=f"[bold blue]{category.capitalize()} - {item['name'].capitalize()} Results[/bold blue]",
                          box=box.ROUNDED, border_style="green", highlight=True)
            table.add_column("[bold magenta]Key[/bold magenta]", justify="left")
            table.add_column("[bold cyan]Value[/bold cyan]", justify="left")
            item_data = item['data']['data']
            if isinstance(item_data, dict):
                for key, value in item_data.items():
                    table.add_row(f"[bold yellow]{key}[/bold yellow]", str(value))
            elif isinstance(item_data, list):
                for sub_item in item_data:
                    if isinstance(sub_item, dict):
                        for key, value in sub_item.items():
                            table.add_row(f"[bold yellow]{key}[/bold yellow]", str(value))
                    else:
                        table.add_row("[bold yellow]Value[/bold yellow]", str(sub_item))
            console.print(table)

def main():
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
        elif choice == 'q':
            print_formatted_text(FormattedText([("class:error", "Exiting...")]), style=style)
            break
        else:
            print_formatted_text(FormattedText([("class:error", "Invalid option. Try again.")]), style=style)

        if choice in {'1', '2', '3', '4', '5'}:
            prompt(FormattedText([("class:prompt", "Press Enter to return to main menu...")]), style=style)

if __name__ == "__main__":
    main()
