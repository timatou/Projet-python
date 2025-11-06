"""
model.borne
Composant simulé : délivrance de ticket.
"""

from datetime import datetime
from typing import Dict
import random


class Borne:
    """
    Simule une borne qui délivre un ticket.
    """

    def delivrer_ticket(self, immatriculation: str, id_place: int, abonne: bool = False) -> Dict[str, object]:
        id_ticket = f"T-{random.randint(1000, 9999)}"
        ticket = {
            "id_ticket": id_ticket,
            "immatriculation": immatriculation,
            "id_place": id_place,
            "date_entree": datetime.now().isoformat(),
            "mode_paiement": "Abonnement" if abonne else "CB"
        }
        return ticket
