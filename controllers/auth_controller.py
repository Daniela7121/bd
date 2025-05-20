from models.mock_data import usuarios_mock

def autenticar_usuario(nombre, contrasena):
    for usuario in usuarios_mock:
        if usuario['nombre'] == nombre and usuario['contrasena'] == contrasena:
            return usuario
    return None
