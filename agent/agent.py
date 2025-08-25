import psutil
import platform
import socket
import requests
import time
import ctypes
from datetime import datetime
import wmi


API_BASE = "http://localhost:8000/api"

def safe_get(f, default=None):
    try:
        return f()
    except Exception:
        return default


def get_system_info():
    hostname = socket.gethostname()
    ip_addr = safe_get(lambda: socket.gethostbyname(hostname), "0.0.0.0")
    boot_time = psutil.boot_time()
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('C:\\')  # Use C: drive for Windows

    cpu_freq = psutil.cpu_freq() or type("obj", (), {"current": 0, "max": 0})

    system = platform.system()
    release = platform.release()
    version = platform.version()

    # 🔧 Fix: Detect Windows 11 correctly
    if system == "Windows" and release == "10":
        try:
            build = int(version.split(".")[2])
            if build >= 22000:
                release = "11"
        except Exception:
            pass

    return {
        "hostname": hostname,
        "ip": ip_addr,
        "os": system,
        "os_version": version,
        "release": release,
        "machine": platform.machine(),
        "processor": platform.processor() or platform.uname().processor,
        "physical_cores": psutil.cpu_count(logical=False) or 0,
        "logical_cores": psutil.cpu_count(logical=True) or 0,
        "cpu_freq_current": getattr(cpu_freq, "current", 0),
        "cpu_freq_max": getattr(cpu_freq, "max", 0),
        "total_ram": mem.total,
        "used_ram": mem.used,
        "available_ram": mem.available,
        "storage_total": disk.total,
        "storage_free": disk.free,
        "storage_used": disk.used,
        "boot_time": int(boot_time),
        "collected_at": datetime.utcnow().isoformat() + "Z",
        "cpu_percent": psutil.cpu_percent(interval=1.0),
    }

def get_process_list():
    # First pass to prime CPU calculations
    for proc in psutil.process_iter(['pid']):
        try:
            proc.cpu_percent(interval=None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Wait to get accurate CPU measurements
    time.sleep(0.5)
    
    hostname = socket.gethostname()
    processes = []
    collected_pids = set()
    
    # Get processes using psutil
    for proc in psutil.process_iter(['pid', 'name', 'username', 'ppid', 'cpu_percent']):
        try:
            with proc.oneshot():
                pid = proc.info['pid']
                
                # Skip if we already collected this PID
                if pid in collected_pids:
                    continue
                    
                name = proc.info.get('name', 'unknown') or "unknown"
                ppid = proc.info.get('ppid', 0)
                username = proc.info.get('username', '') or ""
                
                # Memory usage using memory_full_info()
                try:
                    mem_info = proc.memory_full_info()
                    memory_mb = getattr(mem_info, "private", mem_info.rss) / (1024 * 1024)
                except (psutil.AccessDenied, AttributeError):
                    memory_mb = 0.0
                except:
                    memory_mb = 0.0
                
                # CPU usage
                try:
                    cpu_percent = proc.info.get('cpu_percent', 0)
                    if cpu_percent is None:
                        cpu_percent = 0.0
                except:
                    cpu_percent = 0.0
                
                process_data = {
                    "hostname": hostname,
                    "pid": pid,
                    "ppid": ppid,
                    "name": name,
                    "cpu_percent": round(float(cpu_percent), 1),
                    "memory_mb": round(memory_mb, 2),
                    "username": username.split('\\')[-1] if '\\' in username else username,
                    "sample_time": int(time.time()),
                }
                processes.append(process_data)
                collected_pids.add(pid)
                
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
        except Exception as e:
            print(f"Error getting info for process {pid}: {e}")
            continue
    
    # Additional method: Use WMI to get more processes (Windows only)
    if platform.system() == "Windows":
        try:
            c = wmi.WMI()
            for process in c.Win32_Process():
                pid = process.ProcessId
                if pid in collected_pids:
                    continue
                    
                # Convert memory from bytes to MB
                memory_mb = int(process.WorkingSetSize or 0) / (1024 * 1024)
                
                process_data = {
                    "hostname": hostname,
                    "pid": pid,
                    "ppid": process.ParentProcessId or 0,
                    "name": process.Name or "unknown",
                    "cpu_percent": 0.0,  # WMI doesn't provide CPU percentage easily
                    "memory_mb": round(memory_mb, 2),
                    "username": "",  # WMI requires more work to get username
                    "sample_time": int(time.time()),
                }
                processes.append(process_data)
                collected_pids.add(pid)
                
        except ImportError:
            print("WMI not available. Install with: pip install wmi")
        except Exception as e:
            print(f"Error with WMI method: {e}")
    
    return processes


def analyze_processes(processes):
    """Analyze and print information about collected processes"""
    print(f"Collected {len(processes)} unique processes")
    
    # Check for browser processes
    browser_keywords = ['chrome', 'edge', 'firefox', 'opera', 'brave', 'browser', 'msedge', 'tab', 'render', 'gpu']
    browser_processes = [p for p in processes if any(keyword in p['name'].lower() for keyword in browser_keywords)]

    print(f"Browser-related processes found: {len(browser_processes)}")

    if browser_processes:
        print("\nBrowser processes found:")
        for p in browser_processes[:10]:  # Show first 10
            print(f"  {p['name']} (PID: {p['pid']}, Memory: {p['memory_mb']} MB)")
    else:
        print("No browser processes found.")

    # Show top 10 processes by memory usage
    print("\nTop 10 processes by memory usage:")
    top_memory = sorted(processes, key=lambda x: x['memory_mb'], reverse=True)[:10]
    for i, p in enumerate(top_memory, 1):
        print(f"{i}. {p['name']}: {p['memory_mb']} MB")

    # Check if we have any processes with common names
    common_names = ['explorer', 'svchost', 'dwm', 'python', 'code', 'node', 'java']
    print(f"\nProcesses with common names:")
    for name in common_names:
        count = len([p for p in processes if name in p['name'].lower()])
        if count > 0:
            print(f"  {name}: {count} processes")

def post_system_info(info):
    try:
        url = f"{API_BASE}/system-info/"
        r = requests.post(url, json=info, timeout=15)
        r.raise_for_status()
        print("[SystemInfo] Uploaded successfully.")
        return True
    except requests.exceptions.RequestException as e:
        print("[SystemInfo] Upload failed:", e)
        return False

def post_processes_bulk(processes):
    if not processes:
        return False
    try:
        url = f"{API_BASE}/processes/bulk/"
        r = requests.post(url, json=processes, timeout=30)
        r.raise_for_status()
        print(f"[Processes] Uploaded {len(processes)} processes for {processes[0]['hostname']}")
        return True
    except requests.exceptions.RequestException as e:
        print("[Processes] Upload failed:", e)
        return False

def is_admin():
    """Check if the script is running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    # Check if running as admin
    if platform.system() == "Windows" and not is_admin():
        print("Warning: Not running as administrator. Some processes may not be accessible.")
        print("For best results, run this script as Administrator.")
    
    # Run continuously and refresh every 5 seconds
    refresh_interval = 5  # seconds
    
    while True:
        try:
            print(f"\n{'='*50}")
            print(f"Cycle started at {datetime.now().strftime('%H:%M:%S')}")
            print(f"{'='*50}")
            
            # Get and post system info
            print("Collecting system information...")
            sys_info = get_system_info()
            system_success = post_system_info(sys_info)
            
            # Get and post process info
            print("Collecting process information...")
            processes = get_process_list()
            
            # Analyze processes
            analyze_processes(processes)
            
            processes_success = post_processes_bulk(processes)
            
            if system_success and processes_success:
                print(f"Cycle completed successfully. Next update in {refresh_interval} seconds...")
            else:
                print(f"Cycle completed with errors. Next update in {refresh_interval} seconds...")
            
            time.sleep(refresh_interval)
            
        except KeyboardInterrupt:
            print("\nStopping agent...")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            print(f"Retrying in {refresh_interval} seconds...")
            time.sleep(refresh_interval)