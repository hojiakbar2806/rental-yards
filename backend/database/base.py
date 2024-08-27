from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import as_declarative

from utils.utils import to_came_case


@as_declarative()
class Base:
    id: int
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return to_came_case(cls.__name__)
