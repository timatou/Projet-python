"""
Exécution d'un exemple pour la Partie 1
"""
from controller.parking_controller import ParkingController

def main():
    ctrl = ParkingController()
    ctrl.se_garer("AB-123-CD", 4.2, 1.8)
    ctrl.se_garer("EF-456-GH", 4.0, 1.9)

if __name__ == "__main__":
    main()
