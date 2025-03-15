import subprocess
import winreg

# List of unwanted software
UNWANTED_SOFTWARE = [
    "TeamViewer", "AnyDesk", "LogMeIn", "UltraVNC", "Ammyy Admin", "RemotePC", "RealVNC",
    "Chrome Remote Desktop", "AeroAdmin", "GoToMyPC", "ConnectWise Control",
    "VMware", "VirtualBox", "Hyper-V", "QEMU", "Sandboxie", "Parallels Desktop", "KVM", "Windows Sandbox",
    "CCleaner", "Advanced SystemCare", "Wise Registry Cleaner", "Glary Utilities",
    "Auslogics BoostSpeed", "Reimage Repair", "PC Optimizer Pro", "System Mechanic",
    "Wireshark", "Cain", "John the Ripper", "Mimikatz", "Metasploit", "Hydra",
    "Aircrack-ng", "KMSPico", "Nmap", "Nikto", "Snort",
    "uTorrent", "BitTorrent", "qBittorrent", "FrostWire", "Deluge", "Tixati", "Vuze",
    "Opera Browser", "Yahoo Toolbar", "Ask Toolbar", "Baidu Antivirus",
    "MySearchDial", "Search Protect by Conduit", "Reimage Repair", "SweetIM",
    "Spigot Toolbar", "Softonic Downloader",
    "Revealer Keylogger", "Spyrix Free Keylogger", "Elite Keylogger", "KidLogger",
    "Refog Keylogger", "Ardamax Keylogger", "Actual Keylogger", "Iwantsoft Keylogger",
    "McAfee Security Scan", "Norton Security", "WildTangent Games",
    "Microsoft News", "Candy Crush Saga", "CyberLink PowerDVD",
    "HP JumpStart", "Lenovo Vantage"
]

def get_installed_software():
    installed_programs = []
    registry_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]
    for reg_path in registry_paths:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                for i in range(0, winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                program_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                                installed_programs.append(program_name.lower())
                            except (FileNotFoundError, OSError):
                                continue
                    except (FileNotFoundError, OSError):
                        continue
        except FileNotFoundError:
            continue
    return installed_programs

def get_running_processes():
    try:
        result = subprocess.run(["powershell", "Get-Process | Select-Object ProcessName"], 
                                capture_output=True, text=True, shell=True)
        return result.stdout.lower()
    except Exception:
        return ""

def get_installed_folders():
    program_folders = []
    paths = [r"C:\Program Files", r"C:\Program Files (x86)"]
    for path in paths:
        try:
            result = subprocess.run(["powershell", f"Get-ChildItem '{path}' -Name -Force"], 
                                    capture_output=True, text=True, shell=True)
            program_folders.extend(result.stdout.lower().splitlines())
        except Exception:
            continue
    return program_folders

def detect_unwanted_software():
    installed_programs = get_installed_software()
    running_processes = get_running_processes()
    program_folders = get_installed_folders()

    detected = {"Installed Software": [], "Running Processes": [], "Program Folders": []}

    for software in UNWANTED_SOFTWARE:
        software_lower = software.lower()
        
        # ✅ Check exact software name in installed programs
        if any(program.strip() == software_lower for program in installed_programs):
            detected["Installed Software"].append(software)
        
        # ✅ Check running processes
        if software_lower in running_processes:
            detected["Running Processes"].append(software)
        
        # ✅ Check exact match in program folders
        if any(folder.strip() == software_lower for folder in program_folders):
            detected["Program Folders"].append(software)

    return detected

if __name__ == "__main__":
    results = detect_unwanted_software()

    print("\n🔍 **Unwanted Software Detection Report:**\n")
    for category, software_list in results.items():
        print(f"\n📌 {category}:")
        if software_list:
            for software in software_list:
                print(f"   - ❌ {software} FOUND")
        else:
            print("   ✅ No unwanted software detected.")
