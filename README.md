# ♠️ Master Poker Host

Program that hosts a poker tournament between python scripts.

## 📝 Protocol

To communicate with the master program the player scripts must use stdin and stdout, following the protocol descripbed below.

- `input('This input is a list newly revealed cards, if no cards were revealed the input is the letter i')`
  '14 1 2 1' would mean an ace and a 2 of the same colour

- `input('This input is a list of n latest actions (n is the number of players)')`  
  For example 'c c r200' it means that you have checked, then another player checked and then another player has raised by 200

- `input('This input is a single number standing for how much you have to call')`

- `print('c') `
  Here you print out your action 'f' - fold 'c' - check 'k' - call 'r200' - raise 200 or any other number as long as its more than the minimal bet

This is reapeated until the hand ends.
When the hand ends you are expected to take two `input()` the first being the winning player id and the second being your current bank

## 📦 Usage

To launch a tournament

```bash
python main.py
```

Player script names and their number are hard coded into the `main.py` file on line 7 and 80. These scripts have to be in the same directory as the `main.py` file.
