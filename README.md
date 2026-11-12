# Asterisk 18.6.0 для Astra Linux SE 1.6 amd64

## Один DEB с прикладными библиотеками

**[Скачать пакет со встроенными библиотеками](https://raw.githubusercontent.com/Nickros09/files/master/bundled/asterisk-custom_18.6.0-2+astra16.bundle_amd64.deb)**

Встроены pjproject 2.10, jansson 2.12 и 55 дополнительных библиотек. Они находятся в частном каталоге Asterisk и не заменяют системные библиотеки. Для установки на штатную Astra SE 1.6 amd64 с glibc 2.24 и adduser Интернет не требуется.

```sh
sudo dpkg -i ./asterisk-custom_18.6.0-2+astra16.bundle_amd64.deb
```

После настройки `/etc/asterisk`:

```sh
sudo systemctl enable asterisk
sudo systemctl restart asterisk
sudo asterisk -rvvv
```

[Инструкция](bundled/README.ru.txt) · [Проверки](bundled/VALIDATION.txt) · [Контрольная сумма](bundled/SHA256SUMS.txt) · [Состав библиотек](bundled/BUNDLED-LIBRARIES.tsv) · [Сборка](bundled/BUILD.ru.txt)

Новая версия обновляет прежний `asterisk-custom`, сохраняя изменённые conffiles. Перед обновлением сохраните конфигурацию и данные. Конфликтует с официальными пакетами `asterisk`, `asterisk-config`, `asterisk-modules`.

## Совместимость и проверки

Asterisk/pjproject/jansson собраны в Debian 9 Stretch с `-march=x86-64 -mtune=generic`, без `BUILD_NATIVE`. Проверены установка единственного DEB в чистом контейнере без сети, загрузка зависимостей всех 362 ELF-объектов, запуск 48 модулей PJSIP и штатная остановка нативно и с эмуляцией CPU Nehalem в QEMU 7.2.

На самой Astra Linux и реальном Intel Core i5-760 проверка ещё требуется. Системная glibc, NSS, базовые утилиты и systemd остаются компонентами ОС. Звуковые файлы не включены; абоненты, транки, сертификаты и доверенные CA настраиваются отдельно. Частные библиотеки обновляются вместе с этим пакетом. Это локальная сборка, не официальный пакет Astra Linux.

## Исходники

[Asterisk/pjproject/jansson и исходные сценарии сборки](asterisk-18.6.0-build-sources.tar.gz), [инструкция исходной сборки](BUILD.ru.txt), [сценарий включения библиотек](bundled/build-bundle.py), [версии и архивные исходники библиотек Debian](bundled/LIBRARY-SOURCES.txt).

## Предыдущий вариант

[Пакет с системными библиотечными зависимостями](https://raw.githubusercontent.com/Nickros09/files/master/asterisk-custom_18.6.0-1+astra16_amd64.deb) сохранён для сравнения. Для автономной установки используйте новую сборку из раздела выше.
