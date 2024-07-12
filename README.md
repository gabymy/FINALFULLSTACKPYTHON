**__MASCOTAS_**

MASCOTAS es una aplicación web para la atención a mascotas, compra de accesorios y reserva de turnos para peluquería canina. La aplicación está construida con HTML, CSS, JavaScript para el frontend, y Python con Flask y MySQL para el backend.

**__Características_**

Registro de usuarios para recibir información y ofertas.
Reserva de turnos para peluquería canina.
CRUD completo para gestionar turnos.
Diseño responsivo y accesible.
Interacción dinámica con el usuario utilizando JavaScript.

**__Requisitos_**
Python 3.7 o superior
MySQL


__Crear y activar un entorno virtual_
```
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

__Instalar las dependencias_
```
pip install -r requirements.txt
```

__Configurar la base de datos MySQL_
```
CREATE DATABASE pet_care_db;

USE pet_care_db;

CREATE TABLE turnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_dueno VARCHAR(100),
    nombre_mascota VARCHAR(100),
    fecha_turno DATE
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE
);
```

__Configurar las variables de entorno_
```
MYSQL_HOST=localhost
MYSQL_USER=tu_usuario
MYSQL_PASSWORD=tu_contraseña
MYSQL_DB=pet_care_db
```

__Ejecutar la aplicación_
```
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

En tu navegador... http://127.0.0.1:5000/
