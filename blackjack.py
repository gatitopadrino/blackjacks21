import tkinter as tk
import random
import json
import os
import sys
from PIL import Image, ImageTk

CARD_SCALE = 0.5  # 50% size; adjust as needed

CONFIG_FILE = "window_config.json"

def center_window(root, width=700, height=500):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

def load_window_position():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f).get("geometry")
        except:
            return None
    return None

def save_window_position(root):
    geometry = root.winfo_geometry()
    with open(CONFIG_FILE, 'w') as f:
        json.dump({"geometry": geometry}, f)

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_scaled_card_image(rank, suit):
    # Map suits from symbols to letters
    suit_map = {'♥': 'H', '♦': 'D', '♣': 'C', '♠': 'S'}
    if rank == 'back':
        filename = "back.png"
    else:
        filename = f"{rank}{suit_map[suit]}.png"
    path = get_resource_path(os.path.join("cards", filename))

    # Load and scale image with Pillow
    image = Image.open(path)
    w, h = image.size
    image = image.resize((int(w * CARD_SCALE), int(h * CARD_SCALE)), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(image)

def create_deck():
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['♥', '♦', '♣', '♠']
    return [(r, s) for r in ranks for s in suits]

def card_value(card):
    rank = card[0]
    if rank in ['J','Q','K']:
        return 10
    elif rank == 'A':
        return 11
    else:
        return int(rank)

def hand_value(hand):
    total = sum(card_value(c) for c in hand)
    aces = sum(1 for c in hand if c[0] == 'A')
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

class BlackjackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")

        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        self.player_card_images = []
        self.dealer_card_images = []

        self.create_widgets()
        self.new_game()

    def create_widgets(self):
        dealer_frame = tk.LabelFrame(self.root, text="Dealer", padx=10, pady=10)
        dealer_frame.pack(padx=10, pady=5)
        self.dealer_cards_lbl = tk.Frame(dealer_frame)
        self.dealer_cards_lbl.pack()
        self.dealer_value_lbl = tk.Label(dealer_frame, text="Value: 0", font=('Arial', 14))
        self.dealer_value_lbl.pack()

        player_frame = tk.LabelFrame(self.root, text="Player", padx=10, pady=10)
        player_frame.pack(padx=10, pady=5)
        self.player_cards_lbl = tk.Frame(player_frame)
        self.player_cards_lbl.pack()
        self.player_value_lbl = tk.Label(player_frame, text="Value: 0", font=('Arial', 14))
        self.player_value_lbl.pack()

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        self.hit_btn = tk.Button(button_frame, text="Hit", width=10, command=self.hit)
        self.hit_btn.pack(side='left', padx=5)
        self.stand_btn = tk.Button(button_frame, text="Stand", width=10, command=self.stand)
        self.stand_btn.pack(side='left', padx=5)
        self.new_game_btn = tk.Button(button_frame, text="New Game", width=10, command=self.new_game)
        self.new_game_btn.pack(side='left', padx=5)

        self.result_lbl = tk.Label(self.root, text="", font=('Arial', 16), fg="blue")
        self.result_lbl.pack(pady=10)

    def new_game(self):
        self.deck = create_deck()
        random.shuffle(self.deck)
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.result_lbl.config(text="")
        self.hit_btn.config(state='normal')
        self.stand_btn.config(state='normal')
        self.update_display()

    def update_display(self, reveal_dealer=False):
        for widget in self.dealer_cards_lbl.winfo_children():
            widget.destroy()
        self.dealer_card_images = []
        cards = self.dealer_hand if reveal_dealer else [self.dealer_hand[0], ('back', 'back')]
        for rank, suit in cards:
            img = load_scaled_card_image(rank, suit)
            self.dealer_card_images.append(img)
            lbl = tk.Label(self.dealer_cards_lbl, image=img)
            lbl.pack(side='left', padx=5)

        for widget in self.player_cards_lbl.winfo_children():
            widget.destroy()
        self.player_card_images = []
        for rank, suit in self.player_hand:
            img = load_scaled_card_image(rank, suit)
            self.player_card_images.append(img)
            lbl = tk.Label(self.player_cards_lbl, image=img)
            lbl.pack(side='left', padx=5)

        dealer_val = hand_value(self.dealer_hand) if reveal_dealer else card_value(self.dealer_hand[0])
        self.dealer_value_lbl.config(text=f"Value: {dealer_val}")
        player_val = hand_value(self.player_hand)
        self.player_value_lbl.config(text=f"Value: {player_val}")

    def hit(self):
        self.player_hand.append(self.deck.pop())
        player_val = hand_value(self.player_hand)
        self.update_display()
        if player_val > 21:
            self.result_lbl.config(text="Bust! You lose.")
            self.hit_btn.config(state='disabled')
            self.stand_btn.config(state='disabled')
            self.update_display(reveal_dealer=True)

    def stand(self):
        self.hit_btn.config(state='disabled')
        self.stand_btn.config(state='disabled')
        while hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())
        self.update_display(reveal_dealer=True)
        self.determine_winner()

    def determine_winner(self):
        player_val = hand_value(self.player_hand)
        dealer_val = hand_value(self.dealer_hand)
        if dealer_val > 21:
            self.result_lbl.config(text="Dealer busts! You win!")
        elif player_val > dealer_val:
            self.result_lbl.config(text="You win!")
        elif player_val == dealer_val:
            self.result_lbl.config(text="Push (tie).")
        else:
            self.result_lbl.config(text="Dealer wins.")

if __name__ == "__main__":
    root = tk.Tk()
    saved_geometry = load_window_position()
    if saved_geometry:
        root.geometry(saved_geometry)
    else:
        center_window(root, 700, 500)

    app = BlackjackApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (save_window_position(root), root.destroy()))
    root.mainloop()
