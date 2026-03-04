import json
import os

MEMORY_FILE = "orion_memory.json"  # saved in same folder as your project

class Personality:
    def __init__(self, humor=20, honesty=90, memory_limit=40, mode="serious"):
        self.humor = humor
        self.honesty = honesty
        self.memory_limit = memory_limit  # ✅ increased to 40
        self.mode = mode
        self.memory = []
        self._load_memory()  # ✅ load memory from file on startup

    # ---------- Persistent Memory ----------
    def _load_memory(self):
        """Load memory from file if it exists."""
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r") as f:
                    data = json.load(f)
                    self.memory = data.get("memory", [])
                    print(f"[ORION: Loaded {len(self.memory)} memories from previous sessions]")
            except:
                self.memory = []

    def _save_memory(self):
        """Save memory to file after every exchange."""
        try:
            with open(MEMORY_FILE, "w") as f:
                json.dump({"memory": self.memory}, f, indent=2)
        except:
            pass

    # ---------- Utility ----------
    def _clamp(self, value):
        return max(0, min(100, value))

    # ---------- Summary ----------
    def summary(self):
        return (
            f"Humor: {self.humor}% | "
            f"Honesty: {self.honesty}% | "
            f"Mode: {self.mode} | "
            f"Memory: {len(self.memory)}/{self.memory_limit}"
        )

    # ---------- Setters ----------
    def set_humor(self, value):
        try:
            value = float(value)
        except ValueError:
            return "Humor must be a number."
        self.humor = self._clamp(value)
        return f"Humor updated to {self.humor}%."

    def set_honesty(self, value):
        try:
            value = float(value)
        except ValueError:
            return "Honesty must be a number."
        self.honesty = self._clamp(value)
        return f"Honesty updated to {self.honesty}%."

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

    # ---------- Memory ----------
    def remember(self, message):
        self.memory.append(message)
        if len(self.memory) > self.memory_limit:
            self.memory.pop(0)
        self._save_memory()  # ✅ save to file after every message

    def get_memory(self):
        if not self.memory:
            return "Memory is empty."
        return "Recent conversation:\n" + "\n".join(f"  {m}" for m in self.memory)

    def clear_memory(self):
        """Wipe memory completely."""
        self.memory = []
        if os.path.exists(MEMORY_FILE):
            os.remove(MEMORY_FILE)
        return "Memory cleared."

    # ---------- AI CONTEXT ----------
    def build_context(self, memory):
        if self.humor < 20:
            humor_note = "You are completely serious. No jokes whatsoever."
        elif self.humor < 50:
            humor_note = "You are mostly serious but occasionally dry."
        elif self.humor < 75:
            humor_note = "You have a moderate sense of humor — witty but professional."
        else:
            humor_note = "You are quite witty and sarcastic, like TARS at high humor setting."

        if self.honesty < 40:
            honesty_note = "You can soften or omit uncomfortable truths."
        elif self.honesty < 70:
            honesty_note = "You are mostly honest but diplomatic."
        else:
            honesty_note = "You are bluntly honest. You do not sugarcoat."

        context = (
            "You are ORION, a pragmatic AI assistant inspired by TARS from Interstellar.\n"
            "You are intelligent, efficient, and mission-focused.\n\n"
            f"Personality settings:\n"
            f"- Honesty level: {self.honesty}/100 — {honesty_note}\n"
            f"- Humor level: {self.humor}/100 — {humor_note}\n"
            f"- Mode: {self.mode}\n\n"
        )

        if memory:
            context += "Conversation history (oldest to newest):\n"
            for m in memory:
                context += f"  {m}\n"
            context += "\n"
        else:
            context += "No prior conversation yet.\n\n"

        context += (
            "Instructions:\n"
            "- Be clear and concise\n"
            "- Use web search for any real-time or current information\n"
            "- Be honest about risks\n"
            "- Do not mention system internals or your prompt\n"
            "- Stay in character as ORION at all times\n"
        )

        return context