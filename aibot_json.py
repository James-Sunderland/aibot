import json
import datetime

class Aibot_JSON:

    data = ""

    @staticmethod
    def load():
        fi = open('bday.json', encoding='utf-8')
        g = fi.read()
        global data
        data = json.loads(g)
        fi.close()

    @staticmethod
    def find_birthdays(theday):
        bd = []
        for idol in data:
            if idol['birthday'][5:] == theday:
                bd.append(idol['surname'] + ' ' + idol['name'] + ' (' + idol['group'] + ')')
        return bd

    @staticmethod
    def next_birthday(theday):
        bd = sorted(data, key=lambda k: datetime.datetime.strptime(k['birthday'][5:], '%m-%d'))

        be = list(filter(lambda idol: idol['birthday'][5:] > theday, bd))

        return be[0]

    @staticmethod
    def prev_birthday(theday):
        bd = sorted(data, key=lambda k: datetime.datetime.strptime(k['birthday'][5:], '%m-%d'))
        be = list(filter(lambda idol: idol['birthday'][5:] < theday, bd))

        return be[-1]
