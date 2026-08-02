from sqlalchemy.orm import Session
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.persistence.models.user_model import PersonalModel
from src.infrastructure.persistence.mappers.user_mapper import UserMapper


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_dni(self, dni: str) -> User | None:
        model = self._session.query(PersonalModel).filter(PersonalModel.dni == dni).first()
        return UserMapper.to_domain(model)

    def save(self, user: User) -> None:
        model = UserMapper.to_persistence(user)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)