"""State persistence - saves/loads application state to disk"""

import json
import time
from pathlib import Path
from typing import Any


class StateManager:
    """Manages saving and loading application state to JSON file"""

    def __init__(self, filename: str = "app_state.json"):
        """
        Initialize state manager.
        
        Args:
            filename: Name of state file (stored in ~/.productivity_app/)
        """
        self.state_dir = Path.home() / ".productivity_app"
        self.state_file = self.state_dir / filename
        self.state_dir.mkdir(exist_ok=True)

    def save(self, data: dict[str, Any]) -> None:
        """
        Save state to disk.
        
        Args:
            data: Dictionary containing state to persist
        """
        try:
            with open(self.state_file, "w") as f:
                json.dump(data, f, indent=2)
            print(f"[StateManager] Saved state to {self.state_file}")
        except json.JSONDecodeError as e:
            print(f"[StateManager] Error saving state: {e}")

    def load(self) -> dict[str, Any]:
        """
        Load state from disk.
        
        Returns:
            Dictionary with saved state, or default state if file doesn't exist
        """
        if self.state_file.exists():
            try:
                with open(self.state_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                print(f"[StateManager] Error decoding JSON: {e}")

        # Return default state if load fails
        return {
            "goals": [],
            "inactive_goals": [],
            "timestamp": time.time()
        }
