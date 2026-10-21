
import can


class CanManager:
    def __init__(self, channel="can0", interface="socketcan"):
        """Ouvre l'interface CAN."""
        self.bus = can.interface.Bus(
            channel=channel,
            interface=interface
        )

    def send_frame(self, arbitration_id, data):
        """Envoie une trame CAN."""
        message = can.Message(
            arbitration_id=arbitration_id,
            data=data,
            is_extended_id=False
        )
        self.bus.send(message)

    def receive_frame(self, timeout=None):
        """Reçoit une trame CAN, ou None si aucune trame n'arrive."""
        return self.bus.recv(timeout=timeout)

    def close(self):
        """Ferme l'interface CAN."""
        self.bus.shutdown()
