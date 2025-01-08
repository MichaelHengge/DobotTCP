import socket
import time

class DobotMagicianE6:
    def __init__(self, ip='192.168.5.1', port=29999):
        self.ip = ip
        self.port = port
        self.connection = None

    def connect(self):
        try :
            print(f"Connecting to Dobot at {self.ip}:{self.port}...")
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((self.ip, self.port))
            time.sleep(2)  # Wait for the connection to establish
            print("Connected to Dobot Magician E6")
        except:
            print("Connection error")
            self.connection = None

    def EnableRobot(self):
        print("Enabling Dobot Magician E6...")
        return self.send_command("EnableRobot()")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from Dobot Magician E6")

    def send_command(self, command):
        """
            Send a command to the Dobot and receive a response.
            :param sock: The socket object connected to the robot.
            :param command: The command string to send.
            :return: The response from the robot.
        """
        if self.connection:
            try:
                self.sock.sendall(command.encode() + b'\n')
                response = self.sock.recv(1024).decode()
                return response.strip()
            except Exception as e:
                print(f"Error sending command: {e}")
                return None
        else:
            raise Exception("Not connected to Dobot Magician E6")

    def move_to(self, x, y, z, r):
        command = f"MOVE X{x} Y{y} Z{z} R{r}\n"
        response = self.send_command(command)
        print(f"Move command response: {response}")

# Example usage
if __name__ == "__main__":
    dobot = DobotMagicianE6()
    dobot.connect()
    dobot.move_to(200, 0, 50, 0)
    dobot.disconnect()