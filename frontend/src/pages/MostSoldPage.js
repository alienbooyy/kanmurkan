import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { reports } from '../api';
import './MostSoldPage.css';

function MostSoldPage() {
  const [reportData, setReportData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    loadReport();
  }, []);

  const loadReport = async () => {
    try {
      const response = await reports.mostSold();
      setReportData(response.data);
    } catch (error) {
      console.error('Failed to load report:', error);
    }
  };

  return (
    <div className="most-sold-page">
      <header className="report-header">
        <button onClick={() => navigate('/')} className="btn-back">
          ← Back
        </button>
        <h1>Most Sold Items Report</h1>
      </header>

      <div className="report-container">
        {reportData && (
          <>
            <div className="report-section">
              <h2>Top Selling Products</h2>
              <div className="products-list">
                {reportData.most_sold.map(([name, stats], index) => (
                  <div key={index} className="product-stat">
                    <span className="rank">#{index + 1}</span>
                    <div className="product-info">
                      <span className="product-name">{name}</span>
                      <span className="product-details">
                        Quantity: {stats.quantity} | Revenue: {stats.revenue.toFixed(2)} ₺
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="report-section">
              <h2>Least Selling Products</h2>
              <div className="products-list">
                {reportData.least_sold.map(([name, stats], index) => (
                  <div key={index} className="product-stat">
                    <span className="rank">#{index + 1}</span>
                    <div className="product-info">
                      <span className="product-name">{name}</span>
                      <span className="product-details">
                        Quantity: {stats.quantity} | Revenue: {stats.revenue.toFixed(2)} ₺
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default MostSoldPage;
