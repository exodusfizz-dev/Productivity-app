"""Runs backend, stores user data locally."""

import time


# Constants in seconds for clear use.
DAY = 86400
WEEK = 604800


class BackEnd:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.time = time.time()
        self.goals = []

        self.event_bus.subscribe("user_add_goal", self._save_goal)
        self.event_bus.subscribe("reset_goals", self._reset_goals)

    def step(self):
        """Called repeatedly to check if day/week has passed"""
        new_time = time.time()
        elapsed = new_time - self.time

        if elapsed > WEEK:
            self.week()
            self.time = new_time
        elif elapsed > DAY:
            self.day()
            self.time = new_time

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
        self.goals.append(data["goal"])
        print(f"[Backend] Task completed: {data}")
        self.event_bus.emit("goal_saved", {
            "message": f"Goal saved: {data['goal']}",
            "goals": self.goals
        })

    def _reset_goals(self, data):
        """Resets goals when user clicks reset goals button."""
        self.goals = []
        print(f"[Backend] Goals reset: {data}")
        self.event_bus.emit("goals_reset", {
            "message": "Goals have been reset successfully."
        })
