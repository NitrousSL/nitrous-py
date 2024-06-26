import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import box

console = Console()
API_BASE_URL = "https://api.nitrous-oxi.de"

def fetch_data(category, query):
    url = f"{API_BASE_URL}/{category}?query={query}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return data.get("data", {})
        except ValueError:
            console.print(f"[red]Invalid JSON response for {query} in {category}[/red]")
    elif response.status_code == 404:
        console.print(f"[red]No data found for {query} in {category}[/red]")
    else:
        console.print(f"[red]Error fetching data for {query} in {category}[/red]")
    return None

def clean_phone(phone):
    return ''.join(filter(str.isdigit, phone))

def display_menu():
    table = Table(box=box.DOUBLE, highlight=True, title="[bold blue]Select an Option[/bold blue]")
    table.add_column("[bold yellow]Option[/bold yellow]", justify="center")
    table.add_column("[bold magenta]Description[/bold magenta]", justify="center")

    table.add_row("[bold cyan]1[/bold cyan]", " [bold cyan]Username[/bold cyan]")
    table.add_row("[bold cyan]2[/bold cyan]", " [bold cyan]Domain[/bold cyan]")
    table.add_row("[bold cyan]3[/bold cyan]", " [bold cyan]Email[/bold cyan]")
    table.add_row("[bold cyan]4[/bold cyan]", " [bold cyan]Phone[/bold cyan]")
    table.add_row("[bold cyan]5[/bold cyan]", " [bold cyan]IP[/bold cyan]")
    table.add_row("[bold red]q[/bold red]", "[bold red]Quit[/bold red]")

    panel = Panel(table, title="[bold blue]NITROUS-OXI[/bold blue]", border_style="blue")
    console.print(panel)

def search_category(category):
    query = Prompt.ask(f"Enter the [bold yellow]{category}[/bold yellow] to search")
    if category == "phone":
        query = clean_phone(query)
    data = fetch_data(category, query)
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
    while True:
        display_menu()
        choice = Prompt.ask("[bold green]Select an option[/bold green]")
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
            console.print("[bold red]Exiting...[/bold red]")
            break
        else:
            console.print("[bold red]Invalid option. Try again.[/bold red]")
            continue

        if choice in {'1', '2', '3', '4', '5'}:
            input("Press Enter to return to main menu...")

if __name__ == "__main__":
    main()
