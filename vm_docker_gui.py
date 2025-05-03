import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import subprocess
import os

# Globals
ISO_FILE = None
QEMU_EXE = "qemu-system-x86_64.exe"
QEMU_IMG = "qemu-img.exe"

# ----------------------- VM Functions -----------------------

def select_iso():
    global ISO_FILE
    path = filedialog.askopenfilename(title="Select ISO File", filetypes=[("ISO files", "*.iso")])
    if path:
        ISO_FILE = path
        messagebox.showinfo("ISO Selected", f"Using ISO file:\n{ISO_FILE}")

def create_virtual_disk():
    disk_name = simpledialog.askstring("Disk Name", "Enter disk name (e.g., disk1.qcow2):")
    disk_type = simpledialog.askstring("Disk Format", "Enter disk format (e.g., qcow2, raw, vmdk):", initialvalue="qcow2")
    size = simpledialog.askstring("Disk Size", "Enter disk size (e.g., 1G, 5G):")
    if not disk_name or not disk_type or not size:
        return
    cmd = [QEMU_IMG, "create", "-f", disk_type, disk_name, size]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        messagebox.showinfo("Output", result.stdout if result.returncode == 0 else result.stderr)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_vm():
    if not ISO_FILE:
        messagebox.showerror("Error", "Please select an ISO file first.")
        return
    cpu = simpledialog.askstring("CPU Cores", "Enter number of CPU cores (e.g., 2):")
    memory = simpledialog.askstring("Memory", "Enter memory size in MB (e.g., 1024):")
    disk = filedialog.askopenfilename(title="Select Virtual Disk", filetypes=[("QCOW2 files", "*.qcow2")])
    if not cpu or not memory or not disk:
        return
    cmd = [QEMU_EXE, "-m", memory, "-smp", cpu, "-cdrom", ISO_FILE, "-boot", "d", "-hda", disk, "-vga", "std"]
    try:
        subprocess.Popen(cmd)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ----------------------- Docker Functions -----------------------

def create_dockerfile():
    content = simpledialog.askstring("Dockerfile Content", "Enter the contents of your Dockerfile:")
    if not content:
        return
    path = filedialog.asksaveasfilename(title="Save Dockerfile As", defaultextension=".Dockerfile")
    if path:
        with open(path, 'w') as f:
            f.write(content)
        messagebox.showinfo("Success", f"Dockerfile saved to {path}")

def build_docker_image():
    path = filedialog.askopenfilename(title="Select Dockerfile", filetypes=[("Dockerfile", "*.Dockerfile")])
    if not path:
        return
    tag = simpledialog.askstring("Image Tag", "Enter image name:tag (e.g., myimage:latest):")
    if not tag:
        return
    cmd = ["docker", "build", "-t", tag, "-f", path, os.path.dirname(path)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        messagebox.showinfo("Output", result.stdout if result.returncode == 0 else result.stderr)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def list_docker_images():
    cmd = ["docker", "images"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        messagebox.showinfo("Docker Images", result.stdout)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def list_running_containers():
    cmd = ["docker", "ps"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        messagebox.showinfo("Running Containers", result.stdout)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def stop_container():
    container_id = simpledialog.askstring("Container ID", "Enter Container ID or Name to stop:")
    if not container_id:
        return
    cmd = ["docker", "stop", container_id]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        messagebox.showinfo("Result", result.stdout if result.returncode == 0 else result.stderr)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def search_local_image():
    image = simpledialog.askstring("Image Name", "Enter local image name/tag to search:")
    if not image:
        return
    cmd = ["docker", "images", image]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        messagebox.showinfo("Search Result", result.stdout)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def search_dockerhub():
    image = simpledialog.askstring("DockerHub Search", "Enter image name to search on DockerHub:")
    if not image:
        return
    cmd = ["docker", "search", image]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        messagebox.showinfo("DockerHub Search Result", result.stdout)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def pull_image():
    image = simpledialog.askstring("Pull Image", "Enter image name to pull (e.g., ubuntu:latest):")
    if not image:
        return
    cmd = ["docker", "pull", image]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        messagebox.showinfo("Pull Result", result.stdout)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ----------------------- GUI Setup -----------------------

root = tk.Tk()
root.title("Cloud Management System - QEMU + Docker")
root.geometry("600x400")

tabs = ttk.Notebook(root)
vm_tab = ttk.Frame(tabs)
docker_tab = ttk.Frame(tabs)
tabs.add(vm_tab, text="VM Management")
tabs.add(docker_tab, text="Docker Management")
tabs.pack(expand=1, fill="both")

# VM Tab Buttons
tk.Button(vm_tab, text="Select ISO File", width=40, command=select_iso).pack(pady=5)
tk.Button(vm_tab, text="Create Virtual Disk", width=40, command=create_virtual_disk).pack(pady=5)
tk.Button(vm_tab, text="Create Virtual Machine", width=40, command=create_vm).pack(pady=5)

# Docker Tab Buttons
tk.Button(docker_tab, text="Create Dockerfile", width=40, command=create_dockerfile).pack(pady=5)
tk.Button(docker_tab, text="Build Docker Image", width=40, command=build_docker_image).pack(pady=5)
tk.Button(docker_tab, text="List Docker Images", width=40, command=list_docker_images).pack(pady=5)
tk.Button(docker_tab, text="List Running Containers", width=40, command=list_running_containers).pack(pady=5)
tk.Button(docker_tab, text="Stop Container", width=40, command=stop_container).pack(pady=5)
tk.Button(docker_tab, text="Search Local Image", width=40, command=search_local_image).pack(pady=5)
tk.Button(docker_tab, text="Search DockerHub", width=40, command=search_dockerhub).pack(pady=5)
tk.Button(docker_tab, text="Pull Docker Image", width=40, command=pull_image).pack(pady=5)

root.mainloop()