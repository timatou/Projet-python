from datetime import datetime, timedelta 

# ==============================================================================
# CLASSES DE SERVICE
# Auteurs : Abdallah Aboulkhassim
# Date : Novembre 2025
# ==============================================================================

class Service:
    """
    Classe abstraite représentant un service demandé par un Abonné.
    
    Elle sert de base aux services spécifiques (Livraison, Entretien, Maintenance).
    """
    def __init__(self, description: str, date_demande: datetime):
        """

        Initialise un nouveau service.
        
        Paramètres
        ----------
        description : str
            Brève description du service (ex: "Livraison", "Entretien").
        date_demande : datetime
            Date et heure auxquelles le service a été demandé.
        """
        self.description = description
        self.date_demande = date_demande
        self.est_terminé = False
        self.adresse_livraison = None 

class Livraison(Service):
    """
    Service spécifique de livraison du véhicule à une adresse et heure donnée.
    Hérite de Service.
    """
    def __init__(self, adresse: str, heure_livraison: datetime, date_demande: datetime):
        """
        Initialise un service de livraison.
        
        Paramètres
        ----------
        adresse : str
            Adresse de destination du véhicule.
        heure_livraison : datetime
            Heure souhaitée pour la livraison.
        date_demande : datetime
            Date de la demande.
        """
        super().__init__("Livraison du véhicule", date_demande)
        self.adresse_livraison = adresse
        self.heure_livraison = heure_livraison

class Entretien(Service):
    """
    Service spécifique d'entretien ou de maintenance légère du véhicule.
    Hérite de Service.
    """
    def __init__(self, details: str, date_demande: datetime):
        """
        Initialise un service d'entretien.
        
        Paramètres
        ----------
        details : str
            Détails de l'entretien à effectuer (ex: "Vidange", "Pneus").
        date_demande : datetime
            Date de la demande.
        """
        super().__init__(f"Entretien: {details}", date_demande)
        self.details_entretien = details

class Maintenance(Service):
    """
    Service de maintenance ou de réparation plus complexe du véhicule.
    Hérite de Service.
    """
    def __init__(self, probleme: str, date_demande: datetime):
        """
        Initialise un service de maintenance.
        
        Paramètres
        ----------
        probleme : str
            Description du problème nécessitant la maintenance.
        date_demande : datetime
            Date de la demande.
        """
        super().__init__(f"Maintenance: {probleme}", date_demande)
        self.probleme = probleme

# ==============================================================================
# CLASSE CLIENT
# ==============================================================================

class Client:
    """
    Représente le client du parking, incluant son statut d'abonnement et de pack garanti.
    """
    def __init__(self, id_client: int, nom: str, est_abonne: bool = False, pack_garanti: bool = False):
        """
        Initialise un client.
        
        Paramètres
        ----------
        id_client : int
            Identifiant unique du client.
        nom : str
            Nom complet du client.
        est_abonne : bool, optional
            True si le client a un abonnement standard. Par défaut à False.
        pack_garanti : bool, optional
            True si le client a le Pack Garanti (Super Abonné). Par défaut à False.
        """
        self.id = id_client
        self.nom = nom
        self.est_abonne = est_abonne
        self.pack_garanti = pack_garanti
        self.mes_services = [] # Liste des objets Service (en cours ou passés)
        self.voiture_actuelle = None # Lien vers l'objet Vehicule garé (si garé)
        
    def s_inscrire_pack_garanti(self):
        """
        Active le statut Pack Garanti.
        
        Selon les règles métier, active également le statut d'abonné standard.
        """
        self.pack_garanti = True
        self.est_abonne = True 
    
    def demander_service(self, service: Service) -> bool:
        """
        Enregistre une nouvelle demande de service si le client est abonné.
        
        Paramètres
        ----------
        service : Service
            Objet Service (Livraison, Entretien, Maintenance) demandé.
            
        Retourne
        -------
        bool
            True si la demande est enregistrée, False sinon (client non abonné).
        """
        if not self.est_abonne:
            return False 
        self.mes_services.append(service)
        return True

# ==============================================================================
# CLASSE VÉHICULE
# ==============================================================================

class Vehicule:
    """
    Représente une voiture garée dans le parking.
    """
    def __init__(self, immatriculation: str, longueur: float, hauteur: float, proprietaire: Client = None):
        """
        Initialise un véhicule.
        
        Paramètres
        ----------
        immatriculation : str
            Plaque d'immatriculation unique.
        longueur : float
            Longueur du véhicule (pour l'attribution de place).
        hauteur : float
            Hauteur du véhicule (pour l'attribution de place).
        proprietaire : Client, optional
            Objet Client propriétaire du véhicule. Par défaut à None.
        """
        self.immatriculation = immatriculation
        self.longueur = longueur
        self.hauteur = hauteur
        self.proprietaire = proprietaire
        
        # Le statut d'abonnement est hérité du propriétaire lors de l'initialisation
        self.est_abonne = proprietaire.est_abonne if proprietaire else False

# ==============================================================================
# CLASSES DE PLACE ET PLACEMENT
# ==============================================================================

class Place:
    """
    Représente une place physique dans le parking DreamPark.
    """
    def __init__(self, id_place: int, niveau: int, longueur: float, hauteur: float):
        """
        Initialise une place.
        
        Paramètres
        ----------
        id_place : int
            Identifiant unique de la place.
        niveau : int
            Niveau du parking où se situe la place.
        longueur : float
            Longueur maximale de la place.
        hauteur : float
            Hauteur maximale de la place.
        """
        self.id = id_place
        self.niveau = niveau
        self.longueur = longueur
        self.hauteur = hauteur
        self.est_occupée = False 
        self.placement_actuel = None # Lien vers l'enregistrement d'occupation (Placement)

    def liberer(self) -> bool:
        """
        Marque la place comme libre.
        
        Retourne
        -------
        bool
            True si la place a été libérée, False si elle était déjà libre.
        """
        if self.est_occupée:
            self.est_occupée = False
            self.placement_actuel = None
            return True
        return False
    
    def occuper(self, placement) -> bool:
        """
        Marque la place comme occupée par un Placement. (Partie 1)
        
        Paramètres
        ----------
        placement : Placement
            L'objet Placement qui enregistre l'occupation.
            
        Retourne
        -------
        bool
            True si la place a été occupée, False si elle était déjà occupée.
        """
        if not self.est_occupée:
            self.est_occupée = True
            self.placement_actuel = placement
            return True
        return False

class Placement:
    """
    Enregistrement de stationnement. Associe Véhicule, Place et les temps d'entrée/sortie.
    """
    def __init__(self, id_placement: str, vehicule: Vehicule, place: Place, heure_entree: datetime):
        """
        Initialise un enregistrement de placement.
        
        Paramètres
        ----------
        id_placement : str
            Identifiant unique (souvent l'ID du ticket).
        vehicule : Vehicule
            Objet Véhicule concerné.
        place : Place
            Objet Place occupée.
        heure_entree : datetime
            Heure exacte de l'entrée dans le parking.
        """
        self.id = id_placement
        self.vehicule = vehicule
        self.place = place
        self.heure_entree = heure_entree
        self.heure_sortie = None
        self.frais_dus = 0.0

class Ticket:
    """
    Représente le ticket délivré à l'entrée. Sert de clé d'identification.
    """
    def __init__(self, id_ticket: str, placement: Placement, est_payé: bool = False):
        """
        Initialise un ticket.
        
        Paramètres
        ----------
        id_ticket : str
            Identifiant unique du ticket.
        placement : Placement
            Lien vers l'enregistrement de stationnement associé.
        est_payé : bool, optional
            Statut de paiement. Par défaut à False.
        """
        self.id = id_ticket
        self.placement = placement
        self.est_payé = est_payé

# ==============================================================================
# CLASSE PARKING EXTERNE (Pack Garanti)
# ==============================================================================

class ParkingExterne:
    """
    Simule un parking externe utilisé pour le service Pack Garanti Parking.
    """
    def __init__(self, nom: str = "ExternalPark"):
        """Initialise le parking externe."""
        self.nom = nom
        self.reservations = {} # {id_client: Vehicule}

    def reserver_et_garer(self, client: Client, vehicule: Vehicule) -> bool:
        """
        Réserve et simule le stationnement du véhicule dans le parking externe (Partie 1).
        
        Retourne
        -------
        bool
            True si le véhicule est garé.
        """
        if client.id not in self.reservations:
            self.reservations[client.id] = vehicule
            print(f"**Pack Garanti:** Réservation et stationnement dans le parking externe '{self.nom}'.")
            return True
        return False

    def recuperer_vehicule(self, client: Client) -> Vehicule | None:
        """
        Simule la reprise du véhicule par le voiturier pour le client (Partie 2).
        
        Retourne
        -------
        Vehicule ou None
            L'objet Véhicule récupéré, ou None si non trouvé.
        """
        vehicule = self.reservations.get(client.id)
        if vehicule:
            del self.reservations[client.id]
            print(f"**Pack Garanti:** Véhicule récupéré de '{self.nom}'. Prêt à être livré.")
            return vehicule
        return None
    
# ==============================================================================
# CLASSE PARKING (COMPOSANT CENTRAL)
# ==============================================================================

class Parking:
    """
    Le composant central de gestion des places, des placements et des accès aux parkings externes.
    """
    def __init__(self):
        """Initialise le parking et ses composants principaux."""
        self.places = {
            101: Place(101, 1, 5.0, 2.0),
            102: Place(102, 1, 6.0, 3.0)
        }
        self.placements = {}  # {id_ticket: objet Placement}
        self.parking_externe = ParkingExterne() 

    def trouver_placement_par_ticket(self, id_ticket: str) -> Placement | None:
        """
        Recherche un Placement (enregistrement de stationnement local) à partir de l'ID du ticket.
        """
        return self.placements.get(id_ticket)
    
    def supprimer_placement_par_place(self, place: Place) -> bool:
        """
        Supprime le Placement enregistré après qu'une Place ait été libérée par le Téléporteur.
        """
        id_a_supprimer = None
        for id_ticket, placement in self.placements.items():
            if placement.place == place:
                id_a_supprimer = id_ticket
                break
        
        if id_a_supprimer:
            del self.placements[id_a_supprimer]
            return True
        return False
    
    def planifier_reprise_service(self, client: Client, service: Service) -> str:
        """
        Gère la planification de la reprise du véhicule pour un service (Livraison/Entretien),
        que le véhicule soit garé localement ou en externe. (Partie 2)
        """
        if client.voiture_actuelle is None:
            return "Erreur: Le client n'a pas de voiture actuelle associée."

        # 1. Vérification du stationnement local (DreamPark)
        placement_a_reprendre = None
        for p in self.placements.values():
            if p.vehicule == client.voiture_actuelle:
                placement_a_reprendre = p
                break
            
        if placement_a_reprendre:
            # Reprise locale : la logique du Téléporteur/Voiturier sera appliquée
            place = placement_a_reprendre.place
            return f"Reprise locale de la place {place.id} planifiée pour le service {service.description}."
            
        # 2. Vérification du stationnement externe (Pack Garanti)
        if client.pack_garanti and client.id in self.parking_externe.reservations:
            # Reprise externe : on utilise la logique du ParkingExterne pour simuler la récupération
            self.parking_externe.recuperer_vehicule(client)
            return f"Reprise planifiée (Externe) pour le service {service.description}."
            
        return "Erreur: Placement non trouvé pour ce véhicule, ni localement, ni via le Pack Garanti."
    
    def gerer_pack_garanti_si_plein(self, client: Client, vehicule: Vehicule) -> bool:
        """
        Gère le stationnement garanti si DreamPark est plein (logique de la Partie 1).
        L'opération est déléguée au Parking Externe.
        """
        if client.pack_garanti:
            # L'implémentation complète nécessiterait une vérification 'if self.is_full()' ici
            return self.parking_externe.reserver_et_garer(client, vehicule)
        return False