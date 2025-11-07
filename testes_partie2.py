import unittest
from datetime import datetime, timedelta
# Importation des classes des modules précédents
from model import Parking, Place, Placement, Vehicule, Ticket, Livraison, Client, Entretien, Service
from composants import BorneTicket, Teleporteur

# ==============================================================================
# CLASSE DE TESTS UNITAIRES - PARTIE 2
# Auteurs : Abdallah Aboulkhassim
# Date : Novembre 2025
# ==============================================================================


class TestPartie2_ReprendreVoiture(unittest.TestCase):
    """
    Classe de tests unitaires et d'intégration pour le Cas d'Utilisation : Reprendre la voiture (Partie 2).
    
    Elle vérifie la logique de libération de place, le calcul des frais et la gestion des services abonnés.
    """
    
    def setUp(self):
        """
        Configuration initiale pour chaque test.
        
        Crée :
        1. Les composants principaux (Parking, Teleporteur, BorneTicket).
        2. Les clients (Non-abonné, Abonné, Super Abonné) et leurs véhicules associés.
        3. Deux placements réels dans le parking (TICKET001 et TICKET002) pour simuler l'occupation.
        4. Une réservation dans le parking externe pour tester le Pack Garanti.
        """
        # 1. Initialisation des composants
        self.parking = Parking()
        self.teleporteur = Teleporteur(self.parking)
        self.borne = BorneTicket(self.parking, self.teleporteur)
        
        # 2. Création des Clients et des Véhicules (liés)
        self.client_na = Client(1, "Client Standard", est_abonne=False)
        self.client_ab = Client(2, "Client Abonné", est_abonne=True)
        self.client_super = Client(3, "Super Abonné", est_abonne=True, pack_garanti=True) 

        self.v_non_abonne = Vehicule("NA-111-NA", 4.5, 1.8, proprietaire=self.client_na)
        self.v_abonne = Vehicule("AB-222-AB", 5.0, 2.0, proprietaire=self.client_ab)
        self.v_super = Vehicule("SU-999-SU", 5.5, 2.5, proprietaire=self.client_super) 

        # Assurer les liens croisés pour les services
        self.client_na.voiture_actuelle = self.v_non_abonne
        self.client_ab.voiture_actuelle = self.v_abonne
        self.client_super.voiture_actuelle = self.v_super
        
        # 3. Placement (Non-abonné)
        self.place_101 = self.parking.places[101] 
        self.entree_na = datetime.now() - timedelta(hours=3) # Simule 3 heures de stationnement
        self.p_na = Placement("TICKET001", self.v_non_abonne, self.place_101, self.entree_na)
        self.place_101.occuper(self.p_na)
        self.parking.placements["TICKET001"] = self.p_na

        # 4. Placement (Abonné)
        self.place_102 = self.parking.places[102]
        self.entree_ab = datetime.now() - timedelta(minutes=30) # Simule 30 minutes de stationnement
        self.p_ab = Placement("TICKET002", self.v_abonne, self.place_102, self.entree_ab)
        self.place_102.occuper(self.p_ab)
        self.parking.placements["TICKET002"] = self.p_ab

        # Simulation du véhicule SU-999-SU garé en externe via le pack garanti
        self.parking.parking_externe.reservations[self.client_super.id] = self.v_super
        
    # --- Tests Unitaires sur la Libération ---
    
    def test_place_liberer(self):
        """Vérifie que l'objet Place passe correctement à l'état libre (est_occupée=False)."""
        self.assertTrue(self.place_101.est_occupée)
        self.assertTrue(self.place_101.liberer())
        self.assertFalse(self.place_101.est_occupée)

    def test_teleporteur_rapporte_et_libere(self):
        """
        Vérifie la chaîne d'action : Téléporteur -> Place.liberer() -> Parking.supprimer_placement().
        Ceci garantit la cohérence des états après le départ du véhicule.
        """
        id_place_test = self.place_101.id
        id_ticket_test = self.p_na.id
        
        self.assertTrue(self.teleporteur.rapporter_vehicule(self.place_101))
        
        # Post-conditions : Place libre et Placement supprimé
        self.assertFalse(self.parking.places[id_place_test].est_occupée)
        self.assertNotIn(id_ticket_test, self.parking.placements)


    # --- Tests Unitaires sur le Calcul des Frais ---
    
    def test_calcul_frais_non_abonne(self):
        """Vérifie le calcul correct des frais pour 3 heures de stationnement."""
        frais = self.borne.calculer_frais(self.p_na)
        self.assertAlmostEqual(frais, 7.50) # 3 heures * 2.5€ = 7.50€

    def test_calcul_frais_minimum(self):
        """Vérifie l'application du tarif minimum (5.0€) même pour une très courte durée."""
        # Création d'un placement très court (10 minutes)
        entree_courte = datetime.now() - timedelta(minutes=10)
        p_court = Placement("TICKET003", self.v_non_abonne, self.parking.places[102], entree_courte)
        
        frais = self.borne.calculer_frais(p_court)
        self.assertEqual(frais, 5.0) # Le tarif calculé (0.416€) est inférieur au minimum (5.0€)

    def test_calcul_frais_abonne(self):
        """Vérifie que les frais sont nuls (0.0€) pour un client abonné."""
        frais = self.borne.calculer_frais(self.p_ab)
        self.assertEqual(frais, 0.0)

    # --- Tests d'Intégration du Processus de Sortie Standard ---

    def test_processus_sortie_client_abonne(self):
        """Scénario d'intégration : L'abonné sort. Pas de paiement requis."""
        resultat = self.borne.processus_sortie("TICKET002")
        
        self.assertIn("Opération réussie", resultat)
        self.assertIn("Total payé: 0.00€", resultat)
        self.assertFalse(self.place_102.est_occupée)
        self.assertNotIn("TICKET002", self.parking.placements)

    def test_processus_sortie_paiement_requis(self):
        """Scénario d'intégration : Le non-abonné tente de sortir sans payer (1ère tentative)."""
        resultat = self.borne.processus_sortie("TICKET001", paiement_effectue=False)
        
        # Le système doit demander le paiement et ne pas libérer la place
        self.assertIn("Paiement requis:", resultat)
        self.assertTrue(self.place_101.est_occupée)
        
    def test_processus_sortie_paiement_valide(self):
        """Scénario d'intégration : Le non-abonné paie et sort (2ème tentative)."""
        # On simule le paiement réussi
        resultat = self.borne.processus_sortie("TICKET001", paiement_effectue=True) 
        
        # Le système doit réussir la sortie et libérer la place
        self.assertIn("Opération réussie", resultat)
        self.assertFalse(self.place_101.est_occupée)
        self.assertNotIn("TICKET001", self.parking.placements)
        
    # --- Tests sur la Gestion des Services Abonnés ---

    def test_demande_service_abonne(self):
        """Vérifie qu'un abonné peut enregistrer une demande de service (Livraison)."""
        client_ab = self.v_abonne.proprietaire
        demande_livr = Livraison("12 Rue du Cinéma", datetime.now() + timedelta(hours=2), datetime.now())
        
        self.assertTrue(client_ab.demander_service(demande_livr))
        self.assertEqual(len(client_ab.mes_services), 1)

    def test_demande_service_non_abonne(self):
        """Vérifie qu'un non-abonné ne peut PAS demander de service (règle métier)."""
        client_na = self.v_non_abonne.proprietaire
        demande_entr = Entretien("Pneus", datetime.now())
        
        self.assertFalse(client_na.demander_service(demande_entr))
        self.assertEqual(len(client_na.mes_services), 0)

    def test_sortie_bloquee_par_livraison(self):
        """
        Vérifie la règle métier : si un service de livraison est en cours, 
        la sortie standard via la borne est refusée.
        """
        client_ab = self.v_abonne.proprietaire
        
        # 1. Le client demande une livraison
        demande_livr = Livraison("Adresse", datetime.now() + timedelta(hours=1), datetime.now())
        client_ab.demander_service(demande_livr)
        
        # 2. Le client tente de sortir par la borne (TICKET002)
        resultat = self.borne.processus_sortie("TICKET002")
        
        # Le système doit retourner un message de blocage
        self.assertIn("Sortie impossible via la borne. La voiture est en cours de livraison", resultat)
        # La place ne doit PAS être libérée
        self.assertTrue(self.place_102.est_occupée)

    # --- Tests Spécifiques au Pack Garanti ---
    
    def test_client_s_inscrire_pack_garanti(self):
        """Vérifie que l'inscription active le statut garanti ET le statut abonné."""
        client_test = self.client_na 
        self.assertFalse(client_test.pack_garanti)
        self.assertFalse(client_test.est_abonne)
        
        client_test.s_inscrire_pack_garanti()
        
        self.assertTrue(client_test.pack_garanti)
        self.assertTrue(client_test.est_abonne) 

    def test_reprise_vehicule_pack_garanti(self):
        """Vérifie la reprise d'un véhicule garé dans le parking externe (Pack Garanti)."""
        client = self.client_super
        
        # Vérification initiale: La voiture est dans la liste des réservations externes
        self.assertIn(client.id, self.parking.parking_externe.reservations)
        
        # Action: Le système reprend la voiture (délégation à ParkingExterne)
        vehicule_recupere = self.parking.parking_externe.recuperer_vehicule(client)
        
        # Vérification des post-conditions: la voiture a été supprimée de la liste de réservation externe
        self.assertIsNotNone(vehicule_recupere)
        self.assertEqual(vehicule_recupere.immatriculation, "SU-999-SU")
        self.assertNotIn(client.id, self.parking.parking_externe.reservations)
        
if __name__ == '__main__':
    # Cette section permet d'exécuter la démo et les tests directement depuis le fichier
    
    # --- Démonstration du flux de sortie ---
    parking = Parking()
    teleporteur = Teleporteur(parking)
    borne = BorneTicket(parking, teleporteur)

    # Simulation d'un client qui vient de se garer (Partie 1)
    vehicule_test = Vehicule("XYZ-333", 4.0, 1.8)
    place_test = parking.places[101]
    placement_test = Placement("TICKET_DEMO", vehicule_test, place_test, datetime.now() - timedelta(hours=1.5))
    place_test.occuper(placement_test)
    parking.placements["TICKET_DEMO"] = placement_test

    print("\n--- DÉMONSTRATION DU FLUX DE SORTIE ---")
    print("Tentative de sortie (paiement non fait) :")
    borne.processus_sortie("TICKET_DEMO", paiement_effectue=False)

    print("\nTentative de sortie (paiement effectué) :")
    borne.processus_sortie("TICKET_DEMO", paiement_effectue=True)
    
    print("\n--- Exécution des Tests Unitaires ---")
    unittest.main(argv=['first-arg-is-ignored', 'TestPartie2_ReprendreVoiture'], exit=False)