from irc import *
from datetime import date
from aibot_json import *
import calendar
import time

irc = IRC()
aijs = AibotJson()


argum = ''

aijs.load()

irc.connect(server, channel, nickname)


# bday_dict = {
#     'ayaka': '2016-11-14',
#     'sayaka': '2016-11-15',
#     'momoka': '2016-11-16'
# }

def get_birthdays_by_month(bdate):
    ret = ''
    m = 1
    try:
        m = int(bdate)
    except ValueError:
        return 'Please enter valid number'
    if bdate.isdigit():
        idols = aijs.find_birthdays_by_month(bdate)
        last = len(idols)
        for idol in idols[:-1]:   # for each idol except last
            ret += idol              # add her to the return string
            if last > 2 and idol != idols[-2]: # if more than 2 idols and current idol is not 2nd from the end
                ret += ', '           # add a comma
        ret = 'Idols who are born on ' + calendar.month_name[m] + ' are ' + ret + ' and ' + idols[-1]   # for the last idol add 'and' before her name
    else:
        return 'Usage: !bday month_digits (example: !bday 02)'
    return ret


def get_birthdays(bdate='{0:%m-%d}'.format(date.today()), bdst='Today is a birthday of '):
    # print(bdate)
    # global argum
    if argum:
        bdate = argum
    if bdate in calendar.month_abbr or bdate.isdigit():
        # print('entering next function')
        return get_birthdays_by_month(bdate)
    bday_idols = aijs.find_birthdays(bdate) # search all idols who have birthday same as in bdate
    last = len(bday_idols)                  # get the number of found idols
    bdstr = bdst                            # return string with predefined message bdst
    if last == 0:
        bdstr = "No idol has birthday today"
        return bdstr
    if last == 1:                   # if only 1 idol has birthday
        bdstr += bday_idols[-1]     # add that idol to return string
    else:                           # if many idols share same birthday
        for idols in bday_idols[:-1]:   # for each idol except last
            bdstr += idols              # add her to the return string
            if last > 2 and idols != bday_idols[-2]: # if more than 2 idols and current idol is not 2nd from the end
                bdstr += ', '           # add a comma
        bdstr += ' and ' + bday_idols[-1]   # for the last idol add 'and' before her name
    # add birth date using string for Month and number for the day
    bdstr += (' on ' + calendar.month_name[int(bdate[0:2])]) + ' ' + bdate[3:5]
    return bdstr


def get_next_birthdays(bdate):
    bday_idols = aijs.next_birthday(bdate)
    # print(get_birthdays(bday_idols['birthday'][5:], 'Next birthday is for '))
    return get_birthdays(bday_idols['birthday'][5:], 'Next birthday is for ')


def get_prev_birthdays(bdate):
    bday_idols = aijs.prev_birthday(bdate)
    # print(get_birthdays(bday_idols['birthday'][5:], 'Previous birthday was for '))
    return get_birthdays(bday_idols['birthday'][5:], 'Previous birthday was for ')


def get_idols_by_birthplace():
    # global argum
    if not argum:
        return 'Usage: !from place (for example !from Osaka)'
    idols = aijs.from_birthplace(argum)
    print(idols)
    if len(idols) == 0:
        return "There are no idols from " + argum
    elif len(idols) > 1:
        names = ''
        for idol in idols[:-2]:
            names += (idol + ', ')
        s = 'Idols who are from ' + argum + ' are ' + names + idols[-2] + ' and ' + idols[-1] + ' (total: ' + str(len(idols)) + ')'
    else:
        s = 'Only ' + idols[0] + ' is from ' + argum
    return s


def get_birthplaces():
    places = aijs.get_birthplaces()
    s = ''
    for place in places[:-2]:
        s += (place + ', ')
    s = 'There are idols from ' + s + places[-2] + ' and ' + places[-1] + ' (total: ' + str(len(places)) + ')'
    return s


def get_idol_info():
    if not argum:
        return 'Usage !who surname (example: !who Matsumura)'
    s = ''
    idols = aijs.get_idol_info(argum)
    if len(idols) == 0:
        return 'There are no idols with name ' + argum
    elif len(idols) > 1:
        for idol in idols[:-2]:
            s += idol + ', '
        s = 'Idols with name ' + argum + ' are ' + s + idols[-2] + ' and ' + idols[-1] + ' (total: ' + str(len(idols)) + ')'
    else:
        s = idols[0]
    return s


def get_list_of_commands():
    s = ''
    for c in cmd_dict[:-2]:
        s += c + ', '
    s = 'Next commands are available: ' + s + cmd_dict[-2] + ' and ' + cmd_dict[-1]
    return s

cmd_dict = ['!help', '!from', '!next', '!prev', '!test', '!bday', '!places', '!who']


def do_command(thecmd):
    global argum
    ret = ''
    if thecmd == '!test':
        ret = 'test passed'
    if thecmd == '!bday':
        ret = get_birthdays()
    elif thecmd == '!from':
        ret = get_idols_by_birthplace()
    elif thecmd == '!prev':
        ret = get_prev_birthdays('{0:%m-%d}'.format(date.today()))
    elif thecmd == '!next':
        ret = get_next_birthdays('{0:%m-%d}'.format(date.today()))
    elif thecmd == '!places':
        ret = get_birthplaces()
    elif thecmd == '!who':
        ret = get_idol_info()
    elif thecmd == '!help':
        ret = get_list_of_commands()
    argum = ''
    return ret

while True:
    time.sleep(0.1)
    text = irc.get_text().strip()       # get string from IRC
    print(text)
    text_a = text.split(bytes(' ', 'utf8'))
    l = len(text_a)
    if l > 3 and text_a[3][1:2] == bytes("!", 'utf8'):
        cmd = text_a[3][1:]
        if l > 4:
            # global argum
            argum = text_a[4].decode('utf8')
        if str(cmd, 'utf8') in cmd_dict:
            sending_message = do_command(cmd.decode('utf8'))
            # sending_message = cmd_dict[str(cmd, 'utf8')]
            irc.send(channel, sending_message)
            # print(sending_message)


