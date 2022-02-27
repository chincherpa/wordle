import os
from collections import Counter
import random
from rich import box, print
from rich.table import Table
from rich.live import Live
from woerter import words
from letters import letters


dPhrases = {
  0: "Ohoh, letzter Versuch!\nWas nimmst du dieses Mal?",
  1: "Ok, noch 1 Versuch!\nWas nimmst du dieses Mal?",
  2: "Hmmm, noch 2 Versuche!\nWas nimmst du dieses Mal?",
  3: "Aaaah, noch 3 Versuche!\nWas nimmst du dieses Mal?",
  4: "Hmm, ok, noch 4 Versuche!\nWas nimmst du dieses Mal?",
  5: "Ui, noch 5 Versuche!\nWas nimmst du dieses Mal?",
  6: "Alsooo, leg los! Dein erster Versuch",
}

iNum_of_chars = int(input('\n\nWieviele Buchstaben?:\t'))

print(f'Anzahl der Wörter vorher: {len(words)}')
words = [wort for wort in words if len(wort) == iNum_of_chars]
print(f'Anzahl der Wörter danach: {len(words)}')


class Wordle:
  def __init__(self):
    self.words: list = words
    self.sWordle: str = self._select_word()
    # input(f'{self.sWordle = } - weiter...')

    self.max_chars = iNum_of_chars
    self.user_guess: str = ""

  def get_user_guess(self, remaining: int = None):
    self.user_guess = input(f"\n{dPhrases[remaining]}:\n\n").lower()

    if len(self.user_guess) != self.max_chars:
      print(f'\n[red]--- Ooooppssss, {self.user_guess.upper()} hat nicht {self.max_chars} Buchstaben! ---\n')
      self.get_user_guess(remaining=remaining)
    elif self.user_guess not in self.words:
      print('\n[yellow]--- Oh, schade! Das Wort kommt nicht vor!!!! ---\n')
      self.get_user_guess(remaining=remaining)

  def _select_word(self):
    random_index = int(random.random() * len(self.words))
    return self.words[random_index].lower()

  def is_correct_guess(self):
    return self.sWordle.lower() == self.user_guess.lower()

  def check_word(self):
    user_guess_validated = []

    # Stings converted to list
    user_guess = list(self.user_guess)
    lWordle = list(self.sWordle)

    correct_count = dict(Counter(lWordle))

    # Check for exact match
    for idx, char in enumerate(user_guess):
      temp = {'letter': char, 'index': idx}
      if char == lWordle[idx]:
        correct_count[char] -= 1
        temp['color'] = 'green'
        user_guess_validated.append(temp)
      else:
        temp['color'] = 'grey84'
        user_guess_validated.append(temp)

    # Check for letter presence in the correct word
    for idx, char in enumerate(user_guess):
      if char in lWordle:
        # Exceute only when there is a remaining letter on the correct word
        if correct_count[char] != 0:
          # If its already found to be an exact match, ignore it else, change it to orange1
          if user_guess_validated[idx]['color'] != "green":
            user_guess_validated[idx]['color'] = 'orange1'
            # Once Changed reduce the count
            correct_count[char] -= 1
          # If the count is negative, automatically assume the letter is not present.
          elif correct_count[char] < 1:
            user_guess_validated[idx]['color'] = 'grey84'

    # Check if the word is correct directly
    if self.is_correct_guess():
      return True, user_guess_validated

    return False, user_guess_validated


def clear():
  if os.name == 'nt':
    _ = os.system('cls')
  else:
    _ = os.system('clear')


def main():
  puzzle = Wordle()
  table = Table(show_header=False, box=box.ROUNDED)
  for _ in range(iNum_of_chars):
    table.add_column(max_width=13)
  print(table)

  iMax_guesses = 6
  iCounter = 0
  dGuesses = {
    0: None,
    1: None,
    2: None,
    3: None,
    4: None,
    5: None,
  }

  while iCounter < iMax_guesses:
    iRemaining_guesses = iMax_guesses - iCounter
    puzzle.get_user_guess(remaining=iRemaining_guesses)
    status, result = puzzle.check_word()
    dGuesses[iCounter] = result
    clear()
    with Live(table):
      msg_row = [f'[black on {i["color"]}] {letters[i["letter"]]} ' for i in result]
      table.add_row(*msg_row)
    if status:
      iCounter = iMax_guesses
      print('\n :thumbs_up: Wow, du hast es!! :thumbs_up:\n')
    else:
      iCounter += 1

  if not status:
    print(f'\n☹️  Das Wordle war: {puzzle.sWordle.upper()}\n\n')


if __name__ == "__main__":
  main()
