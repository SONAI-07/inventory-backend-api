import { useState, useEffect } from 'react';
import { apiCall } from '../api';

export default function Products() {
    const [products, setProducts] = useState([]);
    const [form, setForm] = useState({ name: '', sku: '', price: '', stock: '' });
    const [editingId, setEditingId] = useState(null);
    const [message, setMessage] = useState('');

    const fetchProducts = () => apiCall('/products/').then(setProducts);
    useEffect(() => { fetchProducts(); }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (editingId) {
                await apiCall(`/products/${editingId}`, 'PUT', form);
                setMessage('Product updated successfully!');
            } else {
                await apiCall('/products/', 'POST', form);
                setMessage('Product added successfully!');
            }
            setForm({ name: '', sku: '', price: '', stock: '' });
            setEditingId(null);
            fetchProducts();
        } catch (err) { setMessage(`Error: ${err.message}`); }
    };

    const handleDelete = async (id) => {
        if(confirm('Delete this product?')) {
            await apiCall(`/products/${id}`, 'DELETE');
            fetchProducts();
        }
    };

    const handleEdit = (p) => {
        setForm({ name: p.name, sku: p.sku, price: p.price, stock: p.stock });
        setEditingId(p.id);
    };

    return (
        <div>
            <h2>Product Management</h2>
            {message && <div className="alert">{message}</div>}

            <form onSubmit={handleSubmit} className="form-grid">
                <input required placeholder="Name" value={form.name} onChange={e => setForm({...form, name: e.target.value})} />
                <input required placeholder="SKU" value={form.sku} onChange={e => setForm({...form, sku: e.target.value})} />
                <input required type="number" step="0.01" min="0.01" placeholder="Price" value={form.price} onChange={e => setForm({...form, price: e.target.value})} />
                <input required type="number" min="0" placeholder="Stock" value={form.stock} onChange={e => setForm({...form, stock: e.target.value})} />
                <button type="submit">{editingId ? 'Update Product' : 'Add Product'}</button>
                {editingId && <button type="button" onClick={() => {setEditingId(null); setForm({name:'', sku:'', price:'', stock:''});}}>Cancel</button>}
            </form>

            <table>
                <thead><tr><th>Name</th><th>SKU</th><th>Price</th><th>Stock</th><th>Actions</th></tr></thead>
                <tbody>
                {products.map(p => (
                    <tr key={p.id}>
                        <td>{p.name}</td><td>{p.sku}</td><td>${p.price}</td><td>{p.stock}</td>
                        <td>
                            <button onClick={() => handleEdit(p)}>Edit</button>
                            <button onClick={() => handleDelete(p.id)} style={{background: 'red', marginLeft: '5px'}}>Delete</button>
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
}