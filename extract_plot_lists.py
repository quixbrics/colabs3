import requests
from bs4 import BeautifulSoup

URL = "https://writingexercises.co.uk/plotgenerator.php"

# Map dropdown names to variable names
DROPDOWNS = {
    "character": "CHARACTERS",
    "setting": "SETTINGS",
    "situation": "SITUATIONS",
    "theme": "THEMES"
}

def extract_options():
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    results = {}
    for dropdown, var_name in DROPDOWNS.items():
        select = soup.find("select", {"name": dropdown})
        if not select:
            print(f"Dropdown '{dropdown}' not found!")
            continue
        options = [opt.text.strip() for opt in select.find_all("option") if opt.text.strip()]
        results[var_name] = options
    return results

def print_lists():
    lists = extract_options()
    for var_name, options in lists.items():
        print(f"{var_name} = [")
        for opt in options:
            print(f'    "{opt}",')
        print("]\n")

if __name__ == "__main__":
    print_lists()
