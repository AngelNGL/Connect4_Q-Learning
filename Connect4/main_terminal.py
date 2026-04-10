from Connect4.play_terminal import play_menu
from Connect4.AI_cpu.train_data import qtables_exist
from Connect4.AI_cpu.config import get_epsilon, set_epsilon


def rng_menu():
    epsilon = get_epsilon()
    print(f"\nCurrent epsilon value: {epsilon}")
    print("This value is the probability that the CPU makes a random move.\nUse a value between 0.0 and 1.0")
    new_value = input("Enter new epsilon value (default: 0.0): ").strip()
    try:
        epsilon = float(new_value)
        if not 0.0 <= epsilon <= 1.0:
            raise ValueError
    except ValueError:
        print("<Invalid option>")
        return
    set_epsilon(epsilon)
    print(f"RNG updated to epsilon: {epsilon}")

def main():
    qtables_exist()
    while True:
        print("\n~~~~ Connect 4: Q-Learning ~~~~")
        print("1) Play")
        print("2) Set RNG")
        print("3) Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            play_menu()
        elif choice == "2":
            rng_menu()
        elif choice == "3":
            print("Thanks for playing!")
            break
        else:
            print("<Invalid option>")


if __name__ == "__main__":
    main()
