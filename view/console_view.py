

from typing import Dict


class ConsoleView:
    """
    Vue console qui affiche les événements (simulation).
    """

    def afficher_message(self, message: str) -> None:
        print(message)

    def afficher_ticket(self, ticket: Dict[str, object]) -> None:
        print(f"Ticket délivré : {ticket}")

    def afficher_teleportation(self, immatriculation: str, id_place: int) -> None:
        print(f"Teleporteur : voiture {immatriculation} transportée vers la place {id_place}")

    def afficher_panneau(self, nb_libres: int) -> None:
        print(f"Panneau : {nb_libres} places disponibles")
