import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
print(sys.path)

from game_entities import Submarine


class TestSubmarine(unittest.TestCase):
    def test_initial_velocity(self):
        """Тестирование начальной скорости подводной лодки."""
        sub = Submarine(0, 0, sprite=None)
        self.assertEqual(sub.vel, Submarine.DEFAULT_VELOCITY)

    def test_alive_status(self):
        """Тестирование начального статуса 'alive' подводной лодки."""
        sub = Submarine(0, 0, sprite=None)
        self.assertTrue(sub.alive)
