# GameHub

Página web de videojuegos hecha con Django. Pantallas: **Inicio**, **Registro** (con validación), **Login** y **Juegos** (datos de la API gratuita [RAWG](https://rawg.io/apidocs)).

## Cómo ejecutarla
1. Crea una clave gratis en https://rawg.io/apidocs (botón *Get API Key*).
2. En la terminal, dentro de la carpeta del proyecto:
   ```
   python -m venv venv
   venv\Scripts\activate        # en Mac/Linux: source venv/bin/activate
   pip install -r requirements.txt
   copy .env.example .env       # en Mac/Linux: cp .env.example .env
   ```
3. Abre `.env` y pega tu clave en `RAWG_API_KEY`.
4. Ejecuta:
   ```
   python manage.py migrate
   python manage.py runserver
   ```
5. Entra a http://127.0.0.1:8000/ y pruebas con `python manage.py test`.

## Seguridad aplicada
- La clave de la API está en `.env` (ignorado por `.gitignore`); en GitHub solo va `.env.example`.
- La API se consume desde el servidor, así que la clave nunca llega al navegador.
- Registro validado: usuario mínimo 3 caracteres, correo válido y único, contraseña robusta y confirmada.
- Contraseñas cifradas (PBKDF2) y protección CSRF en todos los formularios.
- La pantalla de juegos requiere iniciar sesión (`login_required`).
- Entradas limitadas (búsqueda de 50 caracteres), tiempo máximo en la API y manejo de errores sin mostrar detalles internos.

## Capturas para el PDF
Inicio · Registro con errores de validación · Registro correcto · Login · Juegos con resultados · Búsqueda de un juego.

## Subir a GitHub
```
git init
git add .
git status          # comprueba que .env NO aparece en la lista
git commit -m "GameHub"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/gamehub.git
git push -u origin main
```
