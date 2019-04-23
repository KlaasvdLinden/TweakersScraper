import urllib.request
from bs4 import BeautifulSoup

from prettytable import PrettyTable


def get_response(keyword):
    if keyword == "latest":
        link = "https://tweakers.net/categorie/638/games/aanbod/"
    else:
        link = "https://tweakers.net/aanbod/zoeken/?keyword=" + keyword
        link = link.replace(" ", "%20")
    print(link)
    response = ''
    try:
        response = urllib.request.urlopen(link)
    except Exception as e:
        print(e)
        pass

    return response


def response_to_soup(response):
    soup = BeautifulSoup(response, "html.parser")
    return soup


print("Welkom bij de Tweakers V&A scraper!")
userInput = input("Typ de naam van een product: ")

resp = get_response(userInput)
if resp is '':
    print("Geen resultaten gevonden")
else:
    table = response_to_soup(resp).findAll("table")
    for adv in table:
        titles = adv.findAll("p", {"class": "title ellipsis"})
        dates = adv.findAll("span", {"class": "date"})
        scores = adv.findAll("span", {"class": "sprite"})
        prices = adv.findAll("td", {"class": "vaprice"})
        locations = adv.findAll("td", {"class": "location city"})
        locations.extend(adv.findAll("td", {"class": "location city noDistance"}))

        users = adv.findAll("td", {"class": "location"})
        users = [x for x in users if x not in locations]

        pretty_table = PrettyTable(["Title", "Date", "Location", "User", "Score", "Price"])
        for t, d, loc, u, s, p in zip(titles, dates, locations, users, scores, prices):
            t = t.text.strip("\r\n")
            d = d.text.strip("\r\n")
            loc = loc.find("p", {"class": "ellipsis"}).text.strip("\r\n")
            u = u.find("p", {"class": "subtitle"}).text.strip("\r\n")
            s = s.text.strip("\r\n")[-1:]
            p = p.text.strip("\r\n").replace(" ", "")

            pretty_table.add_row([t, d, loc, u, s, p])

        print(pretty_table)
