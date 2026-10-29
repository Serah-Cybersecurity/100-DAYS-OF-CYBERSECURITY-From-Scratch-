
===== COLLECTION METADATA =====
2026-10-29T14:37:38+00:00
Linux 7.0.9+parrot7-amd64 x86_64 GNU/Linux
uid=1000(user) gid=1000(user) groups=1000(user),20(dialout),24(cdrom),25(floppy),27(sudo),29(audio),30(dip),44(video),46(plugdev),101(netdev),103(scanner),105(lpadmin),106(bluetooth),1001(vboxsf)

===== PROCESS SNAPSHOT =====
    PID    PPID USER     STAT     ELAPSED COMMAND
      1       0 root     Ss      01:08:41 systemd
      2       0 root     S       01:08:41 kthreadd
    444       1 root     Ss      01:08:14 systemd-journal
    485       1 root     Ss      01:08:14 systemd-udevd
    758       1 root     Ss      01:08:12 haveged
    761       1 root     Ssl     01:08:12 accounts-daemon
    764       1 root     Ss      01:08:12 cron
    766       1 message+ Ss      01:08:12 dbus-daemon
    781       1 polkitd  Ssl     01:08:12 polkitd
    783       1 root     Ss      01:08:12 rngd
    786       1 root     Ssl     01:08:12 switcheroo-cont
    791       1 root     Ss      01:08:12 systemd-logind
    794       1 root     Ssl     01:08:12 udisksd
    807       1 root     Ssl     01:08:12 NetworkManager
    813       1 root     Ss      01:08:12 wpa_supplicant
    931       1 root     Ss      01:08:12 cpupower-gui-he
    937       1 root     Ssl     01:08:12 ModemManager
    940       1 root     Sl      01:08:12 VBoxService
    995       1 root     Ssl     01:08:11 lightdm
   1002       1 ntpsec   SLs     01:08:11 ntpd
   1090       1 root     Ss+     01:08:11 agetty
   1101       1 user     Ss      01:08:11 systemd
   1153       1 rtkit    SNsl    01:08:10 rtkit-daemon
   1297       1 root     Ssl     01:08:09 power-profiles-
   1460       1 root     Ssl     01:08:05 upowerd

===== RUNNING SYSTEMD SERVICES =====
  UNIT                           LOAD   ACTIVE SUB     DESCRIPTION
  accounts-daemon.service        loaded active running Accounts Service
  cpupower-gui-helper.service    loaded active running cpupower-gui system helper
  cron.service                   loaded active running Regular background program processing daemon
  dbus.service                   loaded active running D-Bus System Message Bus
  getty@tty1.service             loaded active running Getty on tty1
  haveged.service                loaded active running Entropy Daemon based on the HAVEGE algorithm
  lightdm.service                loaded active running Light Display Manager
  ModemManager.service           loaded active running Modem Manager
  NetworkManager.service         loaded active running Network Manager
  ntpsec.service                 loaded active running Network Time Service
  polkit.service                 loaded active running Authorization Manager
  power-profiles-daemon.service  loaded active running Power Profiles daemon
  rngd.service                   loaded active running Start entropy gathering daemon (rngd)
  rtkit-daemon.service           loaded active running RealtimeKit Scheduling Policy Service
  switcheroo-control.service     loaded active running Switcheroo Control Proxy service
  systemd-journald.service       loaded active running Journal Service
  systemd-logind.service         loaded active running User Login Management
  systemd-udevd.service          loaded active running Rule-based Manager for Device Events and Files
  udisks2.service                loaded active running Disk Manager
  upower.service                 loaded active running Daemon for power management
  user@1000.service              loaded active running User Manager for UID 1000
  virtualbox-guest-utils.service loaded active running Virtualbox guest utils
  wpa_supplicant.service         loaded active running WPA supplicant

Legend: LOAD   → Reflects whether the unit definition was properly loaded.
        ACTIVE → The high-level unit activation state, i.e. generalization of SUB.
        SUB    → The low-level unit activation state, values depend on unit type.

23 loaded units listed.

===== LISTENING TCP SOCKETS =====
State Recv-Q Send-Q Local Address:Port Peer Address:Port

===== SYSTEMD TIMERS =====
NEXT                             LEFT LAST                             PASSED UNIT                         ACTIVATES
Thu 2026-10-29 16:30:00 UTC  1h 52min -                                     - sysstat-collect.timer        sysstat-collect.service
Thu 2026-10-29 16:39:00 UTC   2h 1min Thu 2026-10-29 16:29:20 UTC 1h 8min ago phpsessionclean.timer        phpsessionclean.service
Fri 2026-10-30 00:00:00 UTC        9h Thu 2026-10-29 12:25:00 UTC           - dpkg-db-backup.timer         dpkg-db-backup.service
Fri 2026-10-30 00:00:00 UTC        9h -                                     - sysstat-rotate.timer         sysstat-rotate.service
Fri 2026-10-30 00:00:23 UTC        9h Thu 2026-10-29 09:25:25 UTC           - lighttpd-maint.timer         lighttpd-maint.service
Fri 2026-10-30 00:04:55 UTC        9h Wed 2026-10-28 17:21:19 UTC           - apt-daily.timer              apt-daily.service
Fri 2026-10-30 00:07:00 UTC        9h -                                     - sysstat-summary.timer        sysstat-summary.service
Fri 2026-10-30 00:11:07 UTC        9h -                                     - lynis.timer                  lynis.service
Fri 2026-10-30 00:26:06 UTC        9h Thu 2026-10-29 09:37:08 UTC           - logrotate.timer              logrotate.service
Fri 2026-10-30 00:54:29 UTC       10h Tue 2026-10-27 14:14:14 UTC           - man-db.timer                 man-db.service
Fri 2026-10-30 06:18:04 UTC       15h Thu 2026-10-29 10:25:17 UTC           - apt-daily-upgrade.timer      apt-daily-upgrade.service
Fri 2026-10-30 06:25:00 UTC       15h Thu 2026-10-29 12:25:00 UTC           - ntpsec-rotate-stats.timer    ntpsec-rotate-stats.service
Fri 2026-10-30 13:43:57 UTC       23h Thu 2026-10-29 13:43:57 UTC   53min ago systemd-tmpfiles-clean.timer systemd-tmpfiles-clean.service
Sat 2026-10-31 05:22:16 UTC 1 day 14h Wed 2026-10-28 16:40:45 UTC           - geoipupdate.timer            geoipupdate.service
Sun 2026-11-01 03:10:13 UTC    2 days Tue 2026-10-27 11:43:29 UTC           - e2scrub_all.timer            e2scrub_all.service
Sun 2026-11-01 03:10:14 UTC    2 days Tue 2026-10-27 11:42:54 UTC           - xfs_scrub_all.timer          xfs_scrub_all.service
Mon 2026-11-02 00:23:40 UTC    3 days Tue 2026-10-27 16:04:33 UTC           - fstrim.timer                 fstrim.service

17 timers listed.

===== CURRENT USER CRONTAB STATUS =====
No readable current-user crontab was detected.
It may be absent or access may be restricted.

===== SYSTEM-WIDE CRON FILE NAMES =====

--- /etc/cron.d ---
/etc/cron.d/.placeholder
/etc/cron.d/e2scrub_all
/etc/cron.d/geoipupdate
/etc/cron.d/john
/etc/cron.d/ntpsec
/etc/cron.d/php
/etc/cron.d/sysstat

--- /etc/cron.hourly ---
/etc/cron.hourly/.placeholder

--- /etc/cron.daily ---
/etc/cron.daily/.placeholder
/etc/cron.daily/apache2
/etc/cron.daily/apt-compat
/etc/cron.daily/dpkg
/etc/cron.daily/lighttpd
/etc/cron.daily/logrotate
/etc/cron.daily/man-db
/etc/cron.daily/sysstat

--- /etc/cron.weekly ---
/etc/cron.weekly/.placeholder
/etc/cron.weekly/man-db
/etc/cron.weekly/tor

--- /etc/cron.monthly ---
/etc/cron.monthly/.placeholder

===== COLLECTION COMPLETE =====
This script gathered a limited system snapshot.
Its output is not a malware verdict or full forensic record.
