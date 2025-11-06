"""
model.camera
Composant simulé : lecture des données du véhicule.
"""

from typing import Dict


class Camera:
    """
    Simule la capture d'informations d'un véhicule (immatriculation, longueur, hauteur).
    """

    def analyser_voiture(self, immatriculation: str, longueur: float, hauteur: float) -> Dict[str, object]:
        """
        Dans cette simulation, on reçoit directement les paramètres et on retourne un dict.
        """
        return {"immatriculation": immatriculation, "longueur": float(longueur), "hauteur": float(hauteur)}
