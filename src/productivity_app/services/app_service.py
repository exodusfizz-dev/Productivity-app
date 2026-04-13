"""Runs backend, stores user data locally."""

import time
from productivity_app.services.persistence import StateManager
from .backend_state import BackendState


# Constants in seconds for clear use.
DAY = 86400
WEEK = 604800


class BackEnd:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.persistence = StateManager()

        state = self.persistence.load()
        self.state = BackendState(
            goals=state["goals"],
            inactive_goals=state["inactive_goals"],
            timestamp=state["timestamp"]
        )

        self.event_bus.subscribe("user_add_goal", self._save_goal)
        self.event_bus.subscribe("reset_goals", self._reset_goals)

        self.event_bus.subscribe("user_add_inactive_goal", self._save_inactive_goal)
        self.event_bus.subscribe("reset_inactive_goals", self._reset_inactive_goals)

    def step(self):
        """Called repeatedly to check if day/week has passed"""
        new_time = time.time()
        elapsed = new_time - self.state.timestamp

        if elapsed > WEEK:
            self.week()
            self.state.timestamp = new_time
        elif elapsed > DAY:
            self.day()
            self.state.timestamp = new_time


        self._persist_state()

    def _persist_state(self):
        """Save current state to disk"""
        self.persistence.save({
            "timestamp": self.state.timestamp,
            "goals": self.state.goals,
            "inactive_goals": self.state.inactive_goals
        })

    def day(self):
        """Called when a day has passed"""
        print("[Backend] Day event triggered")
        self.event_bus.emit("day_completed", {
            "message": "Day cycle completed",
        })

    def week(self):
        """Called when a week has passed"""
        print("[Backend] Week event triggered")
        self.event_bus.emit("week_completed", {
            "message": "A week has passed. Set new goals."
        })

    def _save_goal(self, data):
        """Saves goals when a user inputs goals into frontend."""
        self.state.goals.append(data["goal"])
        print(f"[Backend] Task completed: {data}")
        self._persist_state()
        self.event_bus.emit("goal_saved", {
            "message": f"Goal saved: {data['goal']}",
            "goals": self.state.goals
        })

    def _reset_goals(self, data):
        """Resets goals when user clicks reset goals button."""
        self.state.goals = []
        print(f"[Backend] Goals reset: {data}")
        self._persist_state()
        self.event_bus.emit("goals_reset", {
            "message": "Goals have been reset successfully.",
            "goals": list(self.state.goals)
        })

    def _save_inactive_goal(self, data):
        """Saves an inactive goal"""
        self.state.inactive_goals.append(data["goal"])
        print(f"[Backend] Inactive goal saved: {data}")
        self._persist_state()
        self.event_bus.emit("inactive_goal_saved", {
            "message": f"Inactive goal saved: {data['goal']}",
            "inactive_goals": list(self.state.inactive_goals)
        })

    def _reset_inactive_goals(self, data):
        """Resets inactive goals"""
        self.state.inactive_goals = []
        print(f"[Backend] Inactive goals reset: {data}")
        self._persist_state()
        self.event_bus.emit("inactive_goals_reset", {
            "message": "Inactive goals have been reset.",
            "inactive_goals": list(self.state.inactive_goals)
        })
