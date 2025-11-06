"""
model.parking
Logique métier du parking : gestion des places et historique minimal.
"""

from datetime import datetime
from typing import List, Optional
from .place import Place
from .voiture import Voiture


class Parking:
    """
    Gère une collection de Place et un historique simple.

    On garde l'implémentation simple : places "standard" créées au constructeur.
    """

    def __init__(self, nb_places: int = 10, place_longueur: float = 5.0, place_hauteur: float = 2.0) -> None:
        self.places: List[Place] = [
            Place(id_place=i + 1, niveau=0, longueur=place_longueur, hauteur=place_hauteur)
            for i in range(nb_places)
        ]
        # historique : liste de dict {immatriculation, id_place, action, date}
        self.historique: List[dict] = []

    def attribuer_place(self, voiture: Voiture) -> Optional[Place]:
        """
        Attribue la première place compatible disponible.
        Retourne Place ou None si aucune place adaptée.
        """
        for place in self.places:
            if place.est_disponible() and place.longueur >= voiture.longueur and place.hauteur >= voiture.hauteur:
                place.occuper()
                self.historique.append({
                    "immatriculation": voiture.immatriculation,
                    "id_place": place.id_place,
                    "action": "entree",
                    "date": datetime.now().isoformat()
                })
                return place
        return None

    def liberer_place(self, id_place: int) -> bool:
        """
        Libère la place identifiée par id_place.
        Retourne True si la place a été libérée, False si non trouvée ou déjà libre.
        """
        for place in self.places:
            if place.id_place == id_place:
                if not place.est_disponible():
                    place.liberer()
                    self.historique.append({
                        "id_place": id_place,
                        "action": "sortie",
                        "date": datetime.now().isoformat()
                    })
                    return True
                return False
        return False

    def compter_places_libres(self) -> int:
        """Retourne le nombre de places libres."""
        return sum(1 for p in self.places if p.est_disponible())
