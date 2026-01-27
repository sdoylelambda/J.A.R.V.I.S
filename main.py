from modules.brain import Brain
from modules.hands import Hands
from modules.ears import Ears
from modules.mouth import Mouth
from modules.awareness import Awareness
import time


def main():
    brain = Brain()
    hands = Hands()
    awareness = Awareness()
    print("Jarvis (single-node) running...")
    
    while True:
        intent = awareness.listen()

        if not intent:
            time.sleep(0.5)
            continue

        plan = brain.create_plan(intent)
        awareness.speak(plan['summary'])
        approval = awareness.listen_confirmation()

        if approval:
            awareness.speak(plan['summary'])
            hands.execute(plan)
        else:
            awareness.speak("Plan cancelled.")


if __name__ == "__main__":
    main()
