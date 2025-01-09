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

    # General Python Commands:

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

    def SetDebug(self, isDebug):
        """
        Set the debug mode for the Dobot Object

        Args
        isDebug (bool): Print Debug messages yes (True) or no  (False).

        Returns:
            None
        """
        self.isDebug = isDebug


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
            response = self.Send_command(f"EnableRobot({load},{centerX},{centerY},{centerZ},{isCheck})")
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


    # Settings Commands

    def SpeedFactor(self, ratio=0):
        """
        Set the global speed factor of the robot.

        Args:
            ratio (int): The global speed factor. Range: 1~100

        Returns:
            The response from the robot.
        """
        if self.isDebug: print(f"  Setting global speed factor to {ratio}")
        return self.Send_command(f"SpeedFactor({ratio})")

    def User(self,index):
        """
        Set the global user coordinate system of the robot. Default is 0.

        Args:
            index (int): Calibrated user coordinate system. Needs to be set up in DobotStudio before it can be used here.

        Returns:
             ResultID which is the algorithm queue ID, which can be used to judge the execution sequence of commands. -1 indicates that the set user coordinate system index does not exist.
        """
        if self.isDebug: print(f"  Setting user index to {index}")
        return self.Send_command(f"User({index})")

    def SetUser(self, index, table):
        """
        Modify the specified user coordinate system of the robot.

        Args:
            index (int): User coordinate system index. Range: [0,9]
            table (string): User coordinate system after modification (format: {x, y, z, rx, ry, rz}).

        Returns:
            The response from the robot.
        """
        if self.isDebug: print(f"  Setting user coordinate system {index} to {table}")
        return self.Send_command(f"SetUser({index},{table})")

    def CalcUser(self, index, matrix_direction, table):
        """
        Calculate the user coordinate system of the robot.

        Args:
            index (int): User coordinate system index. Range: [0,9]
            matrix_direction (int): Calculation method (see TCP protocols for details). 0: right multiplication, 1: left multiplication.
            table (string): User coordinate system offset (format: {x, y, z, rx, ry, rz}).

        Returns:
            The user coordinate system after calculation {x, y, z, rx, ry, rz}.
        """
        if self.isDebug: print(f"  Calculating user coordinate system {index} to {table}")
        return self.Send_command(f"CalcUser({index},{matrix_direction},{table})")

    def Tool(self, index):
        """
        Set the global tool coordinate system of the robot. Default is 0.

        Args:
            index (int): Calibrated tool coordinate system. Needs to be set up in DobotStudio before it can be used here.

        Returns:
            ResultID which is the algorithm queue ID, which can be used to judge the execution sequence of commands. -1 indicates that the set user coordinate system index does not exist.
        """
        if self.isDebug: print(f"  Setting tool index to {index}")
        return self.Send_command(f"Tool({index})")
    
    def SetTool(self, index, table):
        """
        Modify the specified tool coordinate system of the robot.

        Args:
            index (int): Tool coordinate system index. Range: [0,9]
            table (string): Tool coordinate system after modification (format: {x, y, z, rx, ry, rz}).

        Returns:
            The response from the robot.
        """
        if self.isDebug: print(f"  Setting tool coordinate system {index} to {table}")
        return self.Send_command(f"SetTool({index},{table})")
    
    def CalcTool(self, index, matrix_direction, table):
        """
        Calculate the tool coordinate system of the robot.

        Args:
            index (int): Tool coordinate system index. Range: [0,9]
            matrix_direction (int): Calculation method (see TCP protocols for details). 0: right multiplication, 1: left multiplication.
            table (string): Tool coordinate system offset (format: {x, y, z, rx, ry, rz}).

        Returns:
            The tool coordinate system after calculation {x, y, z, rx, ry, rz}.
        """
        if self.isDebug: print(f"  Calculating tool coordinate system {index} to {table}")
        return self.Send_command(f"CalcTool({index},{matrix_direction},{table})")

    @dispatch(str)
    def SetPayload(self, name):
        """
        Set the robot payload.

        Args:
            name (string): Load parameter group saved in DobotStudio.

        Returns:
            ResultID, the algorithm queue ID, which can be used to judge the execution sequence of commands.
        """
        if self.isDebug: print(f"  Setting payload to preset {name})")
        return self.Send_command(f"SetPayload({name})")

    @dispatch(float)
    def SetPayload(self, load):
        """
        Set the robot payload.

        Args:
            load (float): The load weight on the robot. Unit: kg

        Returns:
            ResultID, the algorithm queue ID, which can be used to judge the execution sequence of commands.
        """
        if self.isDebug: print(f"  Setting payload to {load} kg)")
        return self.Send_command(f"SetPayload({load})")

    @dispatch(float, float, float, float)
    def SetPayload(self, load, x, y, z):
        """
        Set the robot payload.

        Args:
            load (float): The load weight on the robot. Unit: kg
            x (float): Eccentric distance in X direction, range: -500~500. Unit: mm
            y (float): Eccentric distance in Y direction, range: -500~500. Unit: mm
            z (float): Eccentric distance in Z direction, range: -500~500. Unit: mm

        Returns:
            ResultID, the algorithm queue ID, which can be used to judge the execution sequence of commands.
        """
        if self.isDebug: print(f"  Setting payload to {load} kg at ({x},{y},{z})")
        return self.Send_command(f"SetPayload({load},{x},{y},{z})")

    def AccJ(self, R=100):
        """
        Set the robot acceleration rate for joint motions.

        Args:
            R (int): Acceleration rate. Range: 1~100. Default is 100.

        Returns:
            The response from the robot.
        """
        if self.isDebug: print(f"  Setting joint acceleration to {R}")
        return self.Send_command(f"AccJ({R})")

    def AccL(self, R=100):
        """
        Set the robot acceleration rate for linear motions.

        Args:
            R (int): Acceleration rate. Range: 1~100. Default is 100.

        Returns:
            The response from the robot.
        """
        if self.isDebug: print(f"  Setting linear acceleration to {R}")
        return self.Send_command(f"AccL({R})")
    
    def VelJ(self, R=100):
        """
        Set the robot velocity rate for joint motions.

        Args:
            R (int): Velocity rate. Range: 1~100. Default is 100.

        Returns:
            The response from the robot.
        """
        if self.isDebug: print(f"  Setting joint velocity to {R}")
        return self.Send_command(f"VelJ({R})")

    def VelL(self, R=100):
        """
        Set the robot velocity rate for linear motions.

        Args:
            R (int): Velocity rate. Range: 1~100. Default is 100.

        Returns:
            The response from the robot.
        """
        if self.isDebug: print(f"  Setting linear velocity to {R}")
        return self.Send_command(f"VelL({R})")

    def CP(self, R=0):
        """
        Set the robot continuous path (CP) rate.

        Args:
            R (int): Continuous path rate. Range: 0~100. Default is 0.

        Returns:
            The response from the robot.
        """
        if self.isDebug: print(f"  Setting continuous path rate to {R}")
        return self.Send_command(f"CP({R})")

    def SetCollisionLevel(self, level):
        """
        Set the robot collision sensitivity level.

        Args:
            level (int): Collision sensitivity level. Range: 0~5. 0: Disable collision detection, 5: More sensitive with higher level.

        Returns:
            ResultID, the algorithm queue ID, which can be used to judge the execution sequence of commands.
        """
        if self.isDebug: print(f"  Setting collision sensitivity level to {level}")
        return self.Send_command(f"SetCollisionLevel({level})")

    def SetBackDistance(self, distance):
        """
        Set the robot backoff distance after a collision is detected.

        Args:
            distance (float): Backoff distance. Range: 0~50. Unit: mm.

        Returns:
            ResultID, the algorithm queue ID, which can be used to judge the execution sequence of commands.
        """
        if self.isDebug: print(f"  Setting back distance to {distance}")
        return self.Send_command(f"SetBackDistance({distance})")

    def SetPostCollisionMode(self, mode):
        """
        Set the robot post-collision mode.

        Args:
            mode (int): Post-collision mode. 0: Stop, 1: Pause.

        Returns:
            ResultID, the algorithm queue ID, which can be used to judge the execution sequence of commands.
        """
        if self.isDebug: print(f"  Setting post-collision mode to {mode}")
        return self.Send_command(f"SetPostCollisionMode({mode})")

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
    
    def MoveL(self,j1,j2,j3,j4,j5,j6):
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
        move_command = f"MovL(joint={{{j1},{j2},{j3},{j4},{j5},{j6}}})"
        return self.Send_command(move_command)

    def Home(self):
        """
        Move the robot to the home position.

        Returns:
            The response from the robot.
        """
        if self.isDebug: print("  Moving robot to home position")
        return self.MoveJ(0,0,0,0,0,0)


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
    dobot.SetSucker(0)
