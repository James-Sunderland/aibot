import socket

channel = "#aidoru-quiz"
server = "chat.freenode.org"
nickname = "aiborg"
password = "AiBorGftW"


class IRC:
    irc = socket.socket()

    def __init__(self):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, chan, msg):
        # print('sending..')
        # self.irc.send(bytes("PRIVMSG %s :test message\n" % channel, 'utf8'))
        self.irc.send(bytes("PRIVMSG %s :%s\n" % (chan, msg), 'utf8'))

    def connect(self, server, channel, botnick):
        # defines the socket
        print("connecting to: " + server)
        self.irc.connect((server, 6667))  # connects to the server

        self.irc.send(bytes("NICK %s\n" % botnick, 'utf8'))
        self.irc.send(bytes("USER %s %s Ibot :%s\n" % (botnick, botnick, botnick), 'utf8'))
        self.irc.send(bytes("JOIN %s\n" % channel, 'utf8'))
        self.irc.send(bytes("PRIVMSG NickServ IDENTIFY %s %s\n" % (botnick, password), 'utf8'))
        self.irc.send(bytes("PRIVMSG %s :Hello Master\n" % channel, 'utf8'))

    def get_text(self):
        text = self.irc.recv(2040)  # receive the text

        if text.find(bytes('PING', 'utf8')) != -1:
            self.irc.send(bytes('PONG ' + str(text.split()[1], 'utf8') + 'rn', 'utf8'))

        return text
