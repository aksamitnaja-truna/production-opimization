class PriorityLevels:
    _config = {
        1: "low",
        2: "medium",
        3: "high",
        4: "urgent",
        5: "critical"
    }

    @staticmethod
    def get_priority(priority):
        return PriorityLevels._config.get(
            priority,
            f"Wrong Priority value ~{priority}, must be in (1, 2, 3, 4, 5)"
        )
