import { useState, useEffect } from 'react';
import { apiCall } from '../api';

export default function Dashboard() {
    const [data, setData] = useState({ products: [], customers: [], orders: [] });

    useEffect(() => {
        Promise.all([
            apiCall('/products/'), apiCall('/customers/'), apiCall('/orders/')
        ]).then(([products, customers, orders]) => {
            setData({ products, customers, orders });
        }).catch(err => console.error(err));
    }, []);

    const lowStock = data.products.filter(p => p.stock < 10);

    return (
        <div>
            <h2>System Dashboard</h2>
            <div style={{ display: 'flex', gap: '20px', marginBottom: '30px' }}>
                <div className="card"><h3>Total Products</h3><p>{data.products.length}</p></div>
                <div className="card"><h3>Total Customers</h3><p>{data.customers.length}</p></div>
                <div className="card"><h3>Total Orders</h3><p>{data.orders.length}</p></div>
            </div>

            <h3>⚠️ Low Stock Alerts (Below 10)</h3>
            {lowStock.length === 0 ? <p>All products are adequately stocked.</p> : (
                <ul>{lowStock.map(p => <li key={p.id} style={{color: 'red'}}>{p.name} - Only {p.stock} left!</li>)}</ul>
            )}
        </div>
    );
}