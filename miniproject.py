import random

def game_rules():
    print("""
Welcome to Snake, Water, Gun Game!
----------------------------------
Rules:
- Snake (s) drinks Water (w): Snake wins!
- Gun (g) shoots Snake (s): Gun wins!
- Water (w) douses Gun (g): Water wins!
- If both players choose the same, it's a draw.
----------------------------------
""")

def snake_water_gun():
    # Corrected dictionaries with proper syntax
    yourdict = {"s": 1, "w": -1, "g": 0}
    reverseDict = {1: "Snake", -1: "Water", 0: "Gun"}

    # Getting input from player with corrected input syntax
    yourstr = input("Enter your choice (s for Snake, w for Water, g for Gun): ").lower()

    # Checking for valid input
    if yourstr not in yourdict:
        print("Invalid choice, please choose 's', 'w', or 'g'")
        return  # Exit the function if input is invalid

    you = yourdict[yourstr]

    # Computer's random choice
    computer = random.choice([-1, 0, 1])

    # Display choices
    print(f"\nYou chose {reverseDict[you]}\nComputer chose {reverseDict[computer]}")

    # Game logic
    if computer == you:
        print("It's a draw!")
    else:
        if (computer == -1 and you == 1) or (computer == 1 and you == 0) or (computer == 0 and you == -1):
            print("You win!")
        else:
            print("You lose!")

# Running the game
if __name__ == "__main__":
    game_rules()  # Display the game rules
    snake_water_gun()
