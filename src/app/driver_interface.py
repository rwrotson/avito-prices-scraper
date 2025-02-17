import tempfile

from fake_useragent import UserAgent
from rich import print

from base.selenium.drivers import ChromeOptions, create_driver
from base.selenium.interface import BrowserInterface


def _create_interface() -> BrowserInterface:
    print("[bold]Creating browser interface...[/bold]")

    print("  Using undetected-chrome webdriver...")

    print("  Adding options...")

    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")

    print(f"  Options added:", end="")
    for i, argument in enumerate(options.arguments):
        print(" " * (5 if i == 0 else 21) + f"[bold green]{argument}[/bold green]")

    print("  Adding user agent...")

    user_agent = UserAgent(browsers=["Chrome"], os=["Linux"], platforms=["desktop"])

    print(f"  User agent added:", end="")
    print(" " * 2 + f"[bold green]--browsers={user_agent.browsers}[/bold green]")
    print(" " * 21 + f"[bold green]--os={user_agent.os}[/bold green]")
    print(" " * 21 + f"[bold green]--platforms={user_agent.platforms}[/bold green]")

    print("  Creating driver...")
    driver = create_driver("undetected_chrome", options=options, user_agent=user_agent)
    print(f"  Driver created: [bold green]{driver.name}[/bold green]")

    driver.set_window_size(1920, 1080)
    print("  Window size set to [bold green]1920x1080[/bold green]")

    interface = BrowserInterface(webdriver=driver)
    print("\n[bold]Browser interface created![/bold]\n")

    return interface


_interface: BrowserInterface | None = None


def mount_interface() -> BrowserInterface:
    global _interface

    _interface = _create_interface()

    return _interface


def get_interface(*, to_create_if_not_found: bool = True) -> BrowserInterface:
    if (_interface is None) and to_create_if_not_found:
        return mount_interface()

    if _interface is None:
        raise ValueError("Interface is not activated")

    return _interface
