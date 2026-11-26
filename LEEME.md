# SmartMenu TV · 1.0
Aplicación escolar de menú digital para un restaurante ficticio. Los platillos, precios y folios son ejemplos; las fotografías y el icono fueron generados con IA. No hay pagos, conexión con cocina ni servidor. El catálogo funciona localmente.

## Abrir en Android Studio (Windows)
1. Extrae todo el ZIP en una ruta corta, por ejemplo C:\Proyectos\SmartMenu. No abras solo app.
2. En Android Studio abre SDK Manager (Tools > SDK Manager, o More Actions > SDK Manager desde inicio). Instala Android SDK Platform 35, Android SDK Build-Tools 35.0.0 (o los requeridos por Gradle), Android SDK Platform-Tools y Android Emulator. En SDK Platforms, Show Package Details permite elegir una imagen Android TV de API 35 o API 34, si está disponible.
3. Usa el JDK integrado de Android Studio (JDK 17 o 21 compatible con Gradle 8.9); en Settings > Build, Execution, Deployment > Build Tools > Gradle configura Gradle JDK. Si la ruta de Studio no es la predeterminada, configura JAVA_HOME manualmente.
4. Ejecuta Generar_APK.bat. Requiere Internet la primera vez para descargar Gradle 8.9 y el plugin Android 8.7.3. El script crea el wrapper y ejecuta assembleDebug. Si tu SDK está en otra carpeta, configura ANDROID_HOME.
5. File > Open, selecciona la carpeta SmartMenu (settings.gradle). Sincroniza Gradle. Si te pide instalar componentes adicionales, acepta. El APK generado por el script queda en SmartMenu-debug.apk; Gradle también lo deja en app/build/outputs/apk/debug/app-debug.apk. El APK debug usa firma de depuración, no de publicación.

## Emulador Android TV
1. Tools > Device Manager > Create Virtual Device. Categoría TV: Android TV (1080p) o un perfil TV disponible equivalente. Elige una imagen Android TV API 34/35 (x86_64 en equipos Intel/AMD). Si no aparece, revisa SDK Manager. Usa 2 GB de RAM o la configuración recomendada por el perfil y gráficos automáticos. Habilita virtualización de hardware si el emulador lo requiere.
2. Inicia el AVD. Selecciona app y el AVD en la barra de Android Studio. Pulsa Run. También puedes arrastrar el APK al emulador o usar `adb install -r SmartMenu-debug.apk`.
3. Usa las flechas y Enter del teclado o el D-pad del control virtual. Atrás cierra el detalle, pedido o exhibición. Desde el menú principal, Atrás sale.
4. Captura evidencia real con el icono de cámara del emulador (Take screenshot) o `adb shell screencap -p /sdcard/smartmenu.png` y `adb pull /sdcard/smartmenu.png`. Guarda capturas de menú, detalle, carrito, confirmación y exhibición.

## Funcionalidad
Menú con seis platillos, categorías, promociones, detalle con ingredientes, carrito con cantidades y total MXN, folio de demostración, modo pantalla con cambio cada 8 segundos. Carrito y contador de folio usan almacenamiento local WebView cuando disponible. Sin permisos de Internet. No incluye datos personales ni backend.

## Código y evidencia
- app/src/main/java/com/smartmenu/tv/MainActivity.java: actividad Java y traducción de teclas del D-pad.
- app/src/main/assets/: HTML, CSS, JavaScript e imágenes locales.
- app/src/main/AndroidManifest.xml: launcher TV, banner, orientación, ausencia de requisito táctil.
- Codigo_fuente.txt: copia de código en texto plano.
- evidencias/: capturas funcionales en Chromium de una copia en memoria de la interfaz, no del emulador Android; pruebas automatizadas con almacenamiento simulado. Los resultados no certifican la ejecución en Android. El APK y las capturas de AVD están pendientes porque este entorno no tiene Android SDK ni acceso a sus descargas.
