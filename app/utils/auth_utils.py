from functools import wraps
from flask import session, abort

def requer_roles(lista_permitida):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "usuario_role" not in session or session["usuario_role"] not in lista_permitida:
                abort(403, description="Acesso Negado")
            return f(*args, **kwargs)
        return decorated_function
    return decorator
