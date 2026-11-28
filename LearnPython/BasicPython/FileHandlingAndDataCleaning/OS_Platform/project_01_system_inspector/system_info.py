import os
import platform
import sys


def collect_system_info():
    """Collect operating-system and Python runtime information."""
    return {
        "os_name": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "os_family": os.name,
        "machine_architecture": platform.machine(),
        "processor": platform.processor(),
        "full_platform": platform.platform(),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "python_executable": sys.executable,
        "python_prefix": sys.prefix,
        "process_id": os.getpid(),
        "current_working_directory": os.getcwd(),
        "script_directory": os.path.dirname(os.path.abspath(__file__)),
        "computer_node_name": platform.node(),
    }
