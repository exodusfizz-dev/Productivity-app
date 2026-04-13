"""Frontend UI using tkinter"""

import tkinter as tk
from tkinter import messagebox
from .inputs import InputDialog
from .image_manager import TkinterImageManager
from pathlib import Path


class FrontEnd:
    FONT = ("Arial", 12)
    PADY = 10
    PADX = 20
    NO_GOALS_TEXT = "Your goals will appear here. Recommend setting 3-5 goals per week."



    def __init__(self, event_bus):
        self.image_manager = TkinterImageManager(
            image_dir=Path(__file__).resolve().parent / "assets"
            )
        self.event_bus = event_bus
        self.window = tk.Tk()
        self.window.title("Productivity App")
        self.window.geometry("800x600")

        self.status_label = tk.Label(
            self.window,
            text="Status: Waiting...",
            font=self.FONT,
            wraplength=500
        )

        self.goals_frame = tk.Frame(self.window)

        self.eye_img = self.image_manager.get_image("eye")
        self.eye_slash_img = self.image_manager.get_image("eye-slash")


        self.goals_header = tk.Label(
            self.goals_frame,
            text=" Current goals",
            image=self.eye_img,
            compound="left",
            font=(self.FONT[0], self.FONT[1], "bold"),
            anchor="w"
            )

        self.goals_label = tk.Label(
            self.goals_frame,
            text=self.NO_GOALS_TEXT,
            font=self.FONT,
            wraplength=500,
            justify="left"
        )

        self.add_goal = tk.Button(
            self.window,
            text="Add goal",
            command=self._on_add_goal,
            font=self.FONT,
            padx=self.PADX,
            pady=self.PADY
        )
        self.reset_goals = tk.Button(
            self.window,
            text="Reset goals",
            command=self._on_reset_goals,
            font=self.FONT,
            padx=self.PADX,
            pady=self.PADY
        )

        self.add_inactive_goal = tk.Button(
            self.window,
            text="Add inactive goal",
            command=self._on_add_inactive_goal,
            font=self.FONT,
            padx=self.PADX,
            pady=self.PADY
        )
        self.reset_inactive_goals = tk.Button(
            self.window,
            text="Reset inactive goals",
            command=self._on_reset_inactive_goals,
            font=self.FONT,
            padx=self.PADX,
            pady=self.PADY
        )

        self.status_label.pack(pady=self.PADY)
        self.add_goal.pack(pady=self.PADY)
        self.reset_goals.pack(pady=self.PADY)
        self.add_inactive_goal.pack(pady=self.PADY)
        self.reset_inactive_goals.pack(pady=self.PADY)

        self.goals_header.pack(anchor="w")
        self.goals_label.pack(anchor="w", pady=(self.PADY, 0))
        self.goals_frame.pack(pady=self.PADY, fill="x")

        self.inactive_goals_label = tk.Label(
            self.window,
            text="Inactive goals: None",
            font=self.FONT,
            wraplength=500,
            justify="left"
        )
        self.inactive_goals_label.pack(pady=self.PADY)


        self.goals_header.bind("<Button-1>", lambda e: self.toggle_goals_visibility())

        self.event_bus.subscribe("day_completed", self._on_day_completed)
        self.event_bus.subscribe("week_completed", self._on_week_completed)
        self.event_bus.subscribe("goal_saved", self._on_successful_save_goal)
        self.event_bus.subscribe("goals_reset", self._on_successful_reset_goals)
        self.event_bus.subscribe("inactive_goal_saved", self._on_successful_save_inactive_goal)
        self.event_bus.subscribe("inactive_goals_reset", self._on_successful_reset_inactive_goals)

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
        goals = "\n".join(data.get("goals", []))

        if goals:
            self.goals_label.config(text=f"Current goals:\n{goals}")
        else:
            self.goals_label.config(text=self.NO_GOALS_TEXT)

    def _on_successful_save_inactive_goal(self, data):
        """Called when backend emits 'inactive_goal_saved'."""
        print(f"[Frontend] Received inactive_goal_saved: {data}")
        goals = "\n".join(data.get("inactive_goals", []))
        self.inactive_goals_label.config(text=f"Inactive goals:\n{goals}" if goals else "Inactive goals: None")

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

    def _on_add_inactive_goal(self):
        """Called when user clicks add inactive goal button"""
        goal = self.get_input(message="Add 1 inactive goal.")
        if goal is not None:
            self.event_bus.emit("user_add_inactive_goal", {"goal": goal})

    def _on_reset_inactive_goals(self):
        """Called when user clicks reset inactive goals button"""
        self.event_bus.emit("reset_inactive_goals", {"message": "Inactive goals reset."})

    def _on_successful_reset_goals(self, data):
        """Called when backend emits 'goals_reset'."""
        print(f"[Frontend] Received goals_reset: {data}")
        self.goals_label.config(text="Your goals will appear here. Recommended: 3-5 goals per week.")
        self.status_label.config(text="Goals have been reset.")

    def _on_successful_reset_inactive_goals(self, data):
        """Called when backend emits 'inactive_goals_reset'."""
        print(f"[Frontend] Received inactive_goals_reset: {data}")
        self.inactive_goals_label.config(text="Inactive goals: None")
        self.status_label.config(text="Inactive goals have been reset.")

    def toggle_goals_visibility(self):
        """Toggle the visibility of the goals label"""

        if self.goals_label.winfo_ismapped():
            self.goals_label.pack_forget()

            if self.eye_slash_img:
                self.goals_header.config(image=self.eye_slash_img)
        else:
            self.goals_label.pack(anchor="w", pady=(self.PADY, 0))

            if self.eye_img:
                self.goals_header.config(image=self.eye_img)
