class PriorityLevels:
    _config = {
        1: "low",
        2: "medium",
        3: "high",
        4: "urgent",
        5: "critical"
    }

    @staticmethod
    def get_priority(priority, is_consensus=False):

        msg = PriorityLevels._config.get(priority, None)
        if msg is None:
            return f'not Valid priority ~{priority}'
        return f'{msg} (consensus)' if is_consensus else msg
# alias
str_prior = PriorityLevels.get_priority