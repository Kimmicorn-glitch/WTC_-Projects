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

Light_Colours = ["Red", "Yellow", "Green", "Blue"]
Dark_Colours = ["Pink", "Orange", "Purple", "Blue"]


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
    print("2. Deck is placed Light side down (Draw pile), Dark side up.")
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
    print("     - Flip: All decks & hands flip to the other side")
    print()
    print("5. Draw card chains accumulate: stacked Draw 2/4 increase pick up count.")
    print()
    print("6. First player to 0 cards wins.")
    print("7. Type 'q' to quit. Opponents win immediately.\n")
    print()
    print("...Press ENTER to START...")
    input()
    clear_screen()


def grim_humor(action=None):
    messages = {
        "Draw Two": [
            "Oops. Too bad",
            "Ah double trouble. How quaint.",
            "Two extra reasons to regret playing.",
            "Enjoy the gift. Misery loves company."
        ],
        "Draw Four": [
            "Suffer, mortal",
            "Four cards, one broken friendship. Worth it.",
            "Hope you like baggage, because here’s four more.",
            "Life gives you lemons, then burns the orchard.",
            "Four strikes of misfortune. Enjoy."
        ],
        "Skip": [
            "Skipped, as is life.",
            "Missed your turn… like opportunities in life.",
            "Skipped, just like your dreams.",
            "The void says ‘next!’",
            "You weren’t important this round anyway.",
            "Skipped. Just like your responsibilities."
        ],
        "Flip": [
            "Life flips again.",
            "All is chaos. Flip, flip, flip.",
            "Your world turns upside down… literally.",
            "Perspective is overrated.",
            "Light, dark… either way, you’re losing.",
            "Flip it! Because chaos is funnier on both sides."
        ],
        "Quit": [
            "They fled. Weak.",
            "Ran from Uno. Life won’t be kinder.",
            "Cowardice is a choice… and you chose it.",
            "Exit achieved. Regret pending."
        ],
        "Reverse": [
            "Direction reversed. Chaos awaits.",
            "Direction reversed. Chaos ensues.",
            "Backwards you go, toward regret.",
            "Time flows differently for fools."
        ],
        "uno": [
            "UNO! Enjoy your fifteen seconds of power before the downfall.",
            "One card left. Don’t choke.",
            "Shout UNO, or let them catch you slacking. We don’t care."
        ],
        "win": [
            "Winner, winner. Now go touch grass.",
            "Congrats. You ruined the game for everyone else.",
            "Victory looks good on you… pity your friends won’t speak to you again."
        ],
        "invalid": [
            "Try again, genius. This isn’t a guessing game.",
            "Wrong input. Are you even playing, or just pressing buttons?",
            "That’s not a valid move. Neither is your life strategy."
        ]
    }

    if action in messages:
        print(random.choice(messages[action]))
    else:
        print(random.choice([
            "The universe laughs.",
            "Pain is optional; suffering is mandatory.",
            "Hope you like disappointment...",
            "Misfortune is compulsory. Enjoy.",
            "Another card, another tiny tragedy.",
            "Your misfortune entertains the cosmos.",
            "Fate smiles, but only because it’s cruel."
        ]))
    time.sleep(2)


def create_deck():
    values_numeric = [str(n) for n in range(1, 10)]
    actions = ["Skip", "Reverse", "Draw Two", "Flip"]

    deck = []
    for lc, dc in zip(Light_Colours, Dark_Colours):
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
            "Pink": dark_pink, "Orange": dark_orange,
            "Purple": dark_purple, "Blue": dark_blue
        }.get(colour_name, RESET)
    else:
        colour_code = {
            "Red": light_red, "Yellow": light_yellow,
            "Green": light_green, "Blue": light_blue
        }.get(colour_name, RESET)

    if card[0] == "Wild":
        return f"{wild_colour}{card[2]}{RESET}"
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
        deck.extend(discard_pile[:])
        random.shuffle(deck)
        discard_pile.clear()
        discard_pile.append(top)


def player_turn(player, hand, top_card, dark_side, deck,
                players, hands, pending_draw=0, discard_pile=None, current_colour=None):
    while True:
        show_hand(player, hand, dark_side)
        tc_colour = top_card[1] if dark_side else top_card[0]
        print(f"Top card: {colour_card_text(top_card, dark_side)}")

        if pending_draw > 0:
            print(f"Warning: You must pick up {pending_draw} cards unless you can stack a Draw card!")

        choice = input("Select card (number), 'd' to draw, or 'q' to Quit. ").strip().lower()
        if choice == "q":
            clear_screen()
            print(f"{player} resigns. Opponents rejoice!!")
            grim_humor("Quit")
            return "quit", 0, current_colour
        elif choice == "d":
            draw_stack_animation(player, max(1, pending_draw), deck, hand, players, discard_pile)
            grim_humor()
            return None, 0, current_colour
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(hand):
                card = hand[idx]
                card_colour = card[1] if dark_side else card[0]
                top_colour = top_card[1] if dark_side else top_card[0]

                # If stacking draw cards
                if pending_draw > 0:
                    if card[2] == "Draw Two":
                        pending_draw += 2
                        return hand.pop(idx), pending_draw, card_colour
                    elif card[2] == "Draw Four":
                        pending_draw += 4
                        return hand.pop(idx), pending_draw, card_colour
                    else:
                        grim_humor("invalid")
                else:
                    can_play = (card_colour == top_colour or
                                card[2] == top_card[2] or
                                card[2] == "Draw Four")

                    if can_play:
                        if card[2] == "Draw Two":
                            pending_draw += 2
                        elif card[2] == "Draw Four":
                            pending_draw += 4
                        return hand.pop(idx), pending_draw, card_colour
                    else:
                        grim_humor("invalid")
            else:
                grim_humor("invalid")
        else:
            grim_humor("invalid")


def computer_turn(player, hand, deck, top_card, dark_side,
                  hands, pending_draw, discard_pile, current_colour):
    time.sleep(1.5)
    playable = []

    i = 0
    while i < len(hand):
        card = hand[i]
        card_colour = card[1] if dark_side else card[0]

        if pending_draw > 0:
            if card[2] in ["Draw Two", "Draw Four"]:
                playable.append((i, card))
        else:
            if (card_colour == current_colour or
                card[2] == top_card[2] or
                card[2] == "Draw Four"):
                playable.append((i, card))
        i += 1

    if playable:
        idx, card = random.choice(playable)
        hand.pop(idx)
        print(f"{player} plays {colour_card_text(card, dark_side)}")
        grim_humor(card[2])

        new_pending = pending_draw
        if card[2] == "Draw Two":
            new_pending += 2
        elif card[2] == "Draw Four":
            new_pending += 4
            valid_colours = Light_Colours if not dark_side else Dark_Colours
            current_colour = random.choice(valid_colours)
            discard_pile.append((current_colour, current_colour, "Draw Four"))
            print(f"{player} chooses {current_colour} as the new colour.")
            return card, new_pending, current_colour

        card_colour = card[1] if dark_side else card[0]
        current_colour = card_colour
        return card, new_pending, current_colour
    else:
        draw_stack_animation(player, max(1, pending_draw), deck, hand, players, discard_pile)
        return None, 0, current_colour


def flip_all(hands, dark_side, deck, discard_pile):
    frames = ["[/////]", "[\\\\\\\\]", "[/////]", "[\\\\\\\\]"]
    for frame in frames:
        clear_screen()
        print("Flipping All cards... \n")
        for i in range(len(hands)):
            hand = hands[i]
            display = " | ".join([f"{frame}{colour_card_text(c, not dark_side)}{frame}" for c in hand])
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
            time.sleep(0.2)

        reshuffle(deck, discard_pile)

        if deck:
            card = deck.pop()
            hand.append(card)
            full_card = colour_card_text(card, False) + " / " + colour_card_text(card, True)
            print(f"{player} drew: {full_card}")
            time.sleep(0.2)
        else:
            print("Deck empty! No cards to draw.")

    for p in players:
        if p != player:
            print(f"{p} laughs at {player}'s misfortune. HAHAHHAAA!")
    time.sleep(1)


def main():
    show_rules()
    while True:
        try:
            num_players = int(input("Number of players (2-10): "))
            if 2 <= num_players <= 10:
                break
            else:
                print("Enter between 2 and 10 mortals.")
        except ValueError:
            print("Not a number. The void mocks you.")

    players = []
    player_types = []
    for i in range(num_players):
        player_type = input(f"Player {i+1} Enter 'h' for Human or 'c' for Computer: ").strip().lower()
        if player_type == "c":
            players.append(f"Computer{i+1}")
            player_types.append("computer")
        else:
            Name = input(f"Enter player {i+1} name: ").strip().capitalize()
            players.append(Name)
            player_types.append('human')

    hands = [[] for _ in range(num_players)]

    deck = create_deck()
    dark_side = False
    discard_pile = [deck.pop()]
    current_colour = discard_pile[-1][0] if not dark_side else discard_pile[-1][1]

    for h in hands:
        for _ in range(7):
            h.append(deck.pop())

    turn = 0
    direction = 1
    pending_draw = 0

    while True:
        current = players[turn]
        msg = f"You must pick up {pending_draw} cards or stack Draw card!" if pending_draw > 0 else None
        hotseat(current, msg)

        if player_types[turn] == "computer":
            played, new_pending, current_colour = computer_turn(
                current,
                hands[turn],
                deck,
                discard_pile[-1],
                dark_side,
                hands,
                pending_draw,
                discard_pile,
                current_colour
            )
        else:
            played, new_pending, current_colour = player_turn(
                current,
                hands[turn],
                discard_pile[-1],
                dark_side,
                deck,
                players,
                hands,
                pending_draw,
                discard_pile,
                current_colour
            )

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

            elif val in ["Draw Two", "Draw Four"]:
                print(f"{current} stacked {val}. Next player must pick up {pending_draw} cards!")
                grim_humor(val)
                if val == "Draw Four" and player_types[turn] == "human":
                    valid_colours = Light_Colours if not dark_side else Dark_Colours
                    while True:
                        new_colour = input(f"{current}, choose a new colour: ").capitalize()
                        if new_colour in valid_colours:
                            discard_pile[-1] = (new_colour, new_colour, "Draw Four")
                            current_colour = new_colour
                            break
                        print(f"Invalid colour. Choose from {', '.join(valid_colours)}.")

            elif val == "Flip":
                dark_side = flip_all(hands, dark_side, deck, discard_pile)
                grim_humor("Flip")

        if len(hands[turn]) == 0:
            clear_screen()
            print(f"{current} wins! All cards gone. Their torment ends…")
            grim_humor("win")
            break

        if len(hands[turn]) == 1:
            print(f"{current} yells UNO!!!")
            grim_humor("uno")

        turn = (turn + direction) % len(players)
        clear_screen()


if __name__ == "__main__":
    main()
