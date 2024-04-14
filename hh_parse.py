import json

import requests


class HHParser:
    def __init__(self):
        self.arguments = {
            'employment': 'probation',
            'no_magic': False
        }
        self.url = 'https://api.hh.ru/vacancies'
        self.yandex_geocoder = 'https://geocode-maps.yandex.ru/1.x/'
        self.yandex_apikey = '40d1649f-0493-4b70-98ba-98533de7710b'

    def get_coordinates(self, city):
        req = requests.get(f'{self.yandex_geocoder}?apikey={self.yandex_apikey}&format=json&geocode={city}')
        if not req:
            print(req.status_code, req.reason)
            return False
        js = req.json()
        toponym = js["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        left_lng, bottom_lat = toponym['boundedBy']['Envelope']['lowerCorner'].split()
        right_lng, top_lat = toponym['boundedBy']['Envelope']['upperCorner'].split()
        return top_lat, bottom_lat, right_lng, left_lng

    def get_vacancies(self):
        res = requests.get(url=self.url, params=self.arguments)
        if not res:
            return f'{res.url} {res.status_code} {res.reason}', False
        return res, True

    def get_vacancy(self, vac_link):
        res = requests.get(vac_link)
        if not res:
            return f'{res.url} {res.status_code} {res.reason}', False
        return res, True

    def parse_vacancy(self, link):
        request, result = self.get_vacancy(link)
        if not result:
            return request
        js = request.json()
        return self.filter_json(js)

    def parse_vacancies(self):
        request, result = self.get_vacancies()
        if not result:
            return request
        js = request.json()
        links = []
        print(len(js['items']))
        for vacancy in js['items']:
            links.append(vacancy['url'])
        results = []
        for link in links:
            results.append(self.parse_vacancy(link))
        return results

    def filter_json(self, vacancy_json):
        name = vacancy_json['name']
        if vacancy_json['salary']:
            sal = vacancy_json['salary']
            if sal['from'] and not sal['to']:
                salary = f'{sal["from"]}+'
            elif not sal['from'] and sal['to']:
                salary = f'до {sal["to"]}'
            else:
                salary = f"{vacancy_json['salary']['from']}-{vacancy_json['salary']['to']}"
        else:
            salary = 'заработная плата не указана'
        schedule = vacancy_json['schedule']['name']
        employment = vacancy_json['employment']['name']
        html_description = vacancy_json['description']
        employer = vacancy_json['employer']['name']
        vacancy_link = vacancy_json['alternate_url']
        return {
            'vacancy_name': name,
            'salary': salary,
            'schedule': schedule,
            'employment': employment,
            'description': html_description,
            'employer_name': employer,
            'link': vacancy_link
        }

    def set_filters(self, **kwargs):
        self.arguments = {
            'employment': 'probation',
            'no_magic': False
        }
        for arg in ['text', 'schedule', 'salary', 'city']:
            if arg in kwargs:
                if arg != 'city':
                    self.arguments[arg] = kwargs[arg]
                else:
                    (self.arguments['top_lat'], self.arguments['bottom_lat'], self.arguments['right_lng'],
                     self.arguments['left_lng']) = self.get_coordinates(kwargs['city'])


if __name__ == '__main__':
    obj = HHParser()
    # vacancies = obj.parse_vacancies()
    # pprint.pprint(vacancies)
    # with open('test3.json', 'w', encoding='utf-8') as new_file:
    #     json.dump(vacancies, new_file, ensure_ascii=False)
    print(obj.get_coordinates('Санкт-Петербург'))
