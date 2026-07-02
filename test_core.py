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
    # create_game_state should build a grid of the right width/height, filled with None
    def test_create_game_state_dimensions(self):
        state = create_game_state(3, 2)
        self.assertEqual(state.width, 3)
        self.assertEqual(state.height, 2)
        self.assertEqual(len(state.grid), 2)
        self.assertEqual(len(state.grid[0]), 3)

    # place_entity should put the entity at (x, y), and find_character should locate it there
    def test_place_entity_and_find_character(self):
        state = create_game_state(3, 3)
        place_entity(state, Character(direction="right"), x=1, y=2)
        self.assertEqual(find_character(state), (1, 2))

    # find_character should return None instead of crashing when there's no character
    def test_find_character_returns_none_when_absent(self):
        state = create_game_state(2, 2)
        self.assertIsNone(find_character(state))


class TestMoveCharacter(unittest.TestCase):
    # moving should update both the character's grid position and its facing direction
    def test_move_updates_position_and_direction(self):
        state = create_game_state(3, 3)
        place_entity(state, Character(direction="right"), x=1, y=1)
        move_character(state, "W")
        self.assertEqual(find_character(state), (1, 0))
        self.assertEqual(state.grid[0][1].direction, "up")
        self.assertIsNone(state.grid[1][1])

    # a Tree in the way should stop the character from moving into that cell
    def test_tree_blocks_movement(self):
        state = create_game_state(3, 3)
        place_entity(state, Character(direction="right"), x=1, y=1)
        place_entity(state, Tree(), x=1, y=0)
        move_character(state, "W")
        self.assertEqual(find_character(state), (1, 1))  # unchanged

    # walking onto the crate should win, and actually move the character onto that cell
    def test_walking_onto_crate_wins(self):
        state = create_game_state(3, 3)
        place_entity(state, Character(direction="right"), x=1, y=1)
        place_entity(state, Crate(), x=1, y=0)
        won = move_character(state, "W")
        self.assertTrue(won)
        self.assertEqual(find_character(state), (1, 0))
        self.assertIsInstance(state.grid[0][1], Character)


class TestReflect(unittest.TestCase):
    # a 45 degree mirror should turn the projectile's direction 90 degrees counter-clockwise
    def test_positive_angle(self):
        self.assertEqual(reflect("right", 45), "up")
        self.assertEqual(reflect("up", 45), "right")
        self.assertEqual(reflect("left", 45), "down")
        self.assertEqual(reflect("down", 45), "left")

    # a -45 degree mirror should turn the projectile's direction 90 degrees clockwise
    def test_negative_angle(self):
        self.assertEqual(reflect("right", -45), "down")
        self.assertEqual(reflect("down", -45), "right")
        self.assertEqual(reflect("left", -45), "up")
        self.assertEqual(reflect("up", -45), "left")


class TestShoot(unittest.TestCase):
    # with no mirror in the way, hitting the crate directly should win immediately
    def test_direct_hit_on_crate_wins(self):
        state = create_game_state(5, 1)
        place_entity(state, Character(direction="right"), x=0, y=0)
        place_entity(state, Crate(), x=3, y=0)
        won = shoot(state)
        self.assertTrue(won)
        self.assertEqual(find_character(state), (3, 0))

    # a Tree before any mirror is reached means X does nothing - no movement at all
    def test_blocked_before_mirror_does_nothing(self):
        state = create_game_state(5, 1)
        place_entity(state, Character(direction="right"), x=0, y=0)
        place_entity(state, Tree(), x=2, y=0)
        place_entity(state, Mirror(angle=45), x=4, y=0)
        result = shoot(state)
        self.assertIsNone(result)
        self.assertEqual(find_character(state), (0, 0))  # character did not move

    # character 2 cells from the mirror; after bouncing it should land
    # exactly 2 cells past the mirror in the reflected direction (mirror-symmetric distance)
    def test_mirror_bounce_travels_symmetric_distance(self):
        state = create_game_state(5, 5)
        place_entity(state, Character(direction="right"), x=0, y=4)
        place_entity(state, Mirror(angle=45), x=2, y=4)
        shoot(state)
        self.assertEqual(find_character(state), (2, 2))

    # if the crate happens to sit exactly at the symmetric-distance landing cell, it's a win
    def test_bounce_landing_exactly_on_crate_wins(self):
        state = create_game_state(5, 5)
        place_entity(state, Character(direction="right"), x=0, y=4)
        place_entity(state, Mirror(angle=45), x=2, y=4)
        place_entity(state, Crate(), x=2, y=2)
        won = shoot(state)
        self.assertTrue(won)
        self.assertEqual(find_character(state), (2, 2))

    # a Tree blocking the path after the bounce, before the full distance is covered,
    # means X does nothing rather than landing the character short of it
    def test_blocked_after_bounce_does_nothing(self):
        state = create_game_state(5, 5)
        place_entity(state, Character(direction="right"), x=0, y=4)
        place_entity(state, Mirror(angle=45), x=2, y=4)
        place_entity(state, Tree(), x=2, y=3)
        result = shoot(state)
        self.assertIsNone(result)
        self.assertEqual(find_character(state), (0, 4))  # character did not move


class TestRunGame(unittest.TestCase):
    # full playthrough: walk into the mirror's row, bounce toward the crate,
    # then walk the remaining distance to win - checks every step is recorded
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

    # run_game deep-copies the state internally, so the caller's original state
    # should be untouched after the run
    def test_run_game_does_not_mutate_original_state(self):
        state = create_game_state(3, 3)
        place_entity(state, Character(direction="right"), x=0, y=0)
        run_game(state, "D")
        self.assertEqual(find_character(state), (0, 0))  # original untouched

    # if the instructions run out without reaching the crate, run_game should report a loss
    def test_unfinished_game_returns_false(self):
        state = create_game_state(3, 3)
        place_entity(state, Character(direction="right"), x=0, y=0)
        won, steps = run_game(state, "D")
        self.assertFalse(won)
        self.assertEqual(len(steps), 1)


if __name__ == "__main__":
    unittest.main()
