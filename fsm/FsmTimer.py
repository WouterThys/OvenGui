

class FsmTimer:
    def __init__(self, overflow_value):
        self.count = 0
        self.overflow_value = overflow_value
        self.overflow = False

    def tick(self):
        self.count += 1
        if self.count >= self.overflow_value:
            self.overflow = True

    def is_overflown(self):
        tmp = self.overflow
        self.overflow = False
        return tmp

    def clear_timer(self):
        self.overflow = False
        self.count = 0