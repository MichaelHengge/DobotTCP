import socket
import time

class DobotMagicianE6:
    def __init__(self, ip='192.168.5.1', port=29999):
        self.ip = ip
        self.port = port
        self.connection = None
        self.isEnabled = False

    def Connect(self):
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
        if self.isEnabled == False:
            print("Enabling Dobot Magician E6...")
            return self.send_command("EnableRobot()")

    def DisableRobot(self):
        if self.isEnabled:
            response = self.send_command("DisableRobot()")
            self.isEnabled = False
            return response

    def Disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Disconnected from Dobot Magician E6")

    def Send_command(self, command):
        """
            Send a command to the Dobot and receive a response.
            :param command: The command string to send.
            :return: The response from the robot.
        """
        if self.connection:
            try:
                self.connection.sendall(command.encode() + b'\n')
                response = self.connection.recv(1024).decode()
                return response.strip()
            except Exception as e:
                print(f"Python error sending command: {e}")
                return None
        else:
            raise Exception("Not connected to Dobot Magician E6")

    def MoveJ(self,j1,j2,j3,j4,j5,j6):
        """
        Move the robot to a specified joint position.
        :param j1: The joint 1 position.
        :param j2: The joint 2 position.
        :param j3: The joint 3 position.
        :param j4: The joint 4 position.
        :param j5: The joint 5 position.
        :param j6: The joint 6 position.
        :return: The response from the robot.
        """
        move_command = f"MovJ(joint={{{j1},{j2},{j3},{j4},{j5},{j6}}})"
        return self.send_command(move_command)

# Example usage
if __name__ == "__main__":
    dobot = DobotMagicianE6()
    dobot.Connect()
    dobot.move_to(0, 0, 0, 0, 0, 0)
    dobot.Disconnect()