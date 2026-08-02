from src.domain.entities.user import User
from src.infrastructure.models.user_model import PersonalModel


class UserMapper:
    @staticmethod
    def to_domain(model: PersonalModel) -> User | None:
        if not model:
            return None
        return User(
            id=model.id,
            nombre=model.nombre,
            apellido=model.apellido,
            dni=model.dni,
            cargo=model.cargo,
            estado=model.estado,
        )

    @staticmethod
    def to_persistence(entity: User) -> PersonalModel:
        return PersonalModel(
            id=entity.id,
            nombre=entity.nombre,
            apellido=entity.apellido,
            dni=entity.dni,
            cargo=entity.cargo,
            estado=entity.estado,
        )