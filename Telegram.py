import asyncio
import time
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from Magician import DobotMagicianE6

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

# Initialize the Dobot Magician
robot = DobotMagicianE6(ip='192.168.5.1', port=29999)

async def connect(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        robot.Connect()
        robot.EnableRobot()
        await update.message.reply_text("Robot connected and enabled. Use /move <j1> <j2> <j3> <j4> <j5> <j6> to move it or /home to return to the home position.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def move(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        joints = list(map(float, context.args))
        if len(joints) != 6:
            await update.message.reply_text("Invalid command! Use /move <j1> <j2> <j3> <j4> <j5> <j6>.")
            return

        response = robot.MoveJ(*joints)
        await update.message.reply_text(f"Robot moving to joints {joints}. Response: {response}")
    except ValueError:
        await update.message.reply_text("Invalid command! Use /move <j1> <j2> <j3> <j4> <j5> <j6>.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def home(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        response = robot.Home()
        await update.message.reply_text(f"Robot returning to home position. Response: {response}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        response = robot.DisableRobot()
        await update.message.reply_text(f"Robot stopped. Response: {response}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def wave(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    robot.MoveJ(176.5, 5.6, -52.9, -32.2, 87.8, 11.8)
    robot.MoveJ(176.5, 5.6, -52.9, 32.2, 87.8, 11.8)
    robot.MoveJ(270, 30, -60, -10, 0, 0)
    robot.MoveJ(270, 60, -30, 30, 0, 0)
    robot.MoveJ(270, 30, -60, -10, 0, 0)
    robot.MoveJ(270, 60, -30, 30, 0, 0)
    robot.MoveJ(270, 0, 0, 0, 0, 0)

async def wiggle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    robot.MoveJ(180, 0, -50, -20, 90, 0)
    robot.MoveJ(180, 0, -50, 50, 90, 0)
    robot.MoveJ(270, 0, 50, -50, 0, 0)
    robot.MoveJ(270, 30, -50, 50, 0, -30)
    robot.MoveJ(270, 0, 50, -50, 0, 0)
    robot.MoveJ(270, 30, -50, 50, 0, -30)
    robot.MoveJ(270, 0, 0, 0, 0, 0)

async def pack(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    robot.MoveJ(-90, 0, -140, -40, 0, 0)

async def greet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    robot.MoveJ(101.3473, -16.4680, 19.3994, -1.0746, 4.1370, 0)
    robot.MoveJ(101.3473, -16.4680, 19.3994, -1.0746, 4.1370, -15)
    robot.MoveJ(101.3473, -16.4680, 19.3994, -1.0746, 4.1370, 15)
    robot.MoveJ(101.3473, -16.4680, 19.3994, -1.0746, 4.1370, 0)

async def suckerON(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    robot.SetSucker(1)

async def suckerOFF(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    robot.SetSucker(0)

async def pickupSign(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    robot.MoveJ(248.9177, -44.9695, -112.8800, 68.0770, 88.3278, 67.6986)
    time.sleep(2)
    robot.SetSucker(1)
    time.sleep(2)
    robot.MoveJ(248.9177, -25.8053, -109.9558, 45.9886, 88.3278, 67.6986)

async def returnSign(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    robot.MoveJ(248.9177, -25.8053, -109.9558, 45.9886, 88.3278, 67.6986)
    robot.MoveJ(248.9177, -44.9695, -112.8800, 68.0770, 88.3278, 67.6986)
    time.sleep(1)
    robot.SetSucker(0)
    time.sleep(1)
    robot.MoveJ(248.9177, -25.8053, -109.9558, 45.9886, 88.3278, 67.6986)

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

    # Register command handlers
    application.add_handler(CommandHandler("connect", connect))
    application.add_handler(CommandHandler("move", move))
    application.add_handler(CommandHandler("home", home))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("wave", wave))
    application.add_handler(CommandHandler("wiggle", wiggle))
    application.add_handler(CommandHandler("suckerON", suckerON))
    application.add_handler(CommandHandler("suckerOFF", suckerOFF))
    application.add_handler(CommandHandler("pickupSign", pickupSign))
    application.add_handler(CommandHandler("returnSign", returnSign))
    application.add_handler(CommandHandler("greet", greet))

    # Create a bot instance
    bot = Bot(token=token)

    # Send startup messages
    loop.run_until_complete(send_startup_messages(bot, user_ids))

    # Run the bot and send startup messages
    print("Bot started...")
    application.run_polling()


if __name__ == '__main__':
    main()
