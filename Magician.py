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

    def DragSensitivity(self, index, value):
        """
        Set the drag sensitivity of the robot. 

        Args:
            index (int): Axis number. 0: All axis, 1-6: J1-J6.
            value (int): Drag sensitivity value. Smaller values equal larger resistance force Range: 1~90.

        Returns:
            The response from the robot.
        """
        if self.isDebug: print(f"  Setting drag sensitivity of axis {index} to {value}")
        return self.Send_command(f"DragSensitivity({index},{value})")

    def EnableSafeSkin(self, status):
        """
        Enable or disable the robot safe skin feature. The magician E6 does not have a safe skin feature.

        Args:
            status (int): Safe skin status. 0: Disable, 1: Enable.

        Returns:
            ResultID is the algorithm queue ID, which can be used to judge the execution sequence of commands.
        """
        if self.isDebug: print(f"  Setting safe skin to {status}")
        return self.Send_command(f"EnableSafeSkin({status})")

    def SetSafeSkin(self, part, status):
        """
        Set the safe skin sensitivity of the robot. The magician E6 does not have a safe skin feature.

        Args:
            part (int): Part of the robot. 3: forearm, 4~6: J4~J6 joints
            status (int): Safe skin sensitivity. 1: Low, 2: Medium, 3: High

        Returns:
            ResultID is the algorithm queue ID, which can be used to judge the execution sequence of commands.
        """
        if self.isDebug: print(f"  Setting safe skin of part {part} to {status}")
        return self.Send_command(f"SetSafeSkin({part},{status})")

    def SetSafeWallEnable(self, index, value):
        """
        Enable or disable the specified robot safe wall feature. Safety wall needs to be set up in DobotStudio before it can be used here.

        Args:
            index (int): Safety wall index. Range: 1~8
            value (int): Safety wall value. 0: Disable, 1: Enable

        Returns:
            ResultID is the algorithm queue ID, which can be used to judge the execution sequence of commands.
        """
        if self.isDebug: print(f"  Setting safety wall {index} to {value}")
        return self.Send_command(f"SetSafeWallEnable({index},{value})")

    def SetWorkZoneEnable(self, index, value):
        """
        Enable or disable the specified robot interference area. Work zone needs to be set up in DobotStudio before it can be used here.

        Args:
            index (int): Work zone index. Range: 1~6
            value (int): Work zone value. 0: Disable, 1: Enable

        Returns:
            ResultID is the algorithm queue ID, which can be used to judge the execution sequence of commands.
        """
        if self.isDebug: print(f"  Setting work zone {index} to {value}")
        return self.Send_command(f"SetWorkZoneEnable({index},{value})")


    # Calculating and obtaining commands:

    def RobotMode(self):
        """
        Get the current state of the robot.

        Args:
            None

        Returns:
            The robot mode.See TCP protocols for details.
        """
        if self.isDebug: print("  Getting robot mode...")
        return self.Send_command("RobotMode()")
    
    def PositiveKin(self, J1, J2, J3, J4, J5, J6, User=0, Tool=0):
        """
        Calculate the coordinates of the end of the robot in the specified Cartesian coordinate system, based on the given angle of each joint. Positive solution.

        Args:
            J1 (float): Joint 1 angle. Unit: degree.
            J2 (float): Joint 2 angle. Unit: degree.
            J3 (float): Joint 3 angle. Unit: degree.
            J4 (float): Joint 4 angle. Unit: degree.
            J5 (float): Joint 5 angle. Unit: degree.
            J6 (float): Joint 6 angle. Unit: degree.
            User (int): User coordinate system index. Default (0) is the global user coordinate system.
            Tool (int): Tool coordinate system index. Default (0) is the global tool coordinate system.

        Returns:
            The cartesian point coordinates {x,y,z,a,b,c}
        """
        if self.isDebug: print(f"  Calculating positive kinematics of robot at ({J1},{J2},{J3},{J4},{J5},{J6})")
        return self.Send_command(f"PositiveKin({J1},{J2},{J3},{J4},{J5},{J6},user={User},tool={Tool})")

    def InverseKin(self, X, Y, Z, Rx, Ry, Rz, User=0, Tool=0, useJointNear=0, JointNear={}):
        """
        Calculate the joint angles of the robot based on the given Cartesian coordinates of the end of the robot. Positive solution.

        Args:
            X (float): X coordinate of the end of the robot. Unit: mm.
            Y (float): Y coordinate of the end of the robot. Unit: mm.
            Z (float): Z coordinate of the end of the robot. Unit: mm.
            Rx (float): Rotation angle around the X axis. Unit: degree.
            Ry (float): Rotation angle around the Y axis. Unit: degree.
            Rz (float): Rotation angle around the Z axis. Unit: degree.
            User (int): User coordinate system index. Default (0) is the global user coordinate system.
            Tool (int): Tool coordinate system index. Default (0) is the global tool coordinate system.
            useJointNear (int): Whether to use the joint near data. 0: No, 1: Yes. Default is 0.
            JointNear (string):  Joint coordinates for selecting joint angles, format: jointNear={j1,j2,j3,j4,j5,j6}

        Returns:
            Joint coordinates {J1, J2, J3, J4, J5, J6}.
        """
        if self.isDebug: print(f"  Calculating inverse kinematics of robot at ({X},{Y},{Z},{Rx},{Ry},{Rz})")
        return self.Send_command(f"InverseKin({X},{Y},{Z},{Rx},{Ry},{Rz},user={User},tool={Tool},useJointNear={useJointNear},JointNear={JointNear})")

    def GetAngle(self):
        """
        Get the current joint angles of the robot posture.

        Args:
            None

        Returns:
            The joint angles {J1, J2, J3, J4, J5, J6}.
        """
        if self.isDebug: print("  Getting robot joint angles...")
        return self.Send_command("GetAngle()")

    def GetPose(self, User=0, Tool=0):
        """
        Get the cartesian coordinates of the current pose of the robot.

        Args:
            User (string): User coordinate system index. Default (0) is the global user coordinate system.
            Tool (string): Tool coordinate system index. Default (0) is the global tool coordinate system.

        Returns:
            The cartesian coordinate points of the current pose {X,Y,Z,Rx,Ry,Rz}.
        """
        if self.isDebug: print("  Getting robot pose...")
        return self.Send_command("GetPose(user={User},tool={Tool})")

    def GetErrorID(self):
        """
        Get the current error code of the robot.

        Args:
            None

        Returns:
            [[id,...,id], [id], [id], [id], [id], [id], [id]]. [id,...,id]: alarm information of the controller and algorithm. The last six indices are the alarm information of the six servos.
        """
        if self.isDebug: print("  Getting robot error ID...")
        return self.Send_command("GetErrorID()")

    def Create1DTray(self, Trayname, Count, Points):
        """
        Create a 1D tray for the robot. A set of points equidistantly spaced on a straight line.

        Args:
            Trayname (string): The name of the tray. Up to 32 bytes. No pure numbers or spaces.
            Count (string): The number of points in the tray in curled brackets. Example: {5}
            Points (string): Two endpoints P1 and P2. Format for each point: pose={x,y,z,rx,ry,rz}

        Returns:
            The response from the robot.
        """
        if self.isDebug: print(f"  Creating tray {Trayname} with {Count} points")
        return self.Send_command(f"CreateTray({Trayname},{Count},{Points})")

    def Create2DTray(self, Trayname, Count, Points):
        """
        Create a 2D tray for the robot. A set of points distributed in an array on a plane.

        Args:
            Trayname (string): The name of the tray. Up to 32 bytes. No pure numbers or spaces.
            Count (string): {row,col} in curled brackets. Row: number of rows (P1-P2), Col: number of columns (P3-P4). Example: {4,5}
            Points (string): Four points P1, P2, P3 and P4. Format for each point: pose={x,y,z,rx,ry,rz}

        Returns:
            The response from the robot.
        """
        if self.isDebug: print(f"  Creating tray {Trayname} with {Count} points")
        return self.Send_command(f"CreateTray({Trayname},{Count},{Points})")

    def Create3DTray(self, Trayname, Count, Points):
        """
        Create a 3D tray for the robot. A set of points distributed three-dimensionally in space and can beconsidered as multiple 2D trays arranged vertically.

        Args:
            Trayname (string): The name of the tray. Up to 32 bytes. No pure numbers or spaces.
            Count (string): {row,col,layer} in curled brackets. Row: number of rows (P1-P2), Col: number of columns (P3-P4), Layer: number of layers (P1-P5). Example: {4,5,6}
            Points (string): Eight points P1, P2, P3, P4, P5, P6, P7 and P8. Format for each point: pose={x,y,z,rx,ry,rz}

        Returns:
            The response from the robot.
        """
        if self.isDebug: print(f"  Creating tray {Trayname} with {Count} points")
        return self.Send_command(f"CreateTray({Trayname},{Count},{Points})")

    def GetTrayPoint(self, Trayname, index):
        """
        Get the specified point coordinates of the specified tray. The point number is related to the order of points passed in when creating the tray (see TCP protocol for details).

        Args:
            Trayname (string): The name of the tray. Up to 32 bytes. No pure numbers or spaces.
            index (int): The index of the point in the tray.

        Returns:
            The point coordinates and result {isErr,x,y,z,rx,ry,rz}. isErr: 0: Success, -1: Failure.
        """
        if self.isDebug: print(f"  Getting point {index} of tray {Trayname}")
        return self.Send_command(f"GetTrayPoint({Trayname},{index})")






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
    dobot.MoveJ(180, 0, -50, -20, 90, 0)
    dobot.MoveJ(180, 0, -50, 50, 90, 0)
    dobot.MoveJ(270, 0, 50, -50, 0, 0)
    dobot.MoveJ(270, 30, -50, 50, 0, -30)
    dobot.MoveJ(270, 0, 50, -50, 0, 0)
    dobot.MoveJ(270, 30, -50, 50, 0, -30)
    dobot.MoveJ(270, 0, 0, 0, 0, 0)
