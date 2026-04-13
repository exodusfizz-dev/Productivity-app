from dataclasses import dataclass, field

@dataclass
class BackendState:
    """Represents the state of the backend, including goals and timestamp."""
    goals: list = field(default_factory=list)
    inactive_goals: list = field(default_factory=list)
    timestamp: float = 0.0
