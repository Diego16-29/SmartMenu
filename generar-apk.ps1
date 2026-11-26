$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
if (-not $env:JAVA_HOME -and (Test-Path "$env:ProgramFiles\Android\Android Studio\jbr\bin\java.exe")) { $env:JAVA_HOME = "$env:ProgramFiles\Android\Android Studio\jbr" }
if ($env:JAVA_HOME) { $env:Path = "$env:JAVA_HOME\bin;$env:Path" }
if (-not (Get-Command java -ErrorAction SilentlyContinue)) { throw 'Instala Android Studio o JDK 17 y configura JAVA_HOME.' }
$sdk = $env:ANDROID_HOME
if (-not $sdk) { $sdk = $env:ANDROID_SDK_ROOT }
if (-not $sdk) { $sdk = "$env:LOCALAPPDATA\Android\Sdk" }
if (-not (Test-Path "$sdk\platforms\android-35\android.jar")) { throw 'Instala Android SDK Platform 35 desde SDK Manager en Android Studio.' }
$env:ANDROID_HOME = $sdk
$env:ANDROID_SDK_ROOT = $sdk
$gradleRoot = Join-Path $env:LOCALAPPDATA 'SmartMenuTools'
$gradle = Join-Path $gradleRoot 'gradle-8.9\bin\gradle.bat'
if (-not (Test-Path $gradle)) {
  New-Item -ItemType Directory -Force $gradleRoot | Out-Null
  $archive = Join-Path $gradleRoot 'gradle-8.9-bin.zip'
  Invoke-WebRequest -Uri 'https://services.gradle.org/distributions/gradle-8.9-bin.zip' -OutFile $archive
  Expand-Archive -Path $archive -DestinationPath $gradleRoot -Force
}
& $gradle --no-daemon wrapper --gradle-version 8.9
if ($LASTEXITCODE -ne 0) { throw 'No se pudo generar el Gradle Wrapper.' }
& $gradle --no-daemon :app:assembleDebug
if ($LASTEXITCODE -ne 0) { throw 'Error de compilacion de Android.' }
Copy-Item 'app\build\outputs\apk\debug\app-debug.apk' 'SmartMenu-debug.apk' -Force
Write-Host "APK generado: $PSScriptRoot\SmartMenu-debug.apk" -ForegroundColor Green
