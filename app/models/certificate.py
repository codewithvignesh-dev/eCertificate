class Certificate:
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
    @classmethod
    def from_row(cls, row): return cls(**row) if row else None
    @property
    def public_url(self): return f"/certificate/{self.public_token}"
    def __repr__(self): return f"<Certificate {self.certificate_number}>"
