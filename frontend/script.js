const API_BASE = 'http://localhost:8000';
let authToken = null;

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    loginForm.addEventListener('submit', login);
    
    const token = localStorage.getItem('authToken');
    if (token) {
        authToken = token;
        showMainApp();
        showSection('dashboard');
        loadDashboard();
    }
});

async function login(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            authToken = data.token;
            localStorage.setItem('authToken', authToken);
            showMainApp();
            showSection('dashboard');
            loadDashboard();
        } else {
            alert('Credenciais inválidas');
        }
    } catch (error) {
        console.error('Erro de login:', error);
        alert('Falha no login');
    }
}

function logout() {
    authToken = null;
    localStorage.removeItem('authToken');
    document.getElementById('main-app').style.display = 'none';
    document.getElementById('login-screen').style.display = 'flex';
}

function showMainApp() {
    document.getElementById('login-screen').style.display = 'none';
    document.getElementById('main-app').style.display = 'block';
}

function showSection(sectionName) {
    const sections = ['dashboard-section', 'shipments-section', 'vehicles-section', 'clients-section'];
    sections.forEach(section => {
        document.getElementById(section).style.display = 'none';
    });
    document.getElementById(`${sectionName}-section`).style.display = 'block';
    
    switch(sectionName) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'shipments':
            loadShipments();
            loadClientsForSelect();
            loadVehiclesForSelect();
            break;
        case 'vehicles':
            loadVehicles();
            break;
        case 'clients':
            loadClients();
            break;
    }
}

async function loadDashboard() {
    try {
        const response = await fetch(`${API_BASE}/dashboard`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        const stats = await response.json();
        displayDashboard(stats);
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

function displayDashboard(stats) {
    const container = document.getElementById('dashboard-stats');
    container.innerHTML = `
        <div class="stat-card">
            <h3>Total de Remessas</h3>
            <div class="number">${stats.shipments.total}</div>
        </div>
        <div class="stat-card">
            <h3>Pendentes</h3>
            <div class="number">${stats.shipments.pending}</div>
        </div>
        <div class="stat-card">
            <h3>Em Trânsito</h3>
            <div class="number">${stats.shipments.in_transit}</div>
        </div>
        <div class="stat-card">
            <h3>Entregues</h3>
            <div class="number">${stats.shipments.delivered}</div>
        </div>
        <div class="stat-card">
            <h3>Total de Veículos</h3>
            <div class="number">${stats.vehicles.total}</div>
        </div>
        <div class="stat-card">
            <h3>Veículos Disponíveis</h3>
            <div class="number">${stats.vehicles.available}</div>
        </div>
        <div class="stat-card">
            <h3>Total de Clientes</h3>
            <div class="number">${stats.clients.total}</div>
        </div>
    `;
}

async function loadShipments() {
    try {
        const response = await fetch(`${API_BASE}/shipments`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        const shipments = await response.json();
        displayShipments(shipments);
    } catch (error) {
        console.error('Error loading shipments:', error);
    }
}

function displayShipments(shipments) {
    const container = document.getElementById('shipments-container');
    container.innerHTML = '';
    
    shipments.forEach(shipment => {
        const card = document.createElement('div');
        card.className = 'shipment-card';
        
        const statusClass = `status-${shipment.status.toLowerCase().replace(' ', '-')}`;
        
        card.innerHTML = `
            <h3>Remessa ${shipment.id.slice(0, 8)}</h3>
            <p><strong>Origem:</strong> ${shipment.origin}</p>
            <p><strong>Destino:</strong> ${shipment.destination}</p>
            <p><strong>Cliente:</strong> ${shipment.client_id ? 'Atribuído' : 'Não atribuído'}</p>
            <p><strong>Veículo:</strong> ${shipment.vehicle_id ? 'Atribuído' : 'Não atribuído'}</p>
            <p><strong>Status:</strong> <span class="${statusClass}">${shipment.status}</span></p>
            <p><strong>Criado em:</strong> ${new Date(shipment.date_created).toLocaleString()}</p>
            <label>Atualizar Status:</label>
            <select onchange="updateStatus('${shipment.id}', this.value)">
                <option value="Pending" ${shipment.status === 'Pending' ? 'selected' : ''}>Pendente</option>
                <option value="In Transit" ${shipment.status === 'In Transit' ? 'selected' : ''}>Em Trânsito</option>
                <option value="Delivered" ${shipment.status === 'Delivered' ? 'selected' : ''}>Entregue</option>
            </select>
        `;
        
        container.appendChild(card);
    });
}

async function createShipment(event) {
    event.preventDefault();
    
    const origin = document.getElementById('origin').value;
    const destination = document.getElementById('destination').value;
    const clientId = document.getElementById('client-select').value;
    const vehicleId = document.getElementById('vehicle-select').value;
    
    try {
        const response = await fetch(`${API_BASE}/shipments`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                origin,
                destination,
                client_id: clientId || null,
                vehicle_id: vehicleId || null
            })
        });
        
        if (response.ok) {
            document.getElementById('origin').value = '';
            document.getElementById('destination').value = '';
            document.getElementById('client-select').value = '';
            document.getElementById('vehicle-select').value = '';
            loadShipments(); 
        } else {
            alert('Erro ao criar remessa');
        }
    } catch (error) {
        console.error('Erro ao criar remessa:', error);
        alert('Erro ao criar remessa');
    }
}

async function loadClientsForSelect() {
    try {
        const response = await fetch(`${API_BASE}/clients`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        const clients = await response.json();
        const select = document.getElementById('client-select');
        select.innerHTML = '<option value="">Selecionar Cliente (Opcional)</option>';
        clients.forEach(client => {
            select.innerHTML += `<option value="${client.id}">${client.name}</option>`;
        });
    } catch (error) {
        console.error('Error loading clients:', error);
    }
}

async function loadVehiclesForSelect() {
    try {
        const response = await fetch(`${API_BASE}/vehicles`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        const vehicles = await response.json();
        const select = document.getElementById('vehicle-select');
        select.innerHTML = '<option value="">Selecionar Veículo (Opcional)</option>';
        vehicles.forEach(vehicle => {
            select.innerHTML += `<option value="${vehicle.id}">${vehicle.license_plate} - ${vehicle.model}</option>`;
        });
    } catch (error) {
        console.error('Error loading vehicles:', error);
    }
}

async function updateStatus(shipmentId, newStatus) {
    try {
        const response = await fetch(`${API_BASE}/shipments/${shipmentId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ status: newStatus })
        });
        
        if (response.ok) {
            loadShipments(); 
        } else {
            alert('Erro ao atualizar status');
        }
    } catch (error) {
        console.error('Erro ao atualizar status:', error);
        alert('Erro ao atualizar status');
    }
}

async function loadVehicles() {
    try {
        const response = await fetch(`${API_BASE}/vehicles`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        const vehicles = await response.json();
        displayVehicles(vehicles);
    } catch (error) {
        console.error('Error loading vehicles:', error);
    }
}

function displayVehicles(vehicles) {
    const container = document.getElementById('vehicles-container');
    container.innerHTML = '';
    
    vehicles.forEach(vehicle => {
        const card = document.createElement('div');
        card.className = 'shipment-card';
        
        card.innerHTML = `
            <h3>${vehicle.license_plate}</h3>
            <p><strong>Modelo:</strong> ${vehicle.model}</p>
            <p><strong>Capacidade:</strong> ${vehicle.capacity}</p>
            <p><strong>Status:</strong> ${vehicle.status}</p>
            <button onclick="deleteVehicle('${vehicle.id}')">Excluir</button>
        `;
        
        container.appendChild(card);
    });
}

async function createVehicle(event) {
    event.preventDefault();
    
    const licensePlate = document.getElementById('license-plate').value;
    const model = document.getElementById('model').value;
    const capacity = document.getElementById('capacity').value;
    
    try {
        const response = await fetch(`${API_BASE}/vehicles`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ license_plate: licensePlate, model, capacity: parseInt(capacity) })
        });
        
        if (response.ok) {
            document.getElementById('license-plate').value = '';
            document.getElementById('model').value = '';
            document.getElementById('capacity').value = '';
            loadVehicles();
        } else {
            alert('Erro ao criar veículo');
        }
    } catch (error) {
        console.error('Erro ao criar veículo:', error);
        alert('Erro ao criar veículo');
    }
}

async function deleteVehicle(vehicleId) {
    try {
        const response = await fetch(`${API_BASE}/vehicles/${vehicleId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (response.ok) {
            loadVehicles();
        } else {
            alert('Erro ao excluir veículo');
        }
    } catch (error) {
        console.error('Erro ao excluir veículo:', error);
        alert('Erro ao excluir veículo');
    }
}

async function loadClients() {
    try {
        const response = await fetch(`${API_BASE}/clients`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        const clients = await response.json();
        displayClients(clients);
    } catch (error) {
        console.error('Error loading clients:', error);
    }
}

function displayClients(clients) {
    const container = document.getElementById('clients-container');
    container.innerHTML = '';
    
    clients.forEach(client => {
        const card = document.createElement('div');
        card.className = 'shipment-card';
        
        card.innerHTML = `
            <h3>${client.name}</h3>
            <p><strong>Email:</strong> ${client.email}</p>
            <p><strong>Telefone:</strong> ${client.phone}</p>
            <button onclick="deleteClient('${client.id}')">Excluir</button>
        `;
        
        container.appendChild(card);
    });
}

async function createClient(event) {
    event.preventDefault();
    
    const name = document.getElementById('client-name').value;
    const email = document.getElementById('client-email').value;
    const phone = document.getElementById('client-phone').value;
    
    try {
        const response = await fetch(`${API_BASE}/clients`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ name, email, phone })
        });
        
        if (response.ok) {
            document.getElementById('client-name').value = '';
            document.getElementById('client-email').value = '';
            document.getElementById('client-phone').value = '';
            loadClients();
        } else {
            alert('Erro ao criar cliente');
        }
    } catch (error) {
        console.error('Erro ao criar cliente:', error);
        alert('Erro ao criar cliente');
    }
}

async function deleteClient(clientId) {
    try {
        const response = await fetch(`${API_BASE}/clients/${clientId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (response.ok) {
            loadClients();
        } else {
            alert('Erro ao excluir cliente');
        }
    } catch (error) {
        console.error('Erro ao excluir cliente:', error);
        alert('Erro ao excluir cliente');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    loginForm.addEventListener('submit', login);
    
    const token = localStorage.getItem('authToken');
    if (token) {
        authToken = token;
        showMainApp();
        showSection('dashboard');
        loadDashboard();
    }
    
    document.getElementById('shipment-form').addEventListener('submit', createShipment);
    document.getElementById('vehicle-form').addEventListener('submit', createVehicle);
    document.getElementById('client-form').addEventListener('submit', createClient);
});