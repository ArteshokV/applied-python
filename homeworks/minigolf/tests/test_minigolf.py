from unittest import TestCase

from minigolf import HitsMatch, HolesMatch, Player


class HwInitFuncTestCase(TestCase):
    def testInit(self):
        players = [Player('A'), Player('B'), Player('C')]
        # Wrong INIT
        with self.assertRaises(TypeError):
            classObj = HitsMatch()

        with self.assertRaises(TypeError):
            classObj = HolesMatch()

        with self.assertRaises(RuntimeError):
            classObj = HitsMatch(10, players)

        with self.assertRaises(RuntimeError):
            classObj = HolesMatch(10, players)

        classHits = HitsMatch(len(players), players)
        self.assertEqual(classHits._results_table, [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ])

        classHoles = HolesMatch(0, [])
        self.assertEqual(classHoles.finished, 1)


class HwGetWinnersFuncTestCase(TestCase):
    def testGetWinners_Hits(self):
        players = [Player('A'), Player('B'), Player('C')]
        classHits = HitsMatch(len(players), players)

        classHits._finished = False
        with self.assertRaises(RuntimeError):
            classHits.get_winners()

        # Test on 1 winner
        classHits._results_table = [
            [1, 4, 2],
            [1, 4, 1],
            [1, 2, 5],
        ]
        classHits._finished = True
        self.assertEqual(classHits.get_winners(), [players[0]])

        # Test on 2 and more winners
        classHits._results_table = [
            [1, 4, 1],
            [1, 4, 1],
            [1, 2, 1],
        ]
        self.assertEqual(classHits.get_winners(), [players[0], players[2]])

    def testGetWinners_Holes(self):
        players = [Player('A'), Player('B'), Player('C')]
        classHoles = HolesMatch(len(players), players)

        classHoles._finished = False
        with self.assertRaises(RuntimeError):
            classHoles.get_winners()

        # Test on 1 winner
        classHoles._results_table = [
            [1, 0, 1],
            [1, 0, 1],
            [1, 0, 0],
        ]
        classHoles._finished = True
        self.assertEqual(classHoles.get_winners(), [players[0]])

        # Test on 2 and more winners
        classHoles._results_table = [
            [1, 0, 1],
            [1, 0, 1],
            [1, 1, 1],
        ]
        self.assertEqual(classHoles.get_winners(), [players[0], players[2]])


class HwGetTableFuncTestCase(TestCase):
    def testGetTable(self):
        players = [Player('A'), Player('B'), Player('C')]
        classHits = HitsMatch(len(players), players)

        # Current hole is not finished and some players did not ended playing, but scored
        classHits._results_table = [
            [1, 0, 1],
            [1, 2, None],
            [None, None, None],
        ]

        classHits._current_hole = 1
        for player in classHits._players_array:
            player.hits_no_more = 0
        classHits. _players_array[0].hits_no_more = 1
        self.assertEqual(classHits.get_table(), [
            ('A', 'B', 'C'),
            (1, 0, 1),
            (1, None, None),
            (None, None, None),
        ])

        # Current hole is finished
        classHits._results_table = [
            [1, 0, 1],
            [1, 2, 0],
            [None, None, None],
        ]

        classHits._current_hole = 2
        for player in classHits._players_array:
            player.hits_no_more = 0
        self.assertEqual(classHits.get_table(), [
            ('A', 'B', 'C'),
            (1, 0, 1),
            (1, 2, 0),
            (None, None, None),
        ])

        # Game finished
        classHits._results_table = [
            [1, 0, 1],
            [1, 2, 0],
            [1, 1, 1],
        ]

        classHits._current_hole = 3
        self.assertEqual(classHits.get_table(), [
            ('A', 'B', 'C'),
            (1, 0, 1),
            (1, 2, 0),
            (1, 1, 1),
        ])

class HwSWtoNextHoleFuncTestCase(TestCase):
    def testNextHole(self):
        players = [Player('A'), Player('B'), Player('C')]
        classHits = HitsMatch(len(players), players)

        classHits._current_hole = 1
        for player in classHits._players_array:
            player.hits_no_more = 1

        # Switch to last hole
        classHits._switch_to_next_hole()

        self.assertEqual(classHits._current_hole, 2)
        for player in classHits._players_array:
            self.assertEqual(player.hits_no_more, 0)
        self.assertEqual(classHits._finished, False)
        self.assertEqual(classHits._current_player, 2)

        # Switch to the end of game
        classHits._switch_to_next_hole()
        self.assertEqual(classHits._current_hole, 3)
        self.assertEqual(classHits._finished, True)


class HwSIsFinishedFuncTestCase(TestCase):
    def testIsFinished(self):
        players = [Player('A'), Player('B'), Player('C')]
        classHits = HitsMatch(len(players), players)

        for player in classHits._players_array:
            player.hits_no_more = 0

        # NOT Everybody finished
        self.assertEqual(classHits._everybody_finished_hole(), False)

        # NOT Everybody finished, only one
        classHits._players_array[0].hits_no_more = 1
        self.assertEqual(classHits._everybody_finished_hole(), False)

        for player in classHits._players_array:
            player.hits_no_more = 1

        # Everybody finished
        self.assertEqual(classHits._everybody_finished_hole(), True)


class HwSetNextUserFuncTestCase(TestCase):
    def testSetNextUser(self):
        players = [Player('A'), Player('B'), Player('C')]
        classHits = HitsMatch(len(players), players)

        # Should set next player 2(last), but not hole
        classHits._current_player = 1
        classHits._current_hole = 1
        classHits._set_next_player_and_hole_if_needed()

        self.assertEqual(classHits._current_hole, 1)
        self.assertEqual(classHits._current_player, 2)

        # Should set next player 0(first)!!!, but not hole
        classHits._set_next_player_and_hole_if_needed()
        self.assertEqual(classHits._current_hole, 1)
        self.assertEqual(classHits._current_player, 0)

        # Should set next player 2(= number of hole), AND next hole 2
        for player in classHits._players_array:
            player.hits_no_more = 1
        classHits._set_next_player_and_hole_if_needed()
        self.assertEqual(classHits._current_hole, 2)
        self.assertEqual(classHits._current_player, 2)

        # Should set finished state
        for player in classHits._players_array:
            player.hits_no_more = 1
        classHits._set_next_player_and_hole_if_needed()
        self.assertEqual(classHits.finished, True)


class HwHitInHitsMatchFuncTestCase(TestCase):
    def testHitInHitsMatch(self):
        players = [Player('A'), Player('B'), Player('C')]
        classHits = HitsMatch(len(players), players)

        # Test usual bad hit for 0 player
        classHits._results_table = [
            [1, 8, 2],
            [1, 8, 0],
            [None, None, None],
        ]

        classHits._current_player = 0
        classHits._current_hole = 2
        classHits.hit()

        self.assertEqual(classHits._results_table,[
            [1, 8, 2],
            [1, 8, 0],
            [1, None, None],
        ])

        for player in classHits._players_array:
            self.assertEqual(player.hits_no_more, 0)

        # Test usual good hit for 1 player
        classHits.hit(True)
        self.assertEqual(classHits._results_table, [
            [1, 8, 2],
            [1, 8, 0],
            [1, 1, None],
        ])

        self.assertEqual(classHits._players_array[0].hits_no_more, 0)
        self.assertEqual(classHits._players_array[1].hits_no_more, 1)
        self.assertEqual(classHits._players_array[2].hits_no_more, 0)

        # Test no hit for 9 points bad hit for 1 player => 10 points
        classHits._players_array[1].hits_no_more = 0
        classHits._current_player = 1
        classHits._current_hole = 0
        classHits.hit()
        self.assertEqual(classHits._results_table, [
            [1, 10, 2],
            [1, 8, 0],
            [1, 1, None],
        ])
        self.assertEqual(classHits._players_array[1].hits_no_more, 1)

        # Test no hit for 8 points GOOD hit for 1 player => 9 points
        classHits._players_array[1].hits_no_more = 0
        classHits._current_player = 1
        classHits._current_hole = 1
        classHits.hit(True)
        self.assertEqual(classHits._results_table, [
            [1, 10, 2],
            [1, 9, 0],
            [1, 1, None],
        ])
        self.assertEqual(classHits._players_array[1].hits_no_more, 1)


class HwHitInHolesMatchFuncTestCase(TestCase):
    def testHitInHolesMatch(self):
        players = [Player('A'), Player('B'), Player('C')]
        classHoles = HolesMatch(len(players), players)

        # Test when last player scores
        classHoles.hit()
        classHoles.hit()
        classHoles.hit(True)

        self.assertEqual(classHoles._results_table, [
            [0, 0, 1],
            [None, None, None],
            [None, None, None],
        ])

        # Test when pre-last player scores
        classHoles.hit()
        classHoles.hit(True)
        classHoles.hit()
        self.assertEqual(classHoles._results_table, [
            [0, 0, 1],
            [0, 0, 1],
            [None, None, None],
        ])

        # Test for 10 misses
        for _ in range(10):
            for _ in range(3):
                classHoles.hit()

        self.assertEqual(classHoles._results_table, [
            [0, 0, 1],
            [0, 0, 1],
            [0, 0, 0],
        ])


class HitsMatchTestCase(TestCase):
    def test_scenario(self):
        players = [Player('A'), Player('B'), Player('C')]
        m = HitsMatch(3, players)
        self._first_hole(m)
        self._second_hole(m)

        with self.assertRaises(RuntimeError):
            m.get_winners()

        self._third_hole(m)

        with self.assertRaises(RuntimeError):
            m.hit()

        self.assertEqual(m.get_winners(), [
            players[0], players[2]
        ])

    def _first_hole(self, m):
        m.hit()     # 1
        m.hit()     # 2
        m.hit(True) # 3
        m.hit(True) # 1
        for _ in range(8):
            m.hit() # 2

        self.assertFalse(m.finished)
        self.assertEqual(m.get_table(), [
            ('A', 'B', 'C'),
            (2, 10, 1),
            (None, None, None),
            (None, None, None),
        ])

    def _second_hole(self, m):
        m.hit() # 2
        for _ in range(3):
            m.hit(True) # 3, 1, 2

        self.assertFalse(m.finished)
        self.assertEqual(m.get_table(), [
            ('A', 'B', 'C'),
            (2, 10, 1),
            (1, 2, 1),
            (None, None, None),
        ])

    def _third_hole(self, m):
        m.hit()     # 3
        m.hit(True) # 1
        m.hit()     # 2
        self.assertEqual(m.get_table(), [
            ('A', 'B', 'C'),
            (2, 10, 1),
            (1, 2, 1),
            (1, None, None),
        ])
        m.hit(True) # 3
        m.hit()     # 2
        m.hit(True) # 2

        self.assertTrue(m.finished)
        self.assertEqual(m.get_table(), [
            ('A', 'B', 'C'),
            (2, 10, 1),
            (1, 2, 1),
            (1, 3, 2),
        ])


class HolesMatchTestCase(TestCase):
    def test_scenario(self):
        players = [Player('A'), Player('B'), Player('C')]
        m = HolesMatch(3, players)

        self._first_hole(m)
        self._second_hole(m)

        with self.assertRaises(RuntimeError):
            m.get_winners()

        self._third_hole(m)

        with self.assertRaises(RuntimeError):
            m.hit()

        self.assertEqual(m.get_winners(), [players[0]])

    def _first_hole(self, m):
        m.hit(True) # 1
        m.hit()     # 2
        m.hit()     # 3

        self.assertFalse(m.finished)
        self.assertEqual(m.get_table(), [
            ('A', 'B', 'C'),
            (1, 0, 0),
            (None, None, None),
            (None, None, None),
        ])

    def _second_hole(self, m):
        for _ in range(10):
            for _ in range(3):
                m.hit() # 2, 3, 1

        self.assertFalse(m.finished)
        self.assertEqual(m.get_table(), [
            ('A', 'B', 'C'),
            (1, 0, 0),
            (0, 0, 0),
            (None, None, None),
        ])

    def _third_hole(self, m):
        for _ in range(9):
            for _ in range(3):
                m.hit() # 3, 1, 2
        m.hit(True) # 3
        self.assertEqual(m.get_table(), [
            ('A', 'B', 'C'),
            (1, 0, 0),
            (0, 0, 0),
            (None, None, 1),
        ])
        m.hit(True) # 1
        m.hit()     # 2

        self.assertTrue(m.finished)
        self.assertEqual(m.get_table(), [
            ('A', 'B', 'C'),
            (1, 0, 0),
            (0, 0, 0),
            (1, 0, 1),
        ])

