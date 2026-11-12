Asterisk 18.6.0 / amd64 / glibc 2.24
==================================
Назначение: Astra Linux SE 1.6 «Смоленск», Intel Core i5-760.
Сборка: Debian 9 Stretch, GCC 6, базовая архитектура x86-64.
Встроены pjproject 2.10 и jansson 2.12 с патчами из Asterisk 18.6.0.
BUILD_NATIVE отключён. CFLAGS: -O2 -march=x86-64 -mtune=generic.
Это локальная сборка, не официальный пакет Astra Linux.

Установка из каталога с пакетом (нужны root и настроенные репозитории Astra):
  apt install ./asterisk-custom_18.6.0-1+astra16_amd64.deb
Пакет включает pjproject и jansson, но не все системные зависимости.
Точный список зависимостей:
  dpkg-deb -f asterisk-custom_18.6.0-1+astra16_amd64.deb Depends

При наличии другой установки Asterisk сначала сохраните /etc/asterisk,
/var/lib/asterisk и /var/spool/asterisk. Пакет объявляет конфликт с пакетами
asterisk, asterisk-config, asterisk-modules: проверьте план изменений apt.
Установку поверх Asterisk, установленного вручную из исходников, не проверяли.

Конфигурация: /etc/asterisk. Включены примеры из исходников; SIP-абоненты
и транки не настроены. Звуковые файлы приветствий и music-on-hold не включены.
Пакет создаёт пользователя asterisk; служба работает под этим пользователем.
Автоматический запуск после установки не выполняется.
После настройки:
  systemctl enable --now asterisk
  systemctl status asterisk
  asterisk -rx 'core show version'
  asterisk -rx 'pjproject show buildopts'
  asterisk -rx 'module show like pjsip'
  asterisk -rvvv

Сборка и проверки описаны в VALIDATION.txt.
Проверки в Debian 9 не заменяют проверку на самой Astra и реальном i5-760.
Указанные версии устарели и содержат известные уязвимости; прямой доступ
к SIP/HTTP/AMI из Интернета требует отдельной оценки и защиты.
