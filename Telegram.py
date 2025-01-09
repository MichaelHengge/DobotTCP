import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from Magician import DobotMagicianE6

# Function to read the API token from a file
def read_api_token(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        raise Exception(f"Config file '{file_path}' not found.")
    except Exception as e:
        raise Exception(f"Error reading API token: {e}")

# Initialize the Dobot Magician
robot = DobotMagicianE6(ip='192.168.5.1', port=29999)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
    robot.MoveJ(270, 0, 0, 0, 0, 0)
    robot.MoveJ(270, 30, -60, -10, 0, 0)
    robot.MoveJ(270, 60, -30, 30, 0, 0)
    robot.MoveJ(270, 30, -60, -10, 0, 0)
    robot.MoveJ(270, 60, -30, 30, 0, 0)

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

def main():
    # Read the API token from config.txt
    token = read_api_token('config.txt')

    application = Application.builder().token(token).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("move", move))
    application.add_handler(CommandHandler("home", home))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("wave", wave))
    application.add_handler(CommandHandler("suckerON", suckerON))
    application.add_handler(CommandHandler("suckerOFF", suckerOFF))
    application.add_handler(CommandHandler("pickupSign", pickupSign))
    application.add_handler(CommandHandler("returnSign", returnSign))
    application.add_handler(CommandHandler("greet", greet))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
