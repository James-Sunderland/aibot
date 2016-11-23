# AiBorGftW

from irc import *
from datetime import date
from aibot_json import *
import calendar

# irc = IRC()
aijs = Aibot_JSON()

aijs.load()

# irc.connect(server, channel, nickname)


# bday_dict = {
#     'ayaka': '2016-11-14',
#     'sayaka': '2016-11-15',
#     'momoka': '2016-11-16'
# }


def get_birthdays(bdate, bdst):
    bday_idols = aijs.find_birthdays(bdate) # search all idols who have birthday same as in bdate
    last = len(bday_idols)                  # get the number of found idols
    bdstr = bdst                            # return string with predefined message bdst
    if last == 1:                   # if only 1 idol has birthday
        bdstr += bday_idols[-1]     # add that idol to return string
    else:                           # if many idols share same birthday
        for idols in bday_idols[:-1]:   # for each idol except last
            bdstr += idols              # add her to the return string
            if last > 2 and idols != bday_idols[-2]: # if more than 2 idols and current idol is not 2nd from the end
                bdstr += ', '           # add a comma
        bdstr += ' and ' + bday_idols[-1]   # for the last idol add 'and' before her name
    # add birth date using string for Month and number for the day
    bdstr += (' at ' + calendar.month_name[int(bdate[0:2])]) + ' ' + bdate[3:5]
    return bdstr


def get_next_birthdays(bdate):
    bday_idols = aijs.next_birthday(bdate)
    print(get_birthdays(bday_idols['birthday'][5:], 'Next birthday is for '))
    return


def get_prev_birthdays(bdate):
    bday_idols = aijs.prev_birthday(bdate)
    print(get_birthdays(bday_idols['birthday'][5:], 'Previous birthday was for '))
    return


cmd_dict = {
    '!load': aijs.load(),
    '!next': get_next_birthdays('{0:%m-%d}'.format(date.today())),
    '!prev': get_prev_birthdays('{0:%m-%d}'.format(date.today())),
    '!quiz': 'quiz starting',
    '!time': date.today(),
    '!bday': get_birthdays('{0:%m-%d}'.format(date.today()), 'Today is a birthday of ')

}

a = cmd_dict['!next']
# print(a)
# for i in a:
# print(i)

'''
while True:
    # sleep(0.1)
    text = irc.get_text().strip()
    print(text)
    text_a = text.split(bytes(' ', 'utf8'))
    if len(text_a) > 3 and text_a[3][1:2] == bytes("!", 'utf8'):
        cmd = text_a[3][1:]
        if str(cmd, 'utf8') in cmd_dict:
            irc.send(channel, cmd_dict[str(cmd, 'utf8')])


'''