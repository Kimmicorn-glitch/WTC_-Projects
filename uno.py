import random
import time

light_red = "\033[91m"
light_yellow = "\033[93m"
light_green = "\033[92m"
light_blue = "\033[94m"
dark_pink = "\033[95m"
dark_purple = "\033[35m"
dark_blue = "\033[34m"
dark_orange = "\033[38;5;208m"
wild_colour = "\033[97m"
RESET = "\033[0m"

Light_Colours = ["Red","Yellow","Green","Blue"]
Dark_Colours = ["Pink","Orange","Purple","Blue"]

def clear_screen():
    print("\033c", end="")

def show_rules():
    clear_screen()
    print("Welcome to Uno Flip: Grim Edition!\n")
    print("GAME RULES:")
    print("1. Each player gets 7 dual-sided cards (LIGHT + DARK)")
    print("     - Light side colours: Red, Yellow, Green, Blue")
    print("     - Dark side colours: Pink, Orange, Purple, Blue")
    print()
    print("2. Deck is placed Light side down(Draw pile), Dark side faces up.")
    print("   First card turned for Discard pile, light side up")
    print()
    print("3. On your turn, you must:")
    print("     - Play a card that matches colour or value of the top discard card")
    print("     - OR play Draw Four")
    print("     - OR draw one card if you can't play.")
    print()
    print("4. Special cards:")
    print("     - Skip: Next player loses turn")
    print("     - Reverse: Direction changes")
    print("     - Draw 2: Next player picks up 2 cards")
    print("     - Draw 4: Next player picks up 4 cards, choose a new colour")
    print("     - Flip: all Decks flip & all players' cards flip to the other side")
    print()
    print("5. Draw card chains accumulate: stacked Draw 2/4 increase pick up count.")
    print()
    print("6. First player to 0 cards wins.")
    print("7. Type 'q' to quit. Opponents win immediately.\n")
    print()
    print("...Press ENTER to START...")


def grim_humor(action=None):
    messages = {
        "Draw Two": "Oops. Too bad",
        "Draw Four": "Suffer, mortal",
        "Skip": "Skipped, as is life.",
        "Flip": "life flips again.",
        "Quit": "They fled. Weak.",
        "Reverse": "Direction reversed. chaos awaits"
    }
    if action in messages:
        print(messages[action])
    else:
        print(random.choice([
            "The universe laughs.",
            "Pain is optional; suffering is mandatory.",
            "Hope you like disappointment...",
            "Your misfortune entertains the cosmos."
        ]))
    time.sleep(2.5)


def create_deck():
    light_colours = Light_Colours
    dark_colours = Dark_Colours
    values_numeric = [str(n) for n in range(1, 10)]
    actions = ["Skip", "Reverse", "Draw Two", "Flip"]

    deck = []
    for lc, dc in zip(light_colours, dark_colours):
      
        deck.append((lc, dc, "0"))
        
        for v in values_numeric:
            deck.append((lc, dc, v))
            deck.append((lc, dc, v))
        
        for a in actions:
            deck.append((lc, dc, a))
            deck.append((lc, dc, a))

    
    for _ in range(4):
        deck.append(("Wild", "Wild", "Draw Four"))

    random.shuffle(deck)
    return deck

def colour_card_text(card, dark_side):
    colour_name = card[1] if dark_side else card[0]
    
    if dark_side:    
        colour_code = { 
            "Pink": dark_pink, "Orange": dark_orange, "Purple": dark_purple, "Blue": dark_blue
        }.get(colour_name,RESET)
    else:
        colour_code = {
            "Red": light_red, "Yellow": light_yellow, "Green": light_green, "Blue": light_blue
        }.get(colour_name,RESET)
    
    if card[0] == "Wild":
        return f"{wild_colour}{card[2]}{REST}"
    return f"{colour_code}{colour_name} {card[2]}{RESET}"


def show_hand(player, hand, dark_side):
    side_name = "Dark" if dark_side else "Light"
    print(f"{player}'s hand ({side_name} side, {len(hand)} cards): ")
    cards_display = []
    idx = 1 
    for card in hand:
        cards_display.append(f"{idx}: {colour_card_text(card, dark_side)}")
        idx += 1
    print(" | ".join(cards_display))
    print()

def hotseat(player, message=None):
    clear_screen()
    print(f"Hotseat!!! {player}, Your Turn...")
    if message:
        print(message)
    input("...Press ENTER when ready...")
    clear_screen()

def reshuffle(deck, discard_pile):
    if not deck and len(discard_pile) > 1:
        top = discard_pile.pop()
        for c in discard_pile:
            deck.append(c)
        random.shuffle(deck)
        discard_pile.clear()
        discard_pile.append(top)


def player_turn(player, hand, top_card, dark_side, deck, players, hands, pending_draw=0, discard_pile=None):
    while True:
        show_hand(player,hand,dark_side)
        tc_colour = top_card[1] if dark_side else top_card[0]
        print(f"Top card: {colour_card_text(top_card, dark_side)}")

        if pending_draw > 0:
            print(f"Warning: You must pick up {pending_draw} cards unless you can stack a Draw card!")
        choice = input("Select card (number), 'd' to draw, or 'q' to Quit. ").strip().lower()
        if choice == "q":
            clear_screen()
            print(f"{player} resigns. Opponents rejoice!!")
            grim_humor("Quit")
            return "quit", 0
        elif choice == "d":
            draw_stack_animation(player, max(1, pending_draw), deck, hand, players, discard_pile)
            grim_humor()
            return None, 0
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(hand):
                card = hand[idx]
                card_colour = card[1] if dark_side else card[0]
                top_colour = top_card[1] if dark_side else top_card[0]
                can_play = card_colour == top_colour or card[2] == top_card[2] or card[2] == "Draw Four"
                
                if can_play:
                    if card[2] == "Draw Two":
                        pending_draw += 2
                    elif card[2] == "Draw Four":
                        pending_draw += 4
                    return hand.pop(idx), pending_draw
                else:
                    print(f"Cannot play card {choice}. Must match colour or value.")
            else:
                print(f"Invalid card number {choice}. Use 1 to {len(hand)}.")
        else:
            print("Invalid input. The abyss mocks your typing.")

def computer_turn(player, hand,deck,dark_side,hands,pending_draw,discard_pile,current_colour):
    time.sleep(1.5)
    playable = []
    i = 0
    while i < len(hand):
        card = hand[i]
        card_colour = card[i] if dark_side else card[0]
        can_play = (card_colour == current_colour or card[2] == top_card[2] or card[0] == "Wild")
        if pending_draw > 0 and card[2] not in ["Draw Two","Draw Four"]:
            pass
        elif can_play:
            playable.append((i,card))
        i += 1
        if playable:
            idx,card = random.choice(player)
            hand.pop(idx)
            print(f"{player} plays {colour_card_text(card, dark_side)}")
            grim_humor()
            if card[2] == "Draw Two":
                pending_draw += 2
                current_colour = card[i] if dark_side else card[0]
            elif card[2] == "Draw Four":
                pending_draw += 4
                valid_colours = Light_Colours if not dark_side else Dark_Colours 
                current_colour = random.choice(valid_colours)
            elif card[2] == "Flip":
                current_colour = card[1] if dark_side else card[0]
            else:
                current_colour = card[1] if dark_side else card[0]
            return card,pending_draw,current_colour
        else:
            draw_stack_animation(player, max(1,pending_draw)deck,hand,players,discard_pile)
            return None,0,current_colour

def flip_all(hands, dark_side, deck, discard_pile):
    frames = ["[/////]", "[\\\\\\\\]", "[/////]", "[\\\\\\\\]"]
    for frame in frames:
        clear_screen()
        print("Flipping All cards... \n")
        for i, hand in enumerate(hands):
            display = " | ".join([f"{frame}{colour_card_text(c,not dark_side)}{frame}" for c in hand])
            print(f"Player {i+1}: {display}")
        time.sleep(0.75)
    dark_side = not dark_side
    clear_screen()
    print(f"All cards flipped. Now showing {'Dark' if dark_side else 'Light'} side.\n")
    time.sleep(1.5)
    return dark_side

def draw_stack_animation(player, pending_draw, deck, hand, players, discard_pile):
    print(f"{player} must pick up {pending_draw} cards! The pile looms...")
    
    for i in range(pending_draw):
        
        for frame in ["*     ", " *    ", "   *   ", "    * ", "     *", "THUD***"]:
            clear_screen()
            print(f"{player} picks up card {i+1}/{pending_draw}: {frame}")
            print("Pile " + "🂠" * (i+1))
            time.sleep(0.5)
        
        reshuffle(deck, discard_pile)
        
        if deck:
            card = deck.pop()
            hand.append(card)
            full_card = colour_card_text(card, False) + " / " + colour_card_text(card, True)
            print(f"{player} drew: {full_card}")
            time.sleep(0.3)
        else:
            print("Deck empty! No cards to draw.")
    
    for p in players:
        if p != player:
            print(f"{p} laughs at {player}'s misfortune. HAHAHHAAA!")
    time.sleep(2)
           

def main():
    show_rules()
    while True:
        try:
            num_players = int(input("Number of player (2-10): "))
            if 2 <= num_players <= 10:
                break
            else:
                print("Enter between 2 and 10 mortals.")
        except ValueError:
            print("Not a number. The void mocks you.")
    
    players = [input(f"Enter Player {i+1} name: ").strip() for i in range(num_players)]
    hands = [[]for _ in range(num_players)]

    deck = create_deck()
    discard_pile = [deck.pop()]

    for h in hands:
        for _ in range(7):
            h.append(deck.pop())

    turn = 0
    direction = 1
    dark_side = False
    pending_draw = 0

    while True:
        current = players[turn]
        msg = f"You must pick up {pending_draw} cards or stack Draw card!" if pending_draw > 0 else None
        hotseat(current, msg)
        played, new_pending = player_turn(current, hands[turn], discard_pile[-1], dark_side, deck, players, hands, pending_draw, discard_pile)
        pending_draw = new_pending

        if played == "quit":
            for i in range(len(players)):
                if i != turn:
                    print(f"{players[i]} wins!! {current} fled like a coward.")
            break
        
        if played:
            discard_pile.append(played)
            val = played[2]

            if val == "Skip":
                turn = (turn + direction) % len(players)
                print(f"{players[turn]} skipped. Grim fate smiles...")
                grim_humor("Skip")
                time.sleep(1.5)

            elif val == "Reverse":
                direction *= -1
                print("Direction Reversed!")
                grim_humor("Reverse")
                time.sleep(1.5)

            elif val in ["Draw Two","Draw Four"]:
                print(f"{current} stacked {val}. Next player must pick up {pending_draw} cards!")
                grim_humor(val)
                if val == "Draw Four":
                    valid_colours = Light_Colours if not dark_side else Dark_Colours
                    while True:
                        new_colour = input(f"{current}, choose a new colour: ").capitalize()
                        if new_colour in valid_colours:
                            discard_pile[-1] = (new_colour, new_colour, "Draw Four")
                            break
                        print(f"Invalid colour. Choose from {', '.join(valid_colours)}.")
                                    

            elif val == "Flip":
                dark_side = flip_all(hands, dark_side, deck, discard_pile)
                grim_humor("Flip")

        if len(hands[turn]) == 0:
            clear_screen()
            print(f"{current} wins! All cards gone. Their torment ends…")
            break

        turn = (turn + direction) % len(players)
        clear_screen()

if __name__ == "__main__":
    main()
