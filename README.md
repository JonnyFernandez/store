# Aplicación Web de Gestión de Pedidos

Este proyecto es una aplicación web desarrollada con **Django** que permite gestionar pedidos, incluyendo funcionalidades como el registro de usuarios, asignación de roles (cliente y vendedor), manejo de imágenes de productos con **Cloudinary**, y la generación de órdenes de compra en **PDF**. Además, el sistema permite agregar múltiples direcciones de envío y administrar el stock de los productos.

## Características Principales

- **Autenticación de usuarios**: Registro e inicio de sesión de usuarios con roles de cliente o vendedor.
- **Gestión de pedidos**: Carrito de compras con opción para agregar productos, gestionar direcciones de envío y generar pedidos.
- **Seguimiento de orden de compra**: Puedes dar seguimiento a tus ordenes de compra para ver si fueron aprobas o estan pendientes.
- **Integración con Cloudinary**: Para un manejo eficiente de las imágenes, asegurando que todas las fotos de productos mantengan un tamaño uniforme.
- **Interfaz minimalista**: Diseño sencillo y amigable, con foco en la experiencia del usuario.

## Tecnologías Utilizadas

- **Python** y **Django** para el backend.
- **SQLite** como base de datos.
- **Cloudinary** para la gestión de imágenes.
- **HTML**, **CSS**, y **Bootstrap** para el frontend.

## Video de la Aplicación

Puedes ver una demostración de la aplicación en el siguiente enlace:  
[Ver video en YouTube](https://youtu.be/CcrS0hB-O0I)

## Instalación y Configuración

1. Clona este repositorio:

   ```bash
   git clone https://github.com/JonnyFernandez/store.git
   ```

### Para Testear la Aplicación

Sigue estos pasos para configurar y ejecutar la aplicación localmente:

1. **Crear el archivo `.env`:**  
   En la carpeta raíz del proyecto, crea un archivo llamado `.env` y añade las siguientes credenciales:

   ```bash
   # Credenciales para Cloudinary
   CLOUDINARY_CLOUD_NAME = cloud-name-de-cludinary
   CLOUDINARY_API_KEY = api-key-de-cludinary
   CLOUDINARY_API_SECRET = api-secret-de-cludinary

   # Credenciales de Gmail
   USER_Gmail= tu-email@gmail.com
   PASS_Gmail= contraseña de aplicación
   ```

2. **Instalar dependencias:**

```
pip install -r requirements.txt
```
