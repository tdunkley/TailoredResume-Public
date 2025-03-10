import logging
from datetime import datetime


class CentralizedTracker:
    def __init__(self):
        self.events = []
        self.errors = []

    def start_tracking(self, event_name):
        """Start tracking an event."""
        event = {
            "name": event_name,
            "start_time": datetime.now(),
            "end_time": None,
            "status": "in_progress",
        }
        self.events.append(event)
        logging.info(f"Started tracking event: {event_name}")

    def end_tracking(self, event_name):
        """End tracking an event."""
        for event in self.events:
            if event["name"] == event_name and event["status"] == "in_progress":
                event["end_time"] = datetime.now()
                event["status"] = "completed"
                logging.info(f"Ended tracking event: {event_name}")
                break

    def track_error(self, error_message):
        """Track an error."""
        error = {"message": error_message, "time": datetime.now()}
        self.errors.append(error)
        logging.error(f"Tracked error: {error_message}")

    def get_events(self):
        """Get all tracked events."""
        return self.events

    def get_errors(self):
        """Get all tracked errors."""
        return self.errors
