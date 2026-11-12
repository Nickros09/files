# Asterisk 18.6.0 для Astra Linux SE 1.6 amd64

Готовый DEB-пакет, исходники и инструкция доступны в [Releases](https://github.com/Nickros09/files/releases).

Встроены pjproject 2.10 и jansson 2.12. Сборка выполнена в Debian 9 Stretch с glibc 2.24 для базовой архитектуры x86-64, без BUILD_NATIVE и без требования AVX.

Проверены установка в чистом Debian 9, запуск PJSIP и штатная остановка, включая эмуляцию CPU Nehalem через QEMU 7.2. На самой Astra Linux и реальном Intel Core i5-760 проверка ещё требуется. Это локальная сборка, не официальный пакет Astra Linux.

Установка из каталога со скачанным пакетом:

```sh
sudo apt install ./asterisk-custom_18.6.0-1+astra16_amd64.deb
```

После настройки `/etc/asterisk`:

```sh
sudo systemctl enable --now asterisk
sudo asterisk -rvvv
```

Перед установкой поверх существующего Asterisk сохраните его конфигурацию и данные. Системные зависимости устанавливаются из репозиториев ОС; звуковые файлы не включены. Подробности и ограничения проверки приведены в README.ru.txt и VALIDATION.txt в релизе.
