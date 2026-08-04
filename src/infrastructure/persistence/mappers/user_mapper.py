from src.domain.entities.trabajador import Trabajador
from src.infrastructure.persistence.models.user_model import PersonalModel


class UserMapper:
    @staticmethod
    def to_domain(model: PersonalModel) -> Trabajador | None:
        if not model:
            return None
        return Trabajador(
            id_trabajador=model.id,
            nombre=model.nombre,
            apellido=model.apellido,
            dni=model.dni,
            cargo=model.cargo,
            estado=model.estado,
        )

    @staticmethod
    def to_persistence(entity: Trabajador) -> PersonalModel:
        return PersonalModel(
            id=entity.id_trabajador,
            nombre=entity.nombre,
            apellido=entity.apellido,
            dni=entity.dni,
            cargo=entity.cargo,
            estado=entity.estado,
        )