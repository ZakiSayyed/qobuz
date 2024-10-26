@echo off

:: Initial adb commands
adb -s 192.168.1.11:5555 tcpip 5556
adb -s 192.168.1.14:5555 tcpip 5557
adb -s 192.168.1.15:5555 tcpip 5558
adb -s 192.168.1.16:5555 tcpip 5559
adb -s 192.168.1.17:5555 tcpip 5560
adb -s 192.168.1.18:5555 tcpip 5561
adb -s 192.168.1.19:5555 tcpip 5562
adb -s 192.168.1.20:5555 tcpip 5563
adb -s 192.168.1.21:5555 tcpip 5564
adb -s 192.168.1.22:5555 tcpip 5565
adb -s 192.168.1.23:5555 tcpip 5566
adb -s 192.168.1.24:5555 tcpip 5567
adb -s 192.168.1.25:5555 tcpip 5568
adb -s 192.168.1.26:5555 tcpip 5569
adb -s 192.168.1.27:5555 tcpip 5570
adb -s 192.168.1.28:5555 tcpip 5571
adb -s 192.168.1.29:5555 tcpip 5572
adb -s 192.168.1.30:5555 tcpip 5573
adb -s 192.168.1.31:5555 tcpip 5574
adb -s 192.168.1.32:5555 tcpip 5575

:: Wait for 5 seconds
timeout /t 5 /nobreak

:: adb connect commands
adb connect 192.168.1.11:5556
adb connect 192.168.1.14:5557
adb connect 192.168.1.15:5558
adb connect 192.168.1.16:5559
adb connect 192.168.1.17:5560
adb connect 192.168.1.18:5561
adb connect 192.168.1.19:5562
adb connect 192.168.1.20:5563
adb connect 192.168.1.21:5564
adb connect 192.168.1.22:5565
adb connect 192.168.1.23:5566
adb connect 192.168.1.24:5567
adb connect 192.168.1.25:5568
adb connect 192.168.1.26:5569
adb connect 192.168.1.27:5570
adb connect 192.168.1.28:5571
adb connect 192.168.1.29:5572
adb connect 192.168.1.30:5573
adb connect 192.168.1.31:5574
adb connect 192.168.1.32:5575

pause
