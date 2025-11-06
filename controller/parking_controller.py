"""
controller.parking_controller
Coordonne Model <-> View pour le use case 'Se garer'.
"""

from typing import Optional, Dict
from model.camera import Camera
from model.borne import Borne
from model.teleporteur import Teleporteur
from model.parking import Parking
from model.voiture import Voiture
from view.console_view import ConsoleView


class ParkingController:
    """
    Controller pour le use case 'Se garer'.
    Le controller ne fait pas d'affichage directement : il appelle la View injectée.
    """

    def __init__(self, parking: Optional[Parking] = None, view: Optional[ConsoleView] = None) -> None:
        self.parking = parking if parking is not None else Parking()
        self.camera = Camera()
        self.borne = Borne()
        self.teleporteur = Teleporteur()
        self.view = view if view is not None else ConsoleView()

    def se_garer(self, immatriculation: str, longueur: float, hauteur: float, abonne: bool = False) -> Optional[Dict[str, object]]:
        """
        Scénario 'Se garer' :
        1) Camera analyse la voiture
        2) Parking attribue une place
        3) Borne délivre ticket
        4) Teleporteur transporte (simulation)
        5) View affiche ticket / panneau
        Retourne le ticket dict ou None si parking complet.
        """
        # 1) lire infos via camera (simulation)
        infos = self.camera.analyser_voiture(immatriculation, longueur, hauteur)
        voiture = Voiture(infos["immatriculation"], infos["longueur"], infos["hauteur"], abonne=abonne)

        # 2) attribuer place
        place = self.parking.attribuer_place(voiture)
        if place is None:
            self.view.afficher_message("[System] Parking complet !")
            return None

        # 3) délivrer ticket
        ticket = self.borne.delivrer_ticket(voiture.immatriculation, place.id_place, abonne=abonne)

        # 4) téléportation (action neutre côté model)
        self.teleporteur.transporter(voiture.immatriculation, place.id_place)
        # 5) affichages via la view
        self.view.afficher_ticket(ticket)
        self.view.afficher_teleportation(voiture.immatriculation, place.id_place)
        self.view.afficher_panneau(self.parking.compter_places_libres())

        return ticket
