import asyncio
import time
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from Magician import DobotMagicianE6

isConnected = False

# Function to read the API token and user IDs from the config file
def read_config(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            token = None
            user_ids = []

            for line in lines:
                if line.startswith("token:"):
                    token = line.split(":", 1)[1].strip()
                elif line.startswith("userIDs:"):
                    user_ids = [uid.strip() for uid in line.split(":", 1)[1].strip().split(",")]

            if not token:
                raise ValueError("Token not found in config file.")
            if not user_ids:
                raise ValueError("User IDs not found in config file.")

            return token, user_ids
    except FileNotFoundError:
        raise Exception(f"Config file '{file_path}' not found.")
    except Exception as e:
        raise Exception(f"Error reading config file: {e}")

# Function to write user IDs back to the config file
def write_config(file_path, token, user_ids):
    try:
        with open(file_path, 'w') as file:
            file.write(f"token: {token}\n")
            file.write(f"userIDs: {','.join(map(str, user_ids))}\n")
    except Exception as e:
        raise Exception(f"Error writing to config file: {e}")

# Initialize the Dobot Magician
robot = DobotMagicianE6(ip='192.168.5.1', port=29999)

# Decorator to check user authorization
def authorized_users_only(user_ids):
    def decorator(func):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            user_id = update.effective_user.id
            if user_id not in user_ids:
                await update.message.reply_text("You are not authorized to use this robot.")
                return
            return await func(update, context, *args, **kwargs)
        return wrapper
    return decorator

@authorized_users_only(user_ids=[])
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

@authorized_users_only(user_ids=[])
async def move(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not isConnected:
        await update.message.reply_text("Robot not connected! Use /connect to connect to the robot.")
        return
    try:
        joints = list(map(float, context.args))
        if len(joints) != 6:
            await update.message.reply_text("Invalid command! Use /move <j1> <j2> <j3> <j4> <j5> <j6>.")
            return

        response = robot.MoveJ(*joints)
        await update.message.reply_text(f"Robot moving to joints {joints}.")
    except ValueError:
        await update.message.reply_text("Invalid command! Use /move <j1> <j2> <j3> <j4> <j5> <j6>.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

@authorized_users_only(user_ids=[])
async def home(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not isConnected:
        await update.message.reply_text("Robot not connected! Use /connect to connect to the robot.")
        return
    try:
        response = robot.Home()
        await update.message.reply_text(f"Robot returning to home position.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

@authorized_users_only(user_ids=[])
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not isConnected:
        await update.message.reply_text("Robot not connected! Use /connect to connect to the robot.")
        return
    try:
        response = robot.DisableRobot()
        await update.message.reply_text(f"Robot stopped.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

@authorized_users_only(user_ids=[])
async def wave(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not isConnected:
        await update.message.reply_text("Robot not connected! Use /connect to connect to the robot.")
        return
    await update.message.reply_text("Waving at the window.")
    robot.MoveJ(176.5, 5.6, -52.9, -32.2, 87.8, 11.8)
    robot.MoveJ(176.5, 5.6, -52.9, 32.2, 87.8, 11.8)
    robot.MoveJ(270, 30, -60, -10, 0, 0)
    robot.MoveJ(270, 60, -30, 30, 0, 0)
    robot.MoveJ(270, 30, -60, -10, 0, 0)
    robot.MoveJ(270, 60, -30, 30, 0, 0)
    robot.MoveJ(270, 0, 0, 0, 0, 0)

@authorized_users_only(user_ids=[])
async def wiggle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not isConnected:
        await update.message.reply_text("Robot not connected! Use /connect to connect to the robot.")
        return
    await update.message.reply_text("Wiggleling at the window.")
    robot.MoveJ(180, 0, -50, -20, 90, 0)
    robot.MoveJ(180, 0, -50, 50, 90, 0)
    robot.MoveJ(270, 0, 50, -50, 0, 0)
    robot.MoveJ(270, 30, -50, 50, 0, -30)
    robot.MoveJ(270, 0, 50, -50, 0, 0)
    robot.MoveJ(270, 30, -50, 50, 0, -30)
    robot.MoveJ(270, 0, 0, 0, 0, 0)

@authorized_users_only(user_ids=[])
async def pack(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not isConnected:
        await update.message.reply_text("Robot not connected! Use /connect to connect to the robot.")
        return
    await update.message.reply_text("Robot packing up.")
    robot.MoveJ(-90, 0, -140, -40, 0, 0)

@authorized_users_only(user_ids=[])
async def greet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not isConnected:
        await update.message.reply_text("Robot not connected! Use /connect to connect to the robot.")
        return
    await update.message.reply_text("Greeting to the door.")
    robot.MoveJ(101.3473, -16.4680, 19.3994, -1.0746, 4.1370, 0)
    robot.MoveJ(101.3473, -16.4680, 19.3994, -1.0746, 4.1370, -15)
    robot.MoveJ(101.3473, -16.4680, 19.3994, -1.0746, 4.1370, 15)
    robot.MoveJ(101.3473, -16.4680, 19.3994, -1.0746, 4.1370, 0)

@authorized_users_only(user_ids=[])
async def suckerON(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not isConnected:
        await update.message.reply_text("Robot not connected! Use /connect to connect to the robot.")
        return
    await update.message.reply_text("Activate sucker.")
    robot.SetSucker(1)

@authorized_users_only(user_ids=[])
async def suckerOFF(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not isConnected:
        await update.message.reply_text("Robot not connected! Use /connect to connect to the robot.")
        return
    await update.message.reply_text("Deactivate sucker.")
    robot.SetSucker(0)

@authorized_users_only(user_ids=[])
async def pickupSign(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not isConnected:
        await update.message.reply_text("Robot not connected! Use /connect to connect to the robot.")
        return
    await update.message.reply_text("Robot picking up sign.")
    robot.MoveJ(248.9177, -44.9695, -112.8800, 68.0770, 88.3278, 67.6986)
    time.sleep(2)
    robot.SetSucker(1)
    time.sleep(2)
    robot.MoveJ(248.9177, -25.8053, -109.9558, 45.9886, 88.3278, 67.6986)

@authorized_users_only(user_ids=[])
async def returnSign(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not isConnected:
        await update.message.reply_text("Robot not connected! Use /connect to connect to the robot.")
        return
    await update.message.reply_text("Robot returning sign.")
    robot.MoveJ(248.9177, -25.8053, -109.9558, 45.9886, 88.3278, 67.6986)
    robot.MoveJ(248.9177, -44.9695, -112.8800, 68.0770, 88.3278, 67.6986)
    time.sleep(1)
    robot.SetSucker(0)
    time.sleep(1)
    robot.MoveJ(248.9177, -25.8053, -109.9558, 45.9886, 88.3278, 67.6986)

@authorized_users_only(user_ids=[])
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I'm a bot controlling a Dobot Magician E6. Use /commands to display all possible commands or start by using /connect to connect to the robot.")

@authorized_users_only(user_ids=[])
async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Available commands:\n"
                                    "/start - Start the bot\n"
                                    "/connect - Connect to the robot\n"
                                    "/commands - Display all available commands\n"
                                    "/move <j1> <j2> <j3> <j4> <j5> <j6> - Move the robot to the specified joint positions\n"
                                    "/home - Return the robot to the home position\n"
                                    "/pack - REturn the robot to the pack position\n"
                                    "/stop - Stop and disconnect the robot\n"
                                    "/wave - Wave at the window\n"
                                    "/wiggle - Wiggle at the window\n"
                                    "/suckerON - Activate the sucker\n"
                                    "/suckerOFF - Deactivate the sucker\n"
                                    "/pickupSign - Pickup the sign\n"
                                    "/returnSign - Return the sign\n"
                                    "/greet - Greet to the door")

@authorized_users_only(user_ids=[])
async def authorize(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if len(context.args) != 1:
            await update.message.reply_text("Invalid command! Use /authorize <user_id>.")
            return

        new_user_id = int(context.args[0])
        token, user_ids = read_config('config.txt')

        if new_user_id in user_ids:
            await update.message.reply_text(f"User ID {new_user_id} is already authorized.")
        else:
            user_ids.append(new_user_id)
            write_config('config.txt', token, user_ids)
            await update.message.reply_text(f"User ID {new_user_id} has been authorized.")

        # Reload user IDs
        globals()['user_ids'] = user_ids
    except ValueError:
        await update.message.reply_text("Invalid user ID! Use /authorize <user_id>.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

@authorized_users_only(user_ids=[])
async def deauthorize(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if len(context.args) != 1:
            await update.message.reply_text("Invalid command! Use /deauthorize <user_id>.")
            return

        user_id_to_remove = int(context.args[0])
        token, user_ids = read_config('config.txt')

        if user_id_to_remove not in user_ids:
            await update.message.reply_text(f"User ID {user_id_to_remove} is not in the authorized list.")
        else:
            user_ids.remove(user_id_to_remove)
            write_config('config.txt', token, user_ids)
            await update.message.reply_text(f"User ID {user_id_to_remove} has been deauthorized.")

        # Reload user IDs
        globals()['user_ids'] = user_ids
    except ValueError:
        await update.message.reply_text("Invalid user ID! Use /deauthorize <user_id>.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")


async def send_startup_messages(bot: Bot, user_ids: list):
    for user_id in user_ids:
        try:
            await bot.send_message(chat_id=user_id, text="Hello! The bot is now online and ready to use.")
        except Exception as e:
            print(f"Error sending startup notification to user {user_id}: {e}")

def main():
    # Create and set the event loop for the main thread
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # Needed for Windows
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Read the token and user IDs from config.txt
    token, user_ids = read_config('config.txt')

    # Initialize the application with the token
    application = Application.builder().token(token).build()

    # Update the user_ids in decorators
    for handler in [start, connect, commands, move, home, pack, stop, wave, wiggle, suckerON, suckerOFF, pickupSign, returnSign, greet, authorize, deauthorize]:
        handler.__wrapped__.__globals__['user_ids'] = user_ids

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
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
    application.add_handler(CommandHandler("pickupSign", pickupSign))
    application.add_handler(CommandHandler("returnSign", returnSign))
    application.add_handler(CommandHandler("greet", greet))
    application.add_handler(CommandHandler("authorize", authorize))
    application.add_handler(CommandHandler("deauthorize", deauthorize))

    # Create a bot instance
    bot = Bot(token=token)

    # Send startup messages
    loop.run_until_complete(send_startup_messages(bot, user_ids))

    # Run the bot and send startup messages
    print("Bot started...")
    application.run_polling()


if __name__ == '__main__':
    main()
