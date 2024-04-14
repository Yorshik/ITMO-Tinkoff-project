from pprint import pprint

from bs4 import BeautifulSoup
import requests


class HabrParser:
    def __init__(self):
        self.specialities = {
            "Разработка": "dev",
            "Тестирование": "testing",
            "Администрирование": "administration",
            "Менеджмент": "management",
            "Дизайн": "design",
            "Аналитика": "analytics",
            "Маркетинг": "marketing"
        }
        self.url = 'https://career.habr.com/'
        self.page = requests.get(self.url)

    def parse(self, speciality):
        soup = BeautifulSoup(self.page.content, "html.parser")

        division = soup.find(attrs={"data-tab": self.specialities[speciality]})
        cards = []

        for el in division.find_all(name="li", attrs={"class": "l-card-list__item"}):
            title = el.find(attrs={"class": "l-vacancy-card__title"}).text
            company = el.find(attrs={"class": "l-vacancy-card__company-title"}).text
            salary = el.find(attrs={"class": "l-vacancy-card__salary"}).text
            place = el.find(attrs={"class": "l-vacancy-card__company-subtitle"}).text

            card = {"title": title,
                    "salary": salary,
                    "place": place,
                    "company": company}

            cards.append(card)
        return cards


if __name__ == "__main__":
    parser = HabrParser()
    vacancy = parser.parse("Разработка")
    pprint(vacancy)
