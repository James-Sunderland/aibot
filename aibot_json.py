import json
import datetime
import calendar


class AibotJson:

    data = ""

    @staticmethod
    def load():
        fi = open('bday.json', encoding='utf-8')
        g = fi.read()
        global data
        data = json.loads(g)
        fi.close()

    @staticmethod
    def find_birthdays_by_month(themonth):
        bd = sorted(data, key=lambda k: datetime.datetime.strptime(k['birthday'][5:], '%m-%d'))
        be = list(filter(lambda idol: idol['birthday'][5:7] == themonth and idol['status'] == '1', bd))
        bd = []
        for idol in be:
            if idol['birthday'][5:7] == themonth and idol['status'] == '1':
                bd.append(idol['surname'] + ' ' + idol['name'] + ' on ' + calendar.month_name[int(themonth)] + ' ' + str(int(idol['birthday'][8:10])) + ' (' + idol['group'] + ')')
        return bd

    @staticmethod
    def find_birthdays(theday):
        bd = []
        for idol in data:
            if idol['birthday'][5:] == theday and idol['status'] == '1':
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

    @staticmethod
    def from_birthplace(theplace):
        be = []
        bd = list(filter(lambda idol: idol['birthplace'] == theplace and idol['status'] == '1', data))
        for idol in bd:
            be.append(idol['surname'] + ' ' + idol['name'] + ' (' + idol['group'] + ')')
        return be

    @staticmethod
    def get_birthplaces():
        be = sorted(set([d['birthplace'] for d in data]))
        return be

    @staticmethod
    def get_idol_info(thename):
        be = []
        ex = ''
        bd = list(filter(lambda idol: idol['surname'] == thename or idol['name'] == thename, data))
        for idol in bd:
            if idol['status'] == '0':
                ex = 'ex-'
            be.append(idol['surname'] + ' ' + idol['name'] + ' (' + ex + idol['group'] + ') born ' + idol['birthday'] + ' in ' + idol['birthplace'])
            ex = ''
        return be
