# Restaurant Automation System

A complete offline restaurant automation system with touch-friendly interfaces for managing tables, orders, inventory, and analytics.

## Features

### Main Home Page
- Visual table management with status indicators (Red = Occupied, Green = Vacant)
- Long press (6 seconds) for advanced table operations (move/merge)
- Touch-optimized interface for tablets

### Order Management (Adisyon)
- Quick order creation and management
- Add/remove items with ease
- Four core actions:
  - **Close**: Close order without processing payment
  - **Split Payment**: Process partial payment for selected items
  - **Payment Received**: Process full payment
  - **Print**: Send order to thermal printers (kitchen/oven)

### Admin Panel (Password Protected)
- **End of Day Reports**: View revenue, sales breakdown, and export to Excel
- **Most Sold Items**: Track profitability and product performance
- **Table Management**: Add, edit, or delete tables
- **Product Management**: Manage menu items and prices
- **Raw Materials**: Track inventory with units
- **Recipe Management**: Define recipes with raw material quantities
- **Stock Management**: Monitor inventory levels

### Analytics
- Most and least sold products
- Revenue tracking
- Profitability analysis
- Historical data with date selection

### Offline Operation
- Works without internet connectivity
- Local SQLite database
- Access via local network from tablets
- Direct thermal printer integration

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM
- **SQLite**: Lightweight local database
- **JWT**: Secure authentication

### Frontend
- **React.js**: Modern UI library
- **React Router**: Navigation
- **Axios**: API communication
- **CSS3**: Touch-optimized styling

### Printing
- **ESC/POS**: Thermal printer protocol support
- Multiple printer configuration (kitchen/oven)

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the backend server:
```bash
python main.py
```

The backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000`

## Default Credentials

- **Username**: admin
- **Password**: admin123

**Important**: Change these credentials in production!

## Usage

### For Staff (Tablets)
1. Access the system via local network (e.g., `http://192.168.1.100:3000`)
2. Click on table buttons to manage orders
3. Add items, process payments, and print receipts

### For Administrators
1. Click "Admin" button on home page
2. Login with credentials
3. Manage tables, products, materials, recipes, and view reports

## Creating an Executable

To package the application for deployment:

### Using Build Scripts

**Linux/Mac:**
```bash
chmod +x build.sh
./build.sh
```

**Windows:**
```bash
build.bat
```

### Manual Build

1. For the backend, use PyInstaller:
```bash
pip install pyinstaller
cd backend
pyinstaller --onefile main.py
```

2. For the frontend, build the production version:
```bash
cd frontend
npm run build
```

3. Serve the frontend build using the backend or a simple HTTP server

## Database

The system uses SQLite database (`restaurant.db`) which is created automatically on first run. The database includes:
- Tables management
- Products catalog
- Raw materials inventory
- Recipes
- Orders and order items
- Admin users

## Sample Data

To populate the database with sample data for testing:

```bash
cd backend
python init_sample_data.py
```

This will create:
- 10 sample tables
- Sample menu items (Lahmacun, Pizza, Kebab, etc.)
- Sample raw materials with stock quantities

## Thermal Printer Setup

1. Connect thermal printers to the local network or via USB
2. Configure printer IPs/ports in the backend
3. Test printing from the order page

## Network Setup

1. Connect all tablets to the same local router
2. Configure the backend server IP in frontend API configuration (`frontend/src/api.js`)
3. Access from tablets using the server's local IP address

## API Documentation

Once the backend is running, visit:
- API Documentation: `http://localhost:8000/docs`
- Alternative Documentation: `http://localhost:8000/redoc`

## Development

### Running Tests
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

### Building for Production
```bash
# Frontend
cd frontend
npm run build

# Backend
cd backend
python main.py
```

## Project Structure

```
kanmurkan/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Database models
│   ├── schemas.py              # Pydantic schemas
│   ├── database.py             # Database configuration
│   ├── requirements.txt        # Python dependencies
│   └── init_sample_data.py     # Sample data script
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── pages/              # React pages
│   │   │   ├── HomePage.js     # Main table view
│   │   │   ├── OrderPage.js    # Order management
│   │   │   ├── AdminPanel.js   # Admin interface
│   │   │   ├── Login.js        # Authentication
│   │   │   └── MostSoldPage.js # Analytics
│   │   ├── App.js              # Main app component
│   │   ├── api.js              # API client
│   │   └── index.js            # Entry point
│   └── package.json
├── build.sh                    # Linux/Mac build script
├── build.bat                   # Windows build script
└── README.md
```

## Support

For issues or questions, please refer to the documentation or contact support.

## License

This project is licensed for restaurant automation purposes.
