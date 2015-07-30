# coding=utf-8


class TTTCell(object):
    def __init__(self, num):
        self.sign = 0
        self.line = num // 3
        self.col = num % 3
        col_list = [self.col, self.col + 3, self.col + 6]
        line_list = [3 * self.line, 3 * self.line + 1, 3 * self.line + 2]
        self.check_lists = [col_list, line_list]
        if self.line == self.col:
            self.check_lists.append([0, 4, 8])
        if (self.line + self.col) == 2:
            self.check_lists.append([2, 4, 6])

    def __str__(self):
        return ' '.join(
            ['sign', str(self.sign), '\nlin', str(self.line), '\ncol', str(self.col)])


class TTTGame(object):
    _field_size = 9
    _state_messages = ['Waiting for opponent.', 'Game is on.', 'No place to make turn. It is draw.']

    def __init__(self):
        self.cells = []
        for i in range(self._field_size):
            self.cells.append(TTTCell(i))
        self.unchanged = self._field_size
        self.players = (0, 0, 0)
        self.turn = 0
        self.state = 0

    def game_on_bitch(self, player_1, player_2):
        """
        Starting game between players 'player_1' and 'player_2'.
        'player_1' is the first to put his chip.
        :param player_1: int
        :param player_2: int
        """
        self.players = (-1, player_1, player_2)
        self.turn = 1
        self.state = 1

    def put(self, player_num, line, col):
        """
        Put chip of player 'player_num' on crossing of line 'line' and colon 'col'.
        If game is not started, inform player.
        If game is finished, inform player.
        If spot is busy, inform player and wait player to choose another spot.
        :param player_num: int
        :param line: int
        :param col: int
        """
        idx = 3 * line + col
        player = self.players.index(player_num)
        if self.state < 1:
            return 'No opponent, can not start the game'
        if self.state > 1:
            return '\n'.join(['Game is over', str(self)])
        if self.cells[idx].sign:
            return 'Can not place chip here. Choose another cell'
        if player == self.turn:
            self.cells[idx].sign = self.turn
            self.unchanged -= 1
            if self._check_state(idx) == self.turn:
                self._state_messages.append(
                    ''.join(['Player ', str(self.turn), '(', str(self.players[self.turn]), ') won!!!']))
                self.state = 3
        else:
            return 'It is turn of your opponent'
        if self.unchanged == 0:
            self.state = 2
        self.turn = (self.turn % 2) + 1
        return str(self)

    def _check_state(self, num):
        for list_of_idx in self.cells[num].check_lists:
            if self._check_list(list_of_idx):
                return self.cells[num].sign
        return 0

    def _check_list(self, list_of_idx):
        return self.cells[list_of_idx[0]].sign == self.cells[list_of_idx[1]].sign == self.cells[list_of_idx[2]].sign

    def __str__(self):
        tmp = ''
        if self.state > 0:
            tmp = ''.join(['It\'s Player ', str(self.turn), ' (', str(self.players[self.turn]), ') turn\n'])
        signs = {0: '_', 1: 'X', 2: 'O'}
        for i in range(3):
            for j in range(3):
                idx = 3 * i + j
                tmp = '|'.join([tmp, signs[self.cells[idx].sign]])
            tmp = '|'.join([tmp, '\n'])
        return ''.join([tmp, self._state_messages[self.state], '\n'])

help_text = """
Methods of TTTPlayer
"get()" - see game field
"get('help')" - get help
"get('info')" - see game info
"start()" - start game
"put([n], [m])" - put chip on [n] line, [m] colon
"end()" - end current game
"""
