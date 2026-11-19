"""Hardware and environment checks run at the start of every notebook."""
from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from typing import Optional


def _run(cmd: list[str]) -> Optional[str]:
    """Run a command and return its output, or None if it is unavailable."""
    try:
        out = subprocess.run(cmd, capture_output=True, text=True,
                             timeout=15, check=True)
        return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None


def _ram_gb() -> Optional[float]:
    try:                                    # Linux (Colab)
        with open('/proc/meminfo') as f:
            for line in f:
                if line.startswith('MemTotal:'):
                    return round(int(line.split()[1]) / 1024 / 1024, 1)
    except OSError:
        pass
    out = _run(['sysctl', '-n', 'hw.memsize'])      # macOS
    return round(int(out) / 1024 ** 3, 1) if out and out.isdigit() else None


def _gpu_info() -> list[dict]:
    out = _run(['nvidia-smi',
                '--query-gpu=name,memory.total,memory.free,driver_version',
                '--format=csv,noheader,nounits'])
    gpus = []
    if out:
        for line in out.splitlines():
            name, total, free, driver = [p.strip() for p in line.split(',')]
            gpus.append({
                'name': name,
                'vram_total_gb': round(int(total) / 1024, 1),
                'vram_free_gb': round(int(free) / 1024, 1),
                'driver': driver,
            })
    return gpus


def get_hardware_report(path: str = '.') -> dict:
    """Collect Python, OS, CPU, RAM, free disk (for `path`) and GPU details."""
    disk = shutil.disk_usage(path)
    return {
        'python': sys.version.split()[0],
        'platform': platform.platform(),
        'cpu_count': os.cpu_count(),
        'ram_gb': _ram_gb(),
        'disk_free_gb': round(disk.free / 1024 ** 3, 1),
        'gpus': _gpu_info(),
    }


def check_requirements(report: dict, need_gpu: bool = False,
                       min_vram_gb: float = 0, min_ram_gb: float = 0,
                       min_disk_gb: float = 0) -> list[str]:
    """Return a list of problems. An empty list means it is safe to proceed."""
    problems = []
    if need_gpu and not report['gpus']:
        problems.append('No GPU found. In Colab: Runtime > Change runtime type > GPU.')
    elif need_gpu and report['gpus'][0]['vram_total_gb'] < min_vram_gb:
        problems.append(f"GPU has {report['gpus'][0]['vram_total_gb']} GB VRAM; "
                        f'{min_vram_gb} GB needed.')
    if report['ram_gb'] is not None and report['ram_gb'] < min_ram_gb:
        problems.append(f"RAM is {report['ram_gb']} GB; {min_ram_gb} GB needed.")
    if report['disk_free_gb'] < min_disk_gb:
        problems.append(f"Free disk is {report['disk_free_gb']} GB; {min_disk_gb} GB needed.")
    return problems
