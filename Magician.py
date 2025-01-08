import socket
import time

class DobotMagicianE6:
    def __init__(self, ip='192.168.5.1', port=29999):
        self.ip = ip
        self.port = port
        self.connection = None
        self.isEnabled = False
        self.isDebug = True

    def Connect(self):
        '''
        Connect to the Dobot Magician E6 robot.
        :return: None
        '''
        try :
            if self.isDebug: print(f"Connecting to Dobot at {self.ip}:{self.port}...")
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((self.ip, self.port))
            time.sleep(2)  # Wait for the connection to establish
            if self.isDebug: print("  Connected to Dobot Magician E6")
            if self.connection == None:
                raise Exception("Connection error")
        except:
            print("  Connection error")
            self.connection = None

    def EnableRobot(self):
        '''
        Enable the Dobot Magician E6 robot.
        :return: The response from the robot.
        '''
        if self.isEnabled == False:
            if self.isDebug: print("  Enabling Dobot Magician E6...")
            response = self.Send_command("EnableRobot()")
            if response == "Control Mode Is Not Tcp":
                self.isEnabled = False
                raise Exception("Control Mode Is Not Tcp")
            else:
                self.isEnabled = True
                return response

    def DisableRobot(self):
        '''
        Disable the Dobot Magician E6 robot.
        :return: The response from the robot.
        '''
        if self.isEnabled:
            response = self.Send_command("DisableRobot()")
            self.isEnabled = False
            if self.isDebug: print("  Disable Dobot Magician E6...")
            return response

    def Disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            if self.isDebug: print("  Disconnected from Dobot Magician E6")

    def ClearError(self):
        '''
        Clear any errors on the Dobot Magician E6 robot.
        :return: The response from the robot.
        '''
        if self.isDebug: print("  Clearing Dobot Magician E6 errors...")
        return self.Send_command("ClearError()")

    def Send_command(self, command):
        '''
        Send a command to the Dobot and receive a response.
        :param command: The command string to send.
        :return: The response from the robot.
        '''
        if self.connection:
            try:
                self.connection.sendall(command.encode() + b'\n')
                response = self.connection.recv(1024).decode()
                return response.strip()
            except Exception as e:
                print(f"  Python error sending command: {e}")
                return None
        else:
            raise Exception("  ! Not connected to Dobot Magician E6")

    def MoveJ(self,j1,j2,j3,j4,j5,j6):
        '''
        Move the robot to a specified joint position.
        :param j1: The joint 1 position.
        :param j2: The joint 2 position.
        :param j3: The joint 3 position.
        :param j4: The joint 4 position.
        :param j5: The joint 5 position.
        :param j6: The joint 6 position.
        :return: The response from the robot.
        '''
        if self.isDebug: print(f"  Joint move robot to ({j1},{j2},{j3},{j4},{j5},{j6})")
        move_command = f"MovJ(joint={{{j1},{j2},{j3},{j4},{j5},{j6}}})"
        return self.Send_command(move_command)
    
    def Home(self):
        '''
        Move the robot to the home position.
        :return: The response from the robot.
        '''
        if self.isDebug: print("  Moving robot to home position")
        return self.MoveJ(0,0,0,0,0,0)

    def SetDebug(self, isDebug):
        '''
        Set the debug mode for the Dobot Object
        :param isDebug: Print Debug messages yes (True) or no  (False).
        :return: None
        '''
        self.isDebug = isDebug

    def ToolDO(self, index, status):
        '''
        Set the digital output of the tool.
        :param index: Tool DO index.
        :param status: Tool DO status. 1: ON, 0: OFF.
        :return: The response from the robot.
        '''
        if self.isDebug: print(f"  Setting tool digital output pin {index} to {status}")
        return self.Send_command(f"ToolDO({index},{status})")
    
    def ClearError(self):
        '''
        Clear any errors on the Dobot Magician E6 robot.
        :return: The response from the robot.
        '''
        if self.isDebug: print("  Clearing Dobot Magician E6 errors...")
        return self.Send_command("ClearError()")

    def SetSucker(self, status):
        '''
        Set the sucker status.
        :param status: Sucker status. 1: ON, 0: OFF.
        :return: The response from the robot.
        '''
        if self.isDebug: print(f"  Setting sucker to {status}")
        return self.ToolDO(1,status)

# Example usage
if __name__ == "__main__":
    dobot = DobotMagicianE6()
    dobot.Connect()
    dobot.EnableRobot()
