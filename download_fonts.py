import json
from urllib.request import urlopen
from pathlib import Path
import rich.progress
import rich.logging
import rich
import logging
import os
FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[rich.logging.RichHandler()]
)
logger=logging.getLogger("Fonts Downloader")
with rich.progress.Progress() as progress:

    api_key=os.environ["API_KEY"]
    url=f"https://www.googleapis.com/webfonts/v1/webfonts?key={api_key}&family=M+PLUS+Rounded+1c"
    task1=progress.add_task("[green]Downloading Metadata...",total=None)
    with urlopen(url)as res:
        data=json.load(res)
    font_root=Path("/usr/share/fonts/googlefonts")
    font_root.mkdir(parents=True,exist_ok=True)
    rich.print(data)
    progress.update(task1,total=len(data["items"]),description="[blue]Downloading Font(s)...")
    
    for family in data["items"]:
        family_root=font_root/family["family"]
        family_root.mkdir(parents=True,exist_ok=True)
        task2=progress.add_task("[red]Downloading Variant(s)...",total=len(family["files"]))
        logger.info(f"Downloading Font '{family['family']}'.")
        for variant,file in family["files"].items():
            with open(family_root/f"""{family["family"]}-{variant}""","bw")as f:
                logger.info(f"Downloading Variant '{family['family']}-{variant}'.")
                with urlopen(file)as res:
                    f.write(res.read())
                progress.update(task2, advance=1)
                logger.info(f"Successfly Downloaded '{family['family']}-{variant}'.")
        progress.remove_task(task2)
        logger.info(f"Successfly Downloaded Font '{family['family']}'.")
        progress.update(task1, advance=1)