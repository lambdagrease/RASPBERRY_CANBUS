
import time
from can_manager import CanManager


def recevoir_reponse(can_manager, identifiant, timeout=2.0):
    """Attend une trame avec l'identifiant attendu."""
    debut = time.monotonic()

    while time.monotonic() - debut < timeout:
        message = can_manager.receive_frame(timeout=0.1)

        if message is not None and message.arbitration_id == identifiant:
            return message

    raise TimeoutError(f"Aucune réponse reçue pour 0x{identifiant:03X}")


def main():
    can_manager = CanManager()

    try:
        # LED ON
        print("TX : commande LED ON")
        can_manager.send_frame(0x100, [0x01])

        ack = recevoir_reponse(can_manager, 0x210)
        print(f"RX : 0x{ack.arbitration_id:03X} ACK={ack.data[0]}")

        time.sleep(0.5)

        # LED OFF
        print("\nTX : commande LED OFF")
        can_manager.send_frame(0x100, [0x00])

        ack = recevoir_reponse(can_manager, 0x210)
        print(f"RX : 0x{ack.arbitration_id:03X} ACK={ack.data[0]}")

        # Demande du compteur
        print("\nTX : demande compteur")
        can_manager.send_frame(0x101, [])

        reponse = recevoir_reponse(can_manager, 0x201)

        if len(reponse.data) < 2:
            raise ValueError("La réponse doit contenir deux octets.")

        valeur = (reponse.data[0] << 8) | reponse.data[1]

        print(f"RX : 0x{reponse.arbitration_id:03X}")
        print(f"Valeur : {valeur}")

    except (TimeoutError, ValueError) as erreur:
        print(f"Erreur : {erreur}")

    finally:
        can_manager.close()


if __name__ == "__main__":
    main()
