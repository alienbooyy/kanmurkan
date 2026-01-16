import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { tables } from '../api';
import './HomePage.css';

function HomePage() {
  const [tablesList, setTablesList] = useState([]);
  const [longPressTimer, setLongPressTimer] = useState(null);
  const [longPressedTable, setLongPressedTable] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    loadTables();
  }, []);

  const loadTables = async () => {
    try {
      const response = await tables.getAll();
      setTablesList(response.data);
    } catch (error) {
      console.error('Failed to load tables:', error);
    }
  };

  const handleTableClick = (table) => {
    if (!longPressedTable) {
      navigate(`/order/${table.id}`);
    }
  };

  const handleTouchStart = (table) => {
    const timer = setTimeout(() => {
      setLongPressedTable(table);
    }, 6000);
    setLongPressTimer(timer);
  };

  const handleTouchEnd = () => {
    if (longPressTimer) {
      clearTimeout(longPressTimer);
      setLongPressTimer(null);
    }
  };

  const closeLongPressMenu = () => {
    setLongPressedTable(null);
  };

  return (
    <div className="home-page">
      <header className="header">
        <h1>Restaurant System</h1>
        <div className="header-buttons">
          <button onClick={() => navigate('/most-sold')} className="btn-secondary">
            Most Sold
          </button>
          <button onClick={() => navigate('/login')} className="btn-secondary">
            Admin
          </button>
        </div>
      </header>

      <div className="tables-grid">
        {tablesList.map((table) => (
          <button
            key={table.id}
            className={`table-button ${table.is_occupied ? 'occupied' : 'vacant'}`}
            onClick={() => handleTableClick(table)}
            onTouchStart={() => handleTouchStart(table)}
            onTouchEnd={handleTouchEnd}
            onMouseDown={() => handleTouchStart(table)}
            onMouseUp={handleTouchEnd}
            onMouseLeave={handleTouchEnd}
          >
            <span className="table-number">Table {table.table_number}</span>
            <span className="table-status">
              {table.is_occupied ? 'Occupied' : 'Vacant'}
            </span>
          </button>
        ))}
      </div>

      {longPressedTable && (
        <div className="modal-overlay" onClick={closeLongPressMenu}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>Table {longPressedTable.table_number} Operations</h2>
            <div className="modal-buttons">
              <button className="btn-primary">Move Table</button>
              <button className="btn-primary">Merge Table</button>
              <button className="btn-secondary" onClick={closeLongPressMenu}>
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default HomePage;
