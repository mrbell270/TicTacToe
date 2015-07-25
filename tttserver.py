#!/usr/bin/python
# coding=utf-8


from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from tttgame import TTTGame
from tttgame import help_text
import textwrap


class TTTPool(object):
    def __init__(self):
        self.game_pool = []
        self.games_stack = []
        self.games_amount = 0
        self.players_stack = dict()
        self.players_amount = 0

    def add_player(self, player_num):
        """
        Add new player.
        If there are free players, start game between player 'player_num' and waiting player.
        If there are no free players, create new game and put player to waiting state.
        :param player_num: int
        :return: int
        """
        if len(self.players_stack):
            tmp = self.players_stack.popitem()
            opponent = tmp[0]
            game_num = tmp[1]
            self.game_pool[game_num].game_on_bitch(opponent, player_num)
        else:
            if len(self.games_stack):
                game_num = self.games_stack.pop()
                pool.game_pool[game_num] = TTTGame()
            else:
                game = TTTGame()
                game_num = self.games_amount
                self.game_pool.append(game)
                self.games_amount += 1
            self.players_stack[player_num] = game_num
        return game_num

    def del_player(self, game_num, player_num):
        """
        Exclude player 'player_num' from game 'game_num'.
        If player has no opponent, end game.
        :param game_num: int
        :param player_num: int
        """
        players = self.game_pool[game_num].players
        if 0 in players:
            del pool.players_stack[player_num]
            pool.games_stack.append(game_num)
            return
        save_player = players[1]
        if save_player == player_num:
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
        Method, giving client information about game:
         - get help;
         - get game field and status;
         - get game number and players' numbers.
        :return:
        """
        request = self.path.split('.')
        if request[2].lower() == 'help':
            self._reply(textwrap.dedent(help_text))
        elif request[2].lower() == 'get':
            if int(request[1]) == -1:
                self._reply('No game started. To start print "start"')
                return
            self._reply(str(pool.game_pool[int(request[1])]))
        elif request[2].lower() == 'info':
            if int(request[1]) < pool.games_amount:
                self._reply(''.join(['Game number: ', request[1], '\nPlayer 1 number: ',
                                     str(pool.game_pool[int(request[1])].players[1]), '\nPlayer 2 number: ',
                                     str(pool.game_pool[int(request[1])].players[2])]))
            else:
                self._reply('Game number error')

        else:
            self._reply('Bad command. Try "get help" for help.')

    def do_PUT(self):
        """
        Method, putting client's chip on field.
        :return:
        """
        cmd = map(int, self.path.split('.'))
        game_field = pool.game_pool[cmd[1]].put(cmd[0], cmd[2] - 1, cmd[3] - 1)
        state = pool.game_pool[cmd[1]].state
        if state > 1:
            self._reply(''.join([game_field, '\nPrint "END" to finish the game and "start" to start new one\n']))
        else:
            self._reply(game_field)

    def do_START(self):
        """
        Method, creating new game for client and (if necessary) assigning player number to client
        :return:
        """
        cmd = map(int, self.path.split('.'))
        if not cmd[0]:
            pool.players_amount += 1
            cmd[0] = pool.players_amount
        game_num = pool.add_player(cmd[0])
        self._reply(
            '\n'.join(['{0}.{1}.Player {0} started game {1}'.format(cmd[0], game_num), str(pool.game_pool[game_num])]))

    def do_END(self):
        """
        Method, ending game of client.
        :return:
        """
        cmd = map(int, self.path.split('.'))
        pool.del_player(cmd[1], cmd[0])
        self._reply()

    def do_SPEC(self):
        """
        Method, showing client requested game field.
        :return:
        """
        num = int(self.path.split('.')[2])
        if num < pool.games_amount:
            self._reply(str(pool.game_pool[num]))
        else:
            self._reply(''.join(
                ['Game ', self.path.split('.')[2], 'is not started yet\nThere are ', str(pool.games_amount),
                 ' games.\n']))


def main():
    print('...')
    server_address = ('127.0.0.1', 80)  # port 80???
    httpd = HTTPServer(server_address, TTTHTTPRequestHandler)
    print('server is running')
    httpd.serve_forever()


if __name__ == '__main__':
    main()
