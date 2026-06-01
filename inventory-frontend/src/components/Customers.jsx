import { useState, useEffect } from 'react';
import { apiCall } from '../api';

export default function Customers() {
    const [customers, setCustomers] = useState([]);
    const [form, setForm] = useState({ name: '', email: '', phone_number: '' });
    const [message, setMessage] = useState('');

    const fetchCustomers = () => apiCall('/customers/').then(setCustomers);
    useEffect(() => { fetchCustomers(); }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await apiCall('/customers/', 'POST', form);
            setMessage('Customer added successfully!');
            setForm({ name: '', email: '', phone_number: '' });
            fetchCustomers();
        } catch (err) { setMessage(`Error: ${err.message}`); }
    };

    const handleDelete = async (id) => {
        if(confirm('Delete customer?')) {
            await apiCall(`/customers/${id}`, 'DELETE');
            fetchCustomers();
        }
    };

    return (
        <div>
            <h2>Customer Management</h2>
            {message && <div className="alert">{message}</div>}

            <form onSubmit={handleSubmit} className="form-grid">
                <input required placeholder="Name" value={form.name} onChange={e => setForm({...form, name: e.target.value})} />
                <input required type="email" placeholder="Email" value={form.email} onChange={e => setForm({...form, email: e.target.value})} />
                <input required pattern="^\+?[1-9]\d{6,14}$" title="Valid phone format (e.g. +1234567890)" placeholder="Phone (+123...)" value={form.phone_number} onChange={e => setForm({...form, phone_number: e.target.value})} />
                <button type="submit">Add Customer</button>
            </form>

            <table>
                <thead><tr><th>Name</th><th>Email</th><th>Phone</th><th>Actions</th></tr></thead>
                <tbody>
                {customers.map(c => (
                    <tr key={c.id}>
                        <td>{c.name}</td><td>{c.email}</td><td>{c.phone_number}</td>
                        <td><button onClick={() => handleDelete(c.id)} style={{background: 'red'}}>Delete</button></td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
}