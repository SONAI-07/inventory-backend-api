
import { useState } from 'react';
import Dashboard from './components/Dashboard';
import Products from './components/Products';
import Customers from './components/Customers';
import Orders from './components/Orders';

export default function App() {
    const [currentTab, setCurrentTab] = useState('dashboard');

    return (
        <div className="container">
            <header>
                <h1>Inventory & Order System</h1>
                <nav>
                    <button onClick={() => setCurrentTab('dashboard')} className={currentTab === 'dashboard' ? 'active' : ''}>Dashboard</button>
                    <button onClick={() => setCurrentTab('products')} className={currentTab === 'products' ? 'active' : ''}>Products</button>
                    <button onClick={() => setCurrentTab('customers')} className={currentTab === 'customers' ? 'active' : ''}>Customers</button>
                    <button onClick={() => setCurrentTab('orders')} className={currentTab === 'orders' ? 'active' : ''}>Orders</button>
                </nav>
            </header>

            <main>
                {currentTab === 'dashboard' && <Dashboard />}
                {currentTab === 'products' && <Products />}
                {currentTab === 'customers' && <Customers />}
                {currentTab === 'orders' && <Orders />}
            </main>
        </div>
    );
}