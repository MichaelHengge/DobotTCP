import socket
import time

from multipledispatch import dispatch

class DobotMagicianE6:
    def __init__(self, ip='192.168.5.1', port=29999):
        self.ip = ip
        self.port = port
        self.connection = None
        self.isEnabled = False
        self.isDebug = True


    def Connect(self):
        """
        Connect to the Dobot Magician E6 robot.

        Args:
            None
        
        Returns:
            None
        
        Raises:
            Exception: If the connection fails.
        """
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

    def Disconnect(self):
        """
        Disconnect from the Dobot Magician E6 robot.

        Args:
            None

        Returns:
            None
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            if self.isDebug: print("  Disconnected from Dobot Magician E6")

    def Send_command(self, command):
        """
        Send a command to the Dobot and receive a response.

        Args:
            command (string): The command to send to the robot.

        Returns:
            The response from the robot.

        Raises:
            Exception: If not connected to the Dobot Magician E6.
        """
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


    # Control Commands:

    def PowerON(self):
        """
        Power on the Dobot Magician E6 robot. This seems to do nothing for the Magician E6.

        Returns:
            The response from the robot.
        """
        if self.isDebug: print("  Powering on Dobot Magician E6...")
        return self.Send_command("PowerOn()")

    @dispatch()
    def EnableRobot(self):
        """
        Enable the Dobot Magician E6 robot.

        Args:
            None

        Returns:
            The response from the robot.
        
        Raises:
            Exception: If the control mode is not TCP.
        """
        if self.isEnabled == False:
            if self.isDebug: print("  Enabling Dobot Magician E6...")
            response = self.Send_command("EnableRobot()")
            if response == "Control Mode Is Not Tcp":
                self.isEnabled = False
                raise Exception("Control Mode Is Not Tcp")
            else:
                self.isEnabled = True
                return response

    @dispatch(float)
    def EnableRobot(self, load):
        """
        Enable the Dobot Magician E6 robot.

        Args:
            load (float): The load weight on the robot. Unit: kg

        Returns:
            The response from the robot.
        
        Raises:
            Exception: If the control mode is not TCP.
        """
        if self.isEnabled == False:
            if self.isDebug: print("  Enabling Dobot Magician E6...")
            response = self.Send_command(f"EnableRobot({load})")
            if response == "Control Mode Is Not Tcp":
                self.isEnabled = False
                raise Exception("Control Mode Is Not Tcp")
            else:
                self.isEnabled = True
                return response
            
    @dispatch(float, float, float, float)
    def EnableRobot(self, load, centerX, centerY, centerZ):
        """
        Enable the Dobot Magician E6 robot.

        Args:
            load (float): The load weight on the robot. Unit: kg
            centerX (float): Eccentric distance in X direction, range: -999~999, unit: mm
            centerY (float): Eccentric distance in Y direction, range: -999~999, unit: mm
            centerZ (float): Eccentric distance in Z direction, range: -999~999, unit: mm

        Returns:
            The response from the robot.
        
        Raises:
            Exception: If the control mode is not TCP.
        """
        if self.isEnabled == False:
            if self.isDebug: print("  Enabling Dobot Magician E6...")
            response = self.Send_command(f"EnableRobot({load},{centerX},{centerY},{centerZ})")
            if response == "Control Mode Is Not Tcp":
                self.isEnabled = False
                raise Exception("Control Mode Is Not Tcp")
            else:
                self.isEnabled = True
                return response

    @dispatch(float, float, float, float, int)
    def EnableRobot(self, load, centerX, centerY, centerZ, isCheck):
        """
        Enable the Dobot Magician E6 robot.

        Args:
            load (float): The load weight on the robot. Unit: kg
            centerX (float): Eccentric distance in X direction, range: -999~999. Unit: mm
            centerY (float): Eccentric distance in Y direction, range: -999~999. Unit: mm
            centerZ (float): Eccentric distance in Z direction, range: -999~999. Unit: mm
            isCheck (int): Whether to check the load. 0: No, 1: Yes

        Returns:
            The response from the robot.
        
        Raises:
            Exception: If the control mode is not TCP.
        """
        if self.isEnabled == False:
            if self.isDebug: print("  Enabling Dobot Magician E6...")
            response = self.Send_command(f"EnableRobot({load},{centerX},{centerY},{centerZ})")
            if response == "Control Mode Is Not Tcp":
                self.isEnabled = False
                raise Exception("Control Mode Is Not Tcp")
            else:
                self.isEnabled = True
                return response

    def DisableRobot(self):
        """
        Disable the Dobot Magician E6 robot.
        
        Args:
            None

        Returns:
            The response from the robot.
        """
        if self.isEnabled:
            response = self.Send_command("DisableRobot()")
            self.isEnabled = False
            if self.isDebug: print("  Disable Dobot Magician E6...")
            return response 

    def ClearError(self):
        """
        Clear any errors on the Dobot Magician E6 robot.

        Args:
            None

        Returns:
            The response from the robot.
        """
        if self.isDebug: print("  Clearing Dobot Magician E6 errors...")
        return self.Send_command("ClearError()")

    def RunScript(self, projectName):
        """
        Run a script on the Dobot Magician E6 robot.

        Args:
            projectName (string): The name of the project to run.

        Returns:
            The response from the robot.
        """
        if self.isDebug: print(f"  Running script {projectName} on Dobot Magician E6...")
        return self.Send_command(f"RunScript({projectName})")

    def Stop(self):
        """
        Stop the Dobot Magician E6 robot motion queue.

        Args:
            None

        Returns:
            The response from the robot.
        """
        if self.isDebug: print("  Stopping Dobot Magician E6...")
        return self.Send_command("Stop()")

    def Pause(self):
        """
        Pause the Dobot Magician E6 robot motion queue.

        Args:
            None

        Returns:
            The response from the robot.
        """
        if self.isDebug: print("  Pausing Dobot Magician E6...")
        return self.Send_command("Pause()")

    def Continue(self):
        """
        Continue the Dobot Magician E6 robot motion queue after it has been paused.

        Args:
            None

        Returns:
            The response from the robot.
        """
        if self.isDebug: print("  Continuing Dobot Magician E6...")
        return self.Send_command("Continue()")

    def EmergencyStop(self, mode):
        """
        Stop the Dobot Magician E6 robot immediately in an emergency. The robot will be disabled and report an error which needs to be cleared before re-anabling.

        Args:
            mode (int): Emergency stop mode. 0: Release emergency stop switch, 1: Press emergency stop switch.

        Returns:
            The response from the robot.
        """
        if self.isDebug: print("  Emergency stopping Dobot Magician E6...")
        return self.Send_command("EmergencyStop()")

    def BrakeControl(self, axisID, value):
        """
        Cotrol the brake of robot joints. Can only be used when the robot is disabled otherise it will return an error (-1).

        Args:
            axisID (int): The joint ID to brake.
            value (int): Brake status. 0: Switch off brake (joints cannot be dragged), 1: switch on brake (joints can be dragged)

        Returns:
            The response from the robot.
        """
        if self.isDebug: print(f"  Setting brake control of axis {axisID} to value {value}")
        return self.Send_command(f"BrakeControl({axisID},{value})")

    def StartDrag(self):
        """
        Enter the drag mode of the robot. CAn't be used when in error state.

        Args:
            None

        Returns:
            The response from the robot.
        """
        if self.isDebug: print("  Entering drag mode...")
        return self.Send_command("StartDrag()")

    def StopDrag(self):
        """
        Exit the drag mode of the robot.

        Args:
            None

        Returns:
            The response from the robot.
        """
        if self.isDebug: print("  Exiting drag mode...")
        return self.Send_command("StopDrag()")

    # Movement Commands:

    def MoveJ(self,j1,j2,j3,j4,j5,j6):
        """
        Move the robot to a specified joint position.

        Args:
            j1 (int): Joint 1 angle.
            j2 (int): Joint 2 angle.
            j3 (int): Joint 3 angle.
            j4 (int): Joint 4 angle.
            j5 (int): Joint 5 angle.
            j6 (int): Joint 6 angle.

        Returns:
            The response from the robot.
        """
        if self.isDebug: print(f"  Joint move robot to ({j1},{j2},{j3},{j4},{j5},{j6})")
        move_command = f"MovJ(joint={{{j1},{j2},{j3},{j4},{j5},{j6}}})"
        return self.Send_command(move_command)
    
    def Home(self):
        """
        Move the robot to the home position.

        Returns:
            The response from the robot.
        """
        if self.isDebug: print("  Moving robot to home position")
        return self.MoveJ(0,0,0,0,0,0)

    def SetDebug(self, isDebug):
        """
        Set the debug mode for the Dobot Object

        Args
        isDebug (bool): Print Debug messages yes (True) or no  (False).

        Returns:
            None
        """
        self.isDebug = isDebug

    def ToolDO(self, index, status):
        """
        Set the digital output of the tool.

        Args:
            index (int): Tool DO index (1 or 2).
            status (int): Tool DO status. 1: ON, 0: OFF.

        Returns:
            The response from the robot.
        """
        if self.isDebug: print(f"  Setting tool digital output pin {index} to {status}")
        return self.Send_command(f"ToolDO({index},{status})")
    
    def ClearError(self):
        """
        Clear any errors on the Dobot Magician E6 robot.

        Returns:
            The response from the robot.
        """
        if self.isDebug: print("  Clearing Dobot Magician E6 errors...")
        return self.Send_command("ClearError()")

    def SetSucker(self, status):
        """
        Set the sucker status.

        Args:
            status (int): Sucker status. 1: ON, 0: OFF.
        
        Returns:
            The response from the robot.
        """
        if self.isDebug: print(f"  Setting sucker to {status}")
        return self.ToolDO(1,status)

    
    
    

# Example usage
if __name__ == "__main__":
    dobot = DobotMagicianE6()
    dobot.Connect()
    dobot.EnableRobot()
    dobot.Home()
