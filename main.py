import sys
from llm_engine import query_llm
from personality import Personality
from voice import listen, speak


def handle_command(command, personality):
    command = command.strip()
    parts = command.split()

    if command == "/status":
        return personality.summary()
    if command == "/memory":
        return personality.get_memory()
    if command == "/clear":
        return personality.clear_memory()  # ✅ wipe memory

    if len(parts) >= 1 and parts[0] == "/set":
        if (
            len(parts) == 5
            and parts[1] in ["honesty", "humor"]
            and parts[2] == "and"
            and parts[3] in ["honesty", "humor"]
        ):
            return personality.set_both(parts[4])

        if len(parts) == 3:
            setting, value = parts[1], parts[2]
            if setting == "humor":
                return personality.set_humor(value)
            elif setting == "honesty":
                return personality.set_honesty(value)
            elif setting == "mode":
                return personality.set_mode(value)
            else:
                return "Unknown setting."

        return "Invalid /set command format."

    return "Invalid command."


def process_input(user_input, orion_personality, voice_mode):
    orion_personality.remember(f"You: {user_input}")
    context = orion_personality.build_context(orion_personality.memory)
    final_prompt = (
        context
        + f"\nUser says: {user_input}\n"
        + "ORION response:"
    )
    ai_response = query_llm(final_prompt)
    orion_personality.remember(f"ORION: {ai_response}")

    if voice_mode:
        speak(ai_response)
    else:
        print(f"ORION: {ai_response}\n")


def start_orion():
    orion_personality = Personality(
        humor=50,
        honesty=60,
        memory_limit=40,
        mode="serious"
    )

    print("=" * 45)
    print("          ORION ONLINE")
    print("=" * 45)
    print(orion_personality.summary())
    print()
    print("Commands:")
    print("  /status               -> personality summary")
    print("  /memory               -> show conversation history")
    print("  /clear                -> wipe all memory")
    print("  /set humor <0-100>")
    print("  /set honesty <0-100>")
    print("  /set mode <serious|casual|dry>")
    print("  /voice                -> switch to voice mode")
    print("  /text                 -> switch to text mode")
    print("  exit / quit           -> shut down")
    print("=" * 45)
    print("Awaiting input...\n")

    voice_mode = False

    while True:

        # ---- VOICE MODE ----
        if voice_mode:
            print("-" * 40)
            print("Press ENTER to speak  |  type 'exit' to quit  |  type '/text' for text mode")
            trigger = input("> ").strip().lower()

            if trigger in ["exit", "quit"]:
                print("ORION: Shutting down. Goodbye.")
                sys.exit(0)

            if trigger == "/text":
                voice_mode = False
                print("Switched to text mode.\n")
                continue

            if trigger.startswith("/"):
                result = handle_command(trigger, orion_personality)
                speak(result)
                continue

            user_input = listen()

            if not user_input:
                print("ORION: Didn't catch that. Press ENTER to try again.\n")
                continue

            spoken = user_input.lower().strip().rstrip(".")
            if spoken in ["exit", "quit", "goodbye", "shut down", "shutdown"]:
                print("ORION: Shutting down. Goodbye.")
                sys.exit(0)

            process_input(user_input, orion_personality, voice_mode)

        # ---- TEXT MODE ----
        else:
            user_input = input("You: ").strip()

            if user_input.lower() in ["exit", "quit"]:
                print("ORION shutting down.")
                sys.exit(0)

            if user_input == "/voice":
                voice_mode = True
                print("ORION: Switched to voice mode.\n")
                continue

            if user_input.startswith("/"):
                result = handle_command(user_input, orion_personality)
                print(f"ORION: {result}\n")
                continue

            if not user_input:
                continue

            process_input(user_input, orion_personality, voice_mode)


if __name__ == "__main__":
    start_orion()