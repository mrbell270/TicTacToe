#!/usr/bin/env python
# coding=utf-8

import httplib


class TTTPlayer(object):
    def __init__(self, ip='127.0.0.1'):
        self._ip = ip
        self.num = 0
        self.game_num = -1

    def get(self, params):
        """
        Method to get information about game.
        params = []: get game field and status.
        params = ['info']: get game number and players' numbers.
        params = ['help']: get help.
        :param params: str[]
        """
        conn = httplib.HTTPConnection(self._ip)
        if not len(params):
            params.append('get')
        conn.request('GET', '.'.join([str(self.num), str(self.game_num), params[0]]))
        rsp = conn.getresponse()
        print(rsp.status, rsp.reason)
        print(rsp.read())
        conn.close()

    def put(self, params):
        """
        Method to put chip on field.
        params is string('n m', where n and m are integers), defining chip place.
        :param params: str[]
        :return:
        """
        if self.game_num == -1:
            print('No game started')
            return
        conn = httplib.HTTPConnection(self._ip)
        try:
            int(params[0])
            int(params[1])
        except Exception:
            print('Wrong usage of "put". Try "get help" for help.')
            return
        spot = '.'.join(params)
        conn.request('PUT', '.'.join([str(self.num), str(self.game_num), spot]))
        rsp = conn.getresponse()
        print(rsp.status, rsp.reason)
        print(rsp.read())
        conn.close()

    def start(self):
        """
        Method to start game. If game is already started, inform player.
        If it's player's first game, give him personal number.
        """
        if self.game_num != -1:
            print('Game {} is already started'.format(self.game_num))
            return
        conn = httplib.HTTPConnection(self._ip)
        conn.request('START', '.'.join(map(str, [self.num, self.game_num])))
        rsp = conn.getresponse()
        print(rsp.status, rsp.reason)
        rsp_list = rsp.read().split('.')
        print(rsp_list[2])
        conn.close()
        self.num = int(rsp_list[0])
        self.game_num = int(rsp_list[1])

    def end(self):
        """
        Method to end game. If game there is no started game, inform player.
        """
        if self.game_num == -1:
            print('No game started')
            return
        conn = httplib.HTTPConnection(self._ip)
        conn.request('END', '.'.join(map(str, [self.num, self.game_num])))
        rsp = conn.getresponse()
        print(rsp.status, rsp.reason)
        print(rsp.read())
        conn.close()
        self.game_num = -1

    def spec(self, params):
        """
        Method to see field of game with number, specified in params
        :param params: str[]
        """
        try:
            int(params[0])
        except Exception:
            print('Wrong usage of "spec". Try "get help" for help.')
            return
        conn = httplib.HTTPConnection(self._ip)
        conn.request('SPEC', str(params[0]))
        rsp = conn.getresponse()
        print(rsp.status, rsp.reason)
        print(rsp.read())
        conn.close()


def main():
    player = TTTPlayer()
    while True:
        comm = raw_input('Player\'s command(for example "get help"): ')
        if comm == 'q':
            player.end()
            break
        cmd = comm.split()[0].upper()
        params = comm.split()[1:]
        if cmd == 'GET':
            player.get(params)
        elif cmd == 'PUT':
            player.put(params)
        elif cmd == 'START':
            player.start()
        elif cmd == 'END':
            player.end()
        elif cmd == 'SPEC':
            player.spec(params)
        else:
            print('Unknown command. Try "get help" for help')

if __name__ == '__main__':
    main()