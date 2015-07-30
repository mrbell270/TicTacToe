#!/usr/bin/python
# coding=utf-8


from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from tttgame import TTTGame
from tttgame import help_text
import textwrap
import sys
import hashlib
import random


class TTTPool(object):
    def __init__(self):
        self.game_pool = []
        self.games_stack = []
        self.games_amount = 0
        self.players_stack = dict()

    def add_player(self, player_id):
        """
        Add new player.
        If there are free players, start game between player 'player_num' and waiting player.
        If there are no free players, create new game and put player to waiting state.
        :param player_id: str
        :return: int
        """
        if len(self.players_stack):
            tmp = self.players_stack.popitem()
            opponent = tmp[0]
            game_num = tmp[1]
            self.game_pool[game_num].game_on_bitch(opponent, player_id)
        else:
            if len(self.games_stack):
                game_num = self.games_stack.pop()
                pool.game_pool[game_num] = TTTGame()
            else:
                game = TTTGame()
                game_num = self.games_amount
                self.game_pool.append(game)
                self.games_amount += 1
            self.players_stack[player_id] = game_num
        print('Player {} connected'.format(player_id))
        return game_num

    def del_player(self, game_num, player_id):
        """
        Exclude player 'player_num' from game 'game_num'.
        If player has no opponent, end game.
        :param game_num: int
        :param player_id: str
        """
        players = self.game_pool[game_num].players
        if 0 in players:
            del pool.players_stack[player_id]
            pool.games_stack.append(game_num)
            return
        save_player = players[1]
        if save_player == player_id:
            save_player = players[2]
        pool.games_stack.append(game_num)
        self.add_player(save_player)


pool = TTTPool()


class TTTHTTPRequestHandler(BaseHTTPRequestHandler):
    def _reply(self, body='', code=200):
        self.send_response(code)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        """
        Method, giving client information about game, creating new game for client and
        (if necessary) assigning player number to client, ending game of client.:
         - get help;
         - get start;
         - get end;
         - get game field and status;
         - get game number and players' numbers.
        :return:
        """
        cmd = self.path.strip('/').split('.')
        player_id = cmd[0]
        game_num = int(cmd[1])
        if cmd[2].lower() == 'help':
            self._reply(textwrap.dedent(help_text))
        elif cmd[2].lower() == 'get':
            if game_num == -1:
                self._reply('No game started. To start print "start"')
                return
            self._reply(str(pool.game_pool[int(cmd[1])]))
        elif cmd[2].lower() == 'info':
            if game_num < pool.games_amount:
                self._reply(''.join(['Game number: ', cmd[1], '\nPlayer 1 number: ',
                                     str(pool.game_pool[game_num].players[1]), '\nPlayer 2 number: ',
                                     str(pool.game_pool[game_num].players[2])]))
            else:
                self._reply('Game number error', 404)
        elif cmd[2].lower() == 'start':
            if player_id == '':
                player_id = hashlib.sha224(str(random.randint(0, sys.maxint))).hexdigest()
            game_num = pool.add_player(player_id)
            self._reply('.'.join([player_id, str(game_num), str(pool.game_pool[game_num])]))
        elif cmd[2].lower() == 'end':
            pool.del_player(game_num, player_id)
            self._reply()
        else:
            self._reply('Bad command. Try "get help" for help.', 404)

    def do_PUT(self):
        """
        Method, putting client's chip on field.
        :return:
        """
        cmd = self.path.strip('/').split('.')
        try:
            player_id = cmd[0]
            game_num = int(cmd[1])
            line = int(cmd[2])
            col = int(cmd[3])
        except:
            self._reply('Wrong usage of "put"')
            return
        game_field = pool.game_pool[game_num].put(player_id, line - 1, col - 1)
        state = pool.game_pool[game_num].state
        if state > 1:
            self._reply(''.join([game_field, '\nPrint "END" to finish the game and "start" to start new one\n']))
        else:
            self._reply(game_field)


def main():
    print('...')
    server_address = ('127.0.0.1', 8080)  # port num???
    httpd = HTTPServer(server_address, TTTHTTPRequestHandler)
    print('server is running')
    httpd.serve_forever()


if __name__ == '__main__':
    main()
