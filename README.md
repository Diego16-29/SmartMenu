# SmartMenu TV

Aplicación de menú digital diseñada para pantallas inteligentes (**Android TV**), desarrollada como proyecto académico para la materia **Desarrollo para dispositivos inteligentes** (Unidad 3: *Aplicaciones para pantallas inteligentes*) de la Ingeniería en Desarrollo y Gestión de Software — Universidad Tecnológica de Coahuila.

## Archivo ejecutable (APK)

El paquete instalable compilado ya se encuentra incluido directamente en la raíz de este repositorio:

- **[SmartMenu.apk](./SmartMenu.apk)** — APK listo para instalar en un emulador Android TV o dispositivo físico compatible (`adb install -r SmartMenu.apk`).

## Características principales

- Catálogo interactivo con 6 platillos organizados por categorías (*Combos*, *Platillos*, *Ligeros* y *Postres*).
- Navegación optimizada para control remoto (D-pad: flechas direccionales, `OK`/`Enter` y `Atrás`/`Escape`).
- Vista detallada de cada platillo con descripción, ingredientes y precio en MXN.
- Sección de promociones con precios especiales y precios anteriores tachados.
- Simulación de pedido (carrito de compras) con control de cantidades, cálculo automático del total y folio de confirmación (`SM-0001`, etc.) persistido en almacenamiento local.
- **Modo pantalla (exhibición automática)** que rota automáticamente las especialidades cada 8 segundos.
- Funcionamiento 100 % local (sin permisos de Internet, sin servidores externos ni cobros reales).

## Estructura del proyecto

- `SmartMenu.apk`: Archivo APK compilado listo para instalación.
- `app/src/main/java/com/smartmenu/tv/MainActivity.java`: Actividad principal en Java con `WebView` inmersivo y mapeo de eventos del control remoto (D-pad).
- `app/src/main/AndroidManifest.xml`: Configuración de `LEANBACK_LAUNCHER`, banner, icono y orientación horizontal (`landscape`).
- `app/src/main/assets/`: Interfaz local (`index.html`, `style.css`, `app.js`) e imágenes locales (`img/`).
- `evidencias/`: Capturas funcionales de la interfaz y pruebas automatizadas (`pruebas_interfaz.py`, `resultados.txt`).
- `Codigo_fuente.txt`: Compilación del código fuente en texto plano.
- `Generar_APK.bat` / `generar-apk.ps1`: Scripts para regenerar el APK debug con Gradle.
- `LEEME.md`: Instrucciones técnicas de apertura y emulación en Android Studio.

## Autor

**Diego Abdiel Cedillo Velázquez**  
Ingeniería en Desarrollo y Gestión de Software  
Universidad Tecnológica de Coahuila
