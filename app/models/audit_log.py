class AuditLog:
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
    @classmethod
    def from_row(cls, row): return cls(**row) if row else None
    def __repr__(self): return f"<AuditLog {self.action}>"
