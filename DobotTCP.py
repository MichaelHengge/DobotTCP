import socket
import struct
import time

from multipledispatch import dispatch

class Dobot:
    def __init__(self, ip='192.168.5.1', port=29999):
        self.ip = ip
        self.port = port
        self.connection = None
        self.isEnabled = False
        self.isDebug = True

    # Error Codes:
    error_codes = {
        0: "No error: The command has been delivered successfully.",
        -1: "Fail to execute: The command has been received but failed to be executed.",
        -2: "In alarm status: The robot cannot execute commands in the alarm status. Clear the alarm and redeliver the command.",
        -3: "In emergency stop status: The robot cannot execute commands in the emergency stop status. Release the emergency stop switch, clear the alarm, and redeliver the command.",
        -4: "In power-off status: The robot cannot execute commands in the power-off status. Power the robot on.",
        -5: "In script running/pause status: The robot cannot execute some commands when it is in script running/pause status. Stop the script first.",
        -10000: "Command error: The command does not exist.",
        -20000: "Parameter number error: The number of parameters in the command is incorrect.",
        -30001: "The type of the first parameter is incorrect: The parameter type is not valid.",
        -30002: "The type of the second parameter is incorrect: The parameter type is not valid.",
        -40001: "The range of the first parameter is incorrect: Ensure the parameter value falls within the valid range.",
        -40002: "The range of the second parameter is incorrect: Ensure the parameter value falls within the valid range.",
        -50001: "The type of the first optional parameter is incorrect: Optional parameter type mismatch.",
        -50002: "The type of the second optional parameter is incorrect: Optional parameter type mismatch.",
        -60001: "The range of the first optional parameter is incorrect: Ensure the optional parameter value is within the valid range.",
        -60002: "The range of the second optional parameter is incorrect: Ensure the optional parameter value is within the valid range."
    }

    # Robot Modes:
    robot_modes = {
    1: "ROBOT_MODE_INIT: Initialized status",
    2: "ROBOT_MODE_BRAKE_OPEN: Brake switched on",
    3: "ROBOT_MODE_POWER_STATUS: Power-off status",
    4: "ROBOT_MODE_DISABLED: Disabled (no brake switched on)",
    5: "ROBOT_MODE_ENABLE: Enabled and idle",
    6: "ROBOT_MODE_BACKDRIVE: Drag mode",
    7: "ROBOT_MODE_RUNNING: Running status (project, TCP queue motion, etc.)",
    8: "ROBOT_MODE_SINGLE_MOVE: Single motion status (jog, RunTo, etc.)",
    9: "ROBOT_MODE_ERROR: There are uncleared alarms. This status has the highest priority. It returns 9 when there is an alarm, regardless of the status of the robot arm",
    10: "ROBOT_MODE_PAUSE: Project pause status",
    11: "ROBOT_MODE_COLLISION: Collision detection trigger status"
}

    # Control Commands:

    def PowerON(self):
        """
        Power on the Dobot Magician E6 robot. This seems to do nothing for the Magician E6.

        Returns:
            The response from the robot.
        
        Example:
            PowerON()
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

        Example:
            EnableRobot()
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

        Example:
            EnableRobot(0.5)
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

        Example:
            EnableRobot(0.5, 0, 0, 0)
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

        Example:
            EnableRobot(0.5, 0, 0, 0, 1)
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

        Example:
            DisableRobot()
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

        Example:
            ClearError()
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

        Example:
            RunScript("123")
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

        Example:
            Stop()
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

        Example:
            Pause()
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

        Example:
            Continue()
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

        Example:
            EmergencyStop(1)
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

        Example:
            BrakeControl(1, 1)
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

        Example:
            StartDrag()
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

        Example:
            StopDrag()
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

        Example:
            SpeedFactor(50)
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

        Example:
            User(1)
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

        Example:
            SetUser(1, "{10,10,10,0,0,0}")
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

        Example:
            CalcUser(1, 0, "{10,10,10,0,0,0}")
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

        Example:
            Tool(1)
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

        Example:
            SetTool(1, "{10,10,10,0,0,0}")
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

        Example:
            CalcTool(1, 0, "{10,10,10,0,0,0}")
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

        Example:
            SetPayload("Load1")
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

        Example:
            SetPayload(0.5)
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

        Example:
            SetPayload(0.5, 0, 0, 0)
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

        Example:
            AccJ(50)
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

        Example:
            AccL(50)
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

        Example:
            VelJ(50)
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

        Example:
            VelL(50)
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

        Example:
            CP(50)
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

        Example:
            SetCollisionLevel(3)
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

        Example:
            SetBackDistance(10)
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

        Example:
            SetPostCollisionMode(1)
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

        Example:
            DragSensitivity(1, 50)
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

        Example:
            EnableSafeSkin(1)
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

        Example:
            SetSafeSkin(3, 1)
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

        Example:
            SetSafeWallEnable(1, 1)
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

        Example:
            SetWorkZoneEnable(1, 1)
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

        Example:
            RobotMode()
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

        Example:
            PositiveKin(0,0,-90,0,90,0,user=1,tool=1)
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

        Example:
            InverseKin(473.000000,-141.000000,469.000000,-180.000000,0.000,-90.000)
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

        Example:
            GetAngle()
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

        Example:
            GetPose(user=1,tool=1)
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

        Example:
            GetErrorID()
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

        Example:
            CreateTray(t1, {5}, {pose = {x1,y1,z1,rx1,ry1,rz1},pose = {x2,y2,z2,rx2,ry2,rz2}})
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

        Example:
            CreateTray(t2, {4,5}, {P1,P2,P3,P4})
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

        Example:
            CreateTray(t2, {4,5,6}, {P1,P2,P3,P4,P5,P6,P7,P8})
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

        Example:
            GetTrayPoint(t1, 1)
        """
        if self.isDebug: print(f"  Getting point {index} of tray {Trayname}")
        return self.Send_command(f"GetTrayPoint({Trayname},{index})")


    # IO Commands:

    @dispatch(int, int)
    def DO(self, index:int, status:int) -> str:
        """
        Set the digital output of the robot.

        Args:
            index (int): Digital output index.
            status (int): Digital output status. 0: OFF, 1: ON.

        Returns:
            ResultID is the algorithm queue ID, which can be used to judge the execution sequence of commands.

        Example:
            DO(1, 1)
        """
        if self.isDebug: print(f"  Setting digital output pin {index} to {status}")
        return self.Send_command(f"DO({index},{status})")

    @dispatch(int, int, int)
    def DO(self, index:int, status:int, time:int):
        """
        Set the digital output of the robot (queue command).

        Args:
            index (int): Digital output index.
            status (int): Digital output status. 0: OFF, 1: ON.
            time (int): Continuous output time. If set the input will be inverted after the specified amount of time. Unit: ms. Range: 25~60000.

        Returns:
            ResultID is the algorithm queue ID, which can be used to judge the execution sequence of commands.

        Example:
            DO(1, 1, 1000)
        """
        if self.isDebug: print(f"  Setting digital output pin {index} to {status} for {time} ms")
        return self.Send_command(f"DO({index},{status},{time})")

    def DOInstant(self, index, status):
        """
        Set the digital output of the robot instantly.

        Args:
            index (int): Digital output index.
            status (int): Digital output status. 0: OFF, 1: ON.

        Returns:
            The response from the robot.

        Example:
            DOInstant(1, 1)
        """
        if self.isDebug: print(f"  Setting digital output pin {index} to {status} instantly")
        return self.Send_command(f"DOInstant({index},{status})")

    def GetDO(self, index):
        """
        Get the digital output status of the robot.

        Args:
            index (int): Digital output index.

        Returns:
            The digital output status. 0: OFF, 1: ON.

        Example:
            GetDO(1)
        """
        if self.isDebug: print(f"  Getting digital output pin {index}")
        return self.Send_command(f"GetDO({index})")

    def DOGroup(self, string):
        """
        Set the digital output of a group of outputs of the robot.

        Args:
            string (string): Digital output group status. Format: index1,status1,index2,status2,... Index: Digital output index, Status: Digital output status. 0: OFF, 1: ON.

        Returns:
            The response from the robot.

        Example:
            DOGroup("1,1,2,0,3,1")
        """
        if self.isDebug: print(f"  Setting digital output group to {string}")
        return self.Send_command(f"DOGroup({string})")

    def GetDOGroup(self, string):
        """
        Get the digital output status of a group of outputs of the robot.

        Args:
            string (string): Digital output group status. Format: index1,index2,... Index: Digital output index.

        Returns:
            The digital output status of the group. Format: {status1,status2,...}. Status: Digital output status. 0: OFF, 1: ON.

        Example:
            GetDOGroup("1,2,3")
        """
        if self.isDebug: print(f"  Getting digital output group {string}")
        return self.Send_command(f"GetDOGroup({string})")

    def ToolDO(self, index, status):
        """
        Set the digital output of the tool (queue command).

        Args:
            index (int): Tool DO index.
            status (int): Tool DO status. 1: ON, 0: OFF.

        Returns:
            ResultID is the algorithm queue ID, which can be used to judge the execution sequence of commands.

        Example:
            ToolDO(1, 1)
        """
        if self.isDebug: print(f"  Setting tool digital output pin {index} to {status}")
        return self.Send_command(f"ToolDO({index},{status})")

    def ToolDOInstant(self, index, status):
        """
        Set the digital output of the tool instantly.

        Args:
            index (int): Tool DO index.
            status (int): Tool DO status. 1: ON, 0: OFF.

        Returns:
            The response from the robot.

        Example:
            ToolDOInstant(1, 1)
        """
        if self.isDebug: print(f"  Setting tool digital output pin {index} to {status} instantly")
        return self.Send_command(f"ToolDOInstant({index},{status})")

    def GetToolDO(self, index):
        """
        Get the digital output status of the tool.

        Args:
            index (int): Tool DO index.

        Returns:
            The digital output status. 0: OFF, 1: ON.

        Example:
            GetToolDO(1)
        """
        if self.isDebug: print(f"  Getting tool digital output pin {index}")
        return self.Send_command(f"GetToolDO({index})")

    def AO(self, index, value):
        """
        Set the analog output of the robot (queue command).

        Args:
            index (int): Analog output index.
            value (int): Analog output value. Voltage range: 0~10, Unit: V; Current range: 4~20, Unit: mA

        Returns:
            The response from the robot.

        Example:
            AO(1, 5)
        """
        if self.isDebug: print(f"  Setting analog output pin {index} to {value}")
        return self.Send_command(f"AO({index},{value})")

    def AOInstant(self, index, value):
        """
        Set the analog output of the robot instantly.

        Args:
            index (int): Analog output index.
            value (int): Analog output value. Voltage range: 0~10, Unit: V; Current range: 4~20, Unit: mA

        Returns:
            The response from the robot.

        Example:
            AOInstant(1, 5)
        """
        if self.isDebug: print(f"  Setting analog output pin {index} to {value} instantly")
        return self.Send_command(f"AOInstant({index},{value})")

    def GetAO(self, index):
        """
        Get the analog output status of the robot.

        Args:
            index (int): Analog output index.

        Returns:
            The analog output value.

        Example:
            GetAO(1)
        """
        if self.isDebug: print(f"  Getting analog output pin {index}")
        return self.Send_command(f"GetAO({index})")

    def DI(self, index):
        """
        Get the digital input status of the robot.

        Args:
            index (int): Digital input index.

        Returns:
            The digital input status. 0: no signal, 1: signal.

        Example:
            DI(1)
        """
        if self.isDebug: print(f"  Getting digital input pin {index}")
        return self.Send_command(f"DI({index})")

    def DIGroup(self, string):
        """
        Get the digital input status of a group of inputs of the robot.

        Args:
            string (string): Digital input group status. Format: index1,index2,... . Index: Digital input index.

        Returns:
            The digital input status of the group. Format: {status1,status2,...}. Status: Digital input status. 0: no signal, 1: signal.

        Example:
            DIGroup("1,2,3")
        """
        if self.isDebug: print(f"  Getting digital input group {string}")
        return self.Send_command(f"DIGroup({string})")

    def ToolDI(self, index):
        """
        Get the digital input status of the tool.

        Args:
            index (int): Tool DI index.

        Returns:
            The digital input status of the tool. 0: OFF, 1: ON.

        Example:
            ToolDI(1)
        """
        if self.isDebug: print(f"  Getting tool digital input pin {index}")
        return self.Send_command(f"ToolDI({index})")

    def AI(self, index):
        """
        Get the analog input status of the robot.

        Args:
            index (int): Analog input index.

        Returns:
            The analog input value.

        Example:
            AI(1)
        """
        if self.isDebug: print(f"  Getting analog input pin {index}")
        return self.Send_command(f"AI({index})")

    def ToolAI(self, index):
        """
        Get the analog input status of the tool.

        Args:
            index (int): Tool AI index.

        Returns:
            The analog input value of the tool.

        Example:
            ToolAI(1)
        """
        if self.isDebug: print(f"  Getting tool analog input pin {index}")
        return self.Send_command(f"ToolAI({index})")

    @dispatch(int, str, int)
    def SetTool485(self, baud, parity="N", stopbit=1):
        """
        Set the tool 485 communication parameters.

        Args:
            baud (int): Baud rate.
            parity (string): Parity bit. N: None, O: Odd, E: Even. Default is none.
            stopbit (int): Stop bit length. 1 or 2. Default is 1.

        Returns:
            The response from the robot.

        Example:
            SetTool485(115200, "N", 1)
        """
        if self.isDebug: print(f"  Setting tool 485 communication to {baud},{parity},{stopbit}")
        return self.Send_command(f"SetTool485({baud},{parity},{stopbit})")

    @dispatch(int, str, int, int)
    def SetTool485(self, baud, parity="N", stopbit=1, identify=1):
        """
        Set the tool 485 communication parameters.

        Args:
            baud (int): Baud rate.
            parity (string): Parity bit. N: None, O: Odd, E: Even. Default is none.
            stopbit (int): Stop bit length. 1 or 2. Default is 1.
            identify (int): If the robot has multiple aviation sockets, which one to use. 1: socket 1, 2: socket 2. Default is 1.

        Returns:
            The response from the robot.

        Example:
            SetTool485(115200, "N", 1, 1)
        """
        if self.isDebug: print(f"  Setting tool 485 communication to {baud},{parity},{stopbit} for socket {identify}")
        return self.Send_command(f"SetTool485({baud},{parity},{stopbit},{identify})")

    @dispatch(int)
    def SetToolPower(self, status):
        """
        Set the power status of the tool. The Magician E6 does not have a tool power feature.

        Args:
            status (int): Power status of the end tool. 0: OFF, 1: ON.

        Returns:
            The response from the robot.

        Example:
            SetToolPower(1)
        """
        if self.isDebug: print(f"  Setting tool power to {status}")
        return self.Send_command(f"SetToolPower({status})")

    @dispatch(int, int)
    def SetToolPower(self, status, identify):
        """
        Set the power status of the tool. The Magician E6 does not have a tool power feature.

        Args:
            status (int): Power status of the end tool. 0: OFF, 1: ON.
            identify (int): If the robot has multiple aviation sockets, which one to use. 1: socket 1, 2: socket 2.

        Returns:
            The response from the robot.

        Example:
            SetToolPower(1, 1)
        """
        if self.isDebug: print(f"  Setting tool power to {status} for socket {identify}")
        return self.Send_command(f"SetToolPower({status},{identify})")

    @dispatch(int, int)
    def SetToolMode(self, mode, type):
        """
        Set the tool multiplexing mode of the robot. The Magician E6 does not have a tool mode feature.

        Args:
            mode (int): Tool multiplexing mode. 1: 485 mode, 2: Analog input mode.
            type (int):  When mode is 1, the parameter is ineffective. When mode is 2, you can set the analog input mode. Check the TCP protocols for details.

        Returns:
            The response from the robot.

        Example:
            SetToolMode(1, 0)
        """
        if self.isDebug: print(f"  Setting tool mode to {mode}")
        return self.Send_command(f"SetToolMode({mode},{type})")

    @dispatch(int, int, int)
    def SetToolMode(self, mode, type, identify):
        """
        Set the tool multiplexing mode of the robot. The Magician E6 does not have a tool mode feature.

        Args:
            mode (int): Tool multiplexing mode. 1: 485 mode, 2: Analog input mode.
            type (int):  When mode is 1, the parameter is ineffective. When mode is 2, you can set the analog input mode. Check the TCP protocols for details.
            identify (int): If the robot has multiple aviation sockets, which one to use. 1: socket 1, 2: socket 2.

        Returns:
            The response from the robot.

        Example:
            SetToolMode(1, 0, 1)
        """
        if self.isDebug: print(f"  Setting tool mode to {mode} for socket {identify}")
        return self.Send_command(f"SetToolMode({mode},{type},{identify})")

    
    # Modbus Commands:

    @dispatch(str, int, int)
    def ModbusCreate(self, ip, port, slave_id):
        """
        Create a Modbus master station and establish slave connection (max 5 devices).

        Args:
            ip (string): IP address of the slave device.
            port (int): Port number of the slave device.
            slave_id (int): ID of the slave station.

        Returns:
            Index: master station index, used when other Modbus commands are called.

        Example:
            ModbusCreate("127.0.0.1",60000,1)
        """
        if self.isDebug: print(f"  Creating Modbus slave device at {ip}:{port} with ID {slave_id}")
        return self.Send_command(f"ModbusCreate({ip},{port},{slave_id})")

    @dispatch(str, int, int, int)
    def ModbusCreate(self, ip, port, slave_id, isRTU):
        """
        Create a Modbus master station and establish slave connection (max 5 devices).

        Args:
            ip (string): IP address of the slave device.
            port (int): Port number of the slave device.
            slave_id (int): ID of the slave station.
            isRTU (int): Communication mode. 0: modbusTCP, 1: modbusRTU.

        Returns:
            Index: master station index, used when other Modbus commands are called.

        Example:
            ModbusCreate(127.0.0.1,60000,1,1)
        """
        if self.isDebug: print(f"  Creating Modbus slave device at {ip}:{port} with ID {slave_id}. Mode: {isRTU}")
        return self.Send_command(f"ModbusCreate({ip},{port},{slave_id},{isRTU})")

    def ModbusRTUCreate(self, slave_id, baud, parity="E", data_bit=8, stop_bit=1):
        """
        Create a Modbus master station based on RS485 and establish slave connection (max 5 devices).

        Args:
            slave_id (int): ID of the slave station.
            baud (int): Baud rate.
            parity (string): Parity bit. N: None, O: Odd, E: Even. Default is even.
            data_bit (int): Data bit length. 8. Default is 8.
            stop_bit (int): Stop bit length. 1. Default is 1.

        Returns:
            Index: master station index, used when other Modbus commands are called.

        Example:
            ModbusRTUCreate(1, 115200)
        """
        if self.isDebug: print(f"  Creating Modbus slave device with ID {slave_id}. Mode: RTU, {baud},{parity},{data_bit},{stop_bit}")
        return self.Send_command(f"ModbusRTUCreate({slave_id},{baud},{parity},{data_bit},{stop_bit})")

    def ModbusClose(self, index):
        """
        Close the Modbus master station.

        Args:
            index (int): Master station index.

        Returns:
            The response from the robot.

        Example:
            ModbusClose(1)
        """
        if self.isDebug: print(f"  Closing Modbus master station {index}")
        return self.Send_command(f"ModbusClose({index})")

    def GetInBits(self, index, address, count):
        """
        Read the contact register from the modbus slave device.

        Args:
            index (int): Master station index.
            address (int): Start address of the contact register.
            count (int): Number of contact registers. Range: 1~16.

        Returns:
            Values of the contact register. Format: {value1,value2,...}.

        Example:
            GetInBits(0, 3000, 5)
        """
        if self.isDebug: print(f"  Getting input bits from Modbus slave device {index} at address {address} for {count} bits")
        return self.Send_command(f"GetInBits({index},{address},{count})")

    def GetInRegs(self, index, address, count, valType="U16"):
        """
        Read the input register from the modbus slave device with a specified data type.

        Args:
            index (int): Master station index.
            address (int): Start address of the input register.
            count (int): Number of values from input registers. Range: 1~4.
            valType (string): Data type. U16: 16-bit unsigned integer (two bytes, occupy one register), 32-bit unsigned integer (four bytes, occupy two registers) ,F32: 32-bit single-precision floating-point number (four bytes, occupy two registers) ,F64: 64-bit double-precision floating-point number (eight bytes, occupy four registers). Default is U16.

        Returns:
            Values of the input register. Format: {value1,value2,...}.

        Example:
            GetInRegs(0, 3000, 3, "U16")
        """
        if self.isDebug: print(f"  Getting input registers from Modbus slave device {index} at address {address} for {count} registers")
        return self.Send_command(f"GetInRegs({index},{address},{count},{valType})")

    def GetCoils(self, index, address, count):
        """
        Read the coil register from the modbus slave device.

        Args:
            index (int): Master station index.
            address (int): Start address of the coil register.
            count (int): Number of values from the coil registers. Range: 1~16.

        Returns:
            Values of the register coil. Format: {value1,value2,...}.

        Example:
            GetCoils(0, 3000, 5)
        """
        if self.isDebug: print(f"  Getting coils from Modbus slave device {index} at address {address} for {count} coils")
        return self.Send_command(f"GetCoils({index},{address},{count})")

    def SetCoils(self, index, address, count, valTab):
        """
        Write the coil register of the modbus slave device.

        Args:
            index (int): Master station index.
            address (int): Start address of the coil register.
            count (int): Number of values from coil register. Range: 1~16.
            valTab (string): Values to write. Format: {value1,value2,...}.

        Returns:
            The response from the robot.

        Example:
            SetCoils(0, 3000, 5, {1,0,1,0,1})
        """
        if self.isDebug: print(f"  Setting coils of Modbus slave device {index} at address {address} to {valTab}")
        return self.Send_command(f"SetCoils({index},{address},{valTab})")

    def GetHoldRegs(self, index, address, count, valType="U16"):
        """
        Read the holding register from the modbus slave device with a specified data type.

        Args:
            index (int): Master station index.
            address (int): Start address of the holding register.
            count (int): Number of values from holding registers. Range: 1~4.
            valType (string): Data type. U16: 16-bit unsigned integer (two bytes, occupy one register), 32-bit unsigned integer (four bytes, occupy two registers) ,F32: 32-bit single-precision floating-point number (four bytes, occupy two registers) ,F64: 64-bit double-precision floating-point number (eight bytes, occupy four registers). Default is U16.

        Returns:
            Values of the holding register. Format: {value1,value2,...}.

        Example:
            GetHoldRegs(0, 3095, 1, "U16")
        """
        if self.isDebug: print(f"  Getting holding registers from Modbus slave device {index} at address {address} for {count} registers")
        return self.Send_command(f"GetHoldRegs({index},{address},{count},{valType})")

    def setHoldRegs(self, index, address, count, valTab, valType="U16"):
        """
        Write the holding register of the modbus slave device with a specified data type.

        Args:
            index (int): Master station index.
            address (int): Start address of the holding register.
            count (int): Number of values from holding registers. Range: 1~4.
            valTab (string): Values to write. Format: {value1,value2,...}.
            valType (string): Data type. U16: 16-bit unsigned integer (two bytes, occupy one register), 32-bit unsigned integer (four bytes, occupy two registers) ,F32: 32-bit single-precision floating-point number (four bytes, occupy two registers) ,F64: 64-bit double-precision floating-point number (eight bytes, occupy four registers). Default is U16.

        Returns:
            The response from the robot.

        Example:
            SetHoldRegs(0,3095,2,{6000,300}, "U16")
        """
        if self.isDebug: print(f"  Setting holding registers of Modbus slave device {index} at address {address} to {valTab}")
        return self.Send_command(f"SetHoldRegs({index},{address},{valTab},{valType})")


    # Bus register Commands:

    def GetInputBool(self, adress):
        """
        Get the input boolean value of the bus register.

        Args:
            adress (int): Bus register address. Range: 0~63.

        Returns:
            The input boolean value. 0: OFF, 1: ON.

        Example:
            GetInputBool(1)
        """
        if self.isDebug: print(f"  Getting input boolean value from bus register {adress}")
        return self.Send_command(f"GetInputBool({adress})")

    def GetInputInt(self, adress):
        """
        Get the input integer value of the bus register.

        Args:
            adress (int): Bus register address. Range: 0~23.

        Returns:
            The input integer value.

        Example:
            GetInputInt(1)
        """
        if self.isDebug: print(f"  Getting input integer value from bus register {adress}")
        return self.Send_command(f"GetInputInt({adress})")

    def GetInputFloat(self, adress):
        """
        Get the input float value of the bus register.

        Args:
            adress (int): Bus register address. Range: 0~23.

        Returns:
            The input float value.

        Example:
            GetInputFloat(1)
        """
        if self.isDebug: print(f"  Getting input float value from bus register {adress}")
        return self.Send_command(f"GetInputFloat({adress})")

    def GetOutputBool(self, adress):
        """
        Get the output boolean value of the bus register.

        Args:
            adress (int): Bus register address. Range: 0~63.

        Returns:
            The output boolean value. 0: OFF, 1: ON.

        Example:
            GetOutputBool(1)
        """
        if self.isDebug: print(f"  Getting output boolean value from bus register {adress}")
        return self.Send_command(f"GetOutputBool({adress})")

    def GetOutputInt(self, adress):
        """
        Get the output integer value of the bus register.

        Args:
            adress (int): Bus register address. Range: 0~23.

        Returns:
            The output integer value.

        Example:
            GetOutputInt(1)
        """
        if self.isDebug: print(f"  Getting output integer value from bus register {adress}")
        return self.Send_command(f"GetOutputInt({adress})")

    def GetOutputFloat(self, adress):
        """
        Get the output float value of the bus register.

        Args:
            adress (int): Bus register address. Range: 0~23.

        Returns:
            The output float value.

        Example:
            GetOutputFloat(1)
        """
        if self.isDebug: print(f"  Getting output float value from bus register {adress}")
        return self.Send_command(f"GetOutputFloat({adress})")

    def SetOutputBool(self, adress, value):
        """
        Set the output boolean value of the bus register.

        Args:
            adress (int): Bus register address. Range: 0~63.
            value (int): Boolean value. 0: OFF, 1: ON.

        Returns:
            The response from the robot.

        Example:
            SetOutputBool(1, 1)
        """
        if self.isDebug: print(f"  Setting output boolean value of bus register {adress} to {value}")
        return self.Send_command(f"SetOutputBool({adress},{value})")

    def SetOutputInt(self, adress, value):
        """
        Set the output integer value of the bus register.

        Args:
            adress (int): Bus register address. Range: 0~23.
            value (int): Integer value.

        Returns:
            The response from the robot.

        Example:
            SetOutputInt(1, 100)
        """
        if self.isDebug: print(f"  Setting output integer value of bus register {adress} to {value}")
        return self.Send_command(f"SetOutputInt({adress},{value})")

    def SetOutputFloat(self, adress, value):
        """
        Set the output float value of the bus register.

        Args:
            adress (int): Bus register address. Range: 0~23.
            value (float): Float value.

        Returns:
            The response from the robot.

        Example:
            SetOutputFloat(1, 100.5)
        """
        if self.isDebug: print(f"  Setting output float value of bus register {adress} to {value}")
        return self.Send_command(f"SetOutputFloat({adress},{value})")


    # Movement Commands:

    @dispatch(str)
    def MovJ(self, P):
        """
        Move the robot to a specified point through joint motion.

        Args:
            P (string): Target point, supporting joint variables or posture variables Format: pose={x,y,z,a,b,c} or joint={j1,j2,j3,j4,j5,j6}

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            MovJ("pose={200,200,200,0,0,0}")
        """
        if self.isDebug: print(f"  Joint move robot to {P}")
        return self.Send_command(f"MovJ({P})")
    
    @dispatch(str, str)
    def MovJ(self, P, parameters):
        """
        Move the robot to a specified point through joint motion.

        Args:
            P (string): Target point, supporting joint variables or posture variables Format: pose={x,y,z,a,b,c} or joint={j1,j2,j3,j4,j5,j6}
            parameters (string): Additional parameters. Format: user={user},tool={tool},a={a},v={v},cp={cp}

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            MovJ("pose={200,200,200,0,0,0}", "user=0,tool=0,a=50,v=100,cp=50")
        """
        if self.isDebug: print(f"  Joint move robot to {P} with parameters {parameters}")
        return self.Send_command(f"MovJ({P},{parameters})")

    @dispatch(str, int, int, int, int, int)
    def MovJ(self, P, user, tool, a, v, cp):
        """
        Move the robot to a specified point through joint motion.

        Args:
            P (string): Target point, supporting joint variables or posture variables Format: pose={x,y,z,a,b,c} or joint={j1,j2,j3,j4,j5,j6}
            user (int): User coordinate system index. (0) is the global user coordinate system.
            tool (int): Tool coordinate system index. (0) is the global tool coordinate system.
            a (int): Acceleration rate. Range: 0~100.
            v (int): Velocity rate. Range: 0~1000.
            cp (int): Continuous path rate. Range: 0~100.

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            MovJ("pose={200,200,200,0,0,0}", 0, 0, 50, 100, 50)
        """
        if self.isDebug: print(f"  Joint move robot to {P} with user {user}, tool {tool}, acceleration {a}, speed {v}, continuos path {cp}")
        return self.Send_command(f"MovJ({P},user={user},tool={tool},a={a},v={v},cp={cp})")

    @dispatch(str)
    def MovL(self, P):
        """
        Move the robot to a specified point through linear motion.

        Args:
            P (string): Target point, supporting joint variables or posture variables Format: pose={x,y,z,a,b,c} or joint={j1,j2,j3,j4,j5,j6}

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            MovL("pose={200,200,200,0,0,0}")
        """
        if self.isDebug: print(f"  Linear move robot to {P}")
        return self.Send_command(f"MovL({P})")

    @dispatch(str, str)
    def MovL(self, P, parameters):
        """
        Move the robot to a specified point through linear motion.

        Args:
            P (string): Target point, supporting joint variables or posture variables Format: pose={x,y,z,a,b,c} or joint={j1,j2,j3,j4,j5,j6}
            parameters (string): Additional parameters. Format: user={user},tool={tool},a={a},v={v},cp={cp|r}

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            MovL("pose={200,200,200,0,0,0}", "user=0,tool=0,a=50,v=100,cp=50")
        """
        if self.isDebug: print(f"  Linear move robot to {P} with parameters {parameters}")
        return self.Send_command(f"MovL({P},{parameters})")
    
    @dispatch(str, int, int, int, int, int, int, int)
    def MovL(self, P, user, tool, a, v, speed, cp, r):
        """
        Move the robot to a specified point through linear motion.

        Args:
            P (string): Target point, supporting joint variables or posture variables Format: pose={x,y,z,a,b,c} or joint={j1,j2,j3,j4,j5,j6}
            user (int): User coordinate system index. (0) is the global user coordinate system.
            tool (int): Tool coordinate system index. (0) is the global tool coordinate system.
            a (int): Acceleration rate. Range: 0~100.
            v (int): Velocity rate. Range: 0~1000.
            speed (int): Target speed. Incompatible with v. Speed takes precedence if both are given. Unit: mm/s. Range: 1~maxSpeed.
            cp (int): Continuous path rate. Range: 0~100.
            r (int): Continuous path radius. Incompatible with cp. R takes precedence if both are given. Unit: mm. Range: 0~100.

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            MovL("pose={200,200,200,0,0,0}", 0, 0, 50, 100, 50, 0, 0)
        """
        if self.isDebug: print(f"  Linear move robot to {P} with user {user}, tool {tool}, acceleration {a}, v {v}, speed {speed}, continuos path {cp}, radius {r}")
        return self.Send_command(f"MovL({P},user={user},tool={tool},a={a},v={v},speed={speed},cp={cp},r={r})")

    @dispatch(str, str)
    def MovLIO(self, P, IO):
        """
        Move the robot to a specified point through linear motion setting status of the digital output.

        Args:
            P (string): Target point, supporting joint variables or posture variables Format: pose={x,y,z,a,b,c} or joint={j1,j2,j3,j4,j5,j6}
            IO (string): IO control. See the TCP protocols for details.

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            MovLIO("pose={-500,100,200,150,0,90}","{0, 30, 2, 1}")
        """
        if self.isDebug: print(f"  Linear move robot to {P} with IO control {IO}")
        return self.Send_command(f"MovL({P},{IO})")

    @dispatch(str, str, int, int, int, int, int, int, int)
    def MovLIO(self, P, IO, user, tool, a, v, speed, cp, r):
        """
        Move the robot to a specified point through linear motion setting status of the digital output.

        Args:
            P (string): Target point, supporting joint variables or posture variables Format: pose={x,y,z,a,b,c} or joint={j1,j2,j3,j4,j5,j6}
            IO (string): IO control. See the TCP protocols for details.
            user (int): User coordinate system index. (0) is the global user coordinate system.
            tool (int): Tool coordinate system index. (0) is the global tool coordinate system.
            a (int): Acceleration rate. Range: 0~100.
            v (int): Velocity rate. Range: 0~1000.
            speed (int): Target speed. Incompatible with v. Speed takes precedence if both are given. Unit: mm/s. Range: 1~maxSpeed.
            cp (int): Continuous path rate. Range: 0~100.
            r (int): Continuous path radius. Incompatible with cp. R takes precedence if both are given. Unit: mm. Range: 0~100.

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            MovLIO("pose={-500,100,200,150,0,90}","{0, 30, 2, 1}", 0, 0, 50, 100, 50, 0, 0)
        """
        if self.isDebug: print(f"  Linear move robot to {P} with IO control {IO}, user {user}, tool {tool}, acceleration {a}, v {v}, speed {speed}, continuos path {cp}, radius {r}")
        return self.Send_command(f"MovL({P},{IO},user={user},tool={tool},a={a},v={v},speed={speed},cp={cp},r={r})")

    @dispatch(str, str)
    def MovJIO(self, P, IO):
        """
        Move the robot to a specified point through joint motion setting status of the digital output.

        Args:
            P (string): Target point, supporting joint variables or posture variables Format: pose={x,y,z,a,b,c} or joint={j1,j2,j3,j4,j5,j6}
            IO (string): IO control. See the TCP protocols for details.

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            MovJIO("pose={-500,100,200,150,0,90}","{0, 30, 2, 1}")
        """
        if self.isDebug: print(f"  Joint move robot to {P} with IO control {IO}")
        return self.Send_command(f"MovJ({P},{IO})")
    
    @dispatch(str, str, int, int, int, int, int, int)
    def MovJIO(self, P, IO, user, tool, a, v, cp, r):
        """
        Move the robot to a specified point through joint motion setting status of the digital output.

        Args:
            P (string): Target point, supporting joint variables or posture variables Format: pose={x,y,z,a,b,c} or joint={j1,j2,j3,j4,j5,j6}
            IO (string): IO control. See the TCP protocols for details.
            user (int): User coordinate system index. (0) is the global user coordinate system.
            tool (int): Tool coordinate system index. (0) is the global tool coordinate system.
            a (int): Acceleration rate. Range: 0~100.
            v (int): Velocity rate. Range: 0~1000.
            cp (int): Continuous path rate. Range: 0~100.
            r (int): Continuous path radius. Incompatible with cp. R takes precedence if both are given. Unit: mm. Range: 0~100.

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            MovJIO("pose={-500,100,200,150,0,90}","{0, 30, 2, 1}", 0, 0, 50, 100, 50, 0)
        """
        if self.isDebug: print(f"  Joint move robot to {P} with IO control {IO}, user {user}, tool {tool}, acceleration {a}, v {v}, continuos path {cp}, radius {r}")
        return self.Send_command(f"MovJ({P},{IO},user={user},tool={tool},a={a},v={v},cp={cp},r={r})")

    @dispatch(str, str)
    def Arc(self, P1, P2):
        """
        Move the robot to a specified point through arc motion.

        Args:
            P1 (string): Intermediate point, supporting joint variables or posture variables Format: pose={x,y,z,a,b,c} or joint={j1,j2,j3,j4,j5,j6}
            P2 (string): End point, supporting joint variables or posture variables Format: pose={x,y,z,a,b,c} or joint={j1,j2,j3,j4,j5,j6}

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            Arc("pose={200,200,200,0,0,0}","pose={300,300,300,0,0,0}")
        """
        if self.isDebug: print(f"  Moving robot from {P1} to {P2} through arc motion")
        return self.Send_command(f"Arc({P1},{P2})")

    @dispatch(str, str, str)
    def Arc(self, P1, P2, parameters):
        """
        Move the robot to a specified point through arc motion.

        Args:
            P1 (string): Intermediate point, supporting joint variables or posture variables Format: pose={x,y,z,a,b,c} or joint={j1,j2,j3,j4,j5,j6}
            P2 (string): End point, supporting joint variables or posture variables Format: pose={x,y,z,a,b,c} or joint={j1,j2,j3,j4,j5,j6}
            parameters (string): Additional parameters. Format: user={user},tool={tool},a={a},v={v},speed={speed},cp={cp|r}

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            Arc("pose={200,200,200,0,0,0}","pose={300,300,300,0,0,0}","user=0,tool=0,a=50,v=100,speed=100,cp=50")
        """
        if self.isDebug: print(f"  Moving robot from {P1} to {P2} through arc motion with parameters {parameters}")
        return self.Send_command(f"Arc({P1},{P2},{parameters})")

    @dispatch(str, str, int, int, int, int, int, int, int)
    def Arc(self, P1, P2, user, tool, a, v, speed, cp, r):
        """
        Move the robot to a specified point through arc motion.

        Args:
            P1 (string): Intermediate point, supporting joint variables or posture variables Format: pose={x,y,z,a,b,c} or joint={j1,j2,j3,j4,j5,j6}
            P2 (string): End point, supporting joint variables or posture variables Format: pose={x,y,z,a,b,c} or joint={j1,j2,j3,j4,j5,j6}
            user (int): User coordinate system index. (0) is the global user coordinate system.
            tool (int): Tool coordinate system index. (0) is the global tool coordinate system.
            a (int): Acceleration rate. Range: 0~100.
            v (int): Velocity rate. Range: 0~1000.
            speed (int): Target speed. Incompatible with v. Speed takes precedence if both are given. Unit: mm/s. Range: 1~maxSpeed.
            cp (int): Continuous path rate. Range: 0~100.
            r (int): Continuous path radius. Incompatible with cp. R takes precedence if both are given. Unit: mm. Range: 0~100.

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            Arc("pose={200,200,200,0,0,0}","pose={300,300,300,0,0,0}", 0, 0, 50, 100, 100, 50, 0)
        """
        if self.isDebug: print(f"  Moving robot from {P1} to {P2} through arc motion with user {user}, tool {tool}, acceleration {a}, v {v}, speed {speed}, continuos path {cp}, radius {r}")
        return self.Send_command(f"Arc({P1},{P2},user={user},tool={tool},a={a},v={v},speed={speed},cp={cp},r={r})")

    @dispatch(str, str, int)
    def Circle(self, P1, P2, count):
        """
        Move the robot to a specified point through circular motion.

        Args:
            P1 (string): Intermediate point, supporting joint variables or posture variables Format: pose={x,y,z,a,b,c} or joint={j1,j2,j3,j4,j5,j6}
            P2 (string): End point, supporting joint variables or posture variables Format: pose={x,y,z,a,b,c} or joint={j1,j2,j3,j4,j5,j6}
            count (int): Number of circular motion. Range: 1~999.

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            Circle("pose={200,200,200,0,0,0}","pose={300,300,300,0,0,0}",1)
        """
        if self.isDebug: print(f"  Moving robot from {P1} to {P2} through circular motion for {count} times")
        return self.Send_command(f"Circle({P1},{P2},{count})")
    
    @dispatch(str, str, int, str)
    def Circle(self, P1, P2, count, parameters):
        """
        Move the robot to a specified point through circular motion.

        Args:
            P1 (string): Intermediate point, supporting joint variables or posture variables Format: pose={x,y,z,a,b,c} or joint={j1,j2,j3,j4,j5,j6}
            P2 (string): End point, supporting joint variables or posture variables Format: pose={x,y,z,a,b,c} or joint={j1,j2,j3,j4,j5,j6}
            count (int): Number of circular motion. Range: 1~999.
            parameters (string): Additional parameters. Format: user={user},tool={tool},a={a},v={v},speed={speed},cp={cp|r}

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            Circle("pose={200,200,200,0,0,0}","pose={300,300,300,0,0,0}",1,"user=0,tool=0,a=50,v=100,speed=100,cp=50")
        """
        if self.isDebug: print(f"  Moving robot from {P1} to {P2} through circular motion with parameters {parameters} for {count} times")
        return self.Send_command(f"Circle({P1},{P2},{count},{parameters})")

    @dispatch(str, str, int, int, int, int, int, int, int, int)
    def Circle(self, P1, P2, count, user, tool, a, v, speed, cp, r):
        """
        Move the robot to a specified point through circular motion.

        Args:
            P1 (string): Intermediate point, supporting joint variables or posture variables Format: pose={x,y,z,a,b,c} or joint={j1,j2,j3,j4,j5,j6}
            P2 (string): End point, supporting joint variables or posture variables Format: pose={x,y,z,a,b,c} or joint={j1,j2,j3,j4,j5,j6}
            count (int): Number of circular motion. Range: 1~999.
            user (int): User coordinate system index. (0) is the global user coordinate system.
            tool (int): Tool coordinate system index. (0) is the global tool coordinate system.
            a (int): Acceleration rate. Range: 0~100.
            v (int): Velocity rate. Range: 0~1000.
            speed (int): Target speed. Incompatible with v. Speed takes precedence if both are given. Unit: mm/s. Range: 1~maxSpeed.
            cp (int): Continuous path rate. Range: 0~100.
            r (int): Continuous path radius. Incompatible with cp. R takes precedence if both are given. Unit: mm. Range: 0~100.

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.
        """
        if self.isDebug: print(f"  Moving robot from {P1} to {P2} through circular motion with user {user}, tool {tool}, acceleration {a}, v {v}, speed {speed}, continuos path {cp}, radius {r} for {count} times")
        return self.Send_command(f"Circle({P1},{P2},{count},user={user},tool={tool},a={a},v={v},speed={speed},cp={cp},r={r})")

    def ServoJ(self, Joint, t=0.1, aheadtime=50, gain=500):
        """
        The dynamic following command based on joint space.

        Args:
            Joint (string): Target point joint varaibles. Format: {j1,j2,j3,j4,j5,j6}
            t (int): Running time of the point. Unit: s. Range: 0.02~3600.0. Default is 0.1.
            aheadtime (int): Advanced time, similar to the D in PID control. Range: 20.0~100.0. default is 50.
            gain (int): Proportional gain of the target position, similar to the P in PID control. Range: 200.0~1000.0. Default is 500.

        Returns:
            Response from the robot.

        Example:
            ServoJ("{0,0,0,0,0,0}", 0.1, 50, 500)
        """
        if self.isDebug: print(f"  Moving robot to joint {Joint} with time {t}, ahead time {aheadtime}, gain {gain}")
        return self.Send_command(f"ServoJ({Joint},{t},{aheadtime},{gain})")

    def ServoP(self, Pose, t=0.1, aheadtime=50, gain=500):
        """
        The dynamic following command based on pose space.

        Args:
            Pose (string): Target point pose varaibles. Format: {x,y,z,a,b,c}
            t (int): Running time of the point. Unit: s. Range: 0.02~3600.0. Default is 0.1.
            aheadtime (int): Advanced time, similar to the D in PID control. Range: 20.0~100.0. default is 50.
            gain (int): Proportional gain of the target position, similar to the P in PID control. Range: 200.0~1000.0. Default is 500.

        Returns:
            Response from the robot.

        Example:
            ServoP("{200,200,200,0,0,0}", 0.1, 50, 500)
        """
        if self.isDebug: print(f"  Moving robot to pose {Pose} with time {t}, ahead time {aheadtime}, gain {gain}")
        return self.Send_command(f"ServoP({Pose},{t},{aheadtime},{gain})")

    def MoveJog(self, axisID, coordType=0, user=0, tool=0):
        """
        Jog the robot arm or stop it. After the command is delivered, the robot arm will continuously jog along the specified axis, and it will stop once MoveJog () is delivered. In addition, when the robot arm is jogging, the delivery of MoveJog (string) with any non-specified string will also stop the motion of the robot arm.

        Args:
            axisID (string): Axis ID (case sensitive). J1-6/X/Y/Z/Rx/Ry/Rz+: positive direction. J1-6/X/Y/Z/Rx/Ry/Rz-: negative direction.
            coordType (int): Specify the coordinate system of axis (effective only when axisID specifies the axis in Cartesian coordinate system). 0: joint, 1: user coordinate system, 2: tool coordinate system. Default is 0.
            user (int): User coordinate system index. (0) is the global user coordinate system. Default is 0.
            tool (int): Tool coordinate system index. (0) is the global tool coordinate system. Default is 0.

        Returns:
            Response from the robot.

        Example:
            MoveJog("X+",coordType=1,user=1,tool=1)
        """
        if self.isDebug: print(f"  Jogging robot on axis {axisID} with coordinate type {coordType}, user {user}, tool {tool}")
        return self.Send_command(f"MoveJog({axisID},{coordType},{user},{tool})")

    def GetStartPose(self, traceName):
        """
        Get the start point of the trajectory.

        Args:
            traceName (string): Trajectory file name (including suffix). The trajectory file is stored in /dobot/userdata/project/process/trajectory/

        Returns:
            Pointtype, refers to the type of point returned. 0: taught point, 1: joint variable, 2: posture variable. See the TCP protocols for details.

        Example:
            GetStartPose("test1.csv")
        """
        if self.isDebug: print(f"  Getting start pose of trace {traceName}")
        return self.Send_command(f"GetStartPose({traceName})")

    @dispatch(str)
    def StartPath(self, traceName):
        """
        Move according to the recorded points (including at least 4 points) in the specified trajectory file to play back the recorded trajectory.

        Args:
            traceName (string): Trajectory file name (including suffix). The trajectory file is stored in /dobot/userdata/project/process/trajectory/

        Returns:
            Response from the robot.

        Example:
            StartPath("test1.csv")
        """
        if self.isDebug: print(f"  Starting path {traceName}")
        return self.Send_command(f"StartPath({traceName})")

    @dispatch(str, int, float, int, int)
    def StartPath(self, traceName, isConst, multi, user, tool):
        """
        Move according to the recorded points (including at least 4 points) in the specified trajectory file to play back the recorded trajectory.

        Args:
            traceName (string): Trajectory file name (including suffix). The trajectory file is stored in /dobot/userdata/project/process/trajectory/
            isConst (int): Whether the trajectory is played at constant speed. 0: variable speed as recorded, 1: constant speed.
            multi (float): Playback speed multiplier. Valid only when isConst is 0. Range: 0.25~2. Default is 1
            user (int): User coordinate system index. If not specified use the system in the trajectory file.
            tool (int): Tool coordinate system index. If not specified use the system in the trajectory file.

        Returns:
            Response from the robot.

        Example:
            StartPath("test1.csv", 0, 1, 0, 0)
        """
        if self.isDebug: print(f"  Starting path {traceName} with constant speed {isConst}, repetitions {multi}, user {user}, tool {tool}")
        return self.Send_command(f"StartPath({traceName},{isConst},{multi},{user},{tool})")

    @dispatch(float, float, float, float, float, float)
    def RelMovJTool(self, offsetX, offsetY, offsetZ, offsetRx, offsetRy, offsetRz):
        """
        Perform relative motion along the tool coordinate system, and the end motion is joint motion.

        Args:
            offsetX (float): X-axis coordinates. Unit: mm
            offsetY (float): Y-axis coordinates. Unit: mm.
            offsetZ (float): Z-axis coordinates. Unit: mm.
            offsetRx (float): Rx-axis coordinates. Unit: degree.
            offsetRy (float): Ry-axis coordinates. Unit: degree.
            offsetRz (float): Rz-axis coordinates. Unit: degree.
            user (int): User coordinate system index. (0) is the global user coordinate system.
            tool (int): Tool coordinate system index. (0) is the global tool coordinate system.
            a (int): Acceleration rate. Range: 0~100.
            v (int): Velocity rate. Range: 0~100.
            cp (int): Continuous path rate. Range: 0~100.

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            RelMovJTool(10,10,10,0,0,0)
        """
        if self.isDebug: print(f"  Joint move robot to offset ({offsetX},{offsetY},{offsetZ},{offsetRx},{offsetRy},{offsetRz})")
        return self.Send_command(f"MelMovJTool({offsetX},{offsetY},{offsetZ},{offsetRx},{offsetRy},{offsetRz})")

    @dispatch(float, float, float, float, float, float, int, int, int, int, int)
    def RelMovJTool(self, offsetX, offsetY, offsetZ, offsetRx, offsetRy, offsetRz, user, tool, a, v, cp):
        """
        Perform relative motion along the tool coordinate system, and the end motion is joint motion.

        Args:
            offsetX (float): X-axis coordinates. Unit: mm
            offsetY (float): Y-axis coordinates. Unit: mm.
            offsetZ (float): Z-axis coordinates. Unit: mm.
            offsetRx (float): Rx-axis coordinates. Unit: degree.
            offsetRy (float): Ry-axis coordinates. Unit: degree.
            offsetRz (float): Rz-axis coordinates. Unit: degree.
            user (int): User coordinate system index. (0) is the global user coordinate system.
            tool (int): Tool coordinate system index. (0) is the global tool coordinate system.
            a (int): Acceleration rate. Range: 0~100.
            v (int): Velocity rate. Range: 0~100.
            cp (int): Continuous path rate. Range: 0~100.

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            RelMovJTool(10,10,10,0,0,0,0,0,50,100,50)
        """
        if self.isDebug: print(f"  Joint move robot to offset ({offsetX},{offsetY},{offsetZ},{offsetRx},{offsetRy},{offsetRz}) with user {user}, tool {tool}, acceleration {a}, v {v}, continuos path {cp}")
        return self.Send_command(f"MelMovJTool({offsetX},{offsetY},{offsetZ},{offsetRx},{offsetRy},{offsetRz},{user},{tool},{a},{v},{cp})")

    @dispatch(float, float, float, float, float, float)
    def RelMovLTool(self, offsetX, offsetY, offsetZ, offsetRx, offsetRy, offsetRz):
        """
        Perform relative motion along the tool coordinate system, and the end motion is linear motion.

        Args:
            offsetX (float): X-axis coordinates. Unit: mm
            offsetY (float): Y-axis coordinates. Unit: mm.
            offsetZ (float): Z-axis coordinates. Unit: mm.
            offsetRx (float): Rx-axis coordinates. Unit: degree.
            offsetRy (float): Ry-axis coordinates. Unit: degree.
            offsetRz (float): Rz-axis coordinates. Unit: degree.

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            RelMovLTool(10,10,10,0,0,0)
        """
        if self.isDebug: print(f"  Linear move robot to offset ({offsetX},{offsetY},{offsetZ},{offsetRx},{offsetRy},{offsetRz})")
        return self.Send_command(f"MelMovLTool({offsetX},{offsetY},{offsetZ},{offsetRx},{offsetRy},{offsetRz})")

    @dispatch(float, float, float, float, float, float, int, int, int, int, int, int, int)
    def RelMovLTool(self, offsetX, offsetY, offsetZ, offsetRx, offsetRy, offsetRz, user, tool, a, v, speed, cp, r):
        """
        Perform relative motion along the tool coordinate system, and the end motion is linear motion.

        Args:
            offsetX (float): X-axis coordinates. Unit: mm
            offsetY (float): Y-axis coordinates. Unit: mm.
            offsetZ (float): Z-axis coordinates. Unit: mm.
            offsetRx (float): Rx-axis coordinates. Unit: degree.
            offsetRy (float): Ry-axis coordinates. Unit: degree.
            offsetRz (float): Rz-axis coordinates. Unit: degree.
            user (int): User coordinate system index. (0) is the global user coordinate system.
            tool (int): Tool coordinate system index. (0) is the global tool coordinate system.
            a (int): Acceleration rate. Range: 0~100.
            v (int): Velocity rate. Range: 0~100.
            speed (int): Target speed. Incompatible with v. Speed takes precedence if both are given. Unit: mm/s. Range: 1~maxSpeed.
            cp (int): Continuous path rate. Range: 0~100.
            r (int): Continuous path radius. Incompatible with cp. R takes precedence if both are given. Unit: mm. Range: 0~100.

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            RelMovLTool(10,10,10,0,0,0,0,0,50,100,50,0,0)
        """
        if self.isDebug: print(f"  Linear move robot to offset ({offsetX},{offsetY},{offsetZ},{offsetRx},{offsetRy},{offsetRz}) with user {user}, tool {tool}, acceleration {a}, v {v}, speed {speed}, continuos path {cp}, radius {r}")
        return self.Send_command(f"MelMovLTool({offsetX},{offsetY},{offsetZ},{offsetRx},{offsetRy},{offsetRz},{user},{tool},{a},{v},{speed},{cp},{r})")

    @dispatch(float, float, float, float, float, float)
    def RelMovJUser(self, offsetX, offsetY, offsetZ, offsetRx, offsetRy, offsetRz):
        """
        Perform relative motion along the user coordinate system, and the end motion is joint motion.

        Args:
            offsetX (float): X-axis coordinates. Unit: mm
            offsetY (float): Y-axis coordinates. Unit: mm.
            offsetZ (float): Z-axis coordinates. Unit: mm.
            offsetRx (float): Rx-axis coordinates. Unit: degree.
            offsetRy (float): Ry-axis coordinates. Unit: degree.
            offsetRz (float): Rz-axis coordinates. Unit: degree.

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            RelMovJUser(10,10,10,0,0,0)
        """
        if self.isDebug: print(f"  Joint move robot to offset ({offsetX},{offsetY},{offsetZ},{offsetRx},{offsetRy},{offsetRz})")
        return self.Send_command(f"MelMovJUser({offsetX},{offsetY},{offsetZ},{offsetRx},{offsetRy},{offsetRz})")

    @dispatch(float, float, float, float, float, float, int, int, int, int, int)
    def RelMovJUser(self, offsetX, offsetY, offsetZ, offsetRx, offsetRy, offsetRz, user, tool, a, v, cp):
        """
        Perform relative motion along the user coordinate system, and the end motion is joint motion.

        Args:
            offsetX (float): X-axis coordinates. Unit: mm
            offsetY (float): Y-axis coordinates. Unit: mm.
            offsetZ (float): Z-axis coordinates. Unit: mm.
            offsetRx (float): Rx-axis coordinates. Unit: degree.
            offsetRy (float): Ry-axis coordinates. Unit: degree.
            offsetRz (float): Rz-axis coordinates. Unit: degree.
            user (int): User coordinate system index. (0) is the global user coordinate system.
            tool (int): Tool coordinate system index. (0) is the global tool coordinate system.
            a (int): Acceleration rate. Range: 0~100.
            v (int): Velocity rate. Range: 0~100.
            cp (int): Continuous path rate. Range: 0~100.

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            RelMovJUser(10,10,10,0,0,0,0,0,50,100,50)
        """
        if self.isDebug: print(f"  Joint move robot to offset ({offsetX},{offsetY},{offsetZ},{offsetRx},{offsetRy},{offsetRz}) with user {user}, tool {tool}, acceleration {a}, v {v}, continuos path {cp}")
        return self.Send_command(f"MelMovJUser({offsetX},{offsetY},{offsetZ},{offsetRx},{offsetRy},{offsetRz},{user},{tool},{a},{v},{cp})")

    @dispatch(float, float, float, float, float, float)
    def RelMovLUser(self, offsetX, offsetY, offsetZ, offsetRx, offsetRy, offsetRz):
        """
        Perform relative motion along the user coordinate system, and the end motion is linear motion.

        Args:
            offsetX (float): X-axis coordinates. Unit: mm
            offsetY (float): Y-axis coordinates. Unit: mm.
            offsetZ (float): Z-axis coordinates. Unit: mm.
            offsetRx (float): Rx-axis coordinates. Unit: degree.
            offsetRy (float): Ry-axis coordinates. Unit: degree.
            offsetRz (float): Rz-axis coordinates. Unit: degree.

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            RelMovLUser(10,10,10,0,0,0)
        """
        if self.isDebug: print(f"  Linear move robot to offset ({offsetX},{offsetY},{offsetZ},{offsetRx},{offsetRy},{offsetRz})")
        return self.Send_command(f"MelMovLUser({offsetX},{offsetY},{offsetZ},{offsetRx},{offsetRy},{offsetRz})")

    @dispatch(float, float, float, float, float, float, int, int, int, int, int, int, int)
    def RelMovLUser(self, offsetX, offsetY, offsetZ, offsetRx, offsetRy, offsetRz, user, tool, a, v, speed, cp, r):
        """
        Perform relative motion along the user coordinate system, and the end motion is linear motion.

        Args:
            offsetX (float): X-axis coordinates. Unit: mm
            offsetY (float): Y-axis coordinates. Unit: mm.
            offsetZ (float): Z-axis coordinates. Unit: mm.
            offsetRx (float): Rx-axis coordinates. Unit: degree.
            offsetRy (float): Ry-axis coordinates. Unit: degree.
            offsetRz (float): Rz-axis coordinates. Unit: degree.
            user (int): User coordinate system index. (0) is the global user coordinate system.
            tool (int): Tool coordinate system index. (0) is the global tool coordinate system.
            a (int): Acceleration rate. Range: 0~100.
            v (int): Velocity rate. Range: 0~100.
            speed (int): Target speed. Incompatible with v. Speed takes precedence if both are given. Unit: mm/s. Range: 1~maxSpeed.
            cp (int): Continuous path rate. Range: 0~100.
            r (int): Continuous path radius. Incompatible with cp. R takes precedence if both are given. Unit: mm. Range: 0~100.

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            RelMovLUser(10,10,10,0,0,0,0,0,50,100,50,0,0)
        """
        if self.isDebug: print(f"  Linear move robot to offset ({offsetX},{offsetY},{offsetZ},{offsetRx},{offsetRy},{offsetRz}) with user {user}, tool {tool}, acceleration {a}, v {v}, speed {speed}, continuos path {cp}, radius {r}")
        return self.Send_command(f"MelMovLUser({offsetX},{offsetY},{offsetZ},{offsetRx},{offsetRy},{offsetRz},{user},{tool},{a},{v},{speed},{cp},{r})")

    @dispatch(float, float, float, float, float, float)
    def RelJointMovJ(self, Offset1, Offset2, Offset3, Offset4, Offset5, Offset6):
        """
        Perform relative motion along the joint coordinate system of each axis, and the end motion mode is joint motion.

        Args:
            Offset1 (float): Joint 1 offset. Unit: degree.
            Offset2 (float): Joint 2 offset. Unit: degree.
            Offset3 (float): Joint 3 offset. Unit: degree.
            Offset4 (float): Joint 4 offset. Unit: degree.
            Offset5 (float): Joint 5 offset. Unit: degree.
            Offset6 (float): Joint 6 offset. Unit: degree.

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            RelJointMovJ(10,10,10,10,10,10)
        """
        if self.isDebug: print(f"  Joint move robot to offset ({Offset1},{Offset2},{Offset3},{Offset4},{Offset5},{Offset6})")
        return self.Send_command(f"MelJointMovJ({Offset1},{Offset2},{Offset3},{Offset4},{Offset5},{Offset6})")

    @dispatch(float, float, float, float, float, float, int, int, int)
    def RelJointMovJ(self, Offset1, Offset2, Offset3, Offset4, Offset5, Offset6, a, v, cp):
        """
        Perform relative motion along the joint coordinate system of each axis, and the end motion mode is joint motion.

        Args:
            Offset1 (float): Joint 1 offset. Unit: degree.
            Offset2 (float): Joint 2 offset. Unit: degree.
            Offset3 (float): Joint 3 offset. Unit: degree.
            Offset4 (float): Joint 4 offset. Unit: degree.
            Offset5 (float): Joint 5 offset. Unit: degree.
            Offset6 (float): Joint 6 offset. Unit: degree.
            a (int): Acceleration rate. Range: 0~100.
            v (int): Velocity rate. Range: 0~100.
            cp (int): Continuous path rate. Range: 0~100.

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            RelJointMovJ(10,10,10,10,10,10,50,100,50)
        """
        if self.isDebug: print(f"  Joint move robot to offset ({Offset1},{Offset2},{Offset3},{Offset4},{Offset5},{Offset6}) with acceleration {a}, v {v}, continuos path {cp}")
        return self.Send_command(f"MelJointMovJ({Offset1},{Offset2},{Offset3},{Offset4},{Offset5},{Offset6},{a},{v},{cp})")

    def GetCurrentCommandID(self):
        """
        Get the current command ID. It can be used to determine which command the robot is executing.

        Returns:
            ResultID, the algorithm queue ID of the current command.

        Example:
            GetCurrentCommandID()
        """
        if self.isDebug: print("  Getting current command ID")
        return self.Send_command("GetCurrentCommandID()")











    # Added Commands (no standard command from TCP protocol):

    def connect(self):
        """
        Connect to the Dobot Magician E6 robot.

        Args:
            None
        
        Returns:
            None
        
        Raises:
            Exception: If the connection fails.

        Example:
            connect()
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

    def disconnect(self):
        """
        Disconnect from the Dobot Magician E6 robot.

        Args:
            None

        Returns:
            None

        Example:
            disconnect()
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            if self.isDebug: print("  Disconnected from Dobot Magician E6")

    def send_command(self, command):
        """
        Send a command to the Dobot and receive a response.

        Args:
            command (string): The command to send to the robot.

        Returns:
            The response from the robot.

        Raises:
            Exception: If not connected to the Dobot Magician E6.
        
        Example:
            send_command("GetPose()")
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

    def setDebug(self, isDebug):
        """
        Set the debug mode for the Dobot Object

        Args
        isDebug (bool): Print Debug messages yes (True) or no  (False).

        Returns:
            None

        Example:
            setDebug(True)
        """
        self.isDebug = isDebug

    def MoveJJ(self,j1,j2,j3,j4,j5,j6):
        """
        Move the robot to a specified joint position using joint motion.

        Args:
            j1 (int): Joint 1 angle.
            j2 (int): Joint 2 angle.
            j3 (int): Joint 3 angle.
            j4 (int): Joint 4 angle.
            j5 (int): Joint 5 angle.
            j6 (int): Joint 6 angle.

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            MoveJJ(-90, 0, -140, -40, 0, 0)
        """
        if self.isDebug: print(f"  Joint move robot to joint ({j1},{j2},{j3},{j4},{j5},{j6})")
        move_command = f"MovJ(joint={{{j1},{j2},{j3},{j4},{j5},{j6}}})"
        return self.Send_command(move_command)

    def MoveJP(self,j1,j2,j3,j4,j5,j6):
        """
        Move the robot to a specified pose using joint motion.

        Args:
            j1 (int): Joint 1 angle.
            j2 (int): Joint 2 angle.
            j3 (int): Joint 3 angle.
            j4 (int): Joint 4 angle.
            j5 (int): Joint 5 angle.
            j6 (int): Joint 6 angle.

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            MoveJP(0, 0, 0, 0, 0, 0)
        """
        if self.isDebug: print(f"  Joint move robot to pose ({j1},{j2},{j3},{j4},{j5},{j6})")
        move_command = f"MovJ(pose={{{j1},{j2},{j3},{j4},{j5},{j6}}})"
        return self.Send_command(move_command)

    def MoveLJ(self,j1,j2,j3,j4,j5,j6):
        """
        Move the robot to a specified joint position using linear motion.

        Args:
            j1 (int): Joint 1 angle.
            j2 (int): Joint 2 angle.
            j3 (int): Joint 3 angle.
            j4 (int): Joint 4 angle.
            j5 (int): Joint 5 angle.
            j6 (int): Joint 6 angle.

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            MoveLJ(-90, 0, -140, -40, 0, 0)
        """
        if self.isDebug: print(f"  Joint move robot to joint({j1},{j2},{j3},{j4},{j5},{j6})")
        move_command = f"MovL(joint={{{j1},{j2},{j3},{j4},{j5},{j6}}})"
        return self.Send_command(move_command)

    def MoveLP(self,j1,j2,j3,j4,j5,j6):
        """
        Move the robot to a specified pose using linear motion.

        Args:
            j1 (int): Joint 1 angle.
            j2 (int): Joint 2 angle.
            j3 (int): Joint 3 angle.
            j4 (int): Joint 4 angle.
            j5 (int): Joint 5 angle.
            j6 (int): Joint 6 angle.

        Returns:
            ResultID is the algorithm queue ID which can be used to judge the sequence of command execution.

        Example:
            MoveLP(0, 0, 0, 0, 0, 0)
        """
        if self.isDebug: print(f"  Joint move robot to pose ({j1},{j2},{j3},{j4},{j5},{j6})")
        move_command = f"MovL(pose={{{j1},{j2},{j3},{j4},{j5},{j6}}})"
        return self.Send_command(move_command)

    def Home(self):
        """
        Move the robot to the home position through joint motion.

        Returns:
            The response from the robot.

        Example:
            Home()
        """
        if self.isDebug: print("  Moving robot to home position")
        return self.MoveJ(0, 0, 0, 0, 0, 0)

    def Pack(self):
        """
        Move the robot to the packing position through joint motion.

        Returns:
            The response from the robot.

        Example:
            Pack()
        """
        if self.isDebug: print("  Moving robot to packing position")
        return self.MoveJJ(-90, 0, -140, -40, 0, 0)
       
    def SetSucker(self, status):
        """
        Set the sucker status.

        Args:
            status (int): Sucker status. 1: ON, 0: OFF.
        
        Returns:
            The response from the robot.

        Example:
            SetSucker(1)
        """
        if self.isDebug: print(f"  Setting sucker to {status}")
        return self.ToolDO(1,status)
    
    def ParseError(self, errcode):
        """
        Parse the error code to a human readable error message.

        Args:
            errcode (int): Error code.

        Returns:
            The error message.

        Example:
            ParseError(1)
        """
        if self.isDebug: print(f"  Parsing error code {errcode}")
        return self.error_codes.get(errcode, "Unknown error code. Check the TCP protocol for further info.")

    def ParseRobotMode(self, mode):
        """
        Parse the robot mode to a human readable message.

        Args:
            mode (int): Robot mode.

        Returns:
            The robot mode message.

        Example:
            ParseRobotMode(1)
        """
        if self.isDebug: print(f"  Parsing robot mode {mode}")
        return self.robot_modes.get(mode, "Unknown robot mode. Check the TCP protocol for further info.")




# Class for the flexible gripper

class FlexGripper:
    """
    Class for the flexible gripper.
    """
    def __init__(self, robot:Dobot, DOvacuum:int=1, DOpressure:int=2):
        """
        Constructor for the flexible gripper.
        
        Args:
            robot (DobotTCP): The robot object.
            DOvacuum (int): Digital port for the vacuum. Default is 1.
            DOpressure (int): Digital port for the pressure. Default is 2.
        """
        self.robot = robot
        self.DOvacuum = DOvacuum
        self.DOpressure = DOpressure

    def open(self) -> str:
        """
        Open the flexible gripper

        Returns:
            The response from the robot.

        Example:
            open()
        """
        if self.robot.isDebug: print(f"  Opening flexible gripper\n    ", end="")
        self.robot.DO(self.DOvacuum,0)
        return self.robot.DO(self.DOpressure,1)  

    def close(self) -> str:
        """
        Closes the flexible gripper

        Returns:
            The response from the robot.

        Example:
            close()
        """
        if self.robot.isDebug: print(f"  Closing flexible gripper\n    ", end="")
        self.robot.DO(self.DOpressure,0)
        return self.robot.DO(self.DOvacuum,1) 
    
    def neutral(self) -> str:
        """
        Puts the flexible gripper in the neutral state.

        Returns:
            The response from the robot.

        Example:
            neutral()
        """
        if self.robot.isDebug: print(f"  Setting flexible gripper to neutral\n    ", end="")
        self.robot.DO(self.DOpressure,0)
        return self.robot.DO(self.DOvacuum,0)
    
    def setState(self, state:int, vacuum:int=1, pressure:int=2) -> str:
        """
        Set the status of the flexible gripper

        Args:
            state (int): State of the gripper. -1: Vacuum (closed), 0:Neutral, 1:Pressure (open)
            vacuum (int): Digital port for the vacuum. Default is 1.
            pressure (int): Digital port for the pressure. Default is 2.

        Returns:
            The response from the robot.

        Example:
            setState(1)
        """
        if self.robot.isDebug: print(f"  Setting flexible gripper to {state}\n    ", end="")
        match state:
            case -1:
                self.robot.DO(pressure,0)
                return self.robot.DO(vacuum,1)
            case 0:
                self.robot.DO(vacuum,0)
                return self.robot.DO(pressure,0)
            case 1:
                self.robot.DO(vacuum,1)
                return self.robot.DO(pressure,1)


# Class for the servo gripper

class ServoGripper:
    """
    Class for the servo gripper.
    """

    def __init__(self, robot:Dobot, DOin1:int=1, DOin2:int=2, DIout1:int=1, DIout2:int=2):
        """
        Constructor for the servo gripper.

        Args:
            robot (DobotTCP): The robot object.
            DOin1 (int): Digital input port 1. Default is 1.
            DOin2 (int): Digital input port 2. Default is 2.
            DIout1 (int): Digital output port 1. Default is 1.
            DIout2 (int): Digital output port 2. Default is 2.
        """

        self.robot = robot
        self.DOin1 = DOin1
        self.DOin2 = DOin2
        self.DIout1 = DIout1
        self.DIout2 = DIout2
    
    def setState(self, state) -> str:
        """
        Set the state of the servo gripper.

        Args:
            state (int): IO State group of the gripper. Range: 1-4.

        Returns:
            The response from the robot.

        Example:
            setState(1)
        """
        if self.robot.isDebug: print(f"  Setting servo gripper group to {state}\n    ", end="")
        match state:
            case 1:
                self.robot.DO(self.DOin1,0)
                if self.robot.isDebug: print("    ", end="")
                return self.robot.DO(self.DOin2,0)
            case 2:
                self.robot.DO(self.DOin1,1)
                if self.robot.isDebug: print("    ", end="")
                return self.robot.DO(self.DOin2,0)
            case 3:
                self.robot.DO(self.DOin1,0)
                if self.robot.isDebug: print("    ", end="")
                return self.robot.DO(self.DOin2,1)
            case 4:
                self.robot.DO(self.DOin1,1)
                if self.robot.isDebug: print("    ", end="")
                return self.robot.DO(self.DOin2,1)
            case _:
                return "    Invalid state group. Please choose a value between 1 and 4."
            
    def getState(self) -> str:
        """
        Get the state of the servo gripper.

        Returns:
            The state of the gripper.

        Example:
            getState()
        """
        if self.robot.isDebug: print(f"  Getting servo gripper state\n    ", end="")
        output1 = self.robot.GetDO(self.DIout1)
        output2 = self.robot.GetDO(self.DIout2)
        match (output1, output2):
            case (0,0):
                print("    Fingers are in motion")
                return "Fingers are in motion"
            case (1,0):
                print("    Fingers are at reference position, No object detected or object has been dropped")
                return "Fingers are at reference position, No object detected or object has been dropped"
            case (0,1):
                print("    Fingers have stopped due to an object detection")
                return "Fingers have stopped due to an object detection"
            case (1,1):
                print("    Fingers are holding an object")
                return "Unknown state"


# Class to receive feedback from the robot

class Feedback:
    """
    Class to receive feedback from the robot.
    """

    def __init__(self, robot:Dobot, port=30004):
        """
        Constructor for the feedback class.

        Args:
            robot (DobotTCP): The robot object.
            port (int): Port to receive feedback. Different ports have different feedback timings. See TCP protocol for details. Default is port 30004.
        """
        self.robot = robot
        self.port = port
        self.client = None
        self.data = {}

    def init(self):
        """
        Connect to the robot's feedback port.

        Returns:
            None

        Example:
            init()
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.robot.ip, self.port))

    def get(self):
        """
        Get feedback from the robot.

        Returns:
            None

        Example:
            get()
        """
        rawdata = self.client.recv(1440)
        self.data = self.parse_feedback(rawdata)

    def parse_feedback(self, data):
        """
        Parse the feedback data from the robot.
        
        Args:
            data (bytes): The feedback data from the robot.
            
        Returns:
            A dictionary with the feedback data.
        
        Example:
            parse_feedback(data)
        """
        feedback_dict = {}

        # Helper function to unpack data and assign it a key
        def unpack(offset, fmt, key):
            size = struct.calcsize(fmt)
            feedback_dict[key] = struct.unpack_from(fmt, data, offset)
            return offset + size

        # Parse fields based on their "Meaning" in the document
        offset = 0
        offset = unpack(offset, 'H', 'MessageSize')                        # Message size (2 bytes)
        offset += 6                                                        # Reserved (6 bytes)
        offset = unpack(offset, 'Q', 'DigitalInputs')                      # Digital inputs (8 bytes)
        offset = unpack(offset, 'Q', 'DigitalOutputs')                     # Digital outputs (8 bytes)
        offset = unpack(offset, 'Q', 'RobotMode')                          # Robot mode (8 bytes)
        offset = unpack(offset, 'Q', 'TimeStamp')                          # Timestamp in milliseconds (8 bytes)
        offset = unpack(offset, 'Q', 'RunTime')                            # Robot running time in milliseconds (8 bytes)
        offset = unpack(offset, 'Q', 'TestValue')                          # Memory test value (8 bytes)
        offset += 8                                                        # Reserved (8 bytes)
        offset = unpack(offset, 'd', 'SpeedScaling')                       # Speed scaling (8 bytes)
        offset += 16                                                       # Reserved (16 bytes)
        offset = unpack(offset, 'd', 'VRobot')                             # Robot voltage (8 bytes)
        offset = unpack(offset, 'd', 'IRobot')                             # Robot current (8 bytes)
        offset = unpack(offset, 'd', 'ProgramState')                       # Script running status (8 bytes)
        offset += 80                                                       # Reserved (80 bytes)

        # Explicitly parse joint-related fields
        offset = unpack(offset, '6d', 'Target Joint Position')             # Target joint positions (6 doubles, 48 bytes)
        offset = unpack(offset, '6d', 'Target Joint Velocity')             # Target joint velocities (6 doubles, 48 bytes)
        offset = unpack(offset, '6d', 'Target Joint Acceleration')         # Target joint accelerations (6 doubles, 48 bytes)
        offset = unpack(offset, '6d', 'Target Joint Current')              # Target joint currents (6 doubles, 48 bytes)
        offset = unpack(offset, '6d', 'Target Joint Torque')               # Target joint torques (6 doubles, 48 bytes)
        offset = unpack(offset, '6d', 'Actual Joint Position')             # Actual joint positions (6 doubles, 48 bytes)
        offset = unpack(offset, '6d', 'Actual Joint Velocity')             # Actual joint velocities (6 doubles, 48 bytes)
        offset = unpack(offset, '6d', 'Actual Joint Current')              # Actual joint currents (6 doubles, 48 bytes)
        offset = unpack(offset, '6d', 'TCP Actual Cartesian Coordinates')  # TCP Cartesian coordinates (6 doubles, 48 bytes)
        offset = unpack(offset, '6d', 'TCP Actual Speed')                  # TCP speed (6 doubles, 48 bytes)
        offset = unpack(offset, '6d', 'TCP Force Value')                   # TCP force values (6 doubles, 48 bytes)
        offset = unpack(offset, '6d', 'TCP Target Cartesian Coordinates')  # TCP target Cartesian coordinates (6 doubles, 48 bytes)
        offset = unpack(offset, '6d', 'TCP Target Speed')                  # TCP target speeds (6 doubles, 48 bytes)
        offset = unpack(offset, '6d', 'Joint Temperatures')                # Joint temperatures (6 doubles, 48 bytes)
        offset = unpack(offset, '6d', 'Joint Control Modes')               # Joint control modes (6 doubles, 48 bytes)
        offset = unpack(offset, '6d', 'Joint Voltage')                     # Joint voltages (6 doubles, 48 bytes)

        offset += 4                                                        # Reserved (4 bytes)
        offset = unpack(offset, 'B', 'User Coordinate System')             # User coordinate system (1 byte)
        offset = unpack(offset, 'B', 'Tool Coordinate System')             # Tool coordinate system (1 byte)
        offset = unpack(offset, 'B', 'Queue Running Flag')                 # Run queued command flag (1 byte)
        offset = unpack(offset, 'B', 'Queue Pause Flag')                   # Queue pause flag (1 byte)
        offset = unpack(offset, 'B', 'Joint Velocity Rate')                # Joint velocity rate (1 byte)
        offset = unpack(offset, 'B', 'Joint Acceleration Rate')            # Joint acceleration rate (1 byte)
        offset += 1                                                        # Reserved (1 byte)
        offset = unpack(offset, 'B', 'Cartesian Velocity Rate')            # Cartesian velocity rate (1 byte)
        offset = unpack(offset, 'B', 'Cartesian Pose Velocity Rate')       # Cartesian pose velocity rate (1 byte)
        offset = unpack(offset, 'B', 'Cartesian Acceleration Rate')        # Cartesian acceleration rate (1 byte)
        offset = unpack(offset, 'B', 'Cartesian Pose Acceleration Rate')   # Cartesian pose acceleration rate (1 byte)
        offset = unpack(offset, 'B', 'Brake Status')                       # Brake status (1 byte)
        offset = unpack(offset, 'B', 'Enable Status')                      # Enable status (1 byte)
        offset = unpack(offset, 'B', 'Drag Status')                        # Drag status (1 byte)
        offset = unpack(offset, 'B', 'Running Status')                     # Running status (1 byte)
        offset = unpack(offset, 'B', 'Alarm Status')                       # Alarm status (1 byte)
        offset = unpack(offset, 'B', 'Jogging Status')                     # Jogging status (1 byte)
        offset = unpack(offset, 'B', 'Robot Type')                         # Robot type (1 byte)
        offset = unpack(offset, 'B', 'Drag Signal')                        # Drag signal (1 byte)
        offset = unpack(offset, 'B', 'Enable Signal')                      # Enable signal (1 byte)
        offset = unpack(offset, 'B', 'Recording Signal')                   # Recording signal (1 byte)
        offset = unpack(offset, 'B', 'Playback Signal')                    # Playback signal (1 byte)
        offset = unpack(offset, 'B', 'Gripper Control Signal')             # Gripper control signal (1 byte)
        offset += 1                                                        # Reserved (1 byte)
        offset = unpack(offset, 'B', 'Collision State')                    # Collision state (1 byte)
        offset = unpack(offset, 'B', 'Forearm SafeSkin Approach Pause')    # Forearm pause state (1 byte)
        offset = unpack(offset, 'B', 'J4 SafeSkin Approach Pause')         # J4 pause state (1 byte)
        offset = unpack(offset, 'B', 'J5 SafeSkin Approach Pause')         # J5 pause state (1 byte)
        offset = unpack(offset, 'B', 'J6 SafeSkin Approach Pause')         # J6 pause state (1 byte)
        offset += 77                                                       # Reserved (77 bytes)
        offset = unpack(offset, 'd', 'Z-axis Jitter Displacement')         # Z-axis jitter displacement (8 bytes)
        offset = unpack(offset, 'Q', 'Current Command ID')                 # Current command ID (8 bytes)
        offset = unpack(offset, '6d', 'Actual Torque')                     # Actual torques (6 doubles, 48 bytes)
        offset = unpack(offset, 'd', 'Payload (kg)')                       # Payload in kg (8 bytes)
        offset = unpack(offset, 'd', 'Eccentric Distance X')               # Eccentric distance X (8 bytes)
        offset = unpack(offset, 'd', 'Eccentric Distance Y')               # Eccentric distance Y (8 bytes)
        offset = unpack(offset, 'd', 'Eccentric Distance Z')               # Eccentric distance Z (8 bytes)
        offset = unpack(offset, '6d', 'User Coordinates')                  # User coordinates (6 doubles, 48 bytes)
        offset = unpack(offset, '6d', 'Tool Coordinates')                  # Tool coordinates (6 doubles, 48 bytes)
        offset += 8                                                        # Reserved (8 bytes)
        offset = unpack(offset, '6d', 'Six-Axis Force')                    # Six-axis force values (6 doubles, 48 bytes)
        offset = unpack(offset, '4d', 'Target Quaternion')                 # Target quaternion (4 doubles, 32 bytes)
        offset = unpack(offset, '4d', 'Actual Quaternion')                 # Actual quaternion (4 doubles, 32 bytes)
        offset = unpack(offset, 'B', 'Manual/Automatic Mode')              # Manual/automatic mode (1 byte)
        offset += 24                                                       # Reserved (24 bytes)

        return feedback_dict