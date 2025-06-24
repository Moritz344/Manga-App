import rich
from rich.console import Console
import logging
from rich.logging import RichHandler

class NerdCLI:
    def __init__(self,):
        print("nerding...")
        self.console = Console()
        FORMAT = "%(message)s"
        logging.basicConfig(
            level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
        )

        self.log = logging.getLogger("rich")

    
    def start_output(self,manga_title):
        self.log.info(f"[green]Title: [/] [bold yellow]{manga_title} [/]",extra={"markup":True})
    
    def print_status_code(self,code):
        if code == 200:
            self.log.info(f"[green]puhhh. We are safe for now. {code}  [/]",extra={"markup":True})
        else:
            self.log.error(f"[bold red blink] CRITICAL: {code} [/]",extra={"markup": True})
        
    def download_output(self,pages,chapter_number,manga_title,host,chapter_hash):
        self.log.info(f"[green] MANGA_TITLE:    {manga_title} [/]")
        self.log.info(f"[green] PAGES:          {pages} [/]")
        self.log.info(f"[green] CHAPTER_NUMBER: {chapter_number} [/]")
        self.log.info(f"[green] HOST:           {host} [/]")
        self.log.info(f"[green] CHAPTER_HASH:   {chapter_hash} [/]")
