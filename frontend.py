"""Frontend UI using tkinter"""

import tkinter as tk
from tkinter import messagebox
from inputs import InputDialog


class FrontEnd:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.window = tk.Tk()
        self.window.title("Productivity App")
        self.window.geometry("600x400")

        self.status_label = tk.Label(
            self.window,
            text="Status: Waiting...",
            font=("Arial", 12),
            wraplength=500
        )
        self.goals_label = tk.Label(
            self.window,
            text="Your goals will appear here. Recommend setting 3-5 goals per week.",
            font=("Arial", 12),
            wraplength=500
        ) # TODO: Turn into dropdown list to allow compacting of gui.

        self.status_label.pack(pady=20)
        self.goals_label.pack(pady=20)

        self.add_goal = tk.Button(
            self.window,
            text="Add goal",
            command=self._on_add_goal,
            font=("Arial", 11),
            padx=20,
            pady=10
        )
        self.reset_goals = tk.Button(
            self.window,
            text="Reset goals",
            command=self._on_reset_goals,
            font=("Arial", 11),
            padx=20,
            pady=10
        )
        self.toggle_goals_button = tk.Button(
            self.window,
            text="Toggle goals visibility",
            command=self.toggle_goals_visibility,
            font=("Arial", 11),
            padx=10,
            pady=5
        )


        self.add_goal.pack(pady=10)
        self.reset_goals.pack(pady=10)
        self.toggle_goals_button.pack(pady=10)


        self.event_bus.subscribe("day_completed", self._on_day_completed)
        self.event_bus.subscribe("week_completed", self._on_week_completed)
        self.event_bus.subscribe("goal_saved", self._on_successful_save_goal)
        self.event_bus.subscribe("goals_reset", self._on_successful_reset_goals)

        print("[Frontend] UI initialized")

    def _on_add_goal(self):
        """Called when user clicks add goal button"""

        goal = self.get_input(message="Add 1 goal.")
        if goal is not None:
            self.event_bus.emit("user_add_goal", {
                "goal": goal,
            })

    def _on_successful_save_goal(self, data):
        """Called when backend emits 'goal_saved'."""
        print(f"[Frontend] Received goal_saved: {data}")
        self.status_label.config(text=f"✓ {data['message']}")
        goals = "\n".join(data["goals"])
        self.goals_label.config(text=f"Current goals:\n{goals}")

    def _on_day_completed(self, data):
        """Handle day_completed event from backend"""
        pass

    def _on_week_completed(self, data):
        """Handle week_completed event from backend"""

        print(f"[Frontend] Received week_completed: {data}")
        self.status_label.config(text=f"★ {data['message']}")
        messagebox.showinfo("Week complete. Set new goals using 'set goal' button.")


    def step(self):
        """Start the UI loop"""

        print("[Frontend] Starting UI loop")
        self.window.mainloop()

    def get_input(self, message) -> str | None:
        """Creates a text box that displays a message.
        Takes a text input then disappears on press of enter.
        """
        input_dialog = InputDialog(self.window, message)
        self.window.wait_window(input_dialog)
        return input_dialog.result

    def _on_reset_goals(self):
        """Called when user clicks reset goals button"""
        self.event_bus.emit("reset_goals", {
            "message": "Goals have been reset."
        })

    def _on_successful_reset_goals(self, data):
        """Called when backend emits 'goals_reset'."""
        print(f"[Frontend] Received goals_reset: {data}")
        self.goals_label.config(text="Your goals will appear here. Recommended: 3-5 goals per week.")
        self.status_label.config(text="Goals have been reset.")

    def toggle_goals_visibility(self):
        """Toggle the visibility of the goals label"""
        if self.goals_label.winfo_viewable():
            self.goals_label.pack_forget()
        else:
            self.goals_label.pack(pady=10)
