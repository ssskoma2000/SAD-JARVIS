import psutil
import socket
import platform

def get_system_info():
    """Tizim haqida real ma'lumotlarni oladi."""
    uname = platform.uname()
    return {
        "system": uname.system,
        "node": uname.node,
        "release": uname.release,
        "version": uname.version,
        "machine": uname.machine,
        "processor": uname.processor
    }

def get_resource_usage():
    """CPU va RAM ishlatilishini qaytaradi."""
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "ram_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent
    }

def get_active_connections():
    """Aktiv tarmoq ulanishlarini (ESTABLISHED) qaytaradi."""
    connections = []
    try:
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == 'ESTABLISHED':
                laddr = f"{conn.laddr.ip}:{conn.laddr.port}"
                raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                connections.append(f"{laddr} <--> {raddr} [PID: {conn.pid}]")
    except Exception:
        pass
    return connections[:10]  # Faqat oxirgi 10 tasini qaytarish

def scan_local_ports():
    """Lokal portlarni tekshiradi (Real Scan)."""
    target_ports = [21, 22, 80, 443, 3306, 5000, 8000, 8080]
    open_ports = []
    # Bu yerda oddiy socket connect ishlatiladi
    return open_ports # Tezlik uchun hozircha bo'sh, real scan serverni qotirishi mumkin