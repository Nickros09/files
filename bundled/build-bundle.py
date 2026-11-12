import os, re, json, shutil, pathlib, subprocess
P=pathlib.Path
src=P('/job/work/pkg'); root=P('/job/work/pkg-bundled'); out=P('/job/output/bundled')
if root.exists(): shutil.rmtree(str(root))
shutil.copytree(str(src),str(root),symlinks=True)
private=root/'usr/lib/asterisk/private'; private.mkdir(parents=True,exist_ok=True)
for p in list((root/'usr/lib').glob('libasterisk*')):
 shutil.move(str(p),str(private/p.name))

def elf(p):
 if not p.is_file() or p.is_symlink(): return False
 with p.open('rb') as f: return f.read(4)==b'\x7fELF'

def cmd(args,**kw): return subprocess.check_output(args,universal_newlines=True,**kw)
base_files={str(P(x).resolve()) for x in cmd(['dpkg-query','-L','libc6:amd64']).splitlines() if x.startswith('/')}
env=dict(os.environ,LD_LIBRARY_PATH=str(private))
libs={}; owners={}
for p in list(root.rglob('*')):
 if not elf(p): continue
 result=cmd(['ldd',str(p)],env=env)
 if 'not found' in result: raise RuntimeError(str(p)+'\n'+result)
 for soname,loc in re.findall(r'^\s*(\S+) => (/\S+)',result,re.M):
  real=P(loc).resolve()
  if str(real) in base_files or str(real).startswith(str(root)+'/'): continue
  if soname in libs and libs[soname]!=str(real): raise RuntimeError('duplicate '+soname)
  libs[soname]=str(real)
for name,loc in sorted(libs.items()):
 shutil.copy2(loc,str(private/name))
 match=cmd(['dpkg-query','-S',loc]).splitlines()[0]
 owner=match.split(': /',1)[0]
 owners[name]=owner
for p in root.rglob('*'):
 if elf(p): subprocess.check_call(['patchelf','--set-rpath','/usr/lib/asterisk/private',str(p)])

def put(rel,s,mode=0o644):
 p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding="utf-8");p.chmod(mode)
put('usr/share/doc/asterisk-custom/README.bundled.ru.txt',"Один DEB для установки без Интернета\n===================================\nAsterisk 18.6.0 / pjproject 2.10 / jansson 2.12 / amd64\nНазначение: Astra Linux SE 1.6 «Смоленск», Intel Core i5-760.\n\nФайл: asterisk-custom_18.6.0-2+astra16.bundle_amd64.deb\nВключены 55 внешних прикладных библиотек и две библиотеки Asterisk.\nОни расположены в /usr/lib/asterisk/private. ELF RUNPATH направляет\nзагрузчик в этот каталог. Системные библиотеки не заменяются.\nСписок версий: BUNDLED-LIBRARIES.tsv.\n\nТребуется штатная базовая ОС amd64 с glibc >= 2.24 и adduser.\nДинамический загрузчик, glibc, NSS, базовые утилиты и systemd остаются\nкомпонентами ОС. Это один DEB, а не полностью независимая от ОС программа.\nДля уже собранных модулей не требуется скачивание библиотечных пакетов.\nПроизвольные дополнительные модули Asterisk в эту сборку не входят.\n\nУстановка под root из каталога со скачанным файлом:\n  dpkg -i ./asterisk-custom_18.6.0-2+astra16.bundle_amd64.deb\nПосле настройки /etc/asterisk:\n  systemctl enable asterisk\n  systemctl restart asterisk\n  systemctl status asterisk\n  asterisk -rx 'core show version'\n  asterisk -rx 'module show like pjsip'\n  asterisk -rvvv\n\nИмя пакета asterisk-custom сохранено. Новая версия обновляет предыдущую\n18.6.0-1+astra16. Изменённые пользователем conffiles сохраняются по правилам\ndpkg. Перед обновлением сделайте резервную копию конфигурации и данных.\nС официальными пакетами asterisk/asterisk-config/asterisk-modules объявлен\nконфликт. Установку поверх ручной сборки Asterisk не проверяли.\n\nПосле установки служба автоматически не запускается. Работает от\nпользователя asterisk. Примеры конфигурации входят; абоненты, транки,\nTLS-сертификаты и доверенные CA для внешних сервисов настраиваются отдельно.\nДля HTTPS можно использовать системный CA-файл, указав его в настройках.\nЗвуковые файлы приветствий и музыка ожидания не включены.\n\nПроверено: dpkg -i без сети в чистом Debian 9; разрешение зависимостей\nвсех ELF-файлов; запуск PJSIP и остановка нативно и при эмуляции Nehalem.\nНа Astra и реальном i5-760 ещё нужна проверка; service manager и мандатный\nконтроль Astra в контейнере не воспроизводились.\n\nВстроенные библиотеки обслуживаются вместе с этим пакетом: установка\nобновлений системных библиотек не обновляет их частные копии.\nСборка не является официальным пакетом Astra Linux.\n")
control=(root/'DEBIAN/control').read_text()
control=re.sub(r'^Version: .*$', 'Version: 18.6.0-2+astra16.bundle',control,flags=re.M)
control=re.sub(r'^Depends: .*$', 'Depends: libc6 (>= 2.24), adduser',control,flags=re.M)
control=control.replace('Description: Asterisk 18.6.0 with bundled pjproject 2.10 and jansson 2.12', 'Description: Asterisk 18.6.0 with private runtime libraries for offline install')
control+=' Application libraries are shipped in /usr/lib/asterisk/private.\n System glibc, NSS, user tools and service manager are provided by the OS.\n'
size=sum(p.stat().st_size for p in root.rglob('*') if p.is_file() and not p.is_symlink())//1024
control+='Installed-Size: '+str(size)+'\n'
put('DEBIAN/control',control)
rows=[]
for name in sorted(libs):
 owner=owners[name]
 meta=cmd(['dpkg-query','-W','-f=${binary:Package}\t${Version}\t${source:Package}\t${source:Version}',owner])
 rows.append(name+'\t'+meta+'\n')
 doc=root/'usr/share/doc/asterisk-custom/bundled-libraries';doc.mkdir(parents=True,exist_ok=True)
 for f in ['copyright','changelog.Debian.gz']:
  p=P('/usr/share/doc')/owner.split(':')[0]/f
  if p.exists(): shutil.copy2(str(p),str(doc/(owner.replace(':','_')+'-'+f)))
put('usr/share/doc/asterisk-custom/bundled-libraries.tsv','SONAME\tBinary package\tBinary version\tSource package\tSource version\n'+''.join(rows))
out.mkdir(parents=True,exist_ok=True)
(out/'BUNDLED-LIBRARIES.tsv').write_text((root/'usr/share/doc/asterisk-custom/bundled-libraries.tsv').read_text())
(out/'LIBRARY-MANIFEST.json').write_text(json.dumps({'private_libraries':libs,'owners':owners,'excluded_base':'libc6:amd64'},indent=2))
for p in [root]+list(root.rglob('*')):
 os.chown(str(p),0,0,follow_symlinks=False)
 if p.is_dir(): p.chmod(0o755)
subprocess.check_call(['dpkg-deb','-Zxz','--build',str(root),str(out/'asterisk-custom_18.6.0-2+astra16.bundle_amd64.deb')])
print('Private external libraries:',len(libs))
