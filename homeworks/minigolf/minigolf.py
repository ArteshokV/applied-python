from abc import ABCMeta, abstractmethod
class Player:
    def __init__(self, name):
        self.name = name
        self.hits_no_more = 0

class Match(metaclass=ABCMeta):

    @property
    def finished(self):
        return self._finished

    def __init__(self,number_of_holes, palyers_array):
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
            return self.select_winners()

    def get_table(self):
        return_array = []
        #appending names
        return_array.append(tuple(item.name for item in self._players_array))
        #appending results from stored table
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

    @abstractmethod
    def hit(self, success=False):
        pass

    @abstractmethod
    def select_winners(self):
        pass



class HitsMatch(Match):
    def _set_next_player_and_hole_if_needed(self):
        self._current_player = self._current_player + 1 if self._current_player != self._number_of_players-1 else 0
        number_of_loops = 0
        while self._players_array[self._current_player].hits_no_more == 1:
            self._current_player = self._current_player + 1 if self._current_player != self._number_of_players-1 else 0
            number_of_loops += 1
            if number_of_loops > self._number_of_players:
                #going to the next hole
                for player_object in self._players_array:
                    player_object.hits_no_more = 0
                self._current_hole += 1
                if self._current_hole == self._number_of_holes:
                    self._finished = True
                self._current_player = self._current_hole
                break

    def hit(self, success=False):
        if self._finished == True:
            raise RuntimeError('Already finished')
        current_hole_array = self._results_table[self._current_hole]
        current_hole_array[self._current_player] = current_hole_array[self._current_player] + 1 if \
            current_hole_array[self._current_player] else 1

        if success:
            self._players_array[self._current_player].hits_no_more = 1
        if self._results_table[self._current_hole][self._current_player] == 9:
            current_hole_array[self._current_player] += 1
            self._players_array[self._current_player].hits_no_more = 1

        self._set_next_player_and_hole_if_needed()

    def select_winners(self):
        points_array = []
        return_array = []
        for playernum in range(self._number_of_players):
            sum = 0
            for holenum in range(self._number_of_holes):
                sum += self._results_table[holenum][playernum]
            points_array.append(sum)
        minpoint = min(points_array)
        for idn,points in enumerate(points_array) :
            if(minpoint == points):
                return_array.append(self._players_array[idn])
        return return_array


class HolesMatch(Match):
    def hit(self, success=False):
        if self._finished == True:
            raise RuntimeError('Already finished')
        current_hole_array = self._results_table[self._current_hole]
        current_hole_array[self._current_player] = current_hole_array[self._current_player] + 1 if \
            current_hole_array[self._current_player] else 1

        if success:
            self._players_array[self._current_player].hits_no_more = 1
        if self._results_table[self._current_hole][self._current_player] == 9:
            current_hole_array[self._current_player] += 1
            self._players_array[self._current_player].hits_no_more = 1

        self._set_next_player_and_hole_if_needed()
    def select_winners(self):
        pass