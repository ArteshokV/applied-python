from abc import ABCMeta, abstractmethod


class Player:
    def __init__(self, name):
        self.name = name
        self.hits_no_more = 0


class Match(metaclass=ABCMeta):

    MAX_HITS_PER_HOLES = 10
    MAX_POINTS_FOR_HITS = MAX_HITS_PER_HOLES-1
    _WINNERS_FUNCTION = min

    @property
    def finished(self):
        return self._finished

    def __init__(self, number_of_holes, palyers_array):
        self._players_array = palyers_array
        self._finished = False
        if not self._players_array:
            self._finished = True
        self._current_player = 0
        self._current_hole = 0
        self._number_of_holes = number_of_holes
        self._number_of_players = len(palyers_array)
        self._results_table = list(list(None for _ in self._players_array) for _ in range(number_of_holes))

    def get_winners(self):
        if not self._finished:
            raise RuntimeError('Not finished')
        else:
            points_array = []
            return_array = []
            for playernum in range(self._number_of_players):
                points_sum = 0
                for holenum in range(self._number_of_holes):
                    points_sum += self._results_table[holenum][playernum]
                points_array.append(points_sum)

            winner_points = self._WINNERS_FUNCTION(points_array)

            # To be ordered:
            for idn, points in enumerate(points_array):
                if (winner_points == points):
                    return_array.append(self._players_array[idn])
            return return_array

    def get_table(self):
        return_array = list()
        # appending names
        return_array.append(tuple(item.name for item in self._players_array))
        # appending results from stored table
        for hole in range(self._number_of_holes):
            if hole == self._current_hole:
                temp_array = []
                for player in range(self._number_of_holes):
                    if self._players_array[player].hits_no_more:
                        temp_array.append(self._results_table[hole][player])
                    else:
                        temp_array.append(None)
                return_array.append(tuple(temp_array))
            else:
                return_array.append(tuple(self._results_table[hole]))
        return return_array

    def _switch_to_next_hole(self):
        # going to the next hole
        for player_object in self._players_array:
            player_object.hits_no_more = 0
        self._current_hole += 1
        if self._current_hole == self._number_of_holes:
            self._finished = True

        self._current_player = self._current_hole % self._number_of_players

    def _everybody_finished_hole(self):
        for player in self._players_array:
            if player.hits_no_more == 0:
                return False
        return True

    def _set_next_player_and_hole_if_needed(self):
        self._current_player = self._current_player + 1 if self._current_player != self._number_of_players-1 else 0

        if self._everybody_finished_hole():
            self._switch_to_next_hole()
            return 1

        return 0

    @abstractmethod
    def hit(self, success=False):
        pass


class HitsMatch(Match):

    _WINNERS_FUNCTION = min

    def hit(self, success=False):
        if self._finished:
            raise RuntimeError('Already finished')

        current_hole_array = self._results_table[self._current_hole]
        current_hole_array[self._current_player] = current_hole_array[self._current_player] + 1 if \
            current_hole_array[self._current_player] else 1

        if success:
            self._players_array[self._current_player].hits_no_more = 1
        elif self._results_table[self._current_hole][self._current_player] == self.MAX_POINTS_FOR_HITS:
            current_hole_array[self._current_player] += 1
            self._players_array[self._current_player].hits_no_more = 1

        self._set_next_player_and_hole_if_needed()
        # For HitsMatch player selection
        while self._players_array[self._current_player].hits_no_more == 1:
            self._current_player = self._current_player + 1 if self._current_player != self._number_of_players - 1 else 0


class HolesMatch(Match):

    _WINNERS_FUNCTION = max

    def __init__(self, number_of_holes, palyers_array):
        Match.__init__(self, number_of_holes, palyers_array)
        self._number_of_fails = 0
        self._was_goal = False

    def hit(self, success=False):
        if self._finished:
            raise RuntimeError('Already finished')

        current_hole_array = self._results_table[self._current_hole]
        if success:
            current_hole_array[self._current_player] = 1
            self._players_array[self._current_player].hits_no_more = 1
            self._was_goal = True
            # Previous players do not hit no more!
            no_more_hit_player_id = self._current_hole
            while no_more_hit_player_id != self._current_player:
                current_hole_array[no_more_hit_player_id] = 0 if not current_hole_array[no_more_hit_player_id] else current_hole_array[no_more_hit_player_id]
                self._players_array[no_more_hit_player_id].hits_no_more = 1
                no_more_hit_player_id = no_more_hit_player_id + 1 if no_more_hit_player_id != self._number_of_players-1\
                    else 0
        else:
            self._number_of_fails += 1
            if self._was_goal:
                self._players_array[self._current_player].hits_no_more = 1
                current_hole_array[self._current_player] = 0

        if self._number_of_fails == self._number_of_players * self.MAX_HITS_PER_HOLES:
            for playerind, player in enumerate(self._players_array):
                player.hits_no_more = 1
                current_hole_array[playerind] = 0

        if self._set_next_player_and_hole_if_needed():
            self._was_goal = False
            self._number_of_fails = 0