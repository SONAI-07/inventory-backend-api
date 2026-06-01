import { useState, useEffect } from 'react';
import { apiCall } from '../api';

export default function Orders() {
    const [orders, setOrders] = useState([]);
    const [products, setProducts] = useState([]);
    const [customers, setCustomers] = useState([]);
    const [form, setForm] = useState({ customer_id: '', product_id: '', quantity: 1 });
    const [message, setMessage] = useState('');
    const [expandedId, setExpandedId] = useState(null);

    const fetchData = () => {
        apiCall('/orders/').then(setOrders);
        apiCall('/products/').then(setProducts);
        apiCall('/customers/').then(setCustomers);
    };
    useEffect(() => { fetchData(); }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const payload = {
                customer_id: form.customer_id,
                items: [{ product_id: form.product_id, quantity: parseInt(form.quantity) }]
            };
            await apiCall('/orders/', 'POST', payload);
            setMessage('Order placed successfully! Stock reduced.');
            setForm({ customer_id: '', product_id: '', quantity: 1 });
            fetchData();
        } catch (err) { setMessage(`Error: ${err.message}`); }
    };

    const getCustomerName = (id) => customers.find(c => c.id === id)?.name || 'Unknown';
    const getProductName = (id) => products.find(p => p.id === id)?.name || 'Unknown';

    return (
        <div>
            <h2>Order Management</h2>
            {message && <div className="alert">{message}</div>}

            <form onSubmit={handleSubmit} className="form-grid">
                <select required value={form.customer_id} onChange={e => setForm({...form, customer_id: e.target.value})}>
                    <option value="">Select Customer...</option>
                    {customers.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                </select>
                <select required value={form.product_id} onChange={e => setForm({...form, product_id: e.target.value})}>
                    <option value="">Select Product...</option>
                    {products.map(p => <option key={p.id} value={p.id}>{p.name} (Stock: {p.stock})</option>)}
                </select>
                <input required type="number" min="1" placeholder="Qty" value={form.quantity} onChange={e => setForm({...form, quantity: e.target.value})} />
                <button type="submit">Place Order</button>
            </form>

            <table>
                <thead><tr><th>Order ID</th><th>Customer</th><th>Total</th><th>Status</th><th>Details</th></tr></thead>
                <tbody>
                {orders.map(o => (
                    <tr key={o.id}>
                        <td>{o.id.substring(0,8)}...</td>
                        <td>{getCustomerName(o.customer_id)}</td>
                        <td>${o.total_amount}</td>
                        <td>{o.status}</td>
                        <td>
                            <button onClick={() => setExpandedId(expandedId === o.id ? null : o.id)}>
                                {expandedId === o.id ? 'Hide' : 'View'}
                            </button>
                            {expandedId === o.id && (
                                <ul style={{marginTop: '10px', fontSize: '0.9em'}}>
                                    {o.items.map(item => (
                                        <li key={item.id}>{getProductName(item.product_id)} x {item.quantity} (@ ${item.unit_price} ea)</li>
                                    ))}
                                </ul>
                            )}
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
}