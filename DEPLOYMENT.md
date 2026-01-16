# Deployment Guide for Restaurant Automation System

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Hardware Setup](#hardware-setup)
3. [Software Installation](#software-installation)
4. [Network Configuration](#network-configuration)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)

## System Requirements

### Server Computer
- Operating System: Windows 10/11, Linux, or macOS
- Processor: Dual-core CPU (2 GHz or higher)
- RAM: 4 GB minimum, 8 GB recommended
- Storage: 10 GB available space
- Network: Ethernet port or Wi-Fi capability

### Staff Tablets
- Operating System: Android 8.0+ or iOS 12+, or Windows tablets
- Screen: 7-inch minimum, 10-inch recommended
- Touch support: Capacitive touch screen
- Network: Wi-Fi capability
- Web Browser: Chrome, Safari, or Edge (latest versions)

### Thermal Printers
- Protocol: ESC/POS compatible
- Connection: Network (Ethernet/Wi-Fi) or USB
- Paper: 58mm or 80mm thermal paper rolls
- Quantity: 2 (one for kitchen, one for oven)

## Hardware Setup

### 1. Network Setup
1. Connect a router to create a local network
2. Connect the server computer to the router (Ethernet recommended)
3. Connect thermal printers to the network
4. Connect all tablets to the same Wi-Fi network

### 2. Printer Configuration
1. Power on thermal printers
2. Configure network settings (refer to printer manual)
3. Note down printer IP addresses
4. Test printer connectivity with ping command

## Software Installation

### Quick Installation (Recommended)

#### Windows
1. Download the latest release package
2. Extract to `C:\RestaurantSystem`
3. Run `install.bat`
4. Follow on-screen instructions

#### Linux
1. Download the latest release package
2. Extract to `/opt/restaurant-system`
3. Run `chmod +x install.sh && ./install.sh`
4. Follow on-screen instructions

### Manual Installation

#### Backend Setup

1. Install Python 3.8 or higher:
   - Windows: Download from https://python.org
   - Linux: `sudo apt-get install python3 python3-pip`
   - macOS: `brew install python3`

2. Navigate to backend directory:
   ```bash
   cd backend
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize database with sample data (optional):
   ```bash
   python init_sample_data.py
   ```

#### Frontend Setup

1. Install Node.js 16 or higher:
   - Download from https://nodejs.org

2. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

3. Install dependencies:
   ```bash
   npm install
   ```

4. Build for production:
   ```bash
   npm run build
   ```

## Network Configuration

### 1. Find Server IP Address

**Windows:**
```cmd
ipconfig
```
Look for "IPv4 Address" under your network adapter

**Linux/macOS:**
```bash
ip addr show
# or
ifconfig
```
Look for `inet` address (e.g., 192.168.1.100)

### 2. Configure Frontend API

Edit `frontend/src/api.js`:
```javascript
const API_BASE_URL = 'http://YOUR_SERVER_IP:8000/api';
```
Replace `YOUR_SERVER_IP` with the actual IP address.

### 3. Configure Printer IPs

Edit `backend/main.py` and update printer configuration:
```python
KITCHEN_PRINTER_IP = "192.168.1.201"
OVEN_PRINTER_IP = "192.168.1.202"
```

## Running the Application

### Development Mode

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

Access the application at `http://localhost:3000`

### Production Mode

#### Option 1: Using Scripts

**Windows:**
```cmd
start_server.bat
```

**Linux:**
```bash
./start_server.sh
```

#### Option 2: Using Executables

After building with `build.sh` or `build.bat`:

1. Start the backend:
   ```bash
   cd backend/dist
   ./restaurant-server
   ```

2. Serve the frontend:
   - Use a web server like nginx or Apache
   - Or use Python's built-in server:
     ```bash
     cd frontend/build
     python -m http.server 3000
     ```

#### Option 3: All-in-One Service

For production deployment, consider using systemd (Linux) or Windows Service to run the application automatically on startup.

## Accessing from Tablets

1. Ensure tablets are connected to the same network
2. Open a web browser on each tablet
3. Navigate to `http://SERVER_IP:3000`
4. Add to home screen for easy access
5. Optionally enable kiosk mode to prevent users from leaving the app

## Default Login Credentials

- **Username:** admin
- **Password:** admin123

**IMPORTANT:** Change these credentials immediately after first login!

To change password:
1. Login to admin panel
2. Navigate to Settings (if implemented)
3. Or manually update in the database

## Initial Configuration

### 1. Add Tables
1. Login to admin panel
2. Go to "Tables" tab
3. Add table numbers (1-50 or as needed)

### 2. Add Products
1. Go to "Products" tab
2. Add menu items with prices
3. Example: Lahmacun - 15.00 TL

### 3. Add Raw Materials (Optional)
1. Go to "Raw Materials" tab
2. Add ingredients with units
3. Set initial stock quantities

### 4. Configure Recipes (Optional)
1. Go to "Recipes" tab
2. Select a product
3. Add raw materials and quantities

## Troubleshooting

### Backend won't start
- Check if port 8000 is already in use
- Verify Python installation: `python --version`
- Check dependencies: `pip list`
- Review error logs

### Frontend won't connect to backend
- Verify backend is running: `curl http://localhost:8000/api/tables`
- Check firewall settings
- Verify API_BASE_URL in `frontend/src/api.js`
- Check browser console for errors

### Tablets can't connect
- Verify all devices are on the same network
- Check server firewall allows incoming connections
- Test connection: `ping SERVER_IP` from tablet
- Ensure backend is listening on 0.0.0.0, not 127.0.0.1

### Printer not working
- Verify printer is powered on and connected
- Check printer IP address is correct
- Test printer with a ping
- Verify ESC/POS compatibility
- Check printer error logs

### Database errors
- Backup existing database
- Delete `restaurant.db`
- Restart application (will create new database)
- Run `init_sample_data.py` to populate

### Long press not working on tablets
- Ensure touch is properly calibrated
- Try adjusting long press duration in code (currently 6 seconds)
- Test with different gestures

## Performance Optimization

### For Server
- Use SSD for database storage
- Increase RAM if handling many simultaneous orders
- Use wired Ethernet connection
- Close unnecessary background applications

### For Tablets
- Clear browser cache regularly
- Use latest browser versions
- Restart tablets daily
- Disable unnecessary background apps

## Backup and Recovery

### Backing Up Database
```bash
# Manual backup
cp backend/restaurant.db backend/backup_$(date +%Y%m%d).db

# Automated backup (Linux/cron)
0 0 * * * cp /path/to/restaurant.db /backup/restaurant_$(date +\%Y\%m\%d).db
```

### Restoring Database
```bash
cp backend/backup_YYYYMMDD.db backend/restaurant.db
```

## Security Recommendations

1. Change default admin password immediately
2. Use HTTPS in production (setup SSL certificate)
3. Regularly update dependencies
4. Restrict network access to trusted devices
5. Regular database backups
6. Keep system and software updated

## Support and Maintenance

### Regular Maintenance Tasks
- Daily: Check printer paper levels
- Weekly: Review system logs
- Monthly: Update software dependencies
- Quarterly: Hardware inspection
- Yearly: Database optimization

### Getting Help
- Check documentation
- Review error logs
- Contact support team

## Appendix

### Useful Commands

**Check server status:**
```bash
curl http://localhost:8000/api/tables
```

**View backend logs:**
```bash
tail -f backend/server.log
```

**Database query:**
```bash
sqlite3 backend/restaurant.db "SELECT * FROM tables;"
```

**Network diagnostics:**
```bash
# Test connectivity
ping 192.168.1.100

# Check open ports
netstat -an | grep 8000
```
