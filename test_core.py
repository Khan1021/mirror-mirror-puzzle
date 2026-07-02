import unittest

from core import (
    create_game_state,
    place_entity,
    find_character,
    move_character,
    reflect,
    shoot,
    run_game,
    Character,
    Tree,
    Mirror,
    Crate,
)


class TestGameState(unittest.TestCase):
    def test_create_game_state_dimensions(self):
        state = create_game_state(3, 2)
        self.assertEqual(state.width, 3)
        self.assertEqual(state.height, 2)
        self.assertEqual(len(state.grid), 2)
        self.assertEqual(len(state.grid[0]), 3)

    def test_place_entity_and_find_character(self):
        state = create_game_state(3, 3)
        place_entity(state, Character(direction="right"), x=1, y=2)
        self.assertEqual(find_character(state), (1, 2))

    def test_find_character_returns_none_when_absent(self):
        state = create_game_state(2, 2)
        self.assertIsNone(find_character(state))


class TestMoveCharacter(unittest.TestCase):
    def test_move_updates_position_and_direction(self):
        state = create_game_state(3, 3)
        place_entity(state, Character(direction="right"), x=1, y=1)
        move_character(state, "W")
        self.assertEqual(find_character(state), (1, 0))
        self.assertEqual(state.grid[0][1].direction, "up")
        self.assertIsNone(state.grid[1][1])

    def test_tree_blocks_movement(self):
        state = create_game_state(3, 3)
        place_entity(state, Character(direction="right"), x=1, y=1)
        place_entity(state, Tree(), x=1, y=0)
        move_character(state, "W")
        self.assertEqual(find_character(state), (1, 1))  # unchanged

    def test_walking_onto_crate_wins(self):
        state = create_game_state(3, 3)
        place_entity(state, Character(direction="right"), x=1, y=1)
        place_entity(state, Crate(), x=1, y=0)
        won = move_character(state, "W")
        self.assertTrue(won)
        self.assertEqual(find_character(state), (1, 0))
        self.assertIsInstance(state.grid[0][1], Character)


class TestReflect(unittest.TestCase):
    def test_positive_angle(self):
        self.assertEqual(reflect("right", 45), "up")
        self.assertEqual(reflect("up", 45), "right")
        self.assertEqual(reflect("left", 45), "down")
        self.assertEqual(reflect("down", 45), "left")

    def test_negative_angle(self):
        self.assertEqual(reflect("right", -45), "down")
        self.assertEqual(reflect("down", -45), "right")
        self.assertEqual(reflect("left", -45), "up")
        self.assertEqual(reflect("up", -45), "left")


class TestShoot(unittest.TestCase):
    def test_direct_hit_on_crate_wins(self):
        state = create_game_state(5, 1)
        place_entity(state, Character(direction="right"), x=0, y=0)
        place_entity(state, Crate(), x=3, y=0)
        won = shoot(state)
        self.assertTrue(won)
        self.assertEqual(find_character(state), (3, 0))

    def test_blocked_before_mirror_does_nothing(self):
        state = create_game_state(5, 1)
        place_entity(state, Character(direction="right"), x=0, y=0)
        place_entity(state, Tree(), x=2, y=0)
        place_entity(state, Mirror(angle=45), x=4, y=0)
        result = shoot(state)
        self.assertIsNone(result)
        self.assertEqual(find_character(state), (0, 0))  # character did not move

    def test_mirror_bounce_travels_symmetric_distance(self):
        # character 2 cells from the mirror; after bouncing it should land
        # exactly 2 cells past the mirror in the reflected direction
        state = create_game_state(5, 5)
        place_entity(state, Character(direction="right"), x=0, y=4)
        place_entity(state, Mirror(angle=45), x=2, y=4)
        shoot(state)
        self.assertEqual(find_character(state), (2, 2))

    def test_bounce_landing_exactly_on_crate_wins(self):
        state = create_game_state(5, 5)
        place_entity(state, Character(direction="right"), x=0, y=4)
        place_entity(state, Mirror(angle=45), x=2, y=4)
        place_entity(state, Crate(), x=2, y=2)
        won = shoot(state)
        self.assertTrue(won)
        self.assertEqual(find_character(state), (2, 2))

    def test_blocked_after_bounce_does_nothing(self):
        state = create_game_state(5, 5)
        place_entity(state, Character(direction="right"), x=0, y=4)
        place_entity(state, Mirror(angle=45), x=2, y=4)
        place_entity(state, Tree(), x=2, y=3)
        result = shoot(state)
        self.assertIsNone(result)
        self.assertEqual(find_character(state), (0, 4))  # character did not move


class TestRunGame(unittest.TestCase):
    def test_run_game_returns_all_steps_and_win_flag(self):
        state = create_game_state(5, 5)
        place_entity(state, Character(direction="right"), x=0, y=2)
        place_entity(state, Mirror(angle=45), x=3, y=4)
        place_entity(state, Crate(), x=3, y=0)
        place_entity(state, Tree(), x=0, y=0)

        won, steps = run_game(state, "SSDXWW")

        self.assertTrue(won)
        self.assertEqual(len(steps), 6)
        self.assertEqual(find_character(steps[-1]), (3, 0))

    def test_run_game_does_not_mutate_original_state(self):
        state = create_game_state(3, 3)
        place_entity(state, Character(direction="right"), x=0, y=0)
        run_game(state, "D")
        self.assertEqual(find_character(state), (0, 0))  # original untouched

    def test_unfinished_game_returns_false(self):
        state = create_game_state(3, 3)
        place_entity(state, Character(direction="right"), x=0, y=0)
        won, steps = run_game(state, "D")
        self.assertFalse(won)
        self.assertEqual(len(steps), 1)


if __name__ == "__main__":
    unittest.main()
