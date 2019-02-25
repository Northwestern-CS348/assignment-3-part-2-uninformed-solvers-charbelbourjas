from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        peg1 = []
        peg2 = []
        peg3 = []

        ask1 = parse_input("fact: (inst ?peg peg)")
        all_pegs = self.kb.kb_ask(ask1)

        for bindings_peg in all_pegs:
            if not Fact(instantiate(Statement(("empty", "?peg")), bindings_peg)) in self.kb.facts:
                all_disks = self.kb.kb_ask(Fact(instantiate(Statement(("on", "?disk", "?peg")), bindings_peg)))
                initial_disks = []

                for bindings_disk in all_disks:
                    disk_first = int(bindings_disk.bindings_dict["?disk"][4])
                    initial_disks.append(disk_first)
                peg_first = int(bindings_peg.bindings_dict["?peg"][3])

                if peg_first == 1:
                    if initial_disks:
                        while initial_disks:
                            smallest = min(initial_disks)
                            peg1.append(smallest)
                            initial_disks.remove(smallest)

                elif peg_first == 2:
                    if initial_disks:
                        while initial_disks:
                            smallest = min(initial_disks)
                            peg2.append(smallest)
                            initial_disks.remove(smallest)

                else:
                    if initial_disks:
                        while initial_disks:
                            smallest = min(initial_disks)
                            peg3.append(smallest)
                            initial_disks.remove(smallest)

        state = (tuple(peg1), tuple(peg2), tuple(peg3))
        return state

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        index = movable_statement.terms
        disk = index[0]
        start = index[1]
        end = index[2]

        new_top = self.kb.kb_ask(Fact(Statement(("onTop", disk, "?obj"))))[0]
        rule1 = Fact(instantiate(Statement(("onTop", disk, "?obj")), new_top))
        ask1 = Fact(instantiate(Statement(("top", "?obj", start)), new_top))
        old_top = self.kb.kb_ask(Fact(Statement(("top", "?obj", end))))[0]

        rule2 = Fact(instantiate(Statement(("top", "?obj", end)), old_top))
        ask2 = Fact(instantiate(Statement(("onTop", disk, "?obj")), old_top))

        self.kb.kb_retract(Fact(Statement(("on", disk, start))))
        self.kb.kb_retract(Fact(Statement(("top", disk, start))))
        self.kb.kb_retract(rule1)
        self.kb.kb_retract(rule2)
        self.kb.kb_assert(Fact(Statement(("on", disk, end))))
        self.kb.kb_assert(Fact(Statement(("top", disk, end))))
        self.kb.kb_assert(ask1)
        self.kb.kb_assert(ask2)


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        cols_rows = {"pos1": ("pos1", "pos2", "pos3"),"pos2": ("pos1", "pos2", "pos3"),"pos3": ("pos1", "pos2", "pos3")}
        state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        for pos_y in cols_rows:
            y = int(pos_y[3]) - 1

            for pos_x in cols_rows[pos_y]:
                x = int(pos_x[3]) - 1

                ask1 = Fact(Statement(["coord", "?tile", pos_x, pos_y]))
                binding = self.kb.kb_ask(ask1)[0]
                tile1 = binding.bindings_dict["?tile"][4]
                tile_start = 0

                if tile1 == 'y':
                    tile_start = -1
                else:
                    tile_start = int(tile1)
                state[y][x] = tile_start

        return tuple([tuple(state[0]), tuple(state[1]), tuple(state[2])])

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        index = movable_statement.terms
        tile = index[0]

        start_x = index[1]
        start_y = index[2]
        end_x = index[3]
        end_y = index[4]



        self.kb.kb_retract(Fact(Statement(("coord", tile, start_x, start_y))))
        self.kb.kb_retract(Fact(Statement(("coord", "empty", end_x, end_y))))
        self.kb.kb_assert(Fact(Statement(("coord", tile, end_x, end_y))))
        self.kb.kb_assert(Fact(Statement(("coord", "empty", start_x, start_y))))


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
