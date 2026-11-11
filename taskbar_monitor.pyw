import tkinter as tk
import psutil
import time
import ctypes

# Windows API constants for click-through
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020


class TaskbarMonitor:
    def __init__(self):
        self.root = tk.Tk()

        # Window setup
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-toolwindow", True)

        # Transparent background
        self.root.config(bg="#111111")
        self.root.attributes("-transparentcolor", "#111111")

        # Keep the original taskbar-sized window, at the user's position
        self.root.geometry("300x45+1620+1111")

        self.canvas = tk.Canvas(
            self.root,
            width=300,
            height=45,
            bg="#111111",
            highlightthickness=0
        )
        self.canvas.pack()

        self.last_net = psutil.net_io_counters()
        self.last_time = time.monotonic()

        # Prime the non-blocking CPU sampler
        psutil.cpu_percent(interval=None, percpu=True)

        # Reuse canvas items to avoid creating more objects each refresh
        self.line1 = self.create_line(8, 12)
        self.line2 = self.create_line(8, 30)

        self.root.update_idletasks()
        self.make_click_through()

        self.root.after(1000, self.refresh)
        self.root.mainloop()

    def make_click_through(self):
        """Allow mouse clicks to pass through the monitor."""
        hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style |= WS_EX_LAYERED | WS_EX_TRANSPARENT
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

    def create_line(self, x, y):
        """Create reusable text and its black outline."""
        items = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            items.append(self.canvas.create_text(
                x + dx, y + dy, text="", fill="black",
                font=("Segoe UI", 9, "bold"), anchor="w"
            ))
        items.append(self.canvas.create_text(
            x, y, text="", fill="white",
            font=("Segoe UI", 9, "bold"), anchor="w"
        ))
        return items

    def update_line(self, items, text):
        for item in items:
            self.canvas.itemconfig(item, text=text)

    def get_net_speed(self):
        now = time.monotonic()
        curr_net = psutil.net_io_counters()
        interval = now - self.last_time

        if interval <= 0 or curr_net is None or self.last_net is None:
            self.last_net = curr_net
            self.last_time = now
            return 0.0, 0.0

        up_bytes = max(0, curr_net.bytes_sent - self.last_net.bytes_sent)
        down_bytes = max(0, curr_net.bytes_recv - self.last_net.bytes_recv)

        self.last_net = curr_net
        self.last_time = now

        return (down_bytes * 8) / interval / 1_000_000, (up_bytes * 8) / interval / 1_000_000

    def refresh(self):
        # Measure each logical processor, T0 through T11 on a 6-core/12-thread CPU
        cpu_threads = psutil.cpu_percent(interval=None, percpu=True)

        if cpu_threads:
            cpu = round(sum(cpu_threads) / len(cpu_threads))
            peak_thread = max(range(len(cpu_threads)), key=lambda i: cpu_threads[i])
            peak_usage = round(cpu_threads[peak_thread])
        else:
            cpu, peak_thread, peak_usage = 0, 0, 0

        ram = round(psutil.virtual_memory().percent)
        down, up = self.get_net_speed()

        line1 = f"CPU: {cpu}% | T{peak_thread}: {peak_usage}% | RAM: {ram}%"
        line2 = f"D: {down:.1f} | U: {up:.1f} Mbps"

        self.update_line(self.line1, line1)
        self.update_line(self.line2, line2)
        self.root.after(1000, self.refresh)


if __name__ == "__main__":
    TaskbarMonitor()
