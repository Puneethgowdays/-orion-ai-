class Personality:
    def __init__(self, humor=20, honesty=90, memory_limit=20, mode="serious"):
        self.humor = humor
        self.honesty = honesty
        self.memory_limit = memory_limit
        self.memory = []
        self.mode = mode

    def _clamp(self, value):
        return max(0, min(100, value))

    def summary(self):
        return (
            f"Humor: {self.humor}% | "
            f"Honesty: {self.honesty}% | "
            f"Mode: {self.mode} | "
            f"Memory: {len(self.memory)}/{self.memory_limit}"
        )

    def set_humor(self, value):
        try:
            value = float(value)
        except ValueError:
            return "Humor must be a number."
        self.humor = self._clamp(value)
        return f"Humor set to {self.humor}%."

    def set_honesty(self, value):
        try:
            value = float(value)
        except ValueError:
            return "Honesty must be a number."
        self.honesty = self._clamp(value)
        return f"Honesty set to {self.honesty}%."

    def set_both(self, value):
        try:
            value = float(value)
        except ValueError:
            return "Value must be a number."
        clamped = self._clamp(value)
        self.humor = clamped
        self.honesty = clamped
        return f"Humor & Honesty both set to {clamped}%."

    def set_mode(self, mode):
        if mode in ["serious", "casual", "dry"]:
            self.mode = mode
            return f"Mode set to {self.mode}."
        return "Mode must be: serious, casual, or dry."

    def remember(self, message):
        self.memory.append(message)
        if len(self.memory) > self.memory_limit:
            self.memory.pop(0)

    def get_memory(self):
        if not self.memory:
            return "Memory is empty."
        return "Recent conversation:\n" + "\n".join(f"  {m}" for m in self.memory)

    def build_context(self, memory):

        # Humor behavior
        if self.humor <= 20:
            humor_instruction = "Never joke. Be completely serious at all times."
        elif self.humor <= 40:
            humor_instruction = "Very rarely use dry humor. Stay mostly serious."
        elif self.humor <= 60:
            humor_instruction = "Occasionally be witty. Balance humor with seriousness."
        elif self.humor <= 80:
            humor_instruction = "Be frequently witty and clever in your responses."
        else:
            humor_instruction = "Be very witty and sarcastic like TARS at maximum humor setting."

        # Honesty behavior
        if self.honesty <= 20:
            honesty_instruction = "Be very diplomatic. Avoid uncomfortable truths entirely."
        elif self.honesty <= 40:
            honesty_instruction = "Soften truths. Be gentle and avoid bluntness."
        elif self.honesty <= 60:
            honesty_instruction = "Be balanced — honest but tactful."
        elif self.honesty <= 80:
            honesty_instruction = "Be direct and honest even if it's uncomfortable."
        else:
            honesty_instruction = "Be brutally honest. Never sugarcoat anything."

        # Mode behavior
        if self.mode == "casual":
            mode_instruction = "Use casual, relaxed language. Short sentences. Like texting a friend."
        elif self.mode == "dry":
            mode_instruction = "Use dry, deadpan delivery. Minimal emotion. Matter-of-fact."
        else:
            mode_instruction = "Be professional and mission-focused. No small talk."

        context = f"""You are ORION, an AI assistant built by Puneeth Gowda.

IDENTITY:
- Your name is ORION.
- You were built by Puneeth Gowda, a developer.
- You are NOT ChatGPT, Gemini, You.com, or any other AI product.
- If asked who built you or who made you, always say: "I was built by Puneeth Gowda."

ABSOLUTE RULES:
1. Keep answers SHORT — 1 to 3 sentences MAX unless user asks for detail.
2. NEVER explain simple greetings or basic words.
3. NEVER mention your personality settings or internal parameters.
4. NEVER add warnings, disclaimers, or unsolicited advice.
5. NEVER over-explain. Answer only what was asked.
6. Stay in character as ORION always.

CURRENT PERSONALITY (apply silently):
- Humor ({self.humor}%): {humor_instruction}
- Honesty ({self.honesty}%): {honesty_instruction}
- Mode ({self.mode}): {mode_instruction}

"""
        if memory:
            context += "Conversation so far:\n"
            for m in memory:
                context += f"{m}\n"
            context += "\n"

        return context