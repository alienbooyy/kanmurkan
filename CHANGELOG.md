# Changelog

All notable changes to the Restaurant Automation System will be documented in this file.

## [1.0.1] - 2024-01-16

### Security
- **CRITICAL**: Updated `fastapi` from 0.104.1 to 0.109.1
  - Fixed Content-Type Header ReDoS vulnerability
- **HIGH**: Updated `pillow` from 10.1.0 to 10.3.0
  - Fixed buffer overflow vulnerability in image processing
- **HIGH**: Updated `python-multipart` from 0.0.6 to 0.0.18
  - Fixed Denial of Service (DoS) vulnerability via malformed multipart/form-data
  - Fixed Content-Type Header ReDoS vulnerability
- **MEDIUM**: Updated `python-jose` from 3.3.0 to 3.4.0
  - Fixed algorithm confusion with OpenSSH ECDSA keys

### Documentation
- Added SECURITY.md with detailed vulnerability information
- Updated README.md with security notice
- Added this CHANGELOG.md

### Testing
- Verified all functionality with updated dependencies
- All tests passing (authentication, orders, reports)
- No breaking changes

## [1.0.0] - 2024-01-16

### Added
- Complete restaurant automation system implementation
- Backend with FastAPI and SQLite
- Frontend with React.js
- Main home page with table management
- Order management page (Adisyon)
- Admin panel with 5 management tabs
- Authentication system with JWT
- Reports and analytics
- Excel export functionality
- Thermal printer support (ESC/POS)
- Touch-optimized UI for tablets
- Offline operation capability
- Local network support

#### Backend Features
- 30+ RESTful API endpoints
- 7 database models
- JWT authentication
- Password hashing with bcrypt
- CORS configuration
- Sample data initialization
- Automated tests

#### Frontend Features
- 5 main pages (Home, Order, Admin, Login, Analytics)
- Touch-friendly interface
- Long press gesture support (6 seconds)
- Color-coded table status (red/green)
- Real-time order totals
- Split payment functionality
- Product catalog
- Responsive design

#### Admin Features
- Table management
- Product management with pricing
- Raw materials inventory
- Recipe management
- Stock management
- End of day reports
- Most sold items analytics
- Date range filtering
- Excel export

#### Documentation
- Comprehensive README.md
- Detailed DEPLOYMENT.md guide
- Complete API.md reference
- Feature documentation (FEATURES.md)
- Project summary (PROJECT_SUMMARY.md)

#### Scripts & Tools
- Build scripts (Linux/Mac/Windows)
- Start scripts (Linux/Mac/Windows)
- System verification script
- Automated test suite

### Technical Stack
- Backend: FastAPI, SQLAlchemy, SQLite
- Frontend: React 18.2, React Router 6.20
- Authentication: JWT with bcrypt
- API: RESTful with Swagger docs
- Database: SQLite
- Printing: ESC/POS protocol

### Testing
- Backend API tests
- Order workflow tests
- System verification
- All tests passing

---

## Version History Summary

- **v1.0.1** (2024-01-16): Security updates - Fixed 5 vulnerabilities
- **v1.0.0** (2024-01-16): Initial release - Complete system implementation

---

## Security Policy

For security issues, please see [SECURITY.md](SECURITY.md).

## Links

- [Installation Guide](README.md)
- [Deployment Guide](DEPLOYMENT.md)
- [API Reference](API.md)
- [Feature Documentation](FEATURES.md)
- [Security Information](SECURITY.md)
