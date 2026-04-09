"""Event bus for decoupled communication between backend and frontend"""


class EventBus:
    """Manages event subscriptions and emission between components"""

    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_name, callback):
        """
        Register a callback to listen for an event.
        
        Args:
            event_name: str - name of the event
            callback: callable - function to call when event is emitted
        """
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(callback)
        print(f"[EventBus] Subscribed to '{event_name}'")

    def emit(self, event_name, data=None):
        """
        Broadcast an event to all subscribers.
        
        Args:
            event_name: str - name of the event
            data: any - data to pass to callbacks
        """
        print(f"[EventBus] Emitting '{event_name}' with data: {data}")
        if event_name in self._subscribers:
            for callback in self._subscribers[event_name]:
                callback(data)
        else:
            print(f"[EventBus] Warning: No subscribers for '{event_name}'")
