import unittest
from model.place import Place


class TestPlace(unittest.TestCase):
    def setUp(self):
        self.place = Place(id_place=1, niveau=0, longueur=5.0, hauteur=2.0)

    def test_est_disponible_initial(self):
        self.assertTrue(self.place.est_disponible())

    def test_occuper_liberer(self):
        self.place.occuper()
        self.assertFalse(self.place.est_disponible())
        self.place.liberer()
        self.assertTrue(self.place.est_disponible())


if __name__ == "__main__":
    unittest.main()
