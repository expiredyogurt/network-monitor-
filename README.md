# network-monitor-
displays your network up and down along with CPU and RAM usage

Lightweight Taskbar System Monitor
A ultra-minimalist, transparent system monitor that sits directly on your Windows taskbar. Built with Python for performance and privacy.

Why I Built This
I wanted a simple way to track my PC's performance without the bloat. I tried several existing solutions, but ran into issues:

TrafficMonitor: Frequently flagged as spyware/vulnerable by modern antivirus software.

kil0bit System Monitor: Had persistent window-locking bugs where the monitor would jump to the wrong location on every reboot, and the developers didn't seem interested in a fix.

I decided to "vibe code" my own solution. This script is transparent, stays exactly where you put it, and uses zero network permissions—so you know your data isn't going anywhere.

Features
Zero-Glow Transparency: Blends perfectly into the Windows 10/11 taskbar.

Minimalist Stats: Tracks CPU %, RAM %, and real-time Network Upload/Download speeds (in Mbps).

Vertical Stack: Designed to stay within the height of the taskbar so it doesn't block other UI elements.

Privacy Focused: No telemetry, no "phoning home," just local hardware monitoring.

Prerequisites
You need Python installed. Once Python is ready, install the only dependency:

Bash
pip install psutil
Setup & Installation
Download the script: Download taskbar_monitor.pyw.

Find your coordinates: * Open the script and look for the line: self.root.geometry("300x45+1511+1111").

Change 1511 and 1111 to match your screen resolution and desired taskbar location.

Run it: Double-click taskbar_monitor.pyw.

Auto-start: * Press Win + R, type shell:startup.

Place a shortcut to your .pyw file in that folder to have it launch when Windows starts.

License
MIT - Feel free to fork it, break it, and fix it!
