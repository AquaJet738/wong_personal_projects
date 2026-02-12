import random

# Stat order: bee name, bee color, base energy, base speed, base attack, base gather amount, base gather time, base conversion amount, base conversion time
# Base energy of 0 = Unlimited energy
# Tabby Bee is assumed to have maximum "Tabby Love" stacks (1000)
bees = {"Common": [["Basic", "White", 20, 14, 1, 10, 4, 80, 4]], 
        "Rare": [["Bomber", "White", 20, 15.4, 2, 10, 4, 120, 4], ["Brave", "White", 30, 16.8, 5, 10, 4, 200, 4], 
                 ["Bumble", "Blue", 50, 10.5, 1, 18, 4, 80, 4], ["Cool", "Blue", 20, 14, 2, 10, 3, 120, 4], 
                 ["Hasty", "White", 20, 19.6, 1, 10, 3, 80, 3], ["Looker", "White", 20, 14, 1, 13, 4, 160, 4], 
                 ["Rad", "Red", 20, 14, 1, 13, 4, 80, 3], ["Rascal", "Red", 20, 16.1, 3, 10, 4, 80, 4], 
                 ["Stubborn", "White", 20, 11.9, 2, 10, 4, 80, 3]],
        "Epic": [["Bubble", "Blue", 20, 16.1, 3, 10, 4, 160, 4], ["Bucko", "Blue", 30, 15.4, 5, 17, 4, 80, 3], 
                 ["Commander", "White", 30, 14, 4, 15, 4, 80, 4], ["Demo", "White", 20, 16.8, 3, 10, 4, 200,4], 
                 ["Exhausted", "White", 0, 10.5, 1, 10, 4.6, 240, 4], ["Fire", "Red", 25, 11.2, 4, 10, 4, 80, 4], 
                 ["Frosty", "Blue", 25, 11.2, 1, 10, 4, 80, 4], ["Honey", "White", 25, 11.2, 1, 10, 4, 80, 4], 
                 ["Rage", "Red", 20, 15.4, 4, 10, 4, 80, 4], ["Riley", "Red", 25, 15.4, 5, 10, 2, 140, 4], 
                 ["Shocked", "White", 20, 19.6, 2, 10, 4, 80, 2]],
        "Legendary": [["Baby", "White", 15, 10.5, 0, 10, 5, 80, 5], ["Carpenter", "White", 25, 11.2, 4, 10, 3, 120, 4],
                      ["Demon", "Red", 20, 10.5, 8, 35, 4, 60, 4], ["Diamond", "Blue", 20, 14, 1, 10, 4, 1000, 4],
                      ["Lion", "White", 60, 19.6, 9, 20, 4, 160, 2], ["Music", "White", 20, 16.1, 1, 16, 4, 240, 4],
                      ["Ninja", "Blue", 20, 21, 4, 10, 2, 80, 3], ["Shy", "Red", 40, 18.2, 2, 10, 2, 320, 4]],
        "Mythic": [["Buoyant", "Blue", 60, 14, 3, 15, 5, 150, 3], ["Fuzzy", "White", 50, 11.9, 3, 100, 6, 40, 6],
                   ["Precise", "Red", 40, 11.2, 8, 20, 4, 130, 4], ["Spicy", "Red", 20, 14, 5, 14, 4, 200, 2],
                   ["Tadpole", "Blue", 10, 11.2, 0.5, 10, 6, 120, 4], ["Vector", "White", 45.6, 16.24, 5, 18, 4, 144, 2.72]],
        "Event": [["Bear", "White", 35, 14, 5, 15, 2, 200, 2], ["Cobalt", "Blue", 35, 18.2, 6, 10, 4, 120, 3],
                  ["Crimson", "Red", 35, 18.2, 6, 10, 4, 120, 3], ["Digital", "White", 20, 11.9, 1, 10, 4, 80, 4],
                  ["Festive", "Red", 20, 16.1, 1, 40, 4, 150, 1], ["Gummy", "White", 50, 14, 3, 10, 4, 700, 4],
                  ["Photon", "White", 0, 21, 3, 20, 2, 240, 2], ["Puppy", "White", 40, 16.1, 2, 25, 4, 280, 4],
                  ["Tabby", "White", 28, 16.1, 4, 110, 4, 1760, 3], ["Vicious", "Blue", 50, 17.5, 8, 10, 4, 80, 4],
                  ["Windy", "White", 20, 19.6, 3, 10, 3, 180, 2]]}


def main():
    valid_bees = []
    for value in bees.values():
        for i in range(len(value)):
            valid_bees.append(value[i][0].lower())

    bee_rarity = random.choice(list(bees.keys()))
    bee_to_guess = random.choice(bees[bee_rarity])
    
    bee_guessed = False
    while True:
        guess = input("Guess the bee (or type \"quit\" to stop playing): ")

        if guess.lower() == "quit":
            break

        guessed_bee = []
        guessed_bee_rarity = ""    
        if guess.lower() in valid_bees:
            for key, value in bees.items():
                for i in range(len(value)):
                    if value[i][0].lower() == guess.lower():
                        guessed_bee_rarity = key
                        guessed_bee = value[i]
            
            guesses = []
            rarity_check = ""
            for s in range(len(guessed_bee)):
                if guessed_bee[s] == bee_to_guess[s]:
                    guesses.append("🟩")
                else:
                    guesses.append("🟥")
            
            if guessed_bee_rarity.lower() == bee_rarity.lower():
                rarity_check = "🟩"
            else:
                rarity_check = "🟥"

            print(f"Bee name: {guessed_bee[0]} Bee   {guesses[0]}\n" +
                f"Bee rarity: {guessed_bee_rarity}   {rarity_check}\n" + 
                f"Bee color: {guessed_bee[1]}   {guesses[1]}\n" + 
                f"Base energy: {guessed_bee[2]}   {guesses[2]}\n" +
                f"Base speed: {guessed_bee[3]}   {guesses[3]}\n" +
                f"Base attack: {guessed_bee[4]}   {guesses[4]}\n" +
                f"Base gather amount: {guessed_bee[5]} pollen   {guesses[5]}\n" +
                f"Base gather time: {guessed_bee[6]} seconds   {guesses[6]}\n" +
                f"Base conversion amount: {guessed_bee[7]} honey   {guesses[7]}\n" +
                f"Base conversion time: {guessed_bee[8]} seconds   {guesses[8]}\n")

            if rarity_check == "🟩" and "🟥" not in guesses:
                print("You guessed the bee!")
                bee_guessed = True
                break

    if not bee_guessed:
        print(f"The bee was: {bee_to_guess[0]} Bee")


if __name__ == "__main__":
    main()