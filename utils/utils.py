from datetime import datetime

presences = ["Présent","Absent","En retard","Incertain"]

def format_datetime(value, format="%d %b %Y"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)

def get_datetime(jour, heure):
    print(jour)
    print(heure)
    #form.date.data.strftime("%Y-%m-%D").split("-")
    j = jour.strftime("%Y-%m-%d").split("-")
    j = [ int(x) for x in j ]
    print(j)
    h = heure.strftime("%H:%M").split(":")
    h = [int(x) for x in h]
    print(h)
    return datetime(year=j[0],month=j[1],day=j[2],hour=h[0],minute=h[1])