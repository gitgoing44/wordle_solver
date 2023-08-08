# Mathias Reed
# 5/30/2023 - Initially started in 2022
# This program is an effort to make guessing the word
# of a Wordle game much easier


def menu_options():
    print(f"Enter 1 to start filter:\n"
          f"Enter 2 to see instructions:\n"
          f"Enter 9 to quit:")


def required_letters(word, required_letters):
    """
    This function checks the current word for required letters that
    must be in the word to ensure that only those words are sent to
    the list of possible words.
    :param word: The word currently being analyzed
    :param required_letters: A list of letters that must be in the word
    :return: True if all the required letters have been found in the
    word. False otherwise.
    """
    counter = 0

    for letter in required_letters:
        if letter not in word:
            return False

        elif letter in word:
            counter += 1

    if counter == len(required_letters):
        return True


def banned_checker(word, banned_letters):
    """
    This function checks the current word for any banned letters. If a banned
    letter is found, the word is not a possible answer and the function returns false.
    :param word: The word currently being analyzed
    :param banned_letters: A list of letters that can not be in the word
    :return: True if the word does not contain any banned letters.
    False otherwise.
    """

    for letter in banned_letters:
        if letter in word:
            return False

    return True


def wrong_word_order(word, wrong_order_set):
    """
    This function compares the word with a set of letters that are in the
    WRONG index. This ensures that any words with a letter at that index
    will be removed from the possibilities.
    :param word: The word currently being analyzed
    :param wrong_order_set: a set of letters that are in the WRONG index
    to ensure any matches to this incorrect index are not returned
    :return: True if there are no letters in the index that they should not be in.
    False otherwise.
    """
    for index, letter in enumerate(word):
        if wrong_order_set[index] == "":
            continue

        if letter in wrong_order_set[index]:
            return False

    return True


def correct_word_order(word, order):
    """
    This function will take a word and the correct word order as
    arguments to see if the word has letters in the correct place. If
    the correct order is not known, it will be blank ("").
    :param word: The word currently being analyzed
    :param order: The correct order the words should be in.
    :return: True if all the letters correspond with the order they should
    be in or the space is blank. False otherwise.
    """

    index = 0
    for letter in word:
        if index >= len(order):
            return False

        order_letter = order[index]

        if order_letter == "":
            index += 1
            continue

        if letter != order_letter:
            return False

        index += 1
    return True


def entrance():
    """
    A simple welcome message
    """
    print("Welcome to the wordle solver!\n"
          "Enter information based on your Wordle game to find the answers\n")


def get_input(correct_order, wrong_order, banned, required):
    """
    This function takes input from the user to update the lists that the filters use to exclude
    words that do not meet the criteria.
    :param correct_order: The correct order all known letters should be in. If the letters are not in this order
    they are excluded.
    :param wrong_order: The wrong order that letters are in, words with letters in this order are excluded.
    :param banned: All the banned letters that should not be in the word. If they are in the word they are excluded.
    :param required: All the required letters in the word. If the word does not have them it is excluded.
    :return: All the updated lists are returned and then used with the filter functions to narrow results.
    """

    # FOR THE UPDATE, I WANT TO ENABLE THE USER TO PUT MULTIPLE VALUES IN THE WRONG ORDER LIST
    # Update word_order
    for i in range(len(correct_order)):
        correct_order[i] = input(f"Enter value for correct letter at[{i}]: ")

    # Update wrong_order
    print()
    for i in range(len(wrong_order)):
        wrong_order[i] = input(f"Enter value for wrong letter at[{i}]: ")

    # Update banned_letters
    banned_input = input("\nEnter banned letters (separated by spaces): ")
    banned.clear()
    banned.extend(banned_input.split())

    # Update required_letters
    required_input = input("\nEnter required letters (separated by spaces): ")
    required.clear()
    required.extend(required_input.split())

    return correct_order, wrong_order, banned, required


def retrieve_dictionary():
    """
    This function runs once at the beginning of the main method. It opens a dictionary of
    sorted 5-letter words and copies them into
    :return: final_dict A sorted list of 20,768 known 5-letter words
    """

    final_dict = []
    with open('5_letter_dict.txt', 'r') as file:
        for line in file:
            word = line.strip()
            final_dict.append(word)
        file.close()

        return final_dict


def instructions():
    print("\nInstructions: \n"
          "NOTE: The index of a word will always start with 0.\n"
          "When updating the letter orders as you use the program,\n"
          "index 0 refers to the first letter, index 4 refers to the last.\n\n"
          "Correct letter: You will enter all known letters into their correct position.\n"
          "Wrong letter: You will enter all known letters that are in the word but are at the wrong index.\n"
          "Banned letters: You will enter all the letters that you know are not in the word and will be banned.\n"
          "Required letters: Here you will enter all letters that are in the word regardless of their position.\n\n"
          "Each time the filters are ran, we get closer to pinpointing what word we are trying to guess.\n"
          "If a value is not known, simply leave it blank and press ENTER.\n\n"
          "WARNING: Be careful when inputting letters, failure to input all letters\n"
          "correctly into each filter will result in incomplete/incorrect output.\n"
          "This is especially true with banned letters. Be careful you do not accidentally ban a letter that\n"
          "is also a required letter as it will result in the correct word not being shown."
          "")


def main():

    """
    This program tries to find a word based on letter positions. It asks the user for correct letter placement,
    incorrect letter placement, all banned letters, and all required letters. It then runs every word in the dictionary
    through filters one by one. If a word passes all filters, it will be displayed after input is complete to help you
    guess the correct word. If the word fails a check, it will not be displayed as an option.
    :return:
    """

    # all lists of for tracking letters
    correct_order = ["", "", "", "", ""]
    wrong_order = ["", "", "", "", ""]
    banned = ["", "", "", "", ""]
    required = ["", "", "", "", ""]

    # calls dictionary method to create a list of all known words
    dictionary = retrieve_dictionary()

    entrance()
    menu_options()
    user_input = int(input())
    while user_input != 9:
        if user_input == 1:
            main_dictionary = []

            # Gets input from the user to update all word collections to put through the filters
            correct_order, wrong_order, banned, required = get_input(correct_order, wrong_order, banned, required)

            # Word order filter
            for word in dictionary:
                result = correct_word_order(word, correct_order)

                # Wrong order filter
                if result:
                    result = wrong_word_order(word, wrong_order)

                    # Banned letter filter
                    if result:
                        result = banned_checker(word, banned)

                        # Required letter filter
                        if result:
                            result = required_letters(word, required)

                            if result:
                                main_dictionary.append(word)

            # Reversing dictionary for better readability
            reverse_dict = sorted(main_dictionary, reverse=True)
            main_dictionary = reverse_dict

            # Removing duplicates from dictionary by converting to a set
            # then back to a list
            temp_list = list(set(main_dictionary))
            main_dictionary = temp_list

            for word in main_dictionary:
                print(word)
            print("Correct order: " + str(correct_order))
            print("Wrong order: " + str(wrong_order))
            print("Banned letters: " + str(banned))
            print("Required letters: " + str(required) + "\n")
            print(str(len(main_dictionary)) + " words remain after the filters\n")
            menu_options()
            user_input = int(input())

        elif user_input == 2:
            instructions()
            print("\n")
            menu_options()
            user_input = int(input())

        elif user_input == 9:
            print("Goodbye")
            break


main()
