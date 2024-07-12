import os

class Config:
    """Configuración base para la aplicación."""
    
    # Configuración de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', '12345')
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'

    # Configuración de SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+mysqlconnector://root:12345@localhost/PetShop'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


