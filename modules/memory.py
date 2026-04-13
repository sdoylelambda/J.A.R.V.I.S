import os
import asyncio
from datetime import datetime


class AtlasMemory:
    """
    MemPalace wrapper for Atlas persistent memory.
    Stores and retrieves conversations, preferences, and facts.
    """

    def __init__(self, config: dict):
        self.config = config.get("memory", {})
        self.enabled = self.config.get("enabled", False)
        self.wing = self.config.get("wing", "atlas")
        self.palace_path = os.path.expanduser(
            self.config.get("palace_path", "~/.mempalace/palace")
        )
        self.debug = True
        self._searcher = None
        self._miner = None

        if self.enabled:
            self._init_mempalace()

    def _init_mempalace(self):
        """Initialize MemPalace searcher."""
        try:
            from mempalace.searcher import search_memories
            self._search_fn = search_memories
            print("[Memory] MemPalace initialized")
        except ImportError:
            print("[Memory] MemPalace not installed — pip install mempalace")
            self.enabled = False
        except Exception as e:
            print(f"[Memory] Init error: {e}")
            self.enabled = False

    # ── Search ────────────────────────────────────────────────────────────

    def recall(self, query: str, n: int = 3) -> str | None:
        """Search memory for relevant context."""
        if not self.enabled:
            return None
        try:
            results = self._search_fn(
                query,
                palace_path=self.palace_path,
                wing=self.wing,
                n=n
            )
            if not results:
                return None

            # format results for injection into Brain context
            parts = []
            for r in results:
                content = r.get('content', '').strip()
                source = r.get('metadata', {}).get('source', '')
                if content:
                    parts.append(f"[{source}]: {content[:300]}")

            result = "\n".join(parts)
            if self.debug:
                print(f"[Memory] Recalled {len(results)} results for: {query[:50]}")
            return result if result else None

        except Exception as e:
            print(f"[Memory] Recall error: {e}")
            return None

    # ── Store ─────────────────────────────────────────────────────────────

    def remember(self, text: str, room: str = "general") -> bool:
        """Store a memory explicitly."""
        if not self.enabled:
            return False
        try:
            from mempalace.miner import file_drawer
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_drawer(
                content=text,
                source=f"voice_memory_{timestamp}",
                wing=self.wing,
                room=room,
                palace_path=self.palace_path
            )
            print(f"[Memory] Stored: {text[:50]}")
            return True
        except Exception as e:
            print(f"[Memory] Store error: {e}")
            return False

    def remember_conversation(self, command: str, response: str) -> bool:
        """Auto-store command/response pairs."""
        if not self.enabled:
            return False
        try:
            from mempalace.miner import file_drawer
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            content = f"[{timestamp}]\nUser: {command}\nAtlas: {response}"
            file_drawer(
                content=content,
                source=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                wing=self.wing,
                room="conversations",
                palace_path=self.palace_path
            )
            return True
        except Exception as e:
            print(f"[Memory] Conversation store error: {e}")
            return False

    # ── Wake-up context ───────────────────────────────────────────────────

    def get_wake_up_context(self) -> str | None:
        """Load critical facts on startup."""
        if not self.enabled:
            return None
        try:
            import subprocess
            result = subprocess.run(
                ['mempalace', 'wake-up', '--wing', self.wing],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                print("[Memory] Wake-up context loaded")
                return result.stdout.strip()
            return None
        except Exception as e:
            print(f"[Memory] Wake-up error: {e}")
            return None

    # ── Voice command helpers ─────────────────────────────────────────────

    def format_for_speech(self, memory_text: str) -> str:
        """Clean memory text for TTS."""
        import re
        text = re.sub(r'\[.*?\]:', '', memory_text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()[:500]
