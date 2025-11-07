from model import Parking, Place, Placement, Ticket, Vehicule, Livraison, Client
from datetime import datetime, timedelta

# ==============================================================================
# CLASSE TELEPORTEUR
# Auteurs : Abdallah Aboulkhassim
# Date : Novembre 2025
# ==============================================================================

class Teleporteur:
    """
    Gère le mouvement du véhicule (téléportage) et la notification de libération de place.
    Il représente le lien entre la Place et l'Accès.
    """
    def __init__(self, parking: Parking):
        """
        Initialise le téléporteur.
        
        Paramètres
        ----------
        parking : Parking
            Référence au composant Parking central pour la mise à jour des états.
        """
        self.parking = parking

    def rapporter_vehicule(self, place: Place) -> bool:
        """
        Simule le téléportage du véhicule depuis sa place vers la sortie.
        Une fois le mouvement simulé, il déclenche la libération de la place.
        
        Paramètres
        ----------
        place : Place
            L'objet Place que le véhicule occupait.
            
        Retourne
        -------
        bool
            True si la place a été libérée et le Placement supprimé, False sinon.
        """
        print(f"Téléportage du véhicule depuis la place {place.id} vers la sortie...")
        
        # Le téléporteur informe le parking (via la place) que l'opération est terminée
        if place.liberer():
            # Le parking doit maintenant supprimer l'enregistrement de placement
            self.parking.supprimer_placement_par_place(place)
            print(f"Place {place.id} libérée et disponible pour réservation.")
            return True
        return False

# ==============================================================================
# CLASSE BORNE TICKET
# ==============================================================================

class BorneTicket:
    """
    Gère l'interface client à l'accès : lecture du ticket, calcul des frais, paiement, 
    et orchestration du processus de sortie (Partie 2).
    """
    def __init__(self, parking: Parking, teleporteur: Teleporteur):
        """
        Initialise la borne avec les références aux composants Parking et Téléporteur.
        
        Paramètres
        ----------
        parking : Parking
            Composant Parking central pour l'accès aux places et placements.
        teleporteur : Teleporteur
            Composant Téléporteur pour gérer le mouvement du véhicule.
        """
        self.parking = parking
        self.teleporteur = teleporteur
        self.TARIF_HORAIRE = 2.5  # Exemple de tarif : 2.50€ par heure
        self.TARIF_MINIMUM = 5.0  # Exemple de tarif : Minimum de 5.00€

    def calculer_frais(self, placement: Placement) -> float:
        """
        Calcule les frais de stationnement basés sur la durée.
        
        Si le véhicule est abonné, les frais sont nuls.
        
        Paramètres
        ----------
        placement : Placement
            L'enregistrement de stationnement à facturer.
            
        Retourne
        -------
        float
            Le montant total dû (0.0 si abonné).
        """
        # Si c'est un abonné, les frais sont 0.
        if placement.vehicule.est_abonne:
            return 0.0

        # Détermination de la durée
        heure_fin = placement.heure_sortie if placement.heure_sortie else datetime.now()
        duree = heure_fin - placement.heure_entree
            
        duree_heures = duree.total_seconds() / 3600

        frais = duree_heures * self.TARIF_HORAIRE

        # Appliquer le tarif minimum
        return max(frais, self.TARIF_MINIMUM)

    def processus_sortie(self, id_ticket: str, paiement_effectue: bool = False) -> str:
        """
        Orchestre le scénario complet "Reprendre la voiture" (Partie 2).
        
        Vérifie le ticket, les services en cours, calcule les frais, gère le paiement 
        et active le téléporteur pour la libération finale.
        
        Paramètres
        ----------
        id_ticket : str
            Identifiant unique du ticket inséré par le client.
        paiement_effectue : bool, optional
            Indique si le paiement a été validé (nécessaire pour la sortie effective).
            
        Retourne
        -------
        str
            Message de statut (succès, paiement requis, ou erreur).
        """
        # 1. Identification du placement
        placement = self.parking.trouver_placement_par_ticket(id_ticket)
        
        if not placement:
            return "Erreur: Ticket invalide ou voiture non trouvée."

        # Préparation du calcul des frais
        placement.heure_sortie = datetime.now()
        
        # 2. Vérification des services en cours (Logique Abonné/Livraison)
        client = placement.vehicule.proprietaire
        
        if client and client.est_abonne:
            services_en_cours = [s for s in client.mes_services if not s.est_terminé]
            
            # Si le client a demandé une livraison, la sortie est déléguée au service/voiturier
            if any(isinstance(s, Livraison) for s in services_en_cours):
                return "Sortie impossible via la borne. La voiture est en cours de livraison (Service Abonné)."
        
        # 3. Calcul et vérification du paiement
        frais = self.calculer_frais(placement)
        placement.frais_dus = frais

        if frais > 0 and not paiement_effectue:
            return f"Paiement requis: {frais:.2f}€. Veuillez payer pour continuer."
        
        # 4. Activation du Téléporteur et libération de la place
        place = placement.place
        succes_teleport = self.teleporteur.rapporter_vehicule(place)

        if succes_teleport:
            return f"Opération réussie. Véhicule récupéré de la place {place.id}. Total payé: {frais:.2f}€."
        else:
            return "Erreur lors de la libération de la place par le téléporteur."
        
    def changer_options_service(self, client: Client, nouvel_option: str) -> bool:
        """
        [cite_start]Implémente la politique de flexibilité: [cite: 27] le client peut changer ses options 
        de service sur simple coup de fil.
        
        Cette méthode simule l'action effectuée par l'Opérateur/Voiturier suite à l'appel du client.
        
        Paramètres
        ----------
        client : Client
            Le client dont les options doivent être modifiées.
        nouvel_option : str
            Description de l'option modifiée (ex: "Annuler Livraison").
            
        Retourne
        -------
        bool
            True si l'option a été changée (si le client est abonné), False sinon.
        """
        if client and client.est_abonne:
            # Ici, une logique complexe mettrait à jour self.mes_services du client.
            print(f"Options du client {client.nom} mises à jour sur simple coup de fil: {nouvel_option}.")
            return True
        return False