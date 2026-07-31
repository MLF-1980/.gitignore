class DomainError(Exception):
    """Excepción base para todos los errores de dominio de SafeCore."""
    pass

class UserNotFoundError(DomainError):
    def __init__(self, user_id: str):
        super().__init__(user_id)

class DuplicateUserError(DomainError):
    def __init__(self, email: str):
        super().__init__(f"El correo electrónico '{email}' ya está registrado.")
        self.email = email