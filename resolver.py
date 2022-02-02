from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from collections import Counter
from selenium.webdriver.common.keys import Keys


def letter_at_pos(words, letter, pos):
    words_list_sorted = [idx for idx in words if idx[pos].lower() == letter.lower()]

    return words_list_sorted


def letter_not_at_pos(words, letter, pos):
    words_list_sorted = [idx for idx in words if letter.lower() in idx.lower()]
    words_list_sorted = [idx for idx in words_list_sorted if idx[pos].lower() != letter.lower()]

    return words_list_sorted


def letter_not_in(words, letter):
    words_list_sorted = [idx for idx in words if letter.lower() not in idx.lower()]

    return words_list_sorted


def find_word_with_max_different_letters(words):
    max_freq = len(words[0])
    max_word = None

    for word in words:
        freq = len(word) - len(Counter(word))

        if freq < max_freq:
            max_freq = freq
            max_word = word

        if freq == 0:
            return max_word

    return max_word


def word_not_dict(words, word):
    words.remove(word)

    return words


# Chargement des mots
with open('dico_sutom.txt', 'r') as file:
    words_list = file.read().split('\n')


# Préparation du web driver
driver = webdriver.Firefox()
driver.get("https://sutom.nocle.fr/")
sleep(2)

word_table = driver.find_element(By.XPATH, "/html/body/div/div[3]/table")
first_letter = word_table.text[0]

available_words = [idx for idx in words_list if len(idx) == 7]
available_words = [idx for idx in available_words if idx[0].lower() == first_letter.lower()]

done = False
x = 1

while not done:
    # Récupération du meilleur mot
    best_world_to_test = find_word_with_max_different_letters(available_words)

    print(available_words)
    print(best_world_to_test)

    # Envoie du meilleur mot
    body = driver.find_element(By.XPATH, "/html/body")
    body.send_keys(best_world_to_test)
    body.send_keys(Keys.ENTER)

    sleep(2)

    # Récupération de la réponse
    if "Ce mot n'est pas dans notre dictionnaire" in body.text and body.find_element(By.XPATH, "//*[contains(text(), 'pas dans notre dictionnaire')]").get_attribute("style") == "opacity: 1;":
        available_words = word_not_dict(available_words, best_world_to_test)
        sleep(2)
    else:
        line = driver.find_element(By.XPATH, f"/html/body/div/div[3]/table/tr[{x}]")
        list_td = line.find_elements(By.TAG_NAME, "td")

        letter_at_good_position = {}
        letter_at_bad_position = {}
        letter_not_here = []

        for td in list_td:
            css_class = td.get_attribute("class")
            position_td = list_td.index(td)
            letter = td.text

            if css_class == "bien-place resultat":
                letter_at_good_position[letter] = position_td
            elif css_class == "mal-place resultat":
                letter_at_bad_position[letter] = position_td
            elif css_class == "non-trouve resultat":
                letter_not_here.append(letter)

        for letter in letter_at_good_position:
            available_words = letter_at_pos(available_words, letter, letter_at_good_position[letter])

        for letter in letter_at_bad_position:
            available_words = letter_not_at_pos(available_words, letter, letter_at_bad_position[letter])

        for letter in letter_not_here:
            if letter in letter_at_good_position.keys() or letter in letter_at_bad_position.keys():
                pass
            else:
                available_words = letter_not_in(available_words, letter)

    if "Félicitations" in body.text:
        print(f"Word found in {x} shot(s)")
        done = True

    x += 1





