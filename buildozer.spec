[app]
title = Fuel Calculator
package.name = fuelcalculator
package.domain = org.fuelcalculator

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

version = 0.1
requirements = python3,kivy==2.1.0,kivymd==1.1.1,pandas,openpyxl,android

orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.1.0

[buildozer]
log_level = 2

icon.filename = %(source.dir)s/icon.png

android.api = 30
android.minapi = 21
android.ndk = 19b
android.ndk_api = 21

# Разрешения для Android
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# Дополнительные настройки для pandas
android.gradle_dependencies = 'androidx.appcompat:appcompat:1.3.1'

# Увеличим память для сборки
android.add_src =
android.add_resources =

# Увеличим лимиты памяти для сборки
android.allow_backup = true
android.accept_sdk_license = true

# Оптимизация размера
android.skip_compile = libffi,openssl,pyjnius