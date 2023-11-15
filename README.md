# Conceptos

## Ambiente Virtual

Un ambiente virtual es una herramienta esencial en el mundo de Python que nos permite gestionar múltiples dependencias de manera eficiente.

Python tiene la particularidad de que todas las dependencias instaladas se almacenan en un entorno global, lo que significa que todas las aplicaciones y scripts de Python comparten acceso a estas dependencias. Esto puede ser problemático cuando deseamos utilizar una biblioteca con una versión específica solo para una aplicación en particular. Aquí es donde el ambiente virtual se convierte en una solución valiosa.

En términos de entornos de desarrollo, un ambiente virtual en Python es similar al archivo `package.json` en el ecosistema de JavaScript. Ambos permiten gestionar las dependencias de manera aislada.

Para crear un ambiente virtual, puedes utilizar el siguiente comando:

### LINUX

python3 -m venv venv \*\* También funciona en windows

### WINDOWS

python3 -m venv venv

Esto nos va a crear una carpeta con unos ejecutables los
cuales ejecutaremos de la siguiente forma.

### LINUX

./venv/bin/activate

### WINDOWS

. ./venv/Scripts/activate
