import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { orders, products } from '../api';
import './OrderPage.css';

function OrderPage() {
  const { tableId } = useParams();
  const navigate = useNavigate();
  const [order, setOrder] = useState(null);
  const [productsList, setProductsList] = useState([]);
  const [selectedItems, setSelectedItems] = useState([]);

  useEffect(() => {
    loadOrder();
    loadProducts();
  }, [tableId]);

  const loadOrder = async () => {
    try {
      const response = await orders.getActiveOrder(tableId);
      if (response.data) {
        setOrder(response.data);
      }
    } catch (error) {
      console.error('Failed to load order:', error);
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

  const createNewOrder = async () => {
    try {
      const response = await orders.create({ table_id: parseInt(tableId) });
      setOrder(response.data);
    } catch (error) {
      console.error('Failed to create order:', error);
    }
  };

  const addProductToOrder = async (product) => {
    try {
      if (!order) {
        await createNewOrder();
      }
      const currentOrder = order || (await orders.getActiveOrder(tableId)).data;
      await orders.addItem(currentOrder.id, {
        product_id: product.id,
        quantity: 1,
      });
      loadOrder();
    } catch (error) {
      console.error('Failed to add product:', error);
    }
  };

  const removeOrderItem = async (itemId) => {
    try {
      await orders.removeItem(order.id, itemId);
      loadOrder();
    } catch (error) {
      console.error('Failed to remove item:', error);
    }
  };

  const handleClose = () => {
    navigate('/');
  };

  const handlePayment = async () => {
    try {
      await orders.payment(order.id);
      alert('Payment received successfully!');
      navigate('/');
    } catch (error) {
      console.error('Failed to process payment:', error);
    }
  };

  const handleSplitPayment = async () => {
    if (selectedItems.length === 0) {
      alert('Please select items to pay for');
      return;
    }
    try {
      await orders.splitPayment(order.id, { order_id: order.id, item_ids: selectedItems });
      alert('Split payment processed successfully!');
      setSelectedItems([]);
      loadOrder();
    } catch (error) {
      console.error('Failed to process split payment:', error);
    }
  };

  const handlePrint = async (printerType) => {
    try {
      const response = await orders.print(order.id, printerType);
      alert(response.data.message);
    } catch (error) {
      console.error('Failed to print:', error);
    }
  };

  const toggleItemSelection = (itemId) => {
    setSelectedItems((prev) =>
      prev.includes(itemId) ? prev.filter((id) => id !== itemId) : [...prev, itemId]
    );
  };

  return (
    <div className="order-page">
      <header className="order-header">
        <button onClick={handleClose} className="btn-back">
          ← Back
        </button>
        <h1>Table {tableId} - Order Management</h1>
      </header>

      <div className="order-container">
        <div className="products-section">
          <h2>Products</h2>
          <div className="products-grid">
            {productsList.map((product) => (
              <button
                key={product.id}
                className="product-button"
                onClick={() => addProductToOrder(product)}
              >
                <span className="product-name">{product.name}</span>
                <span className="product-price">{product.price.toFixed(2)} ₺</span>
              </button>
            ))}
          </div>
        </div>

        <div className="order-section">
          <h2>Current Order</h2>
          {order && order.order_items && order.order_items.length > 0 ? (
            <>
              <div className="order-items">
                {order.order_items.map((item) => (
                  <div
                    key={item.id}
                    className={`order-item ${selectedItems.includes(item.id) ? 'selected' : ''}`}
                    onClick={() => toggleItemSelection(item.id)}
                  >
                    <div className="item-info">
                      <span className="item-name">{item.product?.name || 'Unknown'}</span>
                      <span className="item-quantity">x{item.quantity}</span>
                    </div>
                    <div className="item-actions">
                      <span className="item-price">
                        {(item.unit_price * item.quantity).toFixed(2)} ₺
                      </span>
                      <button
                        className="btn-remove"
                        onClick={(e) => {
                          e.stopPropagation();
                          removeOrderItem(item.id);
                        }}
                      >
                        ✕
                      </button>
                    </div>
                  </div>
                ))}
              </div>
              <div className="order-total">
                <strong>Total: {order.total_amount.toFixed(2)} ₺</strong>
              </div>
              <div className="order-actions">
                <button className="btn-action btn-close" onClick={handleClose}>
                  Close
                </button>
                <button className="btn-action btn-split" onClick={handleSplitPayment}>
                  Split Payment
                </button>
                <button className="btn-action btn-payment" onClick={handlePayment}>
                  Payment Received
                </button>
                <button className="btn-action btn-print" onClick={() => handlePrint('kitchen')}>
                  Print (Kitchen)
                </button>
                <button className="btn-action btn-print" onClick={() => handlePrint('oven')}>
                  Print (Oven)
                </button>
              </div>
            </>
          ) : (
            <p className="empty-order">No items in order</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default OrderPage;
