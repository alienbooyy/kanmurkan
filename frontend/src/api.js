import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const auth = {
  login: (credentials) => api.post('/auth/login', credentials),
};

export const tables = {
  getAll: () => api.get('/tables'),
  create: (data) => api.post('/tables', data),
  update: (id, data) => api.put(`/tables/${id}`, data),
  delete: (id) => api.delete(`/tables/${id}`),
};

export const products = {
  getAll: () => api.get('/products'),
  create: (data) => api.post('/products', data),
  update: (id, data) => api.put(`/products/${id}`, data),
  delete: (id) => api.delete(`/products/${id}`),
};

export const rawMaterials = {
  getAll: () => api.get('/raw-materials'),
  create: (data) => api.post('/raw-materials', data),
  update: (id, data) => api.put(`/raw-materials/${id}`, data),
  delete: (id) => api.delete(`/raw-materials/${id}`),
};

export const recipes = {
  get: (productId) => api.get(`/products/${productId}/recipe`),
  addItem: (productId, data) => api.post(`/products/${productId}/recipe`, data),
  deleteItem: (productId, itemId) => api.delete(`/products/${productId}/recipe/${itemId}`),
};

export const orders = {
  getActiveOrder: (tableId) => api.get(`/orders/table/${tableId}`),
  create: (data) => api.post('/orders', data),
  addItem: (orderId, data) => api.post(`/orders/${orderId}/items`, data),
  removeItem: (orderId, itemId) => api.delete(`/orders/${orderId}/items/${itemId}`),
  close: (orderId) => api.post(`/orders/${orderId}/close`),
  payment: (orderId) => api.post(`/orders/${orderId}/payment`),
  splitPayment: (orderId, data) => api.post(`/orders/${orderId}/split-payment`, data),
  print: (orderId, printerType) => api.get(`/print/order/${orderId}?printer_type=${printerType}`),
};

export const reports = {
  endOfDay: (startDate, endDate) => 
    api.get('/reports/end-of-day', { params: { start_date: startDate, end_date: endDate } }),
  mostSold: () => api.get('/reports/most-sold'),
  exportExcel: (startDate, endDate) => 
    api.get('/reports/export-excel', { 
      params: { start_date: startDate, end_date: endDate },
      responseType: 'blob'
    }),
};

export default api;
