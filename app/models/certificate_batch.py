class CertificateBatch:
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
    @classmethod
    def from_row(cls, row): return cls(**row) if row else None
    def mark_completed(self):
        self.completed_at = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
        self.status = "completed" if self.failed_records == 0 else "completed_with_errors"
    def __repr__(self): return f"<CertificateBatch {self.id}>"
