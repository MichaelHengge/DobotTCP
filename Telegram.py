import asyncio
import time
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from DobotTCP import Dobot

isConnected = False
hasSign = 0 # 0: No sign, 1: Hi sign, 2: Bye sign

# Function to read the API token and user IDs from the config file
def read_config(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            token = None
            admin_id = None
            user_ids = []
            notify_ids = []

            for line in lines:
                if line.startswith("token:"):
                    token = line.split(":", 1)[1].strip()
                elif line.startswith("admin:"):
                    value = line.split(":", 1)[1].strip()
                    admin_id = int(value) if value.isdigit() else None
                elif line.startswith("users:"):
                    user_ids = [
                        int(uid.strip()) for uid in line.split(":", 1)[1].strip().split(",") if uid.strip().isdigit()
                    ]
                elif line.startswith("notify:"):
                    notify_ids = [
                        int(uid.strip()) for uid in line.split(":", 1)[1].strip().split(",") if uid.strip().isdigit()
                    ]

            if not token:
                raise ValueError("Token not found in config file.")

            # Add the admin ID to the user_ids list if it's not already there
            if admin_id and admin_id not in user_ids:
                user_ids.append(admin_id)

            return token, admin_id, user_ids, notify_ids

    except FileNotFoundError:
        raise Exception(f"Config file '{file_path}' not found.")
    except Exception as e:
        raise Exception(f"Error reading config file: {e}")



# Function to write user IDs back to the config file
def write_config(file_path, token, admin_id, user_ids, notify_ids):
    try:
        with open(file_path, 'w') as file:
            file.write(f"token: {token}\n")
            file.write(f"admin: {admin_id}\n")
            file.write(f"users: {','.join(map(str, user_ids))}\n")
            file.write(f"notify: {','.join(map(str, notify_ids))}\n")
    except Exception as e:
        raise Exception(f"Error writing to config file: {e}")

# Initialize the Dobot Magician
robot = Dobot(ip='192.168.5.1', port=29999)

# Decorator to check user authorization
def authorized_users_only():
    def decorator(func):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            # Fetch the latest user_ids dynamically
            token, admin_id, user_ids, notify_ids = read_config('config.txt')
            user_id = update.effective_user.id
            #print(f"User ID: {user_id}, IDs: {user_ids}")  # Debug line
            if user_id not in user_ids:
                await update.message.reply_text("You are not authorized to use this robot.")
                return
            return await func(update, context, *args, **kwargs)
        return wrapper
    return decorator

# Decorator to check admin authorization
def admin_only():
    def decorator(func):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            # Fetch the latest user_ids dynamically
            token, admin_id, user_ids, notify_ids = read_config('config.txt')
            user_id = update.effective_user.id
            if user_id != admin_id:
                await update.message.reply_text("You are not authorized to perform this action. Admin access required.")
                return
            return await func(update, context, *args, **kwargs)
        return wrapper
    return decorator

@authorized_users_only()
async def notify(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_id = update.effective_user.id
        token, admin_id, user_ids, notify_ids = read_config('config.txt')

        if user_id not in notify_ids:
            notify_ids.append(user_id)
            write_config('config.txt', token, admin_id, user_ids, notify_ids)
            await update.message.reply_text("You will now be notified when the bot is online.")
        else:
            await update.message.reply_text("You are already subscribed to notifications.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

@authorized_users_only()
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_id = update.effective_user.id
        token, admin_id, user_ids, notify_ids = read_config('config.txt')

        if user_id in notify_ids:
            notify_ids.remove(user_id)
            write_config('config.txt', token, admin_id, user_ids, notify_ids)
            await update.message.reply_text("You will no longer be notified when the bot is online.")
        else:
            await update.message.reply_text("You are not subscribed to notifications.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")


@authorized_users_only()
async def connect(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global isConnected
    try:
        robot.Connect()
        robot.EnableRobot()
        await update.message.reply_text("Robot connected and enabled.")
        isConnected = True
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
        isConnected = False

@authorized_users_only()
async def move(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not isConnected:
        await update.message.reply_text("Robot not connected! Use /connect to connect to the robot.")
        return
    try:
        joints = list(map(float, context.args))
        if len(joints) != 6:
            await update.message.reply_text("Invalid command! Use /move <j1> <j2> <j3> <j4> <j5> <j6>.")
            return

        response = robot.MoveJJ(*joints)
        await update.message.reply_text(f"Robot moving to joints {joints}.")
    except ValueError:
        await update.message.reply_text("Invalid command! Use /move <j1> <j2> <j3> <j4> <j5> <j6>.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

@authorized_users_only()
async def home(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not isConnected:
        await update.message.reply_text("Robot not connected! Use /connect to connect to the robot.")
        return
    try:
        response = robot.Home()
        await update.message.reply_text(f"Robot returning to home position.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

@authorized_users_only()
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not isConnected:
        await update.message.reply_text("Robot not connected! Use /connect to connect to the robot.")
        return
    try:
        response = robot.DisableRobot()
        await update.message.reply_text(f"Robot stopped.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

@authorized_users_only()
async def wave(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not isConnected:
        await update.message.reply_text("Robot not connected! Use /connect to connect to the robot.")
        return
    await update.message.reply_text("Waving at the window.")
    robot.MoveJJ(176.5, 5.6, -52.9, -32.2, 87.8, 11.8)
    robot.MoveJJ(176.5, 5.6, -52.9, 32.2, 87.8, 11.8)
    robot.MoveJJ(270, 30, -60, -10, 0, 0)
    robot.MoveJJ(270, 60, -30, 30, 0, 0)
    robot.MoveJJ(270, 30, -60, -10, 0, 0)
    robot.MoveJJ(270, 60, -30, 30, 0, 0)
    robot.MoveJJ(270, 0, 0, 0, 0, 0)

@authorized_users_only()
async def wiggle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not isConnected:
        await update.message.reply_text("Robot not connected! Use /connect to connect to the robot.")
        return
    await update.message.reply_text("Wiggleling at the window.")
    robot.MoveJJ(180, 0, -50, -20, 90, 0)
    robot.MoveJJ(180, 0, -50, 50, 90, 0)
    robot.MoveJJ(270, 0, 50, -50, 0, 0)
    robot.MoveJJ(270, 30, -50, 50, 0, -30)
    robot.MoveJJ(270, 0, 50, -50, 0, 0)
    robot.MoveJJ(270, 30, -50, 50, 0, -30)
    robot.MoveJJ(270, 0, 0, 0, 0, 0)

@authorized_users_only()
async def pack(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not isConnected:
        await update.message.reply_text("Robot not connected! Use /connect to connect to the robot.")
        return
    await update.message.reply_text("Robot packing up.")
    robot.MoveJJ(-90, 0, -140, -40, 0, 0)

@authorized_users_only()
async def greet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not isConnected:
        await update.message.reply_text("Robot not connected! Use /connect to connect to the robot.")
        return
    await update.message.reply_text("Greeting to the door.")
    robot.MoveJJ(101.3473, -16.4680, 19.3994, -1.0746, 4.1370, 0)
    robot.MoveJJ(101.3473, -16.4680, 19.3994, -1.0746, 4.1370, -15)
    robot.MoveJJ(101.3473, -16.4680, 19.3994, -1.0746, 4.1370, 15)
    robot.MoveJJ(101.3473, -16.4680, 19.3994, -1.0746, 4.1370, 0)

@authorized_users_only()
async def suckerON(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not isConnected:
        await update.message.reply_text("Robot not connected! Use /connect to connect to the robot.")
        return
    await update.message.reply_text("Activate sucker.")
    robot.SetSucker(1)

@authorized_users_only()
async def suckerOFF(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not isConnected:
        await update.message.reply_text("Robot not connected! Use /connect to connect to the robot.")
        return
    await update.message.reply_text("Deactivate sucker.")
    robot.SetSucker(0)

@authorized_users_only()
async def pickupHi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global hasSign
    if not isConnected:
        await update.message.reply_text("Robot not connected! Use /connect to connect to the robot.")
        return
    if hasSign > 0:
        if hasSign == 1:
            await update.message.reply_text(
            "Robot already carying the HI sign.",
            reply_to_message_id=update.message.message_id
            )
        else:
            await update.message.reply_text(
            "Robot already carying the BYE sign.",
            reply_to_message_id=update.message.message_id
            )
        return
    await update.message.reply_text("Robot picking up sign.")
    hasSign = 1 # HI sign
    robot.MoveJJ(248.9177, -42.4427, -113.0571, 65.7272, 88.3278, 67.6986)
    time.sleep(1)
    robot.MoveJJ(248.9177, -45.4710, -112.8282, 68.5268, 88.3278, 67.6986)
    time.sleep(2)
    robot.SetSucker(1)
    time.sleep(2)
    robot.MoveJJ(248.9177, -25.8053, -109.9558, 45.9886, 88.3278, 67.6986)

@authorized_users_only()
async def pickupBye(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global hasSign
    if not isConnected:
        await update.message.reply_text("Robot not connected! Use /connect to connect to the robot.")
        return
    if hasSign > 0:
        if hasSign == 1:
            await update.message.reply_text(
            "Robot already carying the HI sign.",
            reply_to_message_id=update.message.message_id
            )
        else:
            await update.message.reply_text(
            "Robot already carying the BYE sign.",
            reply_to_message_id=update.message.message_id
            )
        return
    await update.message.reply_text("Robot picking up sign.")
    hasSign = 2 # BYE sign
    robot.MoveJJ(269.8520, -32.2451, -131.6856, 73.5455, 88.3569, 88.6418)
    robot.MoveJJ(269.8520, -40.3747, -131.4702, 81.4597, 88.3569, 88.6418)
    time.sleep(2)
    robot.SetSucker(1)
    time.sleep(2)
    robot.MoveJJ(269.8520, -32.2451, -131.6856, 73.5455, 88.3569, 88.6418)

@authorized_users_only()
async def returnSign(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global hasSign
    if not isConnected:
        await update.message.reply_text("Robot not connected! Use /connect to connect to the robot.")
        return
    await update.message.reply_text("Robot returning sign.")
    if hasSign > 0:
        if hasSign == 1: # HI sign
            robot.MoveJJ(248.9177, -25.8053, -109.9558, 45.9886, 88.3278, 67.6986)
            robot.MoveJJ(248.9177, -44.9695, -112.8800, 68.0770, 88.3278, 67.6986)
            time.sleep(1)
            robot.SetSucker(0)
            time.sleep(1)
            robot.MoveJJ(248.9177, -25.8053, -109.9558, 45.9886, 88.3278, 67.6986)
        else: # BYE sign
            robot.MoveJJ(269.8520, -32.2451, -131.6856, 73.5455, 88.3569, 88.6418)
            robot.MoveJJ(269.8520, -40.3747, -131.4702, 81.4597, 88.3569, 88.6418)
            time.sleep(1)
            robot.SetSucker(0)
            time.sleep(1)
            robot.MoveJJ(269.8520, -32.2451, -131.6856, 73.5455, 88.3569, 88.6418)
        hasSign = 0 # No sign
    else:
        await update.message.reply_text("Robot is not carying any sign.")

@authorized_users_only()
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I'm a bot controlling a Dobot Magician E6. Use /commands to display all possible commands or start by using /connect to connect to the robot.")

@admin_only()
async def authorize(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if len(context.args) != 1:
            await update.message.reply_text("Invalid command! Use /authorize <user_id>.")
            return

        new_user_id = int(context.args[0])
        token, admin_id, user_ids, notify_ids = read_config('config.txt')

        if new_user_id in user_ids:
            await update.message.reply_text(f"User ID {new_user_id} is already authorized.")
        else:
            user_ids.append(new_user_id)
            write_config('config.txt', token, admin_id, user_ids, notify_ids)
            await update.message.reply_text(f"User ID {new_user_id} has been authorized.")

        # Reload user IDs
        globals()['user_ids'] = user_ids
    except ValueError:
        await update.message.reply_text("Invalid user ID! Use /authorize <user_id>.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

@admin_only()
async def deauthorize(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if len(context.args) != 1:
            await update.message.reply_text("Invalid command! Use /deauthorize <user_id>.")
            return

        user_id_to_remove = int(context.args[0])
        token, admin_id, user_ids, notify_ids = read_config('config.txt')

        if user_id_to_remove not in user_ids:
            await update.message.reply_text(f"User ID {user_id_to_remove} is not in the authorized list.")
        else:
            user_ids.remove(user_id_to_remove)
            write_config('config.txt', token, admin_id, user_ids, notify_ids)
            await update.message.reply_text(f"User ID {user_id_to_remove} has been deauthorized.")

        # Reload user IDs
        globals()['user_ids'] = user_ids
    except ValueError:
        await update.message.reply_text("Invalid user ID! Use /deauthorize <user_id>.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def myID(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_id = update.effective_user.id
        await update.message.reply_text(f"Your Telegram ID is: {user_id}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def role(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Adjust to unpack four values
        token, admin_id, user_ids, notify_ids = read_config('config.txt')
        user_id = update.effective_user.id

        # Determine the user's role
        if user_id == admin_id:
            role = "Admin"
        elif user_id in user_ids:
            role = "User"
        else:
            role = "Unauthorized"

        # Reply with the user's role
        await update.message.reply_text(f"Your role is: {role}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_id = update.effective_user.id
        token, admin_id, user_ids, notify_ids = read_config('config.txt')

        # Start with commands available to unauthorized users
        commands = [
            "\nGeneral commands:",
            "  /myid - Get your Telegram ID",
            "  /role - Check your role",
            "  /commands - List available commands",
        ]

        # If the user is a normal user, expand the command list
        if user_id in user_ids:
            commands.extend([
                "\nRobot commands:",
                "  /connect - Connect to the robot",
                "  /greet - Greet to the door",
                "  /home - Move the robot to the home position",
                "  /move <j1> <j2> <j3> <j4> <j5> <j6> - Move the robot",
                "  /mute - Unsubscribe from notifications",
                "  /notify - Subscribe to notifications",
                "  /pack - Return the robot to the pack position",
                "  /pickuphi - Pickup the HI sign",
                "  /returnhi - Return the HI sign",
                "  /returnsign - Return the sign",
                "  /start - Start the robot",
                "  /stop - Stop and disconnect the robot",
                "  /suckerOFF - Deactivate the sucker",
                "  /suckerON - Activate the sucker",
                "  /wave - Wave at the window",
                "  /wiggle - Wiggle at the window",
            ])

        # If the user is the admin, further expand the command list
        if user_id == admin_id:
            commands.extend([
                "\nAdmin commands:",
                "  /authorize <user_id> - Authorize a new user",
                "  /deauthorize <user_id> - Deauthorize a user",
                "  /sendcmd <command> - Send a command to the robot",
            ])

        # Determine the user's role
        if user_id == admin_id:
            role = "Admin"
        elif user_id in user_ids:
            role = "User"
        else:
            role = "Unauthorized"

        # Build the response
        command_list = "\n".join(commands)
        await update.message.reply_text(f"Your role is: {role}\n\nAvailable commands:\n{command_list}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

@admin_only()
async def sendcmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if len(context.args) != 1:
            await update.message.reply_text("Invalid command! Use /sendcmd <command>.")
            return

        command = context.args[0]
        await update.message.reply_text(f"Sending command: {command}")

        # Execute the command
        reply = robot.SendCommand(command)
        await update.message.reply_text(f"Response: {reply}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def send_startup_notifications(bot: Bot, notify_ids: list):
    for user_id in notify_ids:
        try:
            await bot.send_message(chat_id=user_id, text="The bot is now online and ready to use.")
        except Exception as e:
            print(f"Error notifying user {user_id}: {e}")

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text(
            "Unknown command. Use /commands to see the list of available commands.",
            reply_to_message_id=update.message.message_id
        )
    except Exception as e:
        print(f"Error handling unknown command: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Get the message text
        message_text = update.message.text

        # Reply to the user
        await update.message.reply_text(
            "How nice of you to say that! However, I'm just a bot and can only understand commands. Use /commands to see the list of available commands.",
            reply_to_message_id=update.message.message_id
        )
    except Exception as e:
        print(f"Error handling message: {e}")

def main():
    # Create and set the event loop for the main thread
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # Needed for Windows
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Read the token and user IDs from config.txt
    token, admin_id, user_ids, notify_ids = read_config('config.txt')

    # Initialize the application with the token
    application = Application.builder().token(token).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("myid", myID))
    application.add_handler(CommandHandler("role", role))
    application.add_handler(CommandHandler("notify", notify))
    application.add_handler(CommandHandler("mute", mute))
    application.add_handler(CommandHandler("connect", connect))
    application.add_handler(CommandHandler("commands", commands))
    application.add_handler(CommandHandler("move", move))
    application.add_handler(CommandHandler("home", home))
    application.add_handler(CommandHandler("pack", pack))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("wave", wave))
    application.add_handler(CommandHandler("wiggle", wiggle))
    application.add_handler(CommandHandler("suckerON", suckerON))
    application.add_handler(CommandHandler("suckerOFF", suckerOFF))
    application.add_handler(CommandHandler("pickuphi", pickupHi))
    application.add_handler(CommandHandler("pickupbye", pickupBye))
    application.add_handler(CommandHandler("returnsign", returnSign))
    application.add_handler(CommandHandler("greet", greet))
    application.add_handler(CommandHandler("authorize", authorize))
    application.add_handler(CommandHandler("deauthorize", deauthorize))
    application.add_handler(CommandHandler("sendcmd", sendcmd))

    # Add the unknown command handler
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    # Register non-command message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Create a bot instance
    bot = Bot(token=token)

    # Send startup messages
    loop.run_until_complete(send_startup_notifications(bot, notify_ids))

    # Run the bot and send startup messages
    print("Bot started...")
    application.run_polling(drop_pending_updates=True)


if __name__ == '__main__':
    main()
