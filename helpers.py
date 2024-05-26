# Jakob Zielinski
# Update a systeminfo pimenu

import subprocess, time


def ping(menu, ip):
    cmd = "ping -c1 "+ip
    ping = subprocess.call(cmd, shell=True)

    if ping == 0:
        menu.options[0].string = menu.options[0].string+'+'
    else:
        menu.options[0].string = menu.options[0].string+'-'

    time.sleep(0.5)


def reboot():
    cmd = "reboot"
    subprocess.check_output(cmd, shell=True)


def shutdown():
    cmd = "poweroff"
    subprocess.check_output(cmd, shell=True)


def sysinfo_update(menu):
    # Shell scripts for system monitoring from here:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d' ' -f1"
    IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = 'cut -f 1 -d " " /proc/loadavg'
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")

    # Update text for the menu options.

    menu.options[0].string = "IP: " + IP
    menu.options[1].string = "CPU load: " + CPU
    menu.options[2].string = MemUsage
    menu.options[3].string = Disk


