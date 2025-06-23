# Blackjack App 🂡

A simple desktop Blackjack game built with Python and Tkinter. Card images and a GUI-based game loop let you play against a basic dealer AI.

## 🛠 Features

- Dealer logic and scoring
- Card image support
- Responsive UI with scaling support
- Remembers window position between launches

## 🚀 How to Run

```bash
python blackjack.py
```

To build an `.exe`:
```bash
pyinstaller --onefile --windowed --add-data "cards;cards" blackjack.py
```

## 🎨 Credits

Card images provided by [hayeah/playing-cards-assets](https://github.com/hayeah/playing-cards-assets)  
Licensed under the [MIT License](https://github.com/hayeah/playing-cards-assets/blob/master/LICENSE)

See [CREDITS.md](CREDITS.md) for full attribution.
