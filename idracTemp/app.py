from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
import smtplib
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import json
import time
from datetime import datetime, timedelta
import urllib3
import re

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# Configuration
class Config:
    IDRAC_URL = "https://10.129.16.81"
    IDRAC_USERNAME = "root"
    IDRAC_PASSWORD = "P@ssw0rd3128!"
    
    # SMTP Configuration
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SENDER_EMAIL = "iantolentino0110@gmail.com"
    SENDER_PASSWORD = "pbry vaoq jwoz pyyp"
    RECEIVER_EMAIL = "supercompnxp@gmail.com"
    
    # Monitoring Configuration
    CHECK_INTERVAL_MINUTES = 60
    WARNING_THRESHOLD = 27
    CRITICAL_THRESHOLD = 30
    
    # Email Settings
    SEND_WARNING_EMAILS = True
    SEND_CRITICAL_EMAILS = True
    SEND_REGULAR_REPORTS = True

# Global variables
last_temperature = None
last_status = "UNKNOWN"
temperature_history = []
last_email_sent = {}
last_regular_report_sent = None

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('idrac_monitor.log'),
            logging.StreamHandler()
        ]
    )

class IDRACMonitor:
    def __init__(self):
        self.base_url = Config.IDRAC_URL
        self.username = Config.IDRAC_USERNAME
        self.password = Config.IDRAC_PASSWORD
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
    def get_temperature(self):
        """Get temperature from iDRAC using multiple methods"""
        try:
            logging.info("Attempting to get temperature from iDRAC...")
            
            # Try multiple methods in sequence
            methods = [
                self._try_redfish_api,
                self._try_legacy_api, 
                self._try_html_parsing,
                self._try_sensor_api
            ]
            
            for method in methods:
                try:
                    temp, status = method()
                    if temp is not None:
                        logging.info(f"Successfully got temperature via {method.__name__}: {temp}°C")
                        return temp, status
                except Exception as e:
                    logging.warning(f"Method {method.__name__} failed: {str(e)}")
                    continue
            
            logging.error("All temperature retrieval methods failed")
            return None, "All retrieval methods failed"
            
        except Exception as e:
            logging.error(f"Temperature retrieval error: {str(e)}")
            return None, str(e)
    
    def _try_redfish_api(self):
        """Try Redfish API endpoints"""
        endpoints = [
            "/redfish/v1/Chassis/System.Embedded.1/Thermal",
            "/redfish/v1/Chassis/1/Thermal", 
            "/redfish/v1/Chassis/Self/Thermal",
            "/redfish/v1/Chassis/System.Embedded.1/Sensors"
        ]
        
        for endpoint in endpoints:
            try:
                url = f"{self.base_url}{endpoint}"
                response = self.session.get(url, auth=(self.username, self.password), timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    logging.info(f"Redfish response from {endpoint}")
                    
                    # Parse different Redfish structures
                    temp = self._parse_redfish_data(data)
                    if temp is not None:
                        return temp, self._get_temperature_status(temp)
                        
            except Exception as e:
                logging.warning(f"Redfish endpoint {endpoint} failed: {str(e)}")
                continue
                
        return None, "Redfish API unavailable"
    
    def _parse_redfish_data(self, data):
        """Parse temperature from various Redfish structures - WITH -60°C ADJUSTMENT"""
        # Method 1: Look for Temperatures array (most common)
        if 'Temperatures' in data:
            for sensor in data['Temperatures']:
                sensor_name = sensor.get('Name', 'Unknown')
                reading_c = sensor.get('ReadingCelsius')
                reading_raw = sensor.get('Reading')
                
                # Prefer ReadingCelsius if available
                if reading_c is not None:
                    # Apply -60°C adjustment and validate it's a reasonable temperature
                    adjusted_temp = reading_c - 60
                    if 0 <= adjusted_temp <= 100:
                        logging.info(f"Using adjusted ReadingCelsius: {reading_c}°C -> {adjusted_temp}°C from sensor: {sensor_name}")
                        return adjusted_temp
                
                # Fallback to Reading field
                if reading_raw is not None:
                    if isinstance(reading_raw, (int, float)):
                        adjusted_temp = reading_raw - 60
                        if 0 <= adjusted_temp <= 100:
                            logging.info(f"Using adjusted Reading: {reading_raw}°C -> {adjusted_temp}°C from sensor: {sensor_name}")
                            return adjusted_temp
                    elif isinstance(reading_raw, str):
                        match = re.search(r'(\d+)', str(reading_raw))
                        if match:
                            temp = int(match.group(1))
                            adjusted_temp = temp - 60
                            if 0 <= adjusted_temp <= 100:
                                logging.info(f"Using adjusted parsed Reading: {temp}°C -> {adjusted_temp}°C from sensor: {sensor_name}")
                                return adjusted_temp
        
        return None
    
    def _try_legacy_api(self):
        """Try legacy iDRAC API endpoints"""
        endpoints = [
            "/data?get=tempReading,thermalReading",
            "/data?get=tempReading",
            "/data?get=thermalReading",
            "/sysmgmt/2012/server/temperature",
            "/data?get=sensorData"
        ]
        
        for endpoint in endpoints:
            try:
                url = f"{self.base_url}{endpoint}"
                response = self.session.get(url, auth=(self.username, self.password), timeout=10)
                
                if response.status_code == 200:
                    # Try JSON parsing
                    try:
                        data = response.json()
                        if 'tempReading' in data:
                            temp = data['tempReading'] - 60  # Apply adjustment
                            if 0 <= temp <= 100:
                                return temp, self._get_temperature_status(temp)
                        if 'thermalReading' in data:
                            temp = data['thermalReading'] - 60  # Apply adjustment
                            if 0 <= temp <= 100:
                                return temp, self._get_temperature_status(temp)
                    except:
                        # Try text parsing
                        text = response.text
                        temp = self._extract_temperature_from_text(text)
                        if temp is not None:
                            adjusted_temp = temp - 60  # Apply adjustment
                            if 0 <= adjusted_temp <= 100:
                                return adjusted_temp, self._get_temperature_status(adjusted_temp)
                            
            except Exception as e:
                continue
                
        return None, "Legacy API unavailable"
    
    def _try_sensor_api(self):
        """Try sensor-specific endpoints"""
        endpoints = [
            "/sysmgmt/2015/bmc/info",
            "/sysmgmt/2012/server/info",
            "/data?get=ambientTemp",
            "/data?get=cpuTemp"
        ]
        
        for endpoint in endpoints:
            try:
                url = f"{self.base_url}{endpoint}"
                response = self.session.get(url, auth=(self.username, self.password), timeout=10)
                
                if response.status_code == 200:
                    text = response.text
                    temp = self._extract_temperature_from_text(text)
                    if temp is not None:
                        adjusted_temp = temp - 60  # Apply adjustment
                        if 0 <= adjusted_temp <= 100:
                            return adjusted_temp, self._get_temperature_status(adjusted_temp)
                        
            except Exception as e:
                continue
                
        return None, "Sensor API unavailable"
    
    def _try_html_parsing(self):
        """Try parsing temperature from HTML pages"""
        endpoints = [
            "/",
            "/index.html", 
            "/main.html",
            "/restgui/start.html",
            "/sysmgmt/2012/server/dashboard"
        ]
        
        for endpoint in endpoints:
            try:
                url = f"{self.base_url}{endpoint}"
                response = self.session.get(url, auth=(self.username, self.password), timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    text = soup.get_text()
                    temp = self._extract_temperature_from_text(text)
                    if temp is not None:
                        adjusted_temp = temp - 60  # Apply adjustment
                        if 0 <= adjusted_temp <= 100:
                            return adjusted_temp, self._get_temperature_status(adjusted_temp)
                        
            except Exception as e:
                continue
                
        return None, "HTML parsing failed"
    
    def _extract_temperature_from_text(self, text):
        """Extract temperature value from text using regex patterns"""
        patterns = [
            r'temp[^\d]*(\d+)°?c',
            r'temperature[^\d]*(\d+)°?c', 
            r'thermal[^\d]*(\d+)°?c',
            r'(\d+)°?c',
            r'(\d+)\s*degrees',
            r'ReadingCelsius[^\d]*(\d+)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                for match in matches:
                    try:
                        temp = int(match)
                        if 0 <= temp <= 100:
                            return temp
                    except ValueError:
                        continue
        return None
    
    def _get_temperature_status(self, temperature):
        """Determine temperature status"""
        if temperature >= Config.CRITICAL_THRESHOLD:
            return "CRITICAL"
        elif temperature >= Config.WARNING_THRESHOLD:
            return "WARNING"
        else:
            return "NORMAL"

class EmailSender:
    @staticmethod
    def send_email(temperature, status, is_test=False, email_type="status"):
        """Send email with temperature information"""
        try:
            if is_test:
                subject = "TEST: iDRAC Temperature Monitoring System"
                # Get current temperature for test email
                current_temp, current_status = monitor.get_temperature()
                body = EmailSender._create_test_email_body(current_temp, current_status)
            else:
                if email_type == "warning":
                    subject = f"WARNING: High Temperature Alert - {temperature}°C"
                elif email_type == "critical":
                    subject = f"CRITICAL: Immediate Action Required - {temperature}°C"
                elif email_type == "regular":
                    subject = f"Regular Temperature Report - {temperature}°C"
                elif email_type == "manual":
                    subject = f"Manual Temperature Report - {temperature}°C"
                else:
                    subject = f"Temperature Monitoring Report - {status}"
                
                body = EmailSender._create_email_body(temperature, status, email_type)
            
            # Create email manually
            message = f"Subject: {subject}\n\n{body}"
            
            # Send email
            with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
                server.starttls()
                server.login(Config.SENDER_EMAIL, Config.SENDER_PASSWORD)
                server.sendmail(Config.SENDER_EMAIL, Config.RECEIVER_EMAIL, message)
            
            logging.info(f"✅ Email sent successfully - Type: {email_type}, Temperature: {temperature}°C, Status: {status}")
            return True
            
        except Exception as e:
            logging.error(f"❌ Email sending failed: {str(e)}")
            return False
    
    @staticmethod
    def _create_email_body(temperature, status, email_type):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if email_type == "warning":
            recommendations = "• Monitor temperature closely\n• Check cooling systems\n• Ensure proper ventilation"
        elif email_type == "critical":
            recommendations = "• IMMEDIATE ACTION REQUIRED\n• Check server cooling\n• Contact IT support"
        else:
            recommendations = "• System operating normally\n• Continue regular monitoring"
        
        return f"""Temperature Monitoring Report
=====================================

Timestamp: {timestamp}

Temperature: {temperature}°C
Status: {status}
Alert Type: {email_type.upper()}

Thresholds:
• Warning: {Config.WARNING_THRESHOLD}°C
• Critical: {Config.CRITICAL_THRESHOLD}°C

Recommended Actions:
{recommendations}

Monitoring Details:
• iDRAC URL: {Config.IDRAC_URL}
• Monitoring Interval: {Config.CHECK_INTERVAL_MINUTES} Minutes

This is an automated notification."""
    
    @staticmethod
    def _create_test_email_body(current_temp, current_status):
        """Create email body for test email with current temperature"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return f"""✅ TEST EMAIL - iDRAC Temperature Monitoring System

This is a test email to verify the monitoring system is working correctly.

If you received this email, the system is operational and can send alerts.

CURRENT SYSTEM STATUS:
• Current Temperature: {current_temp}°C
• Current Status: {current_status}
• Alert Type: TEST

THRESHOLDS:
• Warning Threshold: {Config.WARNING_THRESHOLD}°C
• Critical Threshold: {Config.CRITICAL_THRESHOLD}°C

System Configuration:
• iDRAC URL: {Config.IDRAC_URL}
• Monitoring Interval: {Config.CHECK_INTERVAL_MINUTES} minutes
• Last Check: {timestamp}

This is an automated test message. No action required."""

# Global instances
monitor = IDRACMonitor()
email_sender = EmailSender()

def should_send_alert_email(status, email_type):
    """Determine if we should send an alert email"""
    global last_email_sent
    
    if email_type == "test":
        return True
    
    # Check configuration
    if status == "WARNING" and not Config.SEND_WARNING_EMAILS:
        return False
    if status == "CRITICAL" and not Config.SEND_CRITICAL_EMAILS:
        return False
    
    # Anti-spam cooldown
    now = datetime.now()
    last_sent = last_email_sent.get(email_type)
    
    if last_sent and (now - last_sent) < timedelta(minutes=30):
        return False
    
    last_email_sent[email_type] = now
    return True

def should_send_regular_report():
    """Determine if we should send a regular report"""
    global last_regular_report_sent
    
    if not Config.SEND_REGULAR_REPORTS:
        return False
    
    now = datetime.now()
    
    if last_regular_report_sent is None:
        last_regular_report_sent = now
        return True
    
    time_since_last = now - last_regular_report_sent
    if time_since_last >= timedelta(minutes=Config.CHECK_INTERVAL_MINUTES):
        last_regular_report_sent = now
        return True
    
    return False

def check_temperature_and_notify():
    """Check temperature and send notifications"""
    global last_temperature, last_status, temperature_history
    
    try:
        logging.info("Checking temperature...")
        temperature, status = monitor.get_temperature()
        
        if temperature is not None:
            last_temperature = temperature
            last_status = status
            
            # Store history
            temperature_history.append({
                'timestamp': datetime.now(),
                'temperature': temperature,
                'status': status
            })
            
            # Keep history manageable
            if len(temperature_history) > 100:
                temperature_history = temperature_history[-100:]
            
            logging.info(f"Temperature: {temperature}°C, Status: {status}")
            
            # Send alert emails based on status
            if status == "CRITICAL" and should_send_alert_email(status, "critical"):
                if email_sender.send_email(temperature, status, email_type="critical"):
                    logging.info("✅ Critical alert email sent")
            
            elif status == "WARNING" and should_send_alert_email(status, "warning"):
                if email_sender.send_email(temperature, status, email_type="warning"):
                    logging.info("✅ Warning alert email sent")
            
            # Send regular report
            if should_send_regular_report():
                if email_sender.send_email(temperature, status, email_type="regular"):
                    logging.info("✅ Regular report email sent")
            
            return temperature, status
        else:
            logging.warning("Could not retrieve temperature")
            return None, status
            
    except Exception as e:
        logging.error(f"Temperature check error: {str(e)}")
        return None, str(e)

def scheduled_monitoring():
    """Scheduled monitoring task"""
    with app.app_context():
        check_temperature_and_notify()

# Initialize scheduler
scheduler = BackgroundScheduler()

# ========== ALL API ENDPOINTS ==========

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/temperature', methods=['GET'])
def api_get_temperature():
    """API endpoint to get current temperature"""
    temperature, status = check_temperature_and_notify()
    
    return jsonify({
        'success': temperature is not None,
        'temperature': temperature,
        'status': status,
        'timestamp': datetime.now().isoformat(),
        'message': 'Temperature retrieved successfully' if temperature else status
    })

@app.route('/api/send-test-email', methods=['POST'])
def api_send_test_email():
    """API endpoint to send test email"""
    success = email_sender.send_email(None, None, is_test=True)
    return jsonify({
        'success': success,
        'message': 'Test email sent successfully' if success else 'Failed to send test email'
    })

@app.route('/api/send-report', methods=['POST'])
def api_send_report():
    """API endpoint to send manual temperature report"""
    try:
        # First, get the current temperature to ensure we have fresh data
        temperature, status = check_temperature_and_notify()
        
        if temperature is None:
            # If we can't get current temperature, try to use the last one
            if last_temperature is None:
                return jsonify({
                    'success': False,
                    'message': 'No temperature data available. Please check iDRAC connection.'
                })
            else:
                temperature = last_temperature
                status = last_status
                logging.info(f"Using last known temperature for manual report: {temperature}°C")
        
        success = email_sender.send_email(temperature, status, email_type="manual")
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Manual report sent successfully! Temperature: {temperature}°C, Status: {status}'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to send manual report email. Check email configuration.'
            })
            
    except Exception as e:
        logging.error(f"Manual report error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error sending manual report: {str(e)}'
        })

@app.route('/api/history', methods=['GET'])
def api_get_history():
    """API endpoint to get temperature history"""
    return jsonify({
        'history': [
            {
                'timestamp': reading['timestamp'].isoformat(),
                'temperature': reading['temperature'],
                'status': reading['status']
            }
            for reading in temperature_history[-24:]  # Last 24 readings
        ]
    })

@app.route('/api/status', methods=['GET'])
def api_get_status():
    """API endpoint to get system status"""
    return jsonify({
        'last_temperature': last_temperature,
        'last_status': last_status,
        'last_check': temperature_history[-1]['timestamp'].isoformat() if temperature_history else None,
        'monitoring_active': scheduler.running,
        'check_interval': Config.CHECK_INTERVAL_MINUTES,
        'email_settings': {
            'send_warning_emails': Config.SEND_WARNING_EMAILS,
            'send_critical_emails': Config.SEND_CRITICAL_EMAILS,
            'send_regular_reports': Config.SEND_REGULAR_REPORTS
        }
    })

@app.route('/api/test-email-connection', methods=['POST'])
def api_test_email_connection():
    """Test email connection and sending"""
    try:
        # Test SMTP connection
        with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(Config.SENDER_EMAIL, Config.SENDER_PASSWORD)
        
        return jsonify({
            'success': True,
            'message': 'SMTP connection successful'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'SMTP connection failed: {str(e)}'
        })

@app.route('/api/settings', methods=['POST'])
def api_update_settings():
    """API endpoint to update monitoring settings"""
    try:
        data = request.get_json()
        
        if 'send_warning_emails' in data:
            Config.SEND_WARNING_EMAILS = bool(data['send_warning_emails'])
        if 'send_critical_emails' in data:
            Config.SEND_CRITICAL_EMAILS = bool(data['send_critical_emails'])
        if 'send_regular_reports' in data:
            Config.SEND_REGULAR_REPORTS = bool(data['send_regular_reports'])
        if 'check_interval' in data:
            Config.CHECK_INTERVAL_MINUTES = int(data['check_interval'])
            
        # Restart scheduler with new interval
        if scheduler.running:
            scheduler.remove_job('temperature_monitoring')
            scheduler.add_job(
                func=scheduled_monitoring,
                trigger="interval",
                minutes=Config.CHECK_INTERVAL_MINUTES,
                id='temperature_monitoring'
            )
        
        return jsonify({
            'success': True,
            'message': 'Settings updated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error updating settings: {str(e)}'
        })

if __name__ == '__main__':
    setup_logging()
    
    logging.info("Starting iDRAC Temperature Monitor...")
    
    # Test initial connection
    logging.info("Testing iDRAC connection...")
    temp, status = monitor.get_temperature()
    
    if temp is not None:
        logging.info(f"Initial temperature reading: {temp}°C")
    else:
        logging.warning(f"Initial temperature reading failed: {status}")
    
    # Start scheduler
    scheduler.add_job(
        func=scheduled_monitoring,
        trigger="interval",
        minutes=Config.CHECK_INTERVAL_MINUTES,
        id='temperature_monitoring'
    )
    scheduler.start()
    logging.info(f"Scheduler started - checking every {Config.CHECK_INTERVAL_MINUTES} minutes")
    
    # Start Flask app
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)