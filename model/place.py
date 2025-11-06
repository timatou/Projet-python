"""
model.place
Représente une place de parking.
Auteur: Mamad
"""

from typing import Any


class Place:
    """
    Représente une place de parking.

    Attributes:
        id_place (int): identifiant unique
        niveau (int): niveau/étage
        longueur (float): longueur disponible en mètres
        hauteur (float): hauteur disponible en mètres
        occupee (bool): True si la place est occupée
    """

    def __init__(self, id_place: int, niveau: int, longueur: float, hauteur: float) -> None:
        self.id_place = id_place
        self.niveau = niveau
        self.longueur = float(longueur)
        self.hauteur = float(hauteur)
        self.occupee = False

    def est_disponible(self) -> bool:
        """Retourne True si la place est libre."""
        return not self.occupee

    def occuper(self) -> None:
        """Marque la place comme occupée."""
        self.occupee = True

    def liberer(self) -> None:
        """Marque la place comme libre."""
        self.occupee = False

    def __repr__(self) -> str:
        etat = "Occupée" if self.occupee else "Libre"
        return f"<Place {self.id_place} niveau={self.niveau} {etat}>"
