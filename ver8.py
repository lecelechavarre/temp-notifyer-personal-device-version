import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import psutil
import winsound
from plyer import notification
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
import csv
import pandas as pd
from tkinter import scrolledtext

class ResponsiveDesign:
    """Handles responsive design and screen adaptation"""
    
    def __init__(self, root):
        self.root = root
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.setup_fullscreen_geometry()
        
    def setup_fullscreen_geometry(self):
        """Set up fullscreen window using geometry and zoomed state"""
        # Set window to full screen using geometry and zoomed state
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.root.state('zoomed')
        self.root.minsize(1000, 700)
        
    def get_scaling_factors(self):
        """Calculate scaling factors based on screen resolution"""
        base_width = 1920  # Base resolution for scaling
        base_height = 1080
        
        width_scale = self.screen_width / base_width
        height_scale = self.screen_height / base_height
        
        # Use the smaller scale to ensure everything fits
        scale_factor = min(width_scale, height_scale, 1.5)  # Cap at 1.5x
        
        return {
            'font_scale': max(0.8, min(scale_factor, 1.2)),
            'padding_scale': max(0.8, min(scale_factor, 1.3)),
            'widget_scale': max(0.9, min(scale_factor, 1.4))
        }

class ThemeManager:
    
    def __init__(self):
        # CHANGED: Set default theme to "light" instead of "dark"
        self.current_theme = "light"  # Default theme is now light
        self.themes = {
            "dark": {
                'primary': '#3b82f6',      # Professional Blue
                'secondary': '#60a5fa',    # Medium Blue
                'accent': '#93c5fd',       # Light Blue
                'background': '#0f172a',   # Dark blue background
                'surface': '#1e293b',      # Card surface
                'card_bg': '#1e293b',      # Card background
                'text_primary': '#f8fafc', # Light text
                'text_secondary': '#cbd5e1', # Medium light text
                'success': '#10b981',      # Green
                'warning': '#f59e0b',      # Amber
                'error': '#ef4444',        # Red
                'border': '#334155',       # Dark border
                'hover': '#374151',        # Hover state
                'grid_color': '#2d3748',   # Grid pattern color
                'input_bg': '#1e293b',     # Input background
                'input_fg': '#f8fafc',     # Input foreground
            },
            "light": {
                'primary': '#2563eb',      # Professional Blue
                'secondary': '#3b82f6',    # Medium Blue
                'accent': '#60a5fa',       # Light Blue
                'background': '#f8fafc',   # Light background
                'surface': '#ffffff',      # Card surface
                'card_bg': '#ffffff',      # Card background
                'text_primary': '#1e293b', # Dark text
                'text_secondary': '#475569', # Medium dark text
                'success': '#059669',      # Green
                'warning': '#d97706',      # Amber
                'error': '#dc2626',        # Red
                'border': '#e2e8f0',       # Light border
                'hover': '#f1f5f9',        # Hover state
                'grid_color': '#e2e8f0',   # Grid pattern color
                'input_bg': '#ffffff',     # Input background
                'input_fg': '#1e293b',     # Input foreground
            }
        }
    
    def get_theme(self):
        """Get current theme colors"""
        return self.themes[self.current_theme]
    
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        return self.get_theme()
    
    def set_theme(self, theme_name):
        """Set specific theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
        return self.get_theme()

class ResponsiveGradientBackground:
    """Creates a responsive gradient background that adapts to theme and window size"""
    def __init__(self, canvas, width, height, theme_colors):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.theme_colors = theme_colors
        self.gradient_ids = []
        self.create_responsive_background()
        
    def create_responsive_background(self):
        """Create responsive gradient background that adapts to theme"""
        # Clear existing gradients
        for grad_id in self.gradient_ids:
            self.canvas.delete(grad_id)
        self.gradient_ids = []
        
        # Set canvas background
        self.canvas.configure(bg=self.theme_colors['background'])
        
        # For light theme, use minimal background with subtle gradient
        if self.theme_colors['background'] == '#f8fafc':  # Light theme
            self.create_light_background()
        else:  # Dark theme
            self.create_dark_background()
    
    def create_light_background(self):
        """Create minimal, clean background for light theme"""
        # Subtle gradient from top to bottom
        colors = [
            self.theme_colors['background'],
            '#f1f5f9',
            self.theme_colors['background']
        ]
        
        for i in range(3):
            color_index = i % len(colors)
            grad_id = self.canvas.create_rectangle(
                0, i * self.height // 3,
                self.width, (i + 1) * self.height // 3,
                fill=colors[color_index],
                outline='',
                width=0
            )
            self.gradient_ids.append(grad_id)
        
        # Add very subtle grid pattern for light theme
        self.create_subtle_grid()
        
    def create_dark_background(self):
        """Create sophisticated gradient background for dark theme"""
        colors = [
            self.theme_colors['background'],
            '#1e293b',
            '#334155',
            self.theme_colors['background']
        ]
        
        for i in range(4):
            color_index = i % len(colors)
            grad_id = self.canvas.create_rectangle(
                0, i * self.height // 4,
                self.width, (i + 1) * self.height // 4,
                fill=colors[color_index],
                outline='',
                width=0
            )
            self.gradient_ids.append(grad_id)
        
        # Add grid pattern for dark theme
        self.create_subtle_grid()
        self.create_minimal_decorations()
    
    def create_subtle_grid(self):
        """Add a very subtle grid pattern that adapts to theme"""
        grid_color = self.theme_colors['grid_color']
        spacing = 100  # Responsive spacing
        
        # Calculate appropriate spacing based on window size
        max_spacing = max(80, min(120, self.width // 15))
        spacing = max_spacing
        
        # Vertical lines - only add if window is wide enough
        if self.width > 600:
            for x in range(0, self.width, spacing):
                line_id = self.canvas.create_line(
                    x, 0, x, self.height,
                    fill=grid_color, 
                    width=0.5, 
                    dash=(2, 4)
                )
                self.gradient_ids.append(line_id)
        
        # Horizontal lines - only add if window is tall enough
        if self.height > 400:
            for y in range(0, self.height, spacing):
                line_id = self.canvas.create_line(
                    0, y, self.width, y,
                    fill=grid_color, 
                    width=0.5, 
                    dash=(2, 4)
                )
                self.gradient_ids.append(line_id)
    
    def create_minimal_decorations(self):
        """Add minimal decorative elements that adapt to theme"""
        if self.theme_colors['background'] == '#f8fafc':  # Light theme
            # Minimal decorations for light theme
            accent_color = self.theme_colors['accent']
            for i in range(3):
                size = 60 + i * 15
                x = self.width * (i % 3) / 3 + 50
                y = self.height * (i // 3) / 2 + 50
                
                circle_id = self.canvas.create_oval(
                    x - size, y - size, x + size, y + size,
                    fill='', 
                    outline=accent_color,
                    width=0.5,
                    dash=(4, 8)
                )
                self.gradient_ids.append(circle_id)
        else:  # Dark theme
            # Slightly more prominent decorations for dark theme
            accent_color = self.theme_colors['accent']
            for i in range(4):
                size = 40 + i * 20
                x = self.width * (i % 4) / 4 + 80
                y = self.height * (i // 4) / 2 + 80
                
                circle_id = self.canvas.create_oval(
                    x - size, y - size, x + size, y + size,
                    fill='', 
                    outline=accent_color,
                    width=1,
                    dash=(6, 10)
                )
                self.gradient_ids.append(circle_id)
    
    def update_theme(self, theme_colors):
        """Update background with new theme colors"""
        self.theme_colors = theme_colors
        self.create_responsive_background()

class StorageTemperatureReader:
    """Storage temperature reader specifically for storage devices using OpenHardwareMonitor"""
    def __init__(self):
        self.wmi_available = False
        self.ohm_available = True
        self.initialize_wmi()
    
    def initialize_wmi(self):
        """Initialize WMI connection and check OpenHardwareMonitor availability"""
        try:
            import wmi
            self.wmi_available = True
            print("✅ WMI support initialized")
            
            # Test if OpenHardwareMonitor is running
            try:
                w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
                sensors = w.Sensor()
                self.ohm_available = True
                print("✅ OpenHardwareMonitor detected and accessible")
                print(f"📊 Found {len(sensors)} sensors")
                
                # Print ALL temperature sensors for debugging
                temp_sensors = [s for s in sensors if s.SensorType == "Temperature"]
                print("🌡️ All temperature sensors:")
                for sensor in temp_sensors:
                    print(f"  - {sensor.Name}: {sensor.Value}°C (Parent: {sensor.Parent})")
                    
            except Exception as e:
                print("❌ OpenHardwareMonitor not detected or not running")
                print("💡 Please run OpenHardwareMonitor as Administrator")
                self.ohm_available = False
                
        except ImportError:
            print("❌ WMI not available - install: pip install wmi")
            self.wmi_available = False
            self.ohm_available = False
    
    def _is_storage_sensor(self, sensor_name, parent_name):
        """Check if sensor belongs to a storage device"""
        storage_keywords = [
            'hdd', 'ssd', 'disk', 'drive', 'nvme', 'sata', 
            'hard disk', 'solid state', 'samsung', 'crucial',
            'western digital', 'seagate', 'kingston', 'adata',
            'sandisk', 'intel ssd', 'toshiba', 'hitachi'
        ]
        
        sensor_lower = sensor_name.lower()
        parent_lower = parent_name.lower() if parent_name else ""
        
        # Check if it's a temperature sensor under a storage device
        if "temperature" in sensor_lower:
            # Check if parent is a storage device
            if any(keyword in parent_lower for keyword in storage_keywords):
                return True
            
            # Check if sensor name itself indicates storage
            if any(keyword in sensor_lower for keyword in storage_keywords):
                return True
        
        return False
    
    def get_storage_temperatures(self):
        """Get temperatures for all storage devices from OpenHardwareMonitor"""
        storage_temps = {}
        
        if not self.ohm_available:
            print("❌ OpenHardwareMonitor not available - no temperature data")
            return None
        
        try:
            import wmi
            w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
            sensors = w.Sensor()
            
            # Look for ALL temperature sensors first
            all_temp_sensors = []
            for sensor in sensors:
                if (sensor.SensorType == "Temperature" and 
                    sensor.Value is not None):
                    
                    all_temp_sensors.append({
                        'name': sensor.Name,
                        'value': float(sensor.Value),
                        'parent': sensor.Parent if hasattr(sensor, 'Parent') else "Unknown"
                    })
            
            print(f"🔍 Found {len(all_temp_sensors)} temperature sensors total")
            
            # Filter for storage temperatures
            storage_sensors = []
            for sensor in all_temp_sensors:
                if self._is_storage_sensor(sensor['name'], sensor['parent']):
                    storage_sensors.append(sensor)
                else:
                    print(f"  Skipping non-storage: {sensor['name']} (Parent: {sensor['parent']})")
            
            print(f"💾 Found {len(storage_sensors)} storage temperature sensors")
            
            # Organize storage temperatures
            for sensor in storage_sensors:
                # Use parent name if available, otherwise use sensor name
                if sensor['parent'] and sensor['parent'] != "Unknown":
                    device_name = sensor['parent']
                else:
                    device_name = sensor['name']
                
                # Subtract 10°C from actual reading for room temperature uniformity
                raw_temp = sensor['value']
                adjusted_temp = raw_temp - 13
                storage_temps[device_name] = adjusted_temp
                
                print(f"  {device_name}: {raw_temp}°C")
            
            # If we found storage temperatures, return them
            if storage_temps:
                print("📊 Storage temperatures found:")
                for device, temp in storage_temps.items():
                    print(f"  {device}: {temp}°C")
                return storage_temps
            else:
                print("❌ No storage temperatures found in OpenHardwareMonitor")
                # Let's try an alternative approach - look for any temperature under storage devices
                return self._find_storage_temps_alternative(sensors)
            
        except Exception as e:
            print(f"❌ Error reading storage temperatures: {e}")
            self.ohm_available = False
            return None
    
    def _find_storage_temps_alternative(self, sensors):
        """Alternative method to find storage temperatures"""
        print("🔄 Trying alternative storage detection method...")
        storage_temps = {}
        
        # Get all hardware items to find storage devices
        try:
            import wmi
            w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
            hardware_items = w.Hardware()
            
            storage_devices = []
            for hardware in hardware_items:
                hw_name = hardware.Name if hardware.Name else ""
                hw_lower = hw_name.lower()
                
                # Check if this is a storage device
                storage_keywords = ['ssd', 'hdd', 'disk', 'drive', 'samsung', 'crucial', 'wd', 'seagate']
                if any(keyword in hw_lower for keyword in storage_keywords):
                    storage_devices.append(hw_name)
                    print(f"  Found storage device: {hw_name}")
            
            # Now look for temperature sensors under these storage devices
            for sensor in sensors:
                if (sensor.SensorType == "Temperature" and 
                    sensor.Value is not None and
                    hasattr(sensor, 'Parent') and
                    sensor.Parent in storage_devices):
                    
                    # Subtract 10°C from actual reading
                    raw_temp = float(sensor.Value)
                    adjusted_temp = raw_temp - 10
                    storage_temps[sensor.Parent] = adjusted_temp
                    print(f"  Found temperature for {sensor.Parent}: {raw_temp}°C -> {adjusted_temp}°C")
        
        except Exception as e:
            print(f"❌ Alternative method failed: {e}")
        
        return storage_temps if storage_temps else None
    
    def get_average_storage_temperature(self):
        """Get the average temperature across all storage devices"""
        storage_temps = self.get_storage_temperatures()
        if storage_temps:
            avg_temp = sum(storage_temps.values()) / len(storage_temps)
            print(f"📈 Average storage temperature: {avg_temp:.1f}°C")
            return avg_temp
        else:
            return None
    
    def get_max_storage_temperature(self):
        """Get the maximum temperature among all storage devices"""
        storage_temps = self.get_storage_temperatures()
        if storage_temps:
            max_temp = max(storage_temps.values())
            max_device = max(storage_temps, key=storage_temps.get)
            print(f"🔥 Hottest storage: {max_device} at {max_temp:.1f}°C")
            return max_temp
        else:
            return None
    
    def get_detailed_sensor_info(self):
        """Get detailed information about all available sensors"""
        if not self.wmi_available:
            return "WMI not available"
        
        try:
            import wmi
            info = []
            
            # OpenHardwareMonitor sensors
            if self.ohm_available:
                try:
                    w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
                    sensors = w.Sensor()
                    info.append("=== OpenHardwareMonitor All Temperature Sensors ===")
                    
                    # Show all temperature sensors with their parent information
                    temp_sensors = [s for s in sensors if s.SensorType == "Temperature" and s.Value is not None]
                    
                    if temp_sensors:
                        for sensor in temp_sensors:
                            parent_info = sensor.Parent if hasattr(sensor, 'Parent') else "No parent"
                            raw_temp = float(sensor.Value)
                            adjusted_temp = raw_temp - 10
                            info.append(f"  {sensor.Name}: {raw_temp}°C -> {adjusted_temp}°C (Parent: {parent_info})")
                    else:
                        info.append("No temperature sensors found")
                        
                except Exception as e:
                    info.append(f"OpenHardwareMonitor error: {e}")
            
            return "\n".join(info) if info else "No sensor information available"
            
        except Exception as e:
            return f"Error getting sensor info: {e}"

class SearchResultModal:
    """Modal window to display search results with time range and history graph"""
    def __init__(self, parent, start_datetime, end_datetime, logs, theme_manager, responsive_design):
        self.parent = parent
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.logs = logs
        self.theme_manager = theme_manager
        self.responsive_design = responsive_design
        self.colors = self.theme_manager.get_theme()
        self.window = None
        self.create_modal()
    
    def create_modal(self):
        """Create the search result modal window"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Search Results - Temperature History")
        
        # Use responsive design for modal
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = min(1200, screen_width - 100)
        window_height = min(800, screen_height - 100)
        self.window.geometry(f"{window_width}x{window_height}")
        self.window.minsize(1000, 700)
        
        # Center the window on screen
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"+{x}+{y}")
        
        # Set proper background color
        if self.colors['background'] == '#0f172a':  # Dark mode
            bg_color = '#1e293b'
            text_bg = '#1e293b'
        else:  # Light mode
            bg_color = '#ffffff'
            text_bg = '#ffffff'
            
        self.window.configure(bg=bg_color)
        
        # Make the window modal
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Configure grid weights for responsiveness
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        
        # Header with search range information
        header_frame = ttk.Frame(self.window, style='Modern.TFrame')
        header_frame.grid(row=0, column=0, sticky='ew', padx=20, pady=20)
        header_frame.columnconfigure(0, weight=1)
        
        # Title with search range
        title_text = f"Temperature History: {self.start_datetime.strftime('%Y-%m-%d %H:%M')} to {self.end_datetime.strftime('%Y-%m-%d %H:%M')}"
        title_label = ttk.Label(header_frame, text=title_text,
                               background=bg_color,
                               foreground=self.colors['text_primary'],
                               font=("Segoe UI", 16, "bold"))
        title_label.grid(row=0, column=0, sticky='w')
        
        # Statistics frame
        stats_frame = ttk.Frame(header_frame, style='Modern.TFrame')
        stats_frame.grid(row=1, column=0, sticky='ew', pady=(10, 0))
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)
        stats_frame.columnconfigure(2, weight=1)
        
        # Parse temperature data for statistics
        temperatures = self.parse_temperature_data()
        
        if temperatures:
            avg_temp = sum(temperatures) / len(temperatures)
            max_temp = max(temperatures)
            min_temp = min(temperatures)
            
            # Average temperature
            avg_frame = ttk.Frame(stats_frame, style='Card.TFrame', padding="10")
            avg_frame.grid(row=0, column=0, sticky='ew', padx=(0, 10))
            
            ttk.Label(avg_frame, text="Average Temp", 
                     background=self.colors['card_bg'],
                     foreground=self.colors['text_secondary'],
                     font=("Segoe UI", 9)).pack(anchor=tk.CENTER)
            ttk.Label(avg_frame, text=f"{avg_temp:.1f}°C", 
                     background=self.colors['card_bg'],
                     foreground=self.colors['primary'],
                     font=("Segoe UI", 14, "bold")).pack(anchor=tk.CENTER)
            
            # Max temperature
            max_frame = ttk.Frame(stats_frame, style='Card.TFrame', padding="10")
            max_frame.grid(row=0, column=1, sticky='ew', padx=5)
            
            ttk.Label(max_frame, text="Max Temp", 
                     background=self.colors['card_bg'],
                     foreground=self.colors['text_secondary'],
                     font=("Segoe UI", 9)).pack(anchor=tk.CENTER)
            ttk.Label(max_frame, text=f"{max_temp:.1f}°C", 
                     background=self.colors['card_bg'],
                     foreground=self.colors['error'],
                     font=("Segoe UI", 14, "bold")).pack(anchor=tk.CENTER)
            
            # Min temperature
            min_frame = ttk.Frame(stats_frame, style='Card.TFrame', padding="10")
            min_frame.grid(row=0, column=2, sticky='ew', padx=(10, 0))
            
            ttk.Label(min_frame, text="Min Temp", 
                     background=self.colors['card_bg'],
                     foreground=self.colors['text_secondary'],
                     font=("Segoe UI", 9)).pack(anchor=tk.CENTER)
            ttk.Label(min_frame, text=f"{min_temp:.1f}°C", 
                     background=self.colors['card_bg'],
                     foreground=self.colors['success'],
                     font=("Segoe UI", 14, "bold")).pack(anchor=tk.CENTER)
        
        # Main content area - Graph
        content_frame = ttk.Frame(self.window, style='Modern.TFrame')
        content_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=(0, 20))
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Create matplotlib figure for graph
        self.setup_graph(content_frame)
        
        # Close button
        button_frame = ttk.Frame(self.window, style='Modern.TFrame')
        button_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=(0, 20))
        
        close_button = ttk.Button(button_frame, text="Close", 
                                 command=self.window.destroy,
                                 style='Primary.TButton')
        close_button.pack(side=tk.RIGHT)
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)
    
    def parse_temperature_data(self):
        """Parse temperature data from logs"""
        temperatures = []
        
        for log_entry in self.logs:
            if '°C' in log_entry:
                try:
                    # Extract temperature value
                    temp_part = log_entry.split('°C')[0]
                    if ':' in temp_part:
                        temp_str = temp_part.split(':')[-1].strip()
                        try:
                            temperature = float(temp_str)
                            temperatures.append(temperature)
                        except ValueError:
                            continue
                except Exception:
                    continue
        
        return temperatures
    
    def setup_graph(self, parent):
        """Setup the matplotlib graph for temperature visualization"""
        # Parse temperature data from logs
        timestamps = []
        temperatures = []
        
        for log_entry in self.logs:
            if '°C' in log_entry:
                try:
                    # Extract timestamp
                    timestamp_str = log_entry.split(']')[0][1:]
                    timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    
                    # Extract temperature value
                    temp_part = log_entry.split('°C')[0]
                    if ':' in temp_part:
                        temp_str = temp_part.split(':')[-1].strip()
                        try:
                            temperature = float(temp_str)
                            timestamps.append(timestamp)
                            temperatures.append(temperature)
                        except ValueError:
                            continue
                except Exception:
                    continue
        
        if not temperatures:
            # Show no data message
            no_data_frame = ttk.Frame(parent, style='Modern.TFrame')
            no_data_frame.grid(row=0, column=0, sticky='nsew')
            no_data_frame.columnconfigure(0, weight=1)
            no_data_frame.rowconfigure(0, weight=1)
            
            no_data_label = ttk.Label(no_data_frame, text="No temperature data found in the selected time range",
                                     background=self.colors['surface'],
                                     foreground=self.colors['text_secondary'],
                                     font=("Segoe UI", 14))
            no_data_label.grid(row=0, column=0, sticky='')
            return
        
        # Create figure and plot
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.fig.patch.set_facecolor(self.colors['card_bg'])
        self.ax.set_facecolor(self.colors['card_bg'])
        
        # Set colors based on theme
        if self.colors['background'] == '#0f172a':  # Dark theme
            text_color = 'white'
            grid_color = '#2d3748'
        else:  # Light theme
            text_color = 'black'
            grid_color = '#e2e8f0'
        
        # Create colored line segments based on temperature thresholds
        critical_temp = 30
        warning_temp = 27
        
        if len(timestamps) > 1:
            # Create segments for different temperature ranges
            segments = []
            current_segment = {'timestamps': [timestamps[0]], 'temps': [temperatures[0]], 'color': self.get_temperature_color(temperatures[0], critical_temp, warning_temp)}
            
            for i in range(1, len(timestamps)):
                current_color = self.get_temperature_color(temperatures[i], critical_temp, warning_temp)
                
                if current_color == current_segment['color']:
                    # Continue current segment
                    current_segment['timestamps'].append(timestamps[i])
                    current_segment['temps'].append(temperatures[i])
                else:
                    # End current segment and start new one
                    segments.append(current_segment)
                    current_segment = {'timestamps': [timestamps[i]], 'temps': [temperatures[i]], 'color': current_color}
            
            segments.append(current_segment)
            
            # Plot each segment with its respective color
            for segment in segments:
                if len(segment['timestamps']) > 1:
                    self.ax.plot(segment['timestamps'], segment['temps'], 
                                color=segment['color'], 
                                linewidth=3, 
                                marker='o', 
                                markersize=4,
                                alpha=0.8)
        
        # Customize graph
        self.ax.tick_params(colors=text_color)
        self.ax.xaxis.label.set_color(text_color)
        self.ax.yaxis.label.set_color(text_color)
        self.ax.title.set_color(text_color)
        
        self.ax.set_xlabel('Time', fontsize=12, fontweight='bold')
        self.ax.set_ylabel('Temperature (°C)', fontsize=12, fontweight='bold')
        
        # Add legend for temperature ranges
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], color='blue', lw=3, label='Normal Temperature (<27°C)'),
            Line2D([0], [0], color='yellow', lw=3, label='Warning (27-30°C)'),
            Line2D([0], [0], color='red', lw=3, label='Critical (>30°C)')
        ]
        self.ax.legend(handles=legend_elements, fontsize=11, framealpha=0.9)
        
        self.ax.grid(True, color=grid_color, alpha=0.3)
        
        # Rotate x-axis labels for better readability
        plt.setp(self.ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Add some statistics to the graph
        avg_temp = sum(temperatures) / len(temperatures)
        max_temp = max(temperatures)
        min_temp = min(temperatures)
        
        # Add horizontal line for average
        self.ax.axhline(y=avg_temp, color=self.colors['accent'], linestyle='--', 
                       alpha=0.7, label=f'Average: {avg_temp:.1f}°C')
        
        # Adjust layout
        self.fig.tight_layout()
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
    
    def get_temperature_color(self, temperature, critical_temp, warning_temp):
        """Get color based on temperature value"""
        if temperature >= critical_temp:
            return 'red'  # Critical
        elif temperature >= warning_temp:
            return 'yellow'  # Warning
        else:
            return 'blue'  # Normal

class TimeRangeSearchWindow:
    """Modal window for time range search and export with graph generation"""
    def __init__(self, parent, log_manager, theme_manager, responsive_design):
        self.parent = parent
        self.log_manager = log_manager
        self.theme_manager = theme_manager
        self.responsive_design = responsive_design
        self.colors = self.theme_manager.get_theme()
        self.window = None
        self.current_logs = []
        self.create_window()
        
    def create_window(self):
        """Create the time search and export modal window"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Search and Export Logs by Time Range")
        
        # Use responsive design for modal
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = min(1100, screen_width - 100)
        window_height = min(700, screen_height - 100)
        self.window.geometry(f"{window_width}x{window_height}")
        
        # Make window responsive
        self.window.minsize(900, 600)
        
        # Center the window on screen
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"+{x}+{y}")
        
        # Set proper background color
        if self.colors['background'] == '#0f172a':  # Dark mode
            bg_color = '#1e293b'
            text_bg = '#1e293b'
        else:  # Light mode
            bg_color = '#ffffff'
            text_bg = '#ffffff'
            
        self.window.configure(bg=bg_color)
        
        # Make the window modal
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Configure grid weights for responsiveness
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        
        # Header
        header_frame = ttk.Frame(self.window, style='Modern.TFrame')
        header_frame.grid(row=0, column=0, sticky='ew', padx=15, pady=15)
        header_frame.columnconfigure(1, weight=1)
        
        title_label = ttk.Label(header_frame, text="Search and Export Logs by Time Range", 
                               background=bg_color,
                               foreground=self.colors['text_primary'],
                               font=("Segoe UI", 16, "bold"))
        title_label.grid(row=0, column=0, sticky='w')
        
        # Search and Export controls frame
        controls_frame = ttk.Frame(self.window, style='Modern.TFrame')
        controls_frame.grid(row=1, column=0, sticky='ew', padx=15, pady=(0, 10))
        controls_frame.columnconfigure(1, weight=1)
        
        # Date and time range selection
        datetime_frame = ttk.Frame(controls_frame, style='Modern.TFrame')
        datetime_frame.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        datetime_frame.columnconfigure(1, weight=1)
        datetime_frame.columnconfigure(3, weight=1)
        
        # Start date and time
        start_frame = ttk.Frame(datetime_frame, style='Modern.TFrame')
        start_frame.grid(row=0, column=0, sticky='w', padx=(0, 20))
        
        ttk.Label(start_frame, text="Start Date & Time:", 
                 background=bg_color,
                 foreground=self.colors['text_secondary'],
                 font=('Segoe UI', 9, 'bold')).grid(row=0, column=0, sticky='w', columnspan=2)
        
        # Date entry
        ttk.Label(start_frame, text="Date (YYYY-MM-DD):", 
                 background=bg_color,
                 foreground=self.colors['text_secondary'],
                 font=('Segoe UI', 8)).grid(row=1, column=0, sticky='w', pady=(5, 2))
        
        self.start_date_var = tk.StringVar(value=datetime.datetime.now().strftime("%Y-%m-%d"))
        start_date_entry = ttk.Entry(start_frame, textvariable=self.start_date_var, width=12, font=('Segoe UI', 8))
        start_date_entry.grid(row=2, column=0, sticky='w', pady=(0, 5))
        
        # Time entry
        ttk.Label(start_frame, text="Time (HH:MM):", 
                 background=bg_color,
                 foreground=self.colors['text_secondary'],
                 font=('Segoe UI', 8)).grid(row=1, column=1, sticky='w', padx=(10, 0), pady=(5, 2))
        
        self.start_time_var = tk.StringVar(value="00:00")
        start_time_entry = ttk.Entry(start_frame, textvariable=self.start_time_var, width=8, font=('Segoe UI', 8))
        start_time_entry.grid(row=2, column=1, sticky='w', padx=(10, 0), pady=(0, 5))
        
        # End date and time
        end_frame = ttk.Frame(datetime_frame, style='Modern.TFrame')
        end_frame.grid(row=0, column=1, sticky='w', padx=(0, 20))
        
        ttk.Label(end_frame, text="End Date & Time:", 
                 background=bg_color,
                 foreground=self.colors['text_secondary'],
                 font=('Segoe UI', 9, 'bold')).grid(row=0, column=0, sticky='w', columnspan=2)
        
        # Date entry
        ttk.Label(end_frame, text="Date (YYYY-MM-DD):", 
                 background=bg_color,
                 foreground=self.colors['text_secondary'],
                 font=('Segoe UI', 8)).grid(row=1, column=0, sticky='w', pady=(5, 2))
        
        self.end_date_var = tk.StringVar(value=datetime.datetime.now().strftime("%Y-%m-%d"))
        end_date_entry = ttk.Entry(end_frame, textvariable=self.end_date_var, width=12, font=('Segoe UI', 8))
        end_date_entry.grid(row=2, column=0, sticky='w', pady=(0, 5))
        
        # Time entry
        ttk.Label(end_frame, text="Time (HH:MM):", 
                 background=bg_color,
                 foreground=self.colors['text_secondary'],
                 font=('Segoe UI', 8)).grid(row=1, column=1, sticky='w', padx=(10, 0), pady=(5, 2))
        
        self.end_time_var = tk.StringVar(value="23:59")
        end_time_entry = ttk.Entry(end_frame, textvariable=self.end_time_var, width=8, font=('Segoe UI', 8))
        end_time_entry.grid(row=2, column=1, sticky='w', padx=(10, 0), pady=(0, 5))
        
        # Quick time range buttons
        quick_buttons_frame = ttk.Frame(datetime_frame, style='Modern.TFrame')
        quick_buttons_frame.grid(row=0, column=2, sticky='w')
        
        ttk.Label(quick_buttons_frame, text="Quick Ranges:", 
                 background=bg_color,
                 foreground=self.colors['text_secondary'],
                 font=('Segoe UI', 9, 'bold')).grid(row=0, column=0, sticky='w', columnspan=2)
        
        # Quick range buttons
        button_frame = ttk.Frame(quick_buttons_frame, style='Modern.TFrame')
        button_frame.grid(row=1, column=0, sticky='w', pady=(5, 0))
        
        ttk.Button(button_frame, text="Last Hour", 
                  command=lambda: self.set_quick_range(1),
                  style='Secondary.TButton', width=10).grid(row=0, column=0, padx=(0, 5))
        
        ttk.Button(button_frame, text="Last 6 Hours", 
                  command=lambda: self.set_quick_range(6),
                  style='Secondary.TButton', width=10).grid(row=0, column=1, padx=(0, 5))
        
        ttk.Button(button_frame, text="Last 24 Hours", 
                  command=lambda: self.set_quick_range(24),
                  style='Secondary.TButton', width=10).grid(row=0, column=2, padx=(0, 5))
        
        ttk.Button(button_frame, text="Today", 
                  command=self.set_today_range,
                  style='Secondary.TButton', width=10).grid(row=1, column=0, padx=(0, 5), pady=(5, 0))
        
        ttk.Button(button_frame, text="Yesterday", 
                  command=self.set_yesterday_range,
                  style='Secondary.TButton', width=10).grid(row=1, column=1, padx=(0, 5), pady=(5, 0))
        
        ttk.Button(button_frame, text="Last 7 Days", 
                  command=lambda: self.set_quick_range(7*24),
                  style='Secondary.TButton', width=10).grid(row=1, column=2, padx=(0, 5), pady=(5, 0))
        
        # Buttons frame
        action_frame = ttk.Frame(controls_frame, style='Modern.TFrame')
        action_frame.grid(row=1, column=0, sticky='ew')
        action_frame.columnconfigure(0, weight=1)
        
        # Search button
        search_button = ttk.Button(action_frame, text="Search Logs", 
                                  command=self.search_logs,
                                  style='Primary.TButton')
        search_button.grid(row=0, column=0, sticky='w', padx=(0, 10))
        
        # Export button
        self.export_button = ttk.Button(action_frame, text="Export Results", 
                                       command=self.export_logs,
                                       style='Secondary.TButton',
                                       state="disabled")
        self.export_button.grid(row=0, column=1, sticky='w', padx=(0, 10))
        
        # Show History Graph button
        self.graph_button = ttk.Button(action_frame, text="Show History Graph", 
                                      command=self.show_history_graph,
                                      style='Secondary.TButton',
                                      state="disabled")
        self.graph_button.grid(row=0, column=2, sticky='w')
        
        # Results info frame
        info_frame = ttk.Frame(controls_frame, style='Modern.TFrame')
        info_frame.grid(row=2, column=0, sticky='ew', pady=(10, 0))
        
        self.results_var = tk.StringVar(value="Enter time range and click 'Search Logs'")
        results_label = ttk.Label(info_frame, textvariable=self.results_var,
                                background=bg_color,
                                foreground=self.colors['text_secondary'],
                                font=("Segoe UI", 9))
        results_label.pack(anchor='w')
        
        # Main content area - Logs
        content_frame = ttk.Frame(self.window, style='Modern.TFrame')
        content_frame.grid(row=2, column=0, sticky='nsew', padx=15, pady=(0, 15))
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Create scrollable text area for logs
        self.log_text = scrolledtext.ScrolledText(
            content_frame,
            wrap=tk.WORD,
            width=100,
            height=25,
            bg=text_bg,
            fg=self.colors['text_primary'],
            font=("Consolas", 9),
            insertbackground=self.colors['text_primary'],
            state='disabled'
        )
        self.log_text.grid(row=0, column=0, sticky='nsew')
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def set_quick_range(self, hours):
        """Set time range for last N hours"""
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(hours=hours)
        
        self.start_date_var.set(start_time.strftime("%Y-%m-%d"))
        self.start_time_var.set(start_time.strftime("%H:%M"))
        self.end_date_var.set(end_time.strftime("%Y-%m-%d"))
        self.end_time_var.set(end_time.strftime("%H:%M"))
    
    def set_today_range(self):
        """Set time range for today"""
        today = datetime.datetime.now()
        self.start_date_var.set(today.strftime("%Y-%m-%d"))
        self.start_time_var.set("00:00")
        self.end_date_var.set(today.strftime("%Y-%m-%d"))
        self.end_time_var.set("23:59")
    
    def set_yesterday_range(self):
        """Set time range for yesterday"""
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        self.start_date_var.set(yesterday.strftime("%Y-%m-%d"))
        self.start_time_var.set("00:00")
        self.end_date_var.set(yesterday.strftime("%Y-%m-%d"))
        self.end_time_var.set("23:59")
    
    def search_logs(self):
        """Search logs for the selected time range"""
        try:
            start_datetime_str = f"{self.start_date_var.get()} {self.start_time_var.get()}"
            end_datetime_str = f"{self.end_date_var.get()} {self.end_time_var.get()}"
            
            # Validate datetime
            try:
                start_datetime = datetime.datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M")
                end_datetime = datetime.datetime.strptime(end_datetime_str, "%Y-%m-%d %H:%M")
                
                if start_datetime > end_datetime:
                    messagebox.showerror("Error", "Start time cannot be after end time")
                    return
                    
            except ValueError:
                messagebox.showerror("Error", "Invalid datetime format. Please use YYYY-MM-DD for date and HH:MM for time")
                return
            
            # Get logs for the time range
            self.current_logs = self.log_manager.get_logs_for_time_range(start_datetime, end_datetime)
            
            # Clear and update log display
            self.log_text.config(state='normal')
            self.log_text.delete(1.0, tk.END)
            
            if self.current_logs:
                for log_entry in self.current_logs:
                    self.log_text.insert(tk.END, log_entry + "\n")
                
                # Scroll to top
                self.log_text.see(1.0)
                
                # Update results info
                log_count = len(self.current_logs)
                self.results_var.set(f"Found {log_count} log entries from {start_datetime_str} to {end_datetime_str}")
                
                # Enable export and graph buttons
                self.export_button.config(state="normal")
                self.graph_button.config(state="normal")
                
            else:
                self.log_text.insert(tk.END, "No logs found for the specified time range.\n")
                self.results_var.set("No logs found for the specified time range")
                self.export_button.config(state="disabled")
                self.graph_button.config(state="disabled")
            
            # Set back to read-only after updating content
            self.log_text.config(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Search Error", f"Failed to search logs: {str(e)}")
    
    def show_history_graph(self):
        """Show the history graph in a modal window"""
        if not self.current_logs:
            messagebox.showinfo("No Data", "No logs to generate graph. Please search for logs first.")
            return
        
        try:
            start_datetime_str = f"{self.start_date_var.get()} {self.start_time_var.get()}"
            end_datetime_str = f"{self.end_date_var.get()} {self.end_time_var.get()}"
            
            # Validate datetime
            try:
                start_datetime = datetime.datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M")
                end_datetime = datetime.datetime.strptime(end_datetime_str, "%Y-%m-%d %H:%M")
            except ValueError:
                messagebox.showerror("Error", "Invalid datetime format in fields")
                return
            
            # Create and show the search result modal
            SearchResultModal(self.window, start_datetime, end_datetime, self.current_logs, self.theme_manager, self.responsive_design)
            
        except Exception as e:
            messagebox.showerror("Graph Error", f"Failed to generate graph: {str(e)}")
    
    def export_logs(self):
        """Export the currently displayed logs to file"""
        if not self.current_logs:
            messagebox.showinfo("No Data", "No logs to export. Please search for logs first.")
            return
        
        try:
            start_datetime_str = f"{self.start_date_var.get()} {self.start_time_var.get()}"
            end_datetime_str = f"{self.end_date_var.get()} {self.end_time_var.get()}"
            
            # Validate datetime
            try:
                start_datetime = datetime.datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M")
                end_datetime = datetime.datetime.strptime(end_datetime_str, "%Y-%m-%d %H:%M")
            except ValueError:
                messagebox.showerror("Error", "Invalid datetime format in fields")
                return
            
            # Export logs using LogManager
            success = self.log_manager.export_logs_to_file_with_time_range(start_datetime, end_datetime)
            
            if success:
                messagebox.showinfo("Export Successful", 
                                  "Logs exported successfully to Downloads folder!")
            else:
                messagebox.showinfo("Export Failed", "Failed to export logs")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export logs: {str(e)}")
    
    def on_close(self):
        """Handle window close"""
        self.window.destroy()

class LiveLogWindow:
    """Live Log window for displaying real-time temperature logs"""
    def __init__(self, parent, log_manager, theme_manager, responsive_design):
        self.parent = parent
        self.log_manager = log_manager
        self.theme_manager = theme_manager
        self.responsive_design = responsive_design
        self.colors = self.theme_manager.get_theme()
        self.window = None
        self.is_running = True
        self.create_window()
        
    def create_window(self):
        """Create the Live Log window"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Live Temperature Log")
        
        # Use responsive design for modal
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = min(1000, screen_width - 100)
        window_height = min(700, screen_height - 100)
        self.window.geometry(f"{window_width}x{window_height}")
        
        # Make window responsive with minimum size
        self.window.minsize(800, 600)
        
        # Center the window on screen
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"+{x}+{y}")
        
        # Set proper background color
        if self.colors['background'] == '#0f172a':  # Dark mode
            bg_color = '#1e293b'
            text_bg = '#1e293b'
        else:  # Light mode
            bg_color = '#ffffff'
            text_bg = '#ffffff'
            
        self.window.configure(bg=bg_color)
        
        # Configure grid for responsiveness
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        
        # Make the window modal
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Header
        header_frame = ttk.Frame(self.window, style='Modern.TFrame')
        header_frame.grid(row=0, column=0, sticky='ew', padx=15, pady=15)
        header_frame.columnconfigure(0, weight=1)
        
        title_label = ttk.Label(header_frame, text="Live Temperature Log", 
                               background=bg_color,
                               foreground=self.colors['text_primary'],
                               font=("Segoe UI", 16, "bold"))
        title_label.grid(row=0, column=0, sticky='w')
        
        # Buttons frame
        button_frame = ttk.Frame(header_frame, style='Modern.TFrame')
        button_frame.grid(row=0, column=1, sticky='e')
        
        # Updated button text to reflect time range functionality
        search_export_button = ttk.Button(button_frame, text="Search & Export by Time Range", 
                                         command=self.show_time_search_modal,
                                         style='Secondary.TButton')
        search_export_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Status info
        self.status_var = tk.StringVar(value="Showing: Live Logs")
        status_label = ttk.Label(header_frame, textvariable=self.status_var,
                                background=bg_color,
                                foreground=self.colors['text_secondary'],
                                font=("Segoe UI", 9))
        status_label.grid(row=1, column=0, sticky='w', pady=(5, 0))
        
        # Log display area
        log_frame = ttk.Frame(self.window, style='Modern.TFrame')
        log_frame.grid(row=1, column=0, sticky='nsew', padx=15, pady=(0, 15))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Create scrollable text area for logs
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            width=120,
            height=30,
            bg=text_bg,
            fg=self.colors['text_primary'],
            font=("Consolas", 9),
            insertbackground=self.colors['text_primary'],
            state='disabled'
        )
        self.log_text.grid(row=0, column=0, sticky='nsew')
        
        # Load existing logs
        self.refresh_log_display()
        
        # Start live updates
        self.update_live_log()
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def show_time_search_modal(self):
        """Show the time range search and export modal window"""
        TimeRangeSearchWindow(self.window, self.log_manager, self.theme_manager, self.responsive_design)
    
    def refresh_log_display(self):
        """Refresh the log display with current logs"""
        logs = self.log_manager.get_all_logs()
        
        # Enable text widget for update
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        
        if logs:
            for log_entry in logs[-1000:]:  # Show last 1000 entries to prevent UI lag
                self.log_text.insert(tk.END, log_entry + "\n")
            
            # Scroll to bottom
            self.log_text.see(tk.END)
        else:
            self.log_text.insert(tk.END, "No logs available yet...\n")
        
        # Set back to read-only after updating content
        self.log_text.config(state='disabled')
    
    def update_live_log(self):
        """Update the log display with new entries"""
        if self.is_running and self.window.winfo_exists():
            # Get only new logs since last update
            new_logs = self.log_manager.get_new_logs()
            
            if new_logs:
                # Enable text widget for update
                self.log_text.config(state='normal')
                
                for log_entry in new_logs:
                    self.log_text.insert(tk.END, log_entry + "\n")
                
                # Auto-scroll to bottom
                self.log_text.see(tk.END)
                
                # Set back to read-only after updating content
                self.log_text.config(state='disabled')
            
            # Schedule next update
            self.window.after(1000, self.update_live_log)
    
    def on_close(self):
        """Handle window close"""
        self.is_running = False
        self.window.destroy()

class LogManager:
    """Manages persistent logging of temperature data with .logs files"""
    def __init__(self):
        # Condition 1: Daily logs in "Daily logs" folder
        self.daily_logs_dir = "Daily logs"
        self.current_log_file = None
        self.log_buffer = []
        self.last_log_index = 0
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging infrastructure with Daily logs folder"""
        # Create Daily logs directory if it doesn't exist
        if not os.path.exists(self.daily_logs_dir):
            os.makedirs(self.daily_logs_dir)
            print(f"✅ Created Daily logs directory: {self.daily_logs_dir}")
        
        # Create or get current log file
        self.current_log_file = self.get_current_log_file()
        print(f"✅ Logging to: {self.current_log_file}")
    
    def get_current_log_file(self):
        """Get the current log file path based on current date"""
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        return os.path.join(self.daily_logs_dir, f"temperature_logs_{current_date}.logs")
    
    def log_temperature(self, temp_type, value, message=""):
        """Log temperature data with timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create log entry
        if message:
            log_entry = f"[{timestamp}] {message}"
        else:
            log_entry = f"[{timestamp}] {temp_type}: {value}°C"
        
        # Add to buffer for live display
        self.log_buffer.append(log_entry)
        
        # Persist to file (non-blocking)
        threading.Thread(target=self._write_to_file, 
                        args=(log_entry,),
                        daemon=True).start()
        
        print(log_entry)  # Also print to console
    
    def _write_to_file(self, log_entry):
        """Write log entry to file in a separate thread"""
        try:
            # Check if we need to rotate to a new daily file
            current_file = self.get_current_log_file()
            if current_file != self.current_log_file:
                self.current_log_file = current_file
            
            # Use UTF-8 encoding with error handling
            with open(self.current_log_file, 'a', encoding='utf-8', errors='replace') as f:
                f.write(log_entry + "\n")
        except Exception as e:
            print(f"Error writing to log file: {e}")
    
    def get_all_logs(self):
        """Get all logs from all .logs files"""
        all_logs = []
        
        try:
            # Check if Daily logs directory exists
            if not os.path.exists(self.daily_logs_dir):
                print(f"⚠️ Daily logs directory '{self.daily_logs_dir}' not found")
                return all_logs
            
            # Get all temperature_logs_*.logs files in the Daily logs directory
            log_files = []
            try:
                log_files = [f for f in os.listdir(self.daily_logs_dir) 
                           if f.startswith('temperature_logs_') and f.endswith('.logs')]
            except FileNotFoundError:
                print(f"❌ Directory '{self.daily_logs_dir}' not found")
                return all_logs
            except PermissionError:
                print(f"❌ Permission denied accessing '{self.daily_logs_dir}'")
                return all_logs
            
            if not log_files:
                print("ℹ️ No log files found in Daily logs directory")
                return all_logs
                
            log_files.sort()  # Sort by filename (which includes date)
            
            # Read all log files with multiple encoding attempts
            for log_file in log_files:
                log_path = os.path.join(self.daily_logs_dir, log_file)
                file_logs = self._read_log_file_with_encoding(log_path)
                if file_logs:
                    all_logs.extend(file_logs)
                    print(f"📖 Read {len(file_logs)} entries from {log_file}")
            
            print(f"📊 Total logs loaded: {len(all_logs)} entries")
            
        except Exception as e:
            print(f"❌ Error reading Daily logs directory: {e}")
        
        return all_logs
    
    def _read_log_file_with_encoding(self, file_path):
        """Read log file trying multiple encodings to handle encoding issues"""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'utf-16']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                    logs = f.readlines()
                    # Filter out empty lines and clean the logs
                    cleaned_logs = [log.strip() for log in logs if log.strip()]
                    return cleaned_logs
            except UnicodeDecodeError:
                print(f"⚠️ Encoding {encoding} failed for {os.path.basename(file_path)}, trying next...")
                continue
            except Exception as e:
                print(f"⚠️ Error reading {os.path.basename(file_path)} with {encoding}: {e}")
                continue
        
        print(f"❌ All encoding attempts failed for {os.path.basename(file_path)}")
        return []
    
    def get_new_logs(self):
        """Get new logs since last check"""
        current_logs = self.get_all_logs()
        new_logs = current_logs[self.last_log_index:]
        self.last_log_index = len(current_logs)
        return new_logs
    
    def get_logs_for_date_range(self, start_date, end_date):
        """Get logs for a specific date range"""
        logs = []
        
        try:
            # Check if directory exists
            if not os.path.exists(self.daily_logs_dir):
                print(f"❌ Daily logs directory '{self.daily_logs_dir}' not found")
                return logs
            
            # Generate all dates in the range
            current_date = start_date
            while current_date <= end_date:
                log_file = os.path.join(self.daily_logs_dir, f"temperature_logs_{current_date.strftime('%Y-%m-%d')}.logs")
                
                if os.path.exists(log_file):
                    file_logs = self._read_log_file_with_encoding(log_file)
                    if file_logs:
                        logs.extend(file_logs)
                        print(f"📖 Read {len(file_logs)} entries from {os.path.basename(log_file)}")
                    else:
                        print(f"⚠️ No readable content in: {os.path.basename(log_file)}")
                else:
                    print(f"ℹ️ No log file for date: {current_date}")
                
                current_date += datetime.timedelta(days=1)
                
            print(f"📊 Found {len(logs)} total log entries for date range {start_date} to {end_date}")
                
        except Exception as e:
            print(f"❌ Error reading logs for date range: {e}")
        
        return logs

    def get_logs_for_time_range(self, start_datetime, end_datetime):
        """Get logs for a specific time range"""
        logs = []
        
        try:
            # Check if directory exists
            if not os.path.exists(self.daily_logs_dir):
                print(f"❌ Daily logs directory '{self.daily_logs_dir}' not found")
                return logs
            
            # Generate all dates in the range
            current_date = start_datetime.date()
            end_date = end_datetime.date()
            
            while current_date <= end_date:
                log_file = os.path.join(self.daily_logs_dir, f"temperature_logs_{current_date.strftime('%Y-%m-%d')}.logs")
                
                if os.path.exists(log_file):
                    file_logs = self._read_log_file_with_encoding(log_file)
                    if file_logs:
                        # Filter logs by time range
                        for log_entry in file_logs:
                            try:
                                # Extract timestamp from log entry
                                timestamp_str = log_entry.split(']')[0][1:]
                                log_datetime = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                                
                                # Check if log datetime is within the specified range
                                if start_datetime <= log_datetime <= end_datetime:
                                    logs.append(log_entry)
                            except ValueError:
                                # Skip entries with invalid timestamps
                                continue
                        
                        print(f"📖 Filtered entries from {os.path.basename(log_file)}")
                    else:
                        print(f"⚠️ No readable content in: {os.path.basename(log_file)}")
                else:
                    print(f"ℹ️ No log file for date: {current_date}")
                
                current_date += datetime.timedelta(days=1)
                
            print(f"📊 Found {len(logs)} total log entries for time range {start_datetime} to {end_datetime}")
                
        except Exception as e:
            print(f"❌ Error reading logs for time range: {e}")
        
        return logs
    
    def export_logs_to_file(self, start_date, end_date):
        """Export logs to .logs file in Downloads folder only"""
        logs = self.get_logs_for_date_range(start_date, end_date)
        
        if not logs:
            print("❌ No logs to export")
            messagebox.showinfo("No Data", "No logs found to export for the specified date range.")
            return False
        
        try:
            # Create filename with date range for EXPORT file
            start_str = start_date.strftime("%Y-%m-%d")
            end_str = end_date.strftime("%Y-%m-%d")
            
            if start_str == end_str:
                export_filename = f"temperature_export_{start_str}.logs"
            else:
                export_filename = f"temperature_export_{start_str}_to_{end_str}.logs"
            
            # Export only to Downloads folder
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads", export_filename)
            
            # Use UTF-8 encoding for export
            with open(downloads_path, 'w', encoding='utf-8') as f:
                f.write("# Temperature Logs Export\n")
                f.write(f"# Date Range: {start_str} to {end_str}\n")
                f.write(f"# Exported on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("# Format: [TIMESTAMP] LOG_ENTRY\n")
                f.write("# Source: Storage Temperature Monitor\n")
                f.write("=" * 60 + "\n")
                for log_entry in logs:
                    f.write(log_entry + "\n")
            
            print(f"✅ Daily logs stored in: {self.daily_logs_dir}/")
            print(f"✅ Export file created: {downloads_path}")
            print(f"✅ Exported {len(logs)} log entries")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting logs: {e}")
            messagebox.showerror("Export Error", f"Failed to export logs: {str(e)}")
            return False

    def export_logs_to_file_with_time_range(self, start_datetime, end_datetime):
        """Export logs with time range to .logs file in Downloads folder"""
        logs = self.get_logs_for_time_range(start_datetime, end_datetime)
        
        if not logs:
            print("❌ No logs to export")
            messagebox.showinfo("No Data", "No logs found to export for the specified time range.")
            return False
        
        try:
            # Create filename with time range for EXPORT file
            start_str = start_datetime.strftime("%Y-%m-%d_%H-%M")
            end_str = end_datetime.strftime("%Y-%m-%d_%H-%M")
            
            export_filename = f"temperature_export_{start_str}_to_{end_str}.logs"
            
            # Export only to Downloads folder
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads", export_filename)
            
            # Use UTF-8 encoding for export
            with open(downloads_path, 'w', encoding='utf-8') as f:
                f.write("# Temperature Logs Export\n")
                f.write(f"# Time Range: {start_datetime.strftime('%Y-%m-%d %H:%M')} to {end_datetime.strftime('%Y-%m-%d %H:%M')}\n")
                f.write(f"# Exported on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("# Format: [TIMESTAMP] LOG_ENTRY\n")
                f.write("# Source: Storage Temperature Monitor\n")
                f.write("=" * 60 + "\n")
                for log_entry in logs:
                    f.write(log_entry + "\n")
            
            print(f"✅ Daily logs stored in: {self.daily_logs_dir}/")
            print(f"✅ Export file created: {downloads_path}")
            print(f"✅ Exported {len(logs)} log entries")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting logs: {e}")
            messagebox.showerror("Export Error", f"Failed to export logs: {str(e)}")
            return False

class TemperatureMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Storage Temperature Monitor")
        
        # Initialize responsive design with fullscreen using geometry and zoomed state
        self.responsive_design = ResponsiveDesign(root)
        self.scaling_factors = self.responsive_design.get_scaling_factors()
        
        # Initialize theme manager
        self.theme_manager = ThemeManager()
        self.colors = self.theme_manager.get_theme()
        
        # Monitoring state
        self.is_monitoring = True
        self.alert_monitoring_active = True
        self.monitor_thread = None
        self.email_thread = None
        
        # Alert tracking
        self.last_warning_time = 0
        self.warning_cooldown = 30
        self.last_email_time = 0
        self.email_interval = 3600  
        
        # Temperature thresholds 
        self.critical_temp = 30  
        self.warning_temp = 27   
        
        # Temperature history for graphing
        self.temp_history = deque(maxlen=50)
        self.time_history = deque(maxlen=50)
        
        # For email statistics
        self.min_temp = float('inf')
        self.max_temp = float('-inf')
        
        # Storage temperatures storage
        self.storage_temperatures = {}
        
        # Storage temperature reader
        self.temp_reader = StorageTemperatureReader()
        
        # Email configuration
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'sender_email': 'iantolentino0110@gmail.com',  # Your email
            'sender_password': 'kwor ngta azao fukw',  # You need to set this
            'receiver_email': 'supercompnxp@gmail.com, ian.tolentino.bp@j-display.com, ferrerasroyce@gmail.com'
        }
        
        # Initialize log manager for persistent logging
        self.log_manager = LogManager()
        
        # Create background and setup UI
        self.setup_background()
        self.setup_modern_styles()
        self.load_settings()
        self.setup_ui()
        self.start_realtime_updates()
        self.start_email_scheduler()
        
        # Start automatic logging when program runs
        self.log_manager.log_temperature("System", "N/A", "Storage Temperature Monitor started - logging initialized")
        
    def setup_background(self):
        """Setup the responsive gradient background"""
        # Create a canvas that covers the entire window
        self.bg_canvas = tk.Canvas(
            self.root,
            highlightthickness=0,
            bg=self.colors['background']
        )
        self.bg_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Update the canvas size after window is created
        self.root.update()
        
        # Create responsive gradient background
        self.responsive_bg = ResponsiveGradientBackground(
            self.bg_canvas, 
            self.root.winfo_width(), 
            self.root.winfo_height(),
            self.colors
        )
        
        # Bind to window resize events
        self.root.bind('<Configure>', self.on_resize)
    
    def on_resize(self, event):
        """Handle window resize events - responsive design"""
        if event.widget == self.root:
            # Update background size
            self.responsive_bg.width = event.width
            self.responsive_bg.height = event.height
            self.responsive_bg.create_responsive_background()
            
            # Update scaling factors when window is resized
            self.scaling_factors = self.responsive_design.get_scaling_factors()
    
    def setup_modern_styles(self):
        """Configure modern professional styling with theme support"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure modern styles with current theme
        style.configure('Modern.TFrame', 
                       background=self.colors['surface'])
        
        style.configure('Card.TFrame', 
                       background=self.colors['card_bg'],
                       relief='flat', 
                       borderwidth=0)
        
        style.configure('Card.TLabelframe', 
                       background=self.colors['card_bg'],
                       relief='flat',
                       borderwidth=1,
                       bordercolor=self.colors['border'])
        
        style.configure('Card.TLabelframe.Label',
                       background=self.colors['card_bg'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 10, 'bold'))
        
        # Modern button styles with responsive scaling
        base_font_size = int(9 * self.scaling_factors['font_scale'])
        base_padding = int(6 * self.scaling_factors['padding_scale'])
        
        style.configure('Primary.TButton',
                       background=self.colors['primary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', base_font_size, 'bold'),
                       padding=(12, base_padding))
        
        style.configure('Secondary.TButton',
                       background=self.colors['surface'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       bordercolor=self.colors['border'],
                       focuscolor='none',
                       font=('Segoe UI', base_font_size),
                       padding=(10, base_padding-1))
        
        style.configure('Theme.TButton',
                       background=self.colors['secondary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', base_font_size-1, 'bold'),
                       padding=(8, base_padding-2))
        
        style.map('Primary.TButton',
                 background=[('active', self.colors['secondary']),
                           ('pressed', self.colors['secondary'])])
        
        style.map('Secondary.TButton',
                 background=[('active', self.colors['hover']),
                           ('pressed', self.colors['hover'])])
        
        style.map('Theme.TButton',
                 background=[('active', self.colors['accent']),
                           ('pressed', self.colors['accent'])])
        
        # Configure entry styles
        style.configure('Modern.TEntry',
                       fieldbackground=self.colors['input_bg'],
                       foreground=self.colors['input_fg'],
                       borderwidth=1,
                       focusthickness=2,
                       focuscolor=self.colors['primary'])
        
        # Redesigned combobox for better visibility
        style.configure('Modern.TCombobox',
                       fieldbackground=self.colors['input_bg'],
                       foreground=self.colors['input_fg'],
                       background=self.colors['input_bg'],
                       borderwidth=1,
                       focusthickness=2,
                       focuscolor=self.colors['primary'],
                       selectbackground=self.colors['primary'],
                       selectforeground=self.colors['text_primary'],
                       arrowcolor=self.colors['text_primary'])
        
        style.map('Modern.TCombobox',
                 fieldbackground=[('readonly', self.colors['input_bg']),
                                ('active', self.colors['input_bg'])],
                 background=[('readonly', self.colors['input_bg']),
                           ('active', self.colors['input_bg'])],
                 foreground=[('readonly', self.colors['input_fg']),
                           ('active', self.colors['input_fg'])],
                 selectbackground=[('readonly', self.colors['primary']),
                                 ('active', self.colors['primary'])],
                 selectforeground=[('readonly', self.colors['text_primary']),
                                 ('active', self.colors['text_primary'])])
    
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        self.colors = self.theme_manager.toggle_theme()
        self.update_theme()
    
    def update_theme(self):
        """Update the entire UI with new theme colors"""
        # Update background
        self.responsive_bg.update_theme(self.colors)
        
        # Update matplotlib graph theme
        self.update_graph_theme()
        
        # Recreate the UI with new theme
        self.setup_modern_styles()
        self.setup_ui()
    
    def update_graph_theme(self):
        """Update matplotlib graph with current theme"""
        plt.rcParams['axes.facecolor'] = self.colors['card_bg']
        plt.rcParams['figure.facecolor'] = self.colors['card_bg']
        plt.rcParams['axes.edgecolor'] = self.colors['border']
        plt.rcParams['axes.labelcolor'] = self.colors['text_primary']
        plt.rcParams['text.color'] = self.colors['text_primary']
        plt.rcParams['xtick.color'] = self.colors['text_secondary']
        plt.rcParams['ytick.color'] = self.colors['text_secondary']
        plt.rcParams['font.size'] = 9
        plt.rcParams['axes.titlesize'] = 12
        plt.rcParams['axes.labelsize'] = 10
        
        # Redraw graph if it exists
        if hasattr(self, 'canvas'):
            self.update_graph()
    
    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists('temperature_monitor_settings.json'):
                with open('temperature_monitor_settings.json', 'r') as f:
                    settings = json.load(f)
                    self.critical_temp = settings.get('critical_temp', 30)
                    self.warning_temp = settings.get('warning_temp', 27)
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_settings(self):
        """Save settings to file"""
        try:
            settings = {
                'critical_temp': self.critical_temp,
                'warning_temp': self.warning_temp
            }
            with open('temperature_monitor_settings.json', 'w') as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")
        
    def setup_ui(self):
        # Clear existing UI
        for widget in self.bg_canvas.winfo_children():
            if isinstance(widget, ttk.Frame):
                widget.destroy()
        
        # Calculate responsive padding
        base_padding = int(20 * self.scaling_factors['padding_scale'])
        
        # Create main frame on top of background canvas
        main_frame = ttk.Frame(self.bg_canvas, style='Modern.TFrame', padding=f"{base_padding}")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights for responsiveness - critical for proper scaling
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header section - Centered and professional
        header_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        header_frame.grid(row=0, column=0, sticky='ew', pady=(0, base_padding))
        header_frame.columnconfigure(0, weight=1)
        
        # Title with centered layout
        title_frame = ttk.Frame(header_frame, style='Modern.TFrame')
        title_frame.grid(row=0, column=0, sticky='ew')
        title_frame.columnconfigure(0, weight=1)
        
        # Calculate responsive font sizes
        title_font_size = int(20 * self.scaling_factors['font_scale'])
        
        # Left side - Title
        title_label = ttk.Label(title_frame, text="Storage Temperature Monitor", 
                               background=self.colors['surface'],
                               foreground=self.colors['text_primary'],
                               font=("Segoe UI", title_font_size, "bold"))
        title_label.grid(row=0, column=0, sticky='w')
        
        # Right side - Theme toggle and Live Log button
        header_buttons_frame = ttk.Frame(title_frame, style='Modern.TFrame')
        header_buttons_frame.grid(row=0, column=1, sticky='e')
        
        live_log_button = ttk.Button(header_buttons_frame, text="Live Log", 
                                command=self.show_live_log,
                                style='Primary.TButton')
        live_log_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        theme_button = ttk.Button(header_buttons_frame, text="Theme", 
                             command=self.toggle_theme,
                             style='Secondary.TButton')
        theme_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Main content area - Two column layout with proper weights
        content_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        content_frame.grid(row=1, column=0, sticky='nsew')
        # Left column gets more weight (70%), right column less (30%)
        content_frame.columnconfigure(0, weight=7)  # Left column (70%)
        content_frame.columnconfigure(1, weight=3)  # Right column (30%)
        content_frame.rowconfigure(0, weight=1)
        
        # Left column - Metrics and Graph (70% width)
        left_column = ttk.Frame(content_frame, style='Modern.TFrame')
        left_column.grid(row=0, column=0, sticky='nsew', padx=(0, base_padding//2))
        left_column.columnconfigure(0, weight=1)
        left_column.rowconfigure(1, weight=1)  # Graph gets most space
        
        # Metrics cards in a compact row
        metrics_frame = ttk.Frame(left_column, style='Modern.TFrame')
        metrics_frame.grid(row=0, column=0, sticky='ew', pady=(0, base_padding))
        # Equal weight for all three metric cards
        metrics_frame.columnconfigure(0, weight=1)
        metrics_frame.columnconfigure(1, weight=1)
        metrics_frame.columnconfigure(2, weight=1)
        
        # Calculate card padding
        card_padding = int(20 * self.scaling_factors['padding_scale'])
        
        # Average temperature card
        avg_card = ttk.Frame(metrics_frame, style='Card.TFrame', padding=f"{card_padding}")
        avg_card.grid(row=0, column=0, sticky='nsew', padx=(0, base_padding//2))
        
        ttk.Label(avg_card, text="Average Temperature", 
                 background=self.colors['card_bg'],
                 foreground=self.colors['text_secondary'],
                 font=("Segoe UI", 10, "bold")).pack(anchor=tk.CENTER)
        
        self.avg_temp_var = tk.StringVar(value="--°C")
        temp_font_size = int(24 * self.scaling_factors['font_scale'])
        self.avg_temp_display = ttk.Label(avg_card, textvariable=self.avg_temp_var, 
                                         background=self.colors['card_bg'],
                                         foreground=self.colors['primary'],
                                         font=("Segoe UI", temp_font_size, "bold"))
        self.avg_temp_display.pack(anchor=tk.CENTER, pady=(8, 0))
        
        # Max temperature card
        max_card = ttk.Frame(metrics_frame, style='Card.TFrame', padding=f"{card_padding}")
        max_card.grid(row=0, column=1, sticky='nsew', padx=(base_padding//2, base_padding//2))
        
        ttk.Label(max_card, text="Max Temperature", 
                 background=self.colors['card_bg'],
                 foreground=self.colors['text_secondary'],
                 font=("Segoe UI", 10, "bold")).pack(anchor=tk.CENTER)
        
        self.max_temp_var = tk.StringVar(value="--°C")
        self.max_temp_display = ttk.Label(max_card, textvariable=self.max_temp_var, 
                                     background=self.colors['card_bg'],
                                     foreground=self.colors['primary'],
                                     font=("Segoe UI", temp_font_size, "bold"))
        self.max_temp_display.pack(anchor=tk.CENTER, pady=(8, 0))
        
        # Sensor status card
        sensor_card = ttk.Frame(metrics_frame, style='Card.TFrame', padding=f"{card_padding}")
        sensor_card.grid(row=0, column=2, sticky='nsew', padx=(base_padding//2, 0))
        
        ttk.Label(sensor_card, text="Sensor Status", 
                 background=self.colors['card_bg'],
                 foreground=self.colors['text_secondary'],
                 font=("Segoe UI", 10, "bold")).pack(anchor=tk.CENTER)
        
        # Sensor connection status
        self.sensor_status_var = tk.StringVar()
        status_font_size = int(12 * self.scaling_factors['font_scale'])
        sensor_status_label = ttk.Label(sensor_card, textvariable=self.sensor_status_var,
                                  background=self.colors['card_bg'],
                                  foreground=self.colors['text_primary'],
                                  font=("Segoe UI", status_font_size, "bold"))
        sensor_status_label.pack(anchor=tk.CENTER, pady=(8, 0))
        
        # System status
        self.status_var = tk.StringVar(value="Initializing...")
        small_font_size = int(9 * self.scaling_factors['font_scale'])
        status_label = ttk.Label(sensor_card, textvariable=self.status_var,
                            background=self.colors['card_bg'],
                            foreground=self.colors['text_secondary'],
                            font=("Segoe UI", small_font_size))
        status_label.pack(anchor=tk.CENTER, pady=(4, 0))
        
        self.update_sensor_status()
        
        # Graph frame - takes most space in left column
        graph_frame = ttk.Frame(left_column, style='Card.TFrame', padding="15")
        graph_frame.grid(row=1, column=0, sticky='nsew')
        graph_frame.columnconfigure(0, weight=1)
        graph_frame.rowconfigure(0, weight=1)
        
        # Create professional matplotlib figure with current theme
        self.update_graph_theme()
        
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.fig.tight_layout(pad=4.0)
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        
        # Right column - Controls and Settings (30% width)
        right_column = ttk.Frame(content_frame, style='Modern.TFrame')
        right_column.grid(row=0, column=1, sticky='nsew', padx=(base_padding//2, 0))
        right_column.columnconfigure(0, weight=1)
        
        # Alert Controls Section
        alert_frame = ttk.LabelFrame(right_column, text="ALERT CONTROLS", 
                                style='Card.TLabelframe', padding="15")
        alert_frame.grid(row=0, column=0, sticky='ew', pady=(0, base_padding))
        
        # Alert status display
        alert_status_frame = ttk.Frame(alert_frame, style='Card.TFrame')
        alert_status_frame.grid(row=0, column=0, sticky='ew', pady=(0, 12))
        
        ttk.Label(alert_status_frame, text="Current Status:", 
                 background=self.colors['card_bg'],
                 foreground=self.colors['text_primary'],
                 font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky='w')
        
        self.alert_status_var = tk.StringVar(value="Alerts: ACTIVE")
        alert_status_label = ttk.Label(alert_status_frame, textvariable=self.alert_status_var,
                                 background=self.colors['card_bg'],
                                 foreground=self.colors['success'],
                                 font=('Segoe UI', 11, 'bold'))
        alert_status_label.grid(row=1, column=0, sticky='w', pady=(5, 0))
        
        # Alert control buttons in a row
        alert_buttons_frame = ttk.Frame(alert_frame, style='Card.TFrame')
        alert_buttons_frame.grid(row=1, column=0, sticky='ew')
        alert_buttons_frame.columnconfigure(0, weight=1)
        alert_buttons_frame.columnconfigure(1, weight=1)
        
        self.start_button = ttk.Button(alert_buttons_frame, text="Enable Alerts", 
                                  command=self.start_alert_monitoring, 
                                  style='Primary.TButton')
        self.start_button.grid(row=0, column=0, sticky='ew', padx=(0, 5))
        
        self.stop_button = ttk.Button(alert_buttons_frame, text="Disable Alerts", 
                                 command=self.stop_alert_monitoring, 
                                 state="disabled", 
                                 style='Secondary.TButton')
        self.stop_button.grid(row=0, column=1, sticky='ew', padx=(5, 0))
        
        # Monitoring Controls Section - Improved spacing and sizing
        monitor_frame = ttk.LabelFrame(right_column, text="MONITORING CONTROLS", 
                                  style='Card.TLabelframe', padding="15")
        monitor_frame.grid(row=1, column=0, sticky='ew', pady=(0, base_padding))
        
        # Refresh rate control - Improved layout
        refresh_frame = ttk.Frame(monitor_frame, style='Card.TFrame')
        refresh_frame.grid(row=0, column=0, sticky='ew', pady=(0, 15))
        
        ttk.Label(refresh_frame, text="Update Interval (seconds):", 
                 background=self.colors['card_bg'],
                 foreground=self.colors['text_primary'],
                 font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=(0, 8))
        
        self.refresh_rate_var = tk.StringVar(value="2")
        refresh_combo = ttk.Combobox(refresh_frame, textvariable=self.refresh_rate_var,
                                values=["1", "2", "5", "10"], 
                                width=12,
                                state="readonly",
                                style='Modern.TCombobox',
                                height=4)
        refresh_combo.grid(row=1, column=0, sticky='ew', pady=(0, 10))
        
        refresh_button = ttk.Button(refresh_frame, text="Refresh Now", 
                              command=self.manual_refresh, 
                              style='Primary.TButton')
        refresh_button.grid(row=2, column=0, sticky='ew')
        
        # Utility buttons grid - Improved spacing
        utils_frame = ttk.Frame(monitor_frame, style='Card.TFrame')
        utils_frame.grid(row=1, column=0, sticky='ew', pady=(15, 0))
        
        # First row of utility buttons
        utils_row1 = ttk.Frame(utils_frame, style='Card.TFrame')
        utils_row1.grid(row=0, column=0, sticky='ew', pady=(0, 8))
        utils_row1.columnconfigure(0, weight=1)
        utils_row1.columnconfigure(1, weight=1)
        
        sensor_button = ttk.Button(utils_row1, text="Sensor Info", 
                              command=self.show_sensor_info, 
                              style='Secondary.TButton')
        sensor_button.grid(row=0, column=0, sticky='ew', padx=(0, 5))
        
        email_button = ttk.Button(utils_row1, text="Test Email", 
                             command=self.send_test_email, 
                             style='Secondary.TButton')
        email_button.grid(row=0, column=1, sticky='ew', padx=(5, 0))
        
        # Temperature Settings Section
        settings_frame = ttk.LabelFrame(right_column, text="TEMPERATURE SETTINGS", 
                                   style='Card.TLabelframe', padding="15")
        settings_frame.grid(row=2, column=0, sticky='ew', pady=(0, base_padding))
        
        # Warning temperature
        warning_frame = ttk.Frame(settings_frame, style='Card.TFrame')
        warning_frame.grid(row=0, column=0, sticky='ew', pady=(0, 12))
        
        ttk.Label(warning_frame, text="Warning Threshold (°C):", 
                 background=self.colors['card_bg'],
                 foreground=self.colors['text_primary'],
                 font=('Segoe UI', 9)).grid(row=0, column=0, sticky='w')
        
        self.warning_var = tk.StringVar(value=str(self.warning_temp))
        warning_entry = ttk.Entry(warning_frame, textvariable=self.warning_var, 
                             width=8,
                             style='Modern.TEntry',
                             font=('Segoe UI', 10),
                             justify=tk.CENTER)
        warning_entry.grid(row=1, column=0, sticky='w', pady=(8, 0))
        
        # Critical temperature
        critical_frame = ttk.Frame(settings_frame, style='Card.TFrame')
        critical_frame.grid(row=1, column=0, sticky='ew', pady=(0, 15))
        
        ttk.Label(critical_frame, text="Critical Threshold (°C):", 
                 background=self.colors['card_bg'],
                 foreground=self.colors['text_primary'],
                 font=('Segoe UI', 9)).grid(row=0, column=0, sticky='w')
        
        self.critical_var = tk.StringVar(value=str(self.critical_temp))
        critical_entry = ttk.Entry(critical_frame, textvariable=self.critical_var, 
                              width=8,
                              style='Modern.TEntry',
                              font=('Segoe UI', 10),
                              justify=tk.CENTER)
        critical_entry.grid(row=1, column=0, sticky='w', pady=(8, 0))
        
        # Save Settings button
        update_button = ttk.Button(settings_frame, text="Save Settings", 
                              command=self.update_settings, 
                              style='Primary.TButton')
        update_button.grid(row=2, column=0, sticky='ew', pady=(10, 0))
        
        # Footer with status information
        footer_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        footer_frame.grid(row=2, column=0, sticky='ew', pady=(base_padding, 0))
        footer_frame.columnconfigure(0, weight=1)
        
        # Left footer - Update time
        self.last_update_var = tk.StringVar(value="Last update: --")
        last_update_label = ttk.Label(footer_frame, textvariable=self.last_update_var,
                                 background=self.colors['surface'],
                                 foreground=self.colors['text_secondary'],
                                 font=("Segoe UI", 9))
        last_update_label.grid(row=0, column=0, sticky='w')
        
        # Center footer - Current time
        self.time_var = tk.StringVar(value="--:--:--")
        time_label = ttk.Label(footer_frame, textvariable=self.time_var,
                          background=self.colors['surface'],
                          foreground=self.colors['text_secondary'],
                          font=("Segoe UI", 9))
        time_label.grid(row=0, column=1, sticky='w', padx=(20, 0))
        
        # Right footer - Next email
        self.next_email_var = tk.StringVar(value="Next report: --")
        next_email_label = ttk.Label(footer_frame, textvariable=self.next_email_var,
                                background=self.colors['surface'],
                                foreground=self.colors['text_secondary'],
                                font=("Segoe UI", 9))
        next_email_label.grid(row=0, column=2, sticky='e')
        
        # Configure grid weights for resizing - essential for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Force update to ensure proper rendering
        self.root.update_idletasks()
    
    def show_live_log(self):
        """Show the Live Log window"""
        LiveLogWindow(self.root, self.log_manager, self.theme_manager, self.responsive_design)
    
    def update_sensor_status(self):
        """Update sensor status display"""
        if self.temp_reader.ohm_available:
            status = "✅ Connected"
            color = self.colors['success']
        else:
            status = "❌ Not Available"
            color = self.colors['error']
        
        self.sensor_status_var.set(status)
    
    def show_sensor_info(self):
        """Show detailed sensor information"""
        info = self.temp_reader.get_detailed_sensor_info()
        messagebox.showinfo("Storage Sensor Information", info)
    
    def start_realtime_updates(self):
        """Start real-time temperature updates immediately"""
        self.is_monitoring = True
        self.update_time_display()
        self.monitor_thread = threading.Thread(target=self.monitor_temperature, daemon=True)
        self.monitor_thread.start()
        
    def start_email_scheduler(self):
        """Start the email scheduler thread"""
        self.email_thread = threading.Thread(target=self.email_scheduler, daemon=True)
        self.email_thread.start()
        
    def update_time_display(self):
        """Update the current time display"""
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.time_var.set(f"Time: {current_time}")
        
        # Update next email report time
        next_email_time = self.last_email_time + self.email_interval
        time_until_next = next_email_time - time.time()
        if time_until_next > 0:
            minutes = int(time_until_next // 60)
            seconds = int(time_until_next % 60)
            self.next_email_var.set(f"Next report: {minutes:02d}:{seconds:02d}")
        else:
            self.next_email_var.set("Next report: Soon")
            
        self.root.after(1000, self.update_time_display)
        
    def get_system_info(self):
        """Get system usage info"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            return cpu_percent, memory_percent
        except:
            return None, None
    
    def update_status_indicator(self, temperature):
        """Update the status indicator color based on temperature"""
        pass
    
    def send_desktop_notification(self, title, message, temp):
        """Send system desktop notification"""
        try:
            notification.notify(
                title=title,
                message=f"{message}\nHottest storage: {temp:.1f}°C",
                timeout=10,
                app_name="Storage Temperature Monitor"
            )
            print(f"Desktop notification sent: {title}")
            
            # Log the notification
            self.log_manager.log_temperature("Alert", temp, f"Alert: {title} - {message}")
            
        except Exception as e:
            print(f"Error sending desktop notification: {e}")
        
        # Play sound alert
        try:
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        except:
            pass
    
    def send_email_report(self):
        """Send email report with temperature statistics"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_config['sender_email']
            msg['To'] = self.email_config['receiver_email']
            msg['Subject'] = f"Storage Temperature Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # Get current temperatures
            current_temps = self.storage_temperatures
            current_max = self.temp_reader.get_max_storage_temperature()
            
            # Prepare actions based on temperature
            actions = []
            if current_max is not None:
                if current_max >= self.critical_temp:
                    actions = [
                        "🚨 IMMEDIATE ACTION REQUIRED:",
                        "- Check cooling system immediately",
                        "- Consider reducing server load",
                        "- Ensure proper ventilation around storage devices",
                        "- Monitor temperatures closely",
                        "- Consider temporary shutdown if temperatures continue to rise"
                    ]
                elif current_max >= self.warning_temp:
                    actions = [
                        "⚠️ WARNING - Monitoring Required:",
                        "- Check ventilation around storage devices",
                        "- Monitor temperature trends",
                        "- Ensure cooling system is functioning properly",
                        "- Consider optimizing server load"
                    ]
                else:
                    actions = [
                        "✅ System operating normally:",
                        "- No immediate action required",
                        "- Continue regular monitoring"
                    ]
            
            # Build email body
            storage_details = "\n".join([f"  - {device}: {temp:.1f}°C" for device, temp in current_temps.items()]) if current_temps else "  No storage temperature data available"
            
            body = f"""
Temperature Monitoring Report
=====================================

Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This automated report provides an overview of the current room temperature status.

Temperature Statistics:
• Current Temperature: {current_max if current_max else 'N/A':.1f}°C
• Estimated IDRAC Temperature: {(current_max -2) if current_max else 'N/A':.1f}°C
• Minimum Temperature: {self.min_temp if self.min_temp != float('inf') else 'N/A':.1f}°C
• Maximum Temperature: {self.max_temp if self.max_temp != float('-inf') else 'N/A':.1f}°C

System Status Overview:
• Warning Threshold: {self.warning_temp}°C
• Critical Threshold: {self.critical_temp}°C
• Current Status: {'CRITICAL' if current_max and current_max >= self.critical_temp else 'WARNING' if current_max and current_max >= self.warning_temp else 'NORMAL'}

Recommended Actions:
{chr(10).join(actions)}

Monitoring Details:
• Device: {os.environ.get('COMPUTERNAME', 'Unknown Device')}
• Report Type: Automated Temperature Monitoring
• Monitoring Interval: 60 Minutes

This is an automated notification from the Temperature Monitoring System.
No response is required unless immediate action is indicated above.
"""
            msg.attach(MIMEText(body, 'plain'))
            
            # Connect to server and send email
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['sender_email'], self.email_config['sender_password'])
            server.send_message(msg)
            server.quit()
            
            print(f"✅ Email report sent successfully at {datetime.datetime.now().strftime('%H:%M:%S')}")
            
            # Log email sent
            self.log_manager.log_temperature("Email", current_max if current_max else 0, "Scheduled email report sent")
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            
            # Log email error
            self.log_manager.log_temperature("Error", 0, f"Failed to send email: {e}")
            
            return False
    
    def send_test_email(self):
        """Send a test email"""
        try:
            success = self.send_email_report()
            if success:
                messagebox.showinfo("Success", "Test email sent successfully!")
            else:
                messagebox.showerror("Error", "Failed to send test email. Check your email configuration.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send test email: {str(e)}")
    
    def email_scheduler(self):
        """Email scheduler that sends reports every 5 minutes"""
        while self.is_monitoring:
            try:
                current_time = time.time()
                
                # Send email every 5 minutes
                if current_time - self.last_email_time >= self.email_interval:
                    if self.storage_temperatures:  # Only send if we have data
                        print("🕒 Sending scheduled email report...")
                        self.send_email_report()
                        self.last_email_time = current_time
                    
                    # Reset min/max for next period
                    self.min_temp = float('inf')
                    self.max_temp = float('-inf')
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                print(f"Email scheduler error: {e}")
                time.sleep(60)
    
    def update_storage_display(self):
        """Update the storage devices display"""
        pass
    
    def update_graph(self):
        """Update the temperature history graph with professional design"""
        self.ax.clear()
        
        if len(self.temp_history) > 0:
            time_minutes = [t/60 for t in self.time_history]
            
            # Create colored line segments based on temperature thresholds
            critical_temp = 30
            warning_temp = 27
            
            if len(time_minutes) > 1:
                # Create segments for different temperature ranges
                segments = []
                current_segment = {'times': [time_minutes[0]], 'temps': [self.temp_history[0]], 'color': self.get_temperature_color(self.temp_history[0], critical_temp, warning_temp)}
                
                for i in range(1, len(time_minutes)):
                    current_color = self.get_temperature_color(self.temp_history[i], critical_temp, warning_temp)
                    
                    if current_color == current_segment['color']:
                        # Continue current segment
                        current_segment['times'].append(time_minutes[i])
                        current_segment['temps'].append(self.temp_history[i])
                    else:
                        # End current segment and start new one
                        segments.append(current_segment)
                        current_segment = {'times': [time_minutes[i]], 'temps': [self.temp_history[i]], 'color': current_color}
                
                segments.append(current_segment)
                
                # Plot each segment with its respective color
                for segment in segments:
                    if len(segment['times']) > 1:
                        self.ax.plot(segment['times'], segment['temps'], 
                                    color=segment['color'], 
                                    linewidth=2.5, 
                                    marker='o',
                                    markersize=3,
                                    alpha=0.9)
            
            # Add legend for temperature ranges
            from matplotlib.lines import Line2D
            legend_elements = [
                Line2D([0], [0], color='blue', lw=3, label='Normal Temperature (<27°C)'),
                Line2D([0], [0], color='yellow', lw=3, label='Warning (27-30°C)'),
                Line2D([0], [0], color='red', lw=3, label='Critical (>30°C)')
            ]
            self.ax.legend(handles=legend_elements, loc='upper right', fontsize=9, framealpha=0.95)
            
            # Professional labels and title
            self.ax.set_ylabel('Temperature (°C)', fontsize=10, fontweight='bold')
            
            # X-axis label now clearly visible
            self.ax.set_xlabel('Time (Minutes)', fontsize=10, fontweight='bold')
            
            # Add "Temperature Trend" title
            self.ax.set_title('Temperature', 
                            fontsize=12, fontweight='bold', pad=20)
            
            # Professional grid
            self.ax.grid(True, alpha=0.2, linestyle='-')
            
            # Set professional y-axis limits
            if self.temp_history:
                current_min = min(self.temp_history)
                current_max = max(self.temp_history)
                padding = max(2, (current_max - current_min) * 0.1)
                self.ax.set_ylim(max(0, current_min - padding), current_max + padding)
            
            # Professional spine styling
            for spine in self.ax.spines.values():
                spine.set_color(self.colors['border'])
                spine.set_linewidth(1)
        
        else:
            # Professional no-data message
            self.ax.text(0.5, 0.5, 'Collecting temperature data...', 
                        horizontalalignment='center', verticalalignment='center',
                        transform=self.ax.transAxes, fontsize=11,
                        bbox=dict(boxstyle="round,pad=0.3", facecolor=self.colors['hover']))
            self.ax.set_xlim(0, 1)
            self.ax.set_ylim(0, 1)
            self.ax.set_xticks([])
            self.ax.set_yticks([])
        
        # Moved note further down with more spacing
        note_text = "Note: Temperatures shown are adjusted for room temperature (not actual device readings)"
        self.ax.text(0.5, -0.35, note_text, transform=self.ax.transAxes, 
                    fontsize=8, color=self.colors['text_secondary'],
                    horizontalalignment='center', verticalalignment='top',
                    style='italic')
        
        # Adjust layout to make more room for the note
        self.fig.tight_layout(rect=[0, 0.12, 1, 0.95])
        
        self.canvas.draw()
    
    def get_temperature_color(self, temperature, critical_temp, warning_temp):
        """Get color based on temperature value"""
        if temperature >= critical_temp:
            return 'red'  # Critical
        elif temperature >= warning_temp:
            return 'yellow'  # Warning
        else:
            return 'blue'  # Normal
    
    def monitor_temperature(self):
        """Main monitoring loop"""
        start_time = time.time()
        
        while self.is_monitoring:
            try:
                # Get all storage temperatures
                self.storage_temperatures = self.temp_reader.get_storage_temperatures()
                max_temp = self.temp_reader.get_max_storage_temperature()
                avg_temp = self.temp_reader.get_average_storage_temperature()
                cpu_percent, memory_percent = self.get_system_info()
                
                if max_temp is not None:
                    current_time = time.time() - start_time
                    
                    # Update min/max for email reports
                    if max_temp < self.min_temp:
                        self.min_temp = max_temp
                    if max_temp > self.max_temp:
                        self.max_temp = max_temp
                    
                    # Update display immediately
                    self.root.after(0, self.update_display, max_temp, avg_temp, cpu_percent, memory_percent, current_time)
                    
                    # Update history with max temperature
                    self.temp_history.append(max_temp)
                    self.time_history.append(current_time)
                    
                    # Log temperature data persistently
                    if avg_temp is not None:
                        self.log_manager.log_temperature("Average Temperature", avg_temp)
                    if max_temp is not None:
                        self.log_manager.log_temperature("Max Temperature", max_temp)
                    if self.storage_temperatures:
                        storage_details = ", ".join([f"{device}: {temp:.1f}°C" for device, temp in self.storage_temperatures.items()])
                        self.log_manager.log_temperature("Storage Details", 0, f"Storage temperatures: {storage_details}")
                    
                    # Check for alerts only if alert monitoring is active
                    if self.alert_monitoring_active:
                        current_absolute_time = time.time()
                        
                        if max_temp >= self.critical_temp:
                            # Send critical alerts (with cooldown)
                            if current_absolute_time - self.last_warning_time > self.warning_cooldown:
                                self.root.after(0, self.send_desktop_notification,
                                              "🔥 CRITICAL STORAGE TEMPERATURE ALERT!",
                                              "Storage temperature is critically high!",
                                              max_temp)
                                self.last_warning_time = current_absolute_time
                                
                        elif max_temp >= self.warning_temp:
                            # Send warning alerts (with cooldown)
                            if current_absolute_time - self.last_warning_time > self.warning_cooldown:
                                self.root.after(0, self.send_desktop_notification,
                                              "⚠️ HIGH STORAGE TEMPERATURE WARNING",
                                              "Storage temperature is above normal",
                                              max_temp)
                                self.last_warning_time = current_absolute_time
                else:
                    # No temperature data available
                    current_time = time.time() - start_time
                    self.root.after(0, self.update_display, None, None, None, None, current_time)
                    
                    # Log sensor unavailability
                    self.log_manager.log_temperature("Error", 0, "No temperature data available from sensors")
                
                # Get refresh rate from UI
                try:
                    refresh_delay = max(1, float(self.refresh_rate_var.get()))
                except:
                    refresh_delay = 2
                    
                time.sleep(refresh_delay)
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                
                # Log monitoring errors
                self.log_manager.log_temperature("Error", 0, f"Monitoring error: {e}")
                
                time.sleep(5)
    
    def update_display(self, max_temp, avg_temp, cpu_percent, memory_percent, current_time):
        """Update the UI display with current readings"""
        # Update average and max temperatures
        if avg_temp is not None:
            self.avg_temp_var.set(f"{avg_temp:.1f}°C")
        else:
            self.avg_temp_var.set("--°C")
            
        if max_temp is not None:
            self.max_temp_var.set(f"{max_temp:.1f}°C")
        else:
            self.max_temp_var.set("--°C")
        
        # Update system status in sensor status section
        if max_temp is None:
            status_text = "No sensor data"
            self.max_temp_display.config(foreground=self.colors['error'])
            self.avg_temp_display.config(foreground=self.colors['error'])
        elif max_temp >= self.critical_temp:
            status_text = f"CRITICAL {max_temp:.1f}°C"
            self.max_temp_display.config(foreground=self.colors['error'])
            self.avg_temp_display.config(foreground=self.colors['error'])
        elif max_temp >= self.warning_temp:
            status_text = f"WARNING {max_temp:.1f}°C"
            self.max_temp_display.config(foreground=self.colors['warning'])
            self.avg_temp_display.config(foreground=self.colors['warning'])
        else:
            status_text = f"Normal {max_temp:.1f}°C"
            self.max_temp_display.config(foreground=self.colors['success'])
            self.avg_temp_display.config(foreground=self.colors['success'])
        
        # Add alert status to display
        if self.alert_monitoring_active:
            status_text += " | Alerts ON"
        else:
            status_text += " | Alerts OFF"
            
        self.status_var.set(status_text)
        
        update_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.last_update_var.set(f"Updated: {update_time}")
        
        self.update_graph()
    
    def start_alert_monitoring(self):
        """Start alert monitoring (notifications)"""
        self.alert_monitoring_active = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        
        # Log alert status change
        self.log_manager.log_temperature("System", 0, "Alert monitoring enabled")
        
        messagebox.showinfo("Alerts Enabled", "Storage temperature alert monitoring is now active!\n\nYou will receive notifications when storage temperatures exceed thresholds.")
    
    def stop_alert_monitoring(self):
        """Stop alert monitoring (notifications)"""
        self.alert_monitoring_active = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        
        # Log alert status change
        self.log_manager.log_temperature("System", 0, "Alert monitoring disabled")
        
        messagebox.showinfo("Alerts Disabled", "Storage temperature alert monitoring is now inactive.")
    
    def manual_refresh(self):
        """Force an immediate temperature refresh"""
        self.storage_temperatures = self.temp_reader.get_storage_temperatures()
        max_temp = self.temp_reader.get_max_storage_temperature()
        avg_temp = self.temp_reader.get_average_storage_temperature()
        cpu_percent, memory_percent = self.get_system_info()
        if max_temp is not None:
            self.update_display(max_temp, avg_temp, cpu_percent, memory_percent, 
                              len(self.time_history) * float(self.refresh_rate_var.get()))
    
    def update_settings(self):
        """Update temperature threshold settings"""
        try:
            new_warning = float(self.warning_var.get())
            new_critical = float(self.critical_var.get())
            
            if new_warning >= new_critical:
                messagebox.showerror("Error", "Warning temperature must be lower than critical temperature")
                return
            
            self.warning_temp = new_warning
            self.critical_temp = new_critical
            self.save_settings()
            
            # Log settings change
            self.log_manager.log_temperature("System", 0, f"Settings updated: Warning={new_warning}°C, Critical={new_critical}°C")
            
            messagebox.showinfo("Success", "Temperature settings updated successfully")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for temperature thresholds")
    
    def on_closing(self):
        """Clean up when closing the application"""
        self.is_monitoring = False
        
        # Log application shutdown
        self.log_manager.log_temperature("System", "N/A", "Storage Temperature Monitor shutting down")
        
        self.save_settings()
        self.root.destroy()

def main():
    # Check dependencies
    try:
        import psutil
        from plyer import notification
        # Try to import WMI (required)
        try:
            import wmi
            print("✅ WMI support available")
        except ImportError:
            print("❌ WMI not available - install with: pip install wmi")
            messagebox.showerror("Missing Dependency", "WMI is required for this application.\n\nPlease install it with: pip install wmi")
            return
            
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install required packages:")
        print("pip install psutil plyer matplotlib wmi")
        messagebox.showerror("Missing Dependencies", f"Missing required packages:\n\nPlease install: pip install psutil plyer matplotlib wmi")
        return
    
    # Create and run the application
    root = tk.Tk()
    app = TemperatureMonitor(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    root.mainloop()

if __name__ == "__main__":
    main()