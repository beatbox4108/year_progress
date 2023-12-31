import yaml
import jinja2
from pathlib import Path
import wand.image
from datetime import datetime,timezone,timedelta,date
import calendar

def round_int(number):
    return int((number * 2 + 1) // 2)

day=timedelta(days=1)
JST=timezone(timedelta(hours=9),"Japan Standard Time")
now=(datetime.now(JST)+day).date()
year=date(now.year,1,1)
yeardays=(now-year).days+1
yeardays_total=366 if calendar.isleap(year.year) else 365

week=(yeardays-year.day)//7+1
week_total=(yeardays_total-year.day)//7+1

data={
    "info":{
        "year":year.year,
        "week":{
            "value": week,
            "total": week_total
        },
        "date":{
            "value": yeardays,
            "total": yeardays_total,
            "string":datetime.now(JST).strftime('%Y-%m-%dT%H:%M')
        }
    }
}
complete=round_int(data["info"]["date"]["value"]/data["info"]["date"]["total"]*100)
data["progress"]={
    "complete":complete,
    "remain":100-complete
}

with open(Path(__file__).parent/"config.yml","r",encoding="utf-8")as f:
    config=yaml.safe_load(f)

with open(Path(__file__).parent/"progress.svg.j2","r",encoding="utf-8")as f:
    template=jinja2.Template(f.read())
with open(Path(__file__).parent/"pub"/"progress.svg","w",encoding="utf-8")as f:
    svg=template.render(**config,**data)
    f.write(svg)
with open(Path(__file__).parent/"pub"/"progress.png","bw")as f:
    wand.image.Image(blob=svg.encode("UTF-8"),format="SVG").convert("PNG").save(f)