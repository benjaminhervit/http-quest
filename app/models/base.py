class Base:
    def to_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.to_dict()}>"
