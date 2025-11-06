import unittest
from controller.parking_controller import ParkingController
from view.console_view import ConsoleView


class DummyView(ConsoleView):
    """View de test qui capture les affichages sans imprimer."""
    def __init__(self):
        self.messages = []
        self.tickets = []
        self.teleports = []
        self.panneau = None

    def afficher_message(self, message: str) -> None:
        self.messages.append(message)

    def afficher_ticket(self, ticket):
        self.tickets.append(ticket)

    def afficher_teleportation(self, immatriculation: str, id_place: int) -> None:
        self.teleports.append((immatriculation, id_place))

    def afficher_panneau(self, nb_libres: int) -> None:
        self.panneau = nb_libres


class TestController(unittest.TestCase):
    def setUp(self):
        self.view = DummyView()
        # Parking petit pour tests
        self.ctrl = ParkingController(view=self.view)
        self.ctrl.parking = self.ctrl.parking.__class__(nb_places=2)

    def test_se_garer_succes(self):
        ticket = self.ctrl.se_garer("TEST-001-AA", 4.0, 1.8)
        self.assertIsNotNone(ticket)
        self.assertIn("id_ticket", ticket)
        self.assertEqual(len(self.view.tickets), 1)
        self.assertEqual(len(self.view.teleports), 1)

    def test_se_garer_parking_plein(self):
        self.ctrl.se_garer("T1-001", 4.0, 1.8)
        self.ctrl.se_garer("T2-002", 4.0, 1.8)
        ticket3 = self.ctrl.se_garer("T3-003", 4.0, 1.8)
        self.assertIsNone(ticket3)
        self.assertTrue(any("[System] Parking complet" in m for m in self.view.messages))


if __name__ == "__main__":
    unittest.main()
