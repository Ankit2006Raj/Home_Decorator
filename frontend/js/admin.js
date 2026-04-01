// Admin Panel JavaScript

let currentTab = 'dashboard';

// Initialize admin panel
document.addEventListener('DOMContentLoaded', async function() {
    await loadDashboardData();
    setupAdminEventListeners();
});

// Setup event listeners
function setupAdminEventListeners() {
    // Tab switching
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const tab = this.getAttribute('data-tab');
            if (tab) switchTab(tab);
        });
    });
}

// Switch tab
function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.add('hidden');
    });

    // Remove active class from nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });

    // Show selected tab
    const selectedTab = document.getElementById(`${tabName}-tab`);
    if (selectedTab) {
        selectedTab.classList.remove('hidden');
    }

    // Set active nav link
    document.querySelector(`[data-tab="${tabName}"]`)?.classList.add('active');

    // Update title
    const titles = {
        'dashboard': 'Dashboard',
        'furniture': 'Furniture Catalog',
        'designs': 'Design Management',
        'users': 'User Management',
        'analytics': 'Analytics'
    };
    document.getElementById('pageTitle').textContent = titles[tabName] || 'Dashboard';

    currentTab = tabName;

    // Load tab-specific data
    if (tabName === 'furniture') {
        loadFurnitureData();
    } else if (tabName === 'designs') {
        loadDesignData();
    } else if (tabName === 'users') {
        loadUserData();
    } else if (tabName === 'analytics') {
        loadAnalyticsData();
    }
}

// Load dashboard data
async function loadDashboardData() {
    try {
        // Get stats
        const furnitureRes = await fetch('/api/furniture/all');
        const furniture = await furnitureRes.json();
        
        // Mock data for demo
        document.getElementById('totalUsersCount').textContent = '42';
        document.getElementById('totalDesignsCount').textContent = '156';
        document.getElementById('totalFurnitureCount').textContent = furniture.furniture?.length || '0';
        document.getElementById('totalRevenueCount').textContent = '$24,560.00';
        
        // Load recent activity
        loadRecentActivity();
        loadPopularRooms();
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

// Load recent activity
function loadRecentActivity() {
    const activities = [
        { user: 'John Doe', action: 'Created new design', time: '2 hours ago' },
        { user: 'Jane Smith', action: 'Updated bedroom design', time: '4 hours ago' },
        { user: 'Mike Johnson', action: 'Exported design as PDF', time: '6 hours ago' },
        { user: 'Sarah Williams', action: 'Created new design', time: '8 hours ago' },
    ];

    const container = document.getElementById('recentActivity');
    if (!container) return;

    container.innerHTML = activities.map(activity => `
        <div class="flex items-start space-x-3">
            <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-semibold">
                ${activity.user[0]}
            </div>
            <div class="flex-1">
                <p class="text-sm font-medium text-gray-900">${activity.user}</p>
                <p class="text-sm text-gray-500">${activity.action}</p>
                <p class="text-xs text-gray-400 mt-1">${activity.time}</p>
            </div>
        </div>
    `).join('');
}

// Load popular rooms
function loadPopularRooms() {
    const rooms = [
        { type: 'Bedroom', count: 45 },
        { type: 'Living Room', count: 38 },
        { type: 'Kitchen', count: 32 },
        { type: 'Office', count: 26 },
    ];

    const container = document.getElementById('popularRooms');
    if (!container) return;

    container.innerHTML = rooms.map(room => `
        <div class="flex justify-between items-center">
            <div>
                <p class="font-medium text-gray-900">${room.type}</p>
                <p class="text-sm text-gray-500">${room.count} designs</p>
            </div>
            <div class="w-20 h-2 bg-gray-200 rounded-full overflow-hidden">
                <div class="h-full bg-blue-600" style="width: ${(room.count / 45) * 100}%"></div>
            </div>
        </div>
    `).join('');
}

// Load furniture data
async function loadFurnitureData() {
    try {
        const response = await fetch('/api/furniture/all');
        const data = await response.json();
        
        const tableBody = document.getElementById('furnitureTableBody');
        if (!tableBody || !data.furniture) return;

        tableBody.innerHTML = data.furniture.slice(0, 10).map(item => `
            <tr>
                <td class="px-6 py-4">${item.name}</td>
                <td class="px-6 py-4">${item.category}</td>
                <td class="px-6 py-4">${item.room_type}</td>
                <td class="px-6 py-4">$${item.price.toFixed(2)}</td>
                <td class="px-6 py-4">
                    <div class="flex gap-2">
                        <button class="action-btn edit" onclick="editFurniture(${item.id})">
                            <i class="fas fa-edit"></i> Edit
                        </button>
                        <button class="action-btn delete" onclick="deleteFurniture(${item.id})">
                            <i class="fas fa-trash"></i> Delete
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading furniture:', error);
    }
}

// Load design data
async function loadDesignData() {
    const designsTableBody = document.getElementById('designsTableBody');
    const mockDesigns = [
        { id: 1, room_name: 'Master Bedroom', room_type: 'Bedroom', items_count: 8, cost: 3450.00, created: '2024-02-15' },
        { id: 2, room_name: 'Living Room', room_type: 'hall', items_count: 12, cost: 5600.00, created: '2024-02-10' },
        { id: 3, room_name: 'Kitchen', room_type: 'kitchen', items_count: 6, cost: 2800.00, created: '2024-02-08' },
    ];

    if (!designsTableBody) return;

    designsTableBody.innerHTML = mockDesigns.map(design => `
        <tr>
            <td class="px-6 py-4">${design.room_name}</td>
            <td class="px-6 py-4">${design.room_type}</td>
            <td class="px-6 py-4">${design.items_count}</td>
            <td class="px-6 py-4">$${design.cost.toFixed(2)}</td>
            <td class="px-6 py-4">${design.created}</td>
            <td class="px-6 py-4">
                <div class="flex gap-2">
                    <button class="action-btn view">
                        <i class="fas fa-eye"></i> View
                    </button>
                    <button class="action-btn delete">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

// Load user data
async function loadUserData() {
    const usersTableBody = document.getElementById('usersTableBody');
    const mockUsers = [
        { id: 1, username: 'johndoe', email: 'john@example.com', designs: 5, joined: '2024-01-15' },
        { id: 2, username: 'janesmith', email: 'jane@example.com', designs: 8, joined: '2024-01-20' },
        { id: 3, username: 'mikejohnson', email: 'mike@example.com', designs: 3, joined: '2024-02-01' },
    ];

    if (!usersTableBody) return;

    usersTableBody.innerHTML = mockUsers.map(user => `
        <tr>
            <td class="px-6 py-4">${user.username}</td>
            <td class="px-6 py-4">${user.email}</td>
            <td class="px-6 py-4">${user.designs}</td>
            <td class="px-6 py-4">${user.joined}</td>
        </tr>
    `).join('');
}

// Load analytics data
function loadAnalyticsData() {
    const mostUsedFurniture = [
        { name: 'Queen Bed', uses: 45 },
        { name: 'L-Shaped Sofa', uses: 38 },
        { name: 'Wooden Desk', uses: 32 },
        { name: 'Office Chair', uses: 28 },
    ];

    const popularStyles = [
        { style: 'Modern', count: 52 },
        { style: 'Classic', count: 35 },
        { style: 'Minimal', count: 28 },
    ];

    const container1 = document.getElementById('mostUsedFurniture');
    const container2 = document.getElementById('popularStyles');

    if (container1) {
        container1.innerHTML = mostUsedFurniture.map(item => `
            <div class="flex justify-between items-center">
                <span>${item.name}</span>
                <span class="font-semibold text-blue-600">${item.uses}</span>
            </div>
        `).join('');
    }

    if (container2) {
        container2.innerHTML = popularStyles.map(style => `
            <div class="flex justify-between items-center">
                <span>${style.style}</span>
                <span class="font-semibold text-blue-600">${style.count}</span>
            </div>
        `).join('');
    }
}

// Show add furniture modal
function showAddFurnitureModal() {
    document.getElementById('addFurnitureModal')?.classList.remove('hidden');
}

// Close add furniture modal
function closeAddFurnitureModal() {
    document.getElementById('addFurnitureModal')?.classList.add('hidden');
}

// Submit add furniture form
async function submitAddFurniture(event) {
    event.preventDefault();

    const name = document.getElementById('furnitureName')?.value;
    const category = document.getElementById('furnitureCategory')?.value;
    const roomType = document.getElementById('furnitureRoomType')?.value;
    const price = parseFloat(document.getElementById('furniturePrice')?.value || 0);
    const length = parseFloat(document.getElementById('furnitureLength')?.value || 1);
    const width = parseFloat(document.getElementById('furnitureWidth')?.value || 1);
    const height = parseFloat(document.getElementById('furnitureHeight')?.value || 1);

    try {
        const response = await fetch('/api/furniture/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name,
                category,
                room_type: roomType,
                price,
                length,
                width,
                height
            })
        });

        const data = await response.json();
        if (data.success) {
            alert('Furniture added successfully!');
            closeAddFurnitureModal();
            loadFurnitureData();
        }
    } catch (error) {
        console.error('Error adding furniture:', error);
    }
}

// Edit furniture item
function editFurniture(id) {
    console.log('Edit furniture:', id);
    // Implement edit functionality
}

// Delete furniture item
function deleteFurniture(id) {
    if (confirm('Are you sure you want to delete this furniture item?')) {
        console.log('Delete furniture:', id);
        // Implement delete functionality
    }
}

// Load initial data
loadDashboardData();
