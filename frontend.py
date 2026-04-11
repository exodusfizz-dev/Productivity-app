"""Frontend UI using tkinter"""

import tkinter as tk
from tkinter import messagebox
from inputs import InputDialog
from pathlib import Path


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

        self.goals_frame = tk.Frame(self.window)


        assets_dir = Path(__file__).resolve().parent / "assets"
        eye_path = assets_dir / "eye.png"
        eye_slash_path = assets_dir / "eye-slash.png"
        self.eye_img = None
        self.eye_slash_img = None
        try:
            if eye_path.exists():
                self.eye_img = tk.PhotoImage(file=str(eye_path))
            if eye_slash_path.exists():
                self.eye_slash_img = tk.PhotoImage(file=str(eye_slash_path))
        except tk.TclError as e:
            print(f"[Frontend] Warning: could not load icon images: {e}")


        if self.eye_img:
            self.goals_header = tk.Label(
                self.goals_frame,
                text=" Current goals",
                image=self.eye_img,
                compound="left",
                font=("Arial", 12, "bold"),
                anchor="w"
            )
        else:
            self.goals_header_icon_visible = "👁"
            self.goals_header_icon_hidden = "🙈"
            self.goals_header = tk.Label(
                self.goals_frame,
                text=f"{self.goals_header_icon_visible} Current goals",
                font=("Arial", 12, "bold"),
                anchor="w"
            )

        self.goals_label = tk.Label(
            self.goals_frame,
            text="Your goals will appear here. Recommend setting 3-5 goals per week.",
            font=("Arial", 12),
            wraplength=500,
            justify="left"
        )

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

        self.add_inactive_goal = tk.Button(
            self.window,
            text="Add inactive goal",
            command=self._on_add_inactive_goal,
            font=("Arial", 11),
            padx=20,
            pady=10
        )
        self.reset_inactive_goals = tk.Button(
            self.window,
            text="Reset inactive goals",
            command=self._on_reset_inactive_goals,
            font=("Arial", 11),
            padx=20,
            pady=10
        )

        self.status_label.pack(pady=10)
        self.add_goal.pack(pady=6)
        self.reset_goals.pack(pady=6)
        self.add_inactive_goal.pack(pady=6)
        self.reset_inactive_goals.pack(pady=6)

        self.goals_header.pack(anchor="w")
        self.goals_label.pack(anchor="w", pady=(6, 0))
        self.goals_frame.pack(pady=12, fill="x")

        self.inactive_goals_label = tk.Label(
            self.window,
            text="Inactive goals: None",
            font=("Arial", 11),
            wraplength=500,
            justify="left"
        )
        self.inactive_goals_label.pack(pady=8)


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
            self.goals_label.config(text="Your goals will appear here. Recommend setting 3-5 goals per week.")

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
                self.goals_header.config(text=f"{self.goals_header_icon_hidden} Current goals")
        else:
            self.goals_label.pack(anchor="w", pady=(6, 0))

            if self.eye_img:
                self.goals_header.config(image=self.eye_img)
            else:
                self.goals_header.config(text=f"{self.goals_header_icon_visible} Current goals")
