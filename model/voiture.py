"""
model.voiture
Représente une voiture.
"""

from typing import Any


class Voiture:
    """
    Représente une voiture entrant dans le parking.

    Attributes:
        immatriculation (str)
        longueur (float)
        hauteur (float)
        abonne (bool)
    """

    def __init__(self, immatriculation: str, longueur: float, hauteur: float, abonne: bool = False) -> None:
        self.immatriculation = immatriculation
        self.longueur = float(longueur)
        self.hauteur = float(hauteur)
        self.abonne = bool(abonne)

    def __repr__(self) -> str:
        return f"<Voiture {self.immatriculation} longueur={self.longueur} hauteur={self.hauteur} abonne={self.abonne}>"
