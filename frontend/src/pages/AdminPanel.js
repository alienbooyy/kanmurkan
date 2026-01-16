import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { tables, products, rawMaterials, recipes, reports } from '../api';
import './AdminPanel.css';

function AdminPanel() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('tables');
  const [tablesList, setTablesList] = useState([]);
  const [productsList, setProductsList] = useState([]);
  const [materialsList, setMaterialsList] = useState([]);
  const [reportData, setReportData] = useState(null);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [recipeItems, setRecipeItems] = useState([]);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  // Form states
  const [newTable, setNewTable] = useState({ table_number: '' });
  const [newProduct, setNewProduct] = useState({ name: '', price: '' });
  const [newMaterial, setNewMaterial] = useState({ name: '', unit: '', stock_quantity: '' });

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
    }
  }, [navigate]);

  useEffect(() => {
    if (activeTab === 'tables') loadTables();
    if (activeTab === 'products') loadProducts();
    if (activeTab === 'materials') loadMaterials();
    if (activeTab === 'reports') loadReport();
  }, [activeTab]);

  const loadTables = async () => {
    try {
      const response = await tables.getAll();
      setTablesList(response.data);
    } catch (error) {
      console.error('Failed to load tables:', error);
    }
  };

  const loadProducts = async () => {
    try {
      const response = await products.getAll();
      setProductsList(response.data);
    } catch (error) {
      console.error('Failed to load products:', error);
    }
  };

  const loadMaterials = async () => {
    try {
      const response = await rawMaterials.getAll();
      setMaterialsList(response.data);
    } catch (error) {
      console.error('Failed to load materials:', error);
    }
  };

  const loadReport = async () => {
    try {
      const response = await reports.endOfDay(startDate, endDate);
      setReportData(response.data);
    } catch (error) {
      console.error('Failed to load report:', error);
    }
  };

  const loadRecipe = async (productId) => {
    try {
      const response = await recipes.get(productId);
      setRecipeItems(response.data);
      setSelectedProduct(productId);
    } catch (error) {
      console.error('Failed to load recipe:', error);
    }
  };

  const handleCreateTable = async (e) => {
    e.preventDefault();
    try {
      await tables.create(newTable);
      setNewTable({ table_number: '' });
      loadTables();
    } catch (error) {
      console.error('Failed to create table:', error);
    }
  };

  const handleDeleteTable = async (id) => {
    try {
      await tables.delete(id);
      loadTables();
    } catch (error) {
      console.error('Failed to delete table:', error);
    }
  };

  const handleCreateProduct = async (e) => {
    e.preventDefault();
    try {
      await products.create(newProduct);
      setNewProduct({ name: '', price: '' });
      loadProducts();
    } catch (error) {
      console.error('Failed to create product:', error);
    }
  };

  const handleDeleteProduct = async (id) => {
    try {
      await products.delete(id);
      loadProducts();
    } catch (error) {
      console.error('Failed to delete product:', error);
    }
  };

  const handleCreateMaterial = async (e) => {
    e.preventDefault();
    try {
      await rawMaterials.create(newMaterial);
      setNewMaterial({ name: '', unit: '', stock_quantity: '' });
      loadMaterials();
    } catch (error) {
      console.error('Failed to create material:', error);
    }
  };

  const handleDeleteMaterial = async (id) => {
    try {
      await rawMaterials.delete(id);
      loadMaterials();
    } catch (error) {
      console.error('Failed to delete material:', error);
    }
  };

  const handleExportExcel = async () => {
    try {
      const response = await reports.exportExcel(startDate, endDate);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'sales_report.xlsx');
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Failed to export excel:', error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div className="admin-panel">
      <header className="admin-header">
        <h1>Admin Panel</h1>
        <div className="header-buttons">
          <button onClick={() => navigate('/')} className="btn-secondary">
            Back to Home
          </button>
          <button onClick={handleLogout} className="btn-secondary">
            Logout
          </button>
        </div>
      </header>

      <div className="admin-container">
        <div className="admin-tabs">
          <button
            className={activeTab === 'tables' ? 'tab-active' : ''}
            onClick={() => setActiveTab('tables')}
          >
            Tables
          </button>
          <button
            className={activeTab === 'products' ? 'tab-active' : ''}
            onClick={() => setActiveTab('products')}
          >
            Products
          </button>
          <button
            className={activeTab === 'materials' ? 'tab-active' : ''}
            onClick={() => setActiveTab('materials')}
          >
            Raw Materials
          </button>
          <button
            className={activeTab === 'recipes' ? 'tab-active' : ''}
            onClick={() => setActiveTab('recipes')}
          >
            Recipes
          </button>
          <button
            className={activeTab === 'reports' ? 'tab-active' : ''}
            onClick={() => setActiveTab('reports')}
          >
            Reports
          </button>
        </div>

        <div className="admin-content">
          {activeTab === 'tables' && (
            <div className="tab-content">
              <h2>Table Management</h2>
              <form onSubmit={handleCreateTable} className="admin-form">
                <input
                  type="number"
                  placeholder="Table Number"
                  value={newTable.table_number}
                  onChange={(e) => setNewTable({ table_number: e.target.value })}
                  required
                />
                <button type="submit" className="btn-primary">Add Table</button>
              </form>
              <div className="items-list">
                {tablesList.map((table) => (
                  <div key={table.id} className="item-card">
                    <span>Table {table.table_number}</span>
                    <button onClick={() => handleDeleteTable(table.id)} className="btn-delete">
                      Delete
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'products' && (
            <div className="tab-content">
              <h2>Product Management</h2>
              <form onSubmit={handleCreateProduct} className="admin-form">
                <input
                  type="text"
                  placeholder="Product Name"
                  value={newProduct.name}
                  onChange={(e) => setNewProduct({ ...newProduct, name: e.target.value })}
                  required
                />
                <input
                  type="number"
                  step="0.01"
                  placeholder="Price"
                  value={newProduct.price}
                  onChange={(e) => setNewProduct({ ...newProduct, price: e.target.value })}
                  required
                />
                <button type="submit" className="btn-primary">Add Product</button>
              </form>
              <div className="items-list">
                {productsList.map((product) => (
                  <div key={product.id} className="item-card">
                    <div>
                      <strong>{product.name}</strong>
                      <span> - {product.price} ₺</span>
                    </div>
                    <button onClick={() => handleDeleteProduct(product.id)} className="btn-delete">
                      Delete
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'materials' && (
            <div className="tab-content">
              <h2>Raw Materials Management</h2>
              <form onSubmit={handleCreateMaterial} className="admin-form">
                <input
                  type="text"
                  placeholder="Material Name"
                  value={newMaterial.name}
                  onChange={(e) => setNewMaterial({ ...newMaterial, name: e.target.value })}
                  required
                />
                <input
                  type="text"
                  placeholder="Unit (g, kg, L, piece)"
                  value={newMaterial.unit}
                  onChange={(e) => setNewMaterial({ ...newMaterial, unit: e.target.value })}
                  required
                />
                <input
                  type="number"
                  step="0.01"
                  placeholder="Stock Quantity"
                  value={newMaterial.stock_quantity}
                  onChange={(e) => setNewMaterial({ ...newMaterial, stock_quantity: e.target.value })}
                  required
                />
                <button type="submit" className="btn-primary">Add Material</button>
              </form>
              <div className="items-list">
                {materialsList.map((material) => (
                  <div key={material.id} className="item-card">
                    <div>
                      <strong>{material.name}</strong>
                      <span> - {material.stock_quantity} {material.unit}</span>
                    </div>
                    <button onClick={() => handleDeleteMaterial(material.id)} className="btn-delete">
                      Delete
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'recipes' && (
            <div className="tab-content">
              <h2>Recipe Management</h2>
              <p>Select a product to view/edit its recipe:</p>
              <div className="products-selector">
                {productsList.map((product) => (
                  <button
                    key={product.id}
                    className={selectedProduct === product.id ? 'selected' : ''}
                    onClick={() => loadRecipe(product.id)}
                  >
                    {product.name}
                  </button>
                ))}
              </div>
              {selectedProduct && (
                <div className="recipe-details">
                  <h3>Recipe Items</h3>
                  <div className="items-list">
                    {recipeItems.map((item) => (
                      <div key={item.id} className="item-card">
                        <span>Material ID: {item.raw_material_id} - Quantity: {item.quantity}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'reports' && (
            <div className="tab-content">
              <h2>End of Day Report</h2>
              <div className="date-selector">
                <input
                  type="date"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  placeholder="Start Date"
                />
                <input
                  type="date"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  placeholder="End Date"
                />
                <button onClick={loadReport} className="btn-primary">
                  Load Report
                </button>
                <button onClick={handleExportExcel} className="btn-primary">
                  Export to Excel
                </button>
              </div>
              {reportData && (
                <div className="report-summary">
                  <div className="report-card">
                    <h3>Total Revenue</h3>
                    <p className="large-number">{reportData.total_revenue.toFixed(2)} ₺</p>
                  </div>
                  <div className="report-card">
                    <h3>Total Orders</h3>
                    <p className="large-number">{reportData.total_orders}</p>
                  </div>
                  <div className="report-card full-width">
                    <h3>Product Sales Breakdown</h3>
                    <div className="product-breakdown">
                      {Object.entries(reportData.product_sales).map(([name, stats]) => (
                        <div key={name} className="breakdown-item">
                          <strong>{name}</strong>
                          <span>Quantity: {stats.quantity}</span>
                          <span>Revenue: {stats.revenue.toFixed(2)} ₺</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default AdminPanel;
