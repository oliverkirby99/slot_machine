import random

# GLOBAL VALUES (these won't change)
MAX_LINES = 3
MAX_BET = 1000
MIN_BET = 1

ROWS = 3
COLS = 3

# DICTIONARY OF POSSIBLE SYMBOLS/ODDS
symbol_odds = {
    "$": 4,
    "!": 8,
    "#": 16,
    "?": 24
}

# DICTIONARY OF WIN MULTIPLIERS
symbol_values = {
    "$": 16,
    "!": 8,
    "#": 4,
    "?": 2
}


def calculate_returns(columns, lines, bet, multipliers):
    # Set winnings to 0
    winnings = 0
    # Create list of potential winning lines
    winning_lines = []
    # Loop through every row/line
    for line in range(lines):
        # Check the first symbol.
        symbol = columns[0][line]
        # Loop all columns and check if the first symbol is repeated.
        for column in columns:
            symbol_to_check = column[line]
            # If symbol is NOT the same...
            if symbol != symbol_to_check:
                # Break if symbols are not the same
                break
        # Else runs if the for loop NEVER BREAKS!
        else:
            # winnings += the symbols value * the bet of the line (total bet/lines)
            winnings += multipliers[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines


# Spin function. Takes in how many rows, columns and the dictionary of symbols
def spin(rows, cols, symbols):
    print("==========SPIN==========")
    # EMPTY LIST FOR SYMBOLS
    all_symbols = []
    # FOR EACH ITEM IN THE DICTIONARY
    for symbol, symbol_odd in symbols.items():  #
        # ADD THE SYMBOL AS MANY TIMES AS THE ODDS OF THAT SYMBOL TO THE LIST
        # "_" IS A VARIABLE THAT DOESN'T NEED TO BE USED
        for _ in range(symbol_odd):
            all_symbols.append(symbol)

    # COLUMN 0, 1, 2 (VERTICAL)
    columns = []
    # Loop through 'cols' amount of times
    # _ means value won't be called
    for _ in range(cols):
        column = []
        # Create copy of 'all_symbols'. [:] clones it. Without [:], it will update with 'all_symbols'
        current_symbols = all_symbols[:]
        # Loop through 'rows' amount of times
        # _ means value won't be called
        for _ in range(rows):
            # choose random value from the 'current_symbols' list
            value = random.choice(current_symbols)
            # remove the value from the list, so it can't be used again this spin.
            current_symbols.remove(value)
            # Add the value to the current column list
            column.append(value)
        # Add column to the columns list (list within a list)
        columns.append(column)
    return columns


def print_lines(columns):
    # Loop through each column, but one index at a time
    for row in range(len(columns[0])):
        # print the symbol in that row.
        for i, column in enumerate(columns):
            # If it is the LAST loop, don't print " | "
            if i != len(column) - 1:
                # At the 'end', don't print a new line
                print(column[row], end="|")
            else:
                # At the 'end', don't print a new line
                print(column[row], end="")
        # NEXT LINE
        print()


def get_deposit():
    while True:
        # Get how much they want to deposit
        amount = input("How much would you like to deposit? £")
        # Check if it is an integer, greater than 0.
        if amount.isdigit():
            # Convert to int.
            amount = int(amount)
            # Final check to make sure that we don't get 0 or less.
            if amount > 0:
                break
            else:
                print("Invalid amount. Please try again.")
        else:
            print("Invalid input.")
    return amount


def get_lines():
    while True:
        # Get how much they want to deposit
        lines = input(f"How many lines do you want to play? (1-{str(MAX_LINES)}) ")
        # Check if it is an integer, greater than 0.
        if lines.isdigit():
            # Convert to int.
            lines = int(lines)
            # Check if value is equal to or greater than 1 AND equal to or less than MAX_LINES (3)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Invalid amount. Please try again.")
        else:
            print("Invalid input.")
    return lines


def get_bet():
    while True:
        # Get how much they want to deposit
        bet = input("How much would you like to bet? £")
        # Check if it is an integer, greater than 0.
        if bet.isdigit():
            # Convert to int.
            bet = int(bet)
            # Final check to make sure that bet is between MIN_BET and MAX_BET.
            if MIN_BET <= bet <= MAX_BET:
                break
            elif bet < MIN_BET:
                print(f"Minimum bet is £{MIN_BET}")
            elif bet > MAX_BET:
                print(f"Maximum bet is £{MAX_BET}")
            else:
                print("Invalid amount. Please try again.")
        else:
            print("Invalid input.")
    return bet


def play_game():
    # GET BALANCE/DEPOSIT AMOUNT
    balance = get_deposit()
    # ASK HOW MANY LINES THEY WANT TO BET
    lines = get_lines()

    if lines > balance:
        print("You don't have enough to play.")
        return
    # ASK HOW MUCH THEY WANT TO BET PER LINE
    # CHECK BET AMOUNT IS VALID
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(f"Insufficient funds. Balance: £{balance}")
        else:
            # UPDATE BALANCE
            balance -= total_bet
            break

    # SUMMARY OF BET
    print(f"BET: £{bet}, LINES: {lines}\nTOTAL BET: £{bet * lines}")
    print(f"Updated Balance: £{balance}")

    # SPIN AND PRINT THE SLOTS/LINES
    slots = spin(ROWS, COLS, symbol_odds)
    print_lines(slots)

    # CALCULATE WINNINGS (if any)
    winnings, winning_lines = calculate_returns(slots, lines, bet, symbol_values)
    # Print how much you won (if anything)
    print(f"You won: £{winnings}")
    # This will only print if winning_lines is NOT empty.
    print(f"WINNING LINES:", *winning_lines)
    # ADD WINNINGS TO BALANCE
    balance += winnings
    # DISPLAY NEW BALANCE!
    print(f"Total Money Returned to you: £{balance}")


# Ask if player wants to play. Yes or No.
while True:
    y = ["y", "yes", "ye", "yea", "yeah", "yeahh", "yup", "yh", "ja"]
    play = input("Do you want to play? ").lower()
    if play not in y and play != "no":
        print("Invalid entry, please try again.")
    elif play in y:
        play_game()
    elif play == "no":
        break
