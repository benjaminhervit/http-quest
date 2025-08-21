import json


class Base:
    def to_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }

    def to_json(self):
        return json.dumps(self.to_dict(), default=str)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.to_dict()}>"
