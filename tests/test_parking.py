import unittest
from model.parking import Parking
from model.voiture import Voiture


class TestParking(unittest.TestCase):
    def setUp(self):
        self.parking = Parking(nb_places=2, place_longueur=5.0, place_hauteur=2.0)
        self.v1 = Voiture("AA-111-AA", 4.0, 1.8)
        self.v2 = Voiture("BB-222-BB", 4.0, 1.8)

    def test_attribuer_place(self):
        p = self.parking.attribuer_place(self.v1)
        self.assertIsNotNone(p)
        self.assertFalse(p.est_disponible())

    def test_liberer_place(self):
        p = self.parking.attribuer_place(self.v1)
        ok = self.parking.liberer_place(p.id_place)
        self.assertTrue(ok)
        self.assertTrue(p.est_disponible())

    def test_parking_plein(self):
        self.parking.attribuer_place(self.v1)
        self.parking.attribuer_place(self.v2)
        v3 = Voiture("CC-333-CC", 4.0, 1.8)
        p3 = self.parking.attribuer_place(v3)
        self.assertIsNone(p3)


if __name__ == "__main__":
    unittest.main()
