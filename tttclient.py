#!/usr/bin/env python
# coding=utf-8

import requests


class TTTPlayer(object):
    def __init__(self, ip='127.0.0.1:8080'):
        self._ip = ip
        self._id = ''
        self._game_num = -1

    def get(self, params=''):
        """
        Method to get information about game.
        params = '': get game field and status.
        params = 'info': get game number and players' numbers.
        params = 'help': get help.
        :param params: str
        """
        if not len(params):
            params = 'get'
        rsp = requests.get('/'.join(['http:/', self._ip, '.'.join([self._id, str(self._game_num), params])]))
        print(rsp.status_code, rsp.reason)
        print(rsp.text)

    def put(self, line, col):
        """
        Method to put chip on field.
        params is string('n m', where n and m are integers), defining chip place.
        :param line: int
        :param col: int
        :return:
        """
        if self._game_num == -1:
            print('No game started')
            return
        rsp = requests.put(
            '/'.join(['http:/', self._ip, '.'.join([self._id, str(self._game_num), str(line), str(col)])]))
        print(rsp.status_code, rsp.reason)
        print(rsp.text)

    def start(self):
        """
        Method to start game. If game is already started, inform player.
        If it's player's first game, give him personal number.
        """
        if self._game_num != -1:
            print('Game {} is already started'.format(self._game_num))
            return
        cmd = '.'.join([self._id, str(self._game_num), 'start'])
        rsp = requests.get('/'.join(['http:/', self._ip, cmd]))
        print(rsp.status_code, rsp.reason)
        rsp_list = rsp.text.split('.')
        print('Player {0} started game {1}'.format(rsp_list[0], rsp_list[1]))
        print(rsp_list[2])
        self._id = rsp_list[0]
        self._game_num = int(rsp_list[1])

    def end(self):
        """
        Method to end game. If game there is no started game, inform player.
        """
        if self._game_num == -1:
            print('No game started')
            return
        rsp = requests.get('/'.join(['http:/', self._ip, '.'.join([self._id, str(self._game_num), 'end'])]))
        print(rsp.status_code, rsp.reason)
        print(rsp.text)
        self._game_num = -1

    def id(self):
        """
        Method to get player's id.
        """
        return self._id
