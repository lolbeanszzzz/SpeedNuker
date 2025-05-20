import discord
from discord.ext import commands
from discord import app_commands
import os
import json
from colorama import init, Fore, Style

init(autoreset=True)

def save_token(token):
    with open("token.json", "w") as file:
        json.dump({"TOKEN": token}, file)

def load_token():
    try:
        with open("token.json", "r") as file:
            data = json.load(file)
            return data.get("TOKEN")
    except FileNotFoundError:
        print(Fore.RED + "Error: token.json not found.")
        return None
    except json.JSONDecodeError:
        print(Fore.RED + "Error: Invalid JSON format in token.json.")
        return None

def display_logo():
    logo = '''
 _______         __                                 .___
 \      \  __ __|  | __ ____   ____  ___________  __| _/
 /   |   \|  |  \  |/ // __ \_/ ___\/  _ \_  __ \/ __ | 
/    |    \  |  /    <\  ___/\  \__(  <_> )  | \/ /_/ | 
\____|__  /____/|__|_ \\___  >\___  >____/|__|  \____ | 
        \/           \/    \/     \/                 \/ 
'''
    os.system('cls' if os.name == 'nt' else 'clear')  
    print(Fore.RED + logo)

def display_status(connected):
    if connected:
        print(Fore.RED + "Status: Connected")
    else:
        print(Fore.BLUE + "Status: Disconnected")

def token_management():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console before showing token options
    print(Fore.BLACK + "Welcome to Nukecord token management!\n")
    print(Fore.RED + "1. Set new token") 
    print(Fore.RED + "2. Load previous token")
    print()
    choice = input(Fore.BLUE + "Choose an option (1, 2): ")

    if choice == "1":
        new_token = input(Fore.RED + "Enter the new token: ")
        save_token(new_token)
        print(Fore.RED + "Token successfully set!")
        return new_token
    elif choice == "2":
        token = load_token()
        if token:
            print(Fore.RED + f"Previous token loaded: {token}")
            return token
        else:
            print(Fore.BLUE + "No token found.")
            return None
    else:
        print(Fore.BLUE + "Invalid choice. Please try again.")
        return None

# Define your premium users (replace with actual user IDs)
premium = [111111111111111111, 222222222222222222]

# Define your bot administrators (replace with actual user IDs)
botadmin = [1369398821238472788, 222222222222222222]  # Example admin user IDs

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix="!", intents=intents)

# Load premium users from file at startup
def save_premium_users():
    with open("premium_users.json", "w") as f:
        json.dump(premium, f)

def load_premium_users():
    global premium
    try:
        with open("premium_users.json", "r") as f:
            premium = json.load(f)
    except FileNotFoundError:
        premium = []

load_premium_users()

class SpamButton(discord.ui.View):
    def __init__(self, message):
        super().__init__()
        self.message = message

    @discord.ui.button(label="Spam", style=discord.ButtonStyle.red)
    async def spam_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        for _ in range(5):
            await interaction.followup.send(self.message)

@bot.event
async def on_ready():
    display_logo()
    display_status(True)
    print("Connected as " + Fore.YELLOW + f"{bot.user}")
    try:
        await bot.tree.sync()
        print(Fore.RED + "Commands successfully synchronized.")
    except Exception as e:
        display_status(False)
        print(Fore.RED + f"Error during synchronization: {e}")

@bot.tree.command(name="customraid", description="Send a message and generate a button to spam")
@app_commands.describe(message="The message you want to spam")
async def customraid(interaction: discord.Interaction, message: str):
    # Check if the user has premium access
    if interaction.user.id not in premium:
        await interaction.response.send_message("You need premium to use this command.", ephemeral=True)
        return

    view = SpamButton(message)
    await interaction.response.send_message(f"Nukecord Raider : {message}", view=view, ephemeral=True)

@bot.tree.command(name="addpremium", description="Adds a user to the premium list.")
@app_commands.describe(user="The user to add.")
async def addpremium(interaction: discord.Interaction, user: discord.Member):
    # Check if the invoker is a bot admin
    if interaction.user.id not in botadmin:
        await interaction.response.send_message("You do not have permission to use this command. Ask an admin for assistance.", ephemeral=True)
        return

    global premium
    if user.id not in premium:
        premium.append(user.id)
        save_premium_users()
        await interaction.response.send_message(f"{user.mention} has been added to the premium list.", ephemeral=False)
    else:
        await interaction.response.send_message(f"{user.mention} is already in the premium list.", ephemeral=False)

@bot.tree.command(name="raid", description="Send a spam message")
async def raid(interaction: discord.Interaction):
    message = "# RAIDED BY NUKECORD LABS! JOIN https://discord.gg/QQ9mv4Hq FUCKERS"  # Fixed message to spam
    view = SpamButton(message)
    await interaction.response.send_message(f"Nukecord Raider: {message}", view=view, ephemeral=True)


@bot.tree.command(name="fakeadmin", description="Pretend someone bypassed Discord's API and became an admin.")
async def fakeadmin(interaction: discord.Interaction, user: discord.Member):
    class FakeAdminButton(discord.ui.View):
        def __init__(self):
            super().__init__()

        @discord.ui.button(label="Fake Admin", style=discord.ButtonStyle.green)
        async def fake_admin_button(self, button: discord.ui.Button, interaction: discord.Interaction):
            # Send a non-ephemeral message
            await interaction.response.send_message(
                f"{user.mention} has bypassed Discord's API! He is now an admin!", ephemeral=False
            )

@bot.tree.command(name="fakeban", description="Pretend someone banned someone successfully.")
async def fakeban(interaction: discord.Interaction, user: discord.Member):
    class FakeBanButton(discord.ui.View):
        def __init__(self):
            super().__init__()

        @discord.ui.button(label="Fake Ban", style=discord.ButtonStyle.red)
        async def fake_ban_button(self, button: discord.ui.Button, interaction: discord.Interaction):
            # Use the provided user for both mentions
            await interaction.response.send_message(
                f"{user.mention} has banned {user.mention} successfully.", ephemeral=False
            )
            
if __name__ == "__main__":
    TOKEN = token_management()
    if TOKEN:
        try:
            bot.run(TOKEN)
        except discord.errors.LoginFailure:
            print(Fore.RED + "Can't connect to token. Please check your token.")
            input(Fore.YELLOW + "Press Enter to go back to the menu...")
            TOKEN = token_management()
            if TOKEN:
                bot.run(TOKEN)
        except Exception as e:
            print(Fore.RED + f"An unexpected error occurred: {e}")
            input(Fore.YELLOW + "Press Enter to restart the menu...")
            TOKEN = token_management()
            if TOKEN:
                bot.run(TOKEN)
    else:
        print(Fore.RED + "❌ Error: Unable to load or set a token.")
