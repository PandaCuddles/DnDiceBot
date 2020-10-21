import random
import re

# Start with #d# or #, then  (+/- followed by #d# or #)
valid_roll = re.compile(
    "(\d+(d|D)\d+|\d+)((\+|\-)(\d+(d|D)\d+|\d+))*$"
)  # $ character matches to end of line

# Check if dice roll
valid_dice = re.compile("\d+(d|D)\d+$")


def dice_print(results):
    print("Formatted dice roll output:")

    output = ""
    counter = 0

    # Formats dice results in rows of 4
    for result in results:
        if (counter > 0) and (counter % 4 == 0):
            output = output + f"\n{result:<6} "
        else:
            output = output + f"{result:<6} "
        counter += 1
    print(f"{output}\n")


def dice(rolls, sides):
    sides = int(sides)
    rolls = int(rolls)

    results = []

    for roll in range(rolls):
        results.append(random.randint(1, sides))
    dice_print(results)
    return sum(results)


# Step 1: Remove spaces from input
def remove_spaces(roll):
    return roll.replace(" ", "")


# Step 2: Check if the input is a valid roll with regex
def check_roll(roll):
    match = valid_roll.match(roll)
    if match:
        return match.group(0)
    else:
        return None


# Step 3: Split roll into components [#d#, +/-, #, etc]
def split_roll(roll):
    split = re.split("(\W)", roll)

    return split


# Step 4: Send #d#/#D# rolls to dice roller and get results
def throw_dice(roll):
    for i in roll:
        index = roll.index(i)
        # Roll the dice rolls, leave the regular number strings alone
        if valid_dice.match(i):
            dice_values = re.split("d|D", i)
            rolls = dice_values[0]
            sides = dice_values[1]
            roll[index] = dice(rolls, sides)
        # Convert the number strings into proper integers so they can be calculated up later
        elif i != "+" and i != "-":
            roll[index] = int(i)
        else:
            continue

    return roll


# Step 5: Add all the dice rolls together and send result to user
def final_results(roll):
    # Ex roll (before processing): "8d20 + 10 - 1D5"
    # Ex roll (after  processing): [100, "+", 10, "-", 4]

    print(f"After Roll   : {roll}")
    size = len(roll)
    nums = []

    # If only one roll, then just return the results of the roll (if only one number, return the number)
    if size == 1:
        return roll[0]

    # Start adding numbers into a list to be added up at the end
    for index in range(0, size, 2):
        # print(index)

        if index == 0:
            nums.append(roll[index])

        elif index <= size:
            if roll[index - 1] == "+":  # Keep number as a positive number
                nums.append(roll[index])
            if roll[index - 1] == "-":  # Turn number into negative number
                nums.append(-roll[index])

        else:
            print("Error!")

    return sum(nums)


# Check dice roll, roll dice, calculate values, return the result
def parse(roll):

    # Check if the roll given is a valid dice roll.
    # e.g. "4d5+10" is valid and returns "4d5+10". "5dd7+12" is not valid and returns None.
    valid_roll = check_roll(remove_spaces(roll))

    # If check failed, return Error message
    if not valid_roll:
        #print("Invalid roll!\n")
        return f"Invalid roll!"

    # Splits up roll string into separate parts.
    # e.g. "10d20+4+8d5" -> ["10d20", "+", "4", "+", "8d5"]
    split = split_roll(valid_roll)

    # Roll the dice, convert string integers into proper integers, return the values.
    # e.g. ["10d20", "+", "4", "+", "8d5"] -> [85, "+", 4, "+", 34]
    thrown = throw_dice(split)

    # Calculate the total value of the dice rolls and integers, and return the result.
    # e.g. [85, "+", 4, "+", 34] -> 123
    total = final_results(thrown)

    return f"Total: {total}"

    #print(f"Final sum    : {total}\n")


# Program requires more robustness to add negative numbers ("1d7 + -4" currently registers as a bad roll)
# TODO: If demand is high enough, create functionality to add negative numbers (e.g. "4+-2")
# TODO: Limit number of dice rolls and dice sides to less than 10,000 (for everyone's sake)
def ex_rolls():
    _rolls = [
        "10d20 + 4 + 8d5 - 20",  # Good roll 1
        "2D20 + 5- 6d7 + 2D3",  # Good roll 2
        "1D20 + 1d5 + 1d30",  # Good roll 3
        "10 d20 + 5 + 10 + 8d7",  # Good roll 4
        "40",  # Good roll 5
        "g1D20+1d10",  # Bad roll 1
        "1D3+",  # Bad roll 2
        "1d7 + -4",  # Bad roll 3
        "4dd8 + 8",  # Bad roll 4
    ]
    for roll in _rolls:
        # print(roll.lower())
        print(f'Original Roll: "{roll}"')
        parse(roll)


#ex_rolls()
