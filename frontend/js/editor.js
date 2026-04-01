// Editor JavaScript - Comprehensive room design editor

let currentDesign = null;
let selectedItem = null;
let furniture = [];
let undoStack = [];
let redoStack = [];
let currentUser = null;
let isDragging = false;
let dragStartX = 0;
let dragStartY = 0;

// Initialize editor on page load
document.addEventListener('DOMContentLoaded', async function() {
    // Get or create user
    const userResponse = await API.getOrCreateDefaultUser();
    if (userResponse.success) {
        currentUser = userResponse.user;
    }

    // Load furniture catalog
    await loadFurnitureCatalog();

    // Setup event listeners
    setupEventListeners();

    // Show room setup modal on first load
    showRoomSetup();
});

// Load all furniture items
async function loadFurnitureCatalog() {
    try {
        const response = await API.getAllFurniture();
        if (response.success) {
            furniture = response.furniture;
            displayFurnitureCatalog(furniture);
        }
    } catch (error) {
        console.error('Error loading furniture:', error);
    }
}

// Display furniture in catalog
function displayFurnitureCatalog(items) {
    const listContainer = document.getElementById('furnitureList');
    listContainer.innerHTML = '';

    items.forEach(item => {
        const card = document.createElement('div');
        card.className = 'furniture-card cursor-grab hover:shadow-lg hover:border-blue-600 transition';
        card.draggable = true;
        
        card.innerHTML = `
            <div class="furniture-card-image bg-gradient-to-br from-blue-100 to-purple-100 rounded flex items-center justify-center mb-3 h-20 text-4xl">
                ${getFurnitureIcon(item.category)}
            </div>
            <div class="furniture-card-name">${item.name}</div>
            <div class="text-xs text-gray-500 mb-2">${item.category}</div>
            <div class="furniture-card-price">$${item.price.toFixed(2)}</div>
            <div class="text-xs text-gray-500 mt-1">${item.width}ft x ${item.length}ft</div>
        `;

        card.dataset.furnitureId = item.id;
        card.dataset.furnitureName = item.name;
        card.dataset.furniturePrice = item.price;
        card.dataset.furnitureWidth = item.width;
        card.dataset.furnitureLength = item.length;
        card.dataset.furnitureHeight = item.height;
        card.dataset.furnitureImage = item.image_url;

        card.addEventListener('dragstart', handleFurnitureDragStart);
        card.addEventListener('dragend', handleFurnitureDragEnd);

        listContainer.appendChild(card);
    });
}

// Get furniture icon based on category
function getFurnitureIcon(category) {
    const icons = {
        'Beds': '🛏️',
        'Sofas': '🛋️',
        'Chairs': '🪑',
        'Tables': '📦',
        'Wardrobes': '🚪',
        'Cabinets': '🗄️',
        'Lighting': '💡',
        'Curtains': '👗',
        'Carpets': '🟫',
        'Decor': '🎨'
    };
    return icons[category] || '📦';
}

// Furniture search and filter
function setupEventListeners() {
    const searchInput = document.getElementById('furnitureSearch');
    const roomFilter = document.getElementById('roomTypeFilter');
    const newDesignBtn = document.getElementById('newDesignBtn');
    const wallColor = document.getElementById('wallColor');
    const floorColor = document.getElementById('floorColor');
    const ceilingColor = document.getElementById('ceilingColor');
    const colorPicker = document.getElementById('colorPicker');
    const aiRecommendations = document.getElementById('aiRecommendations');
    const export3d = document.getElementById('export3d');
    const exportBtn = document.getElementById('exportBtn');
    const saveBtn = document.getElementById('saveBtn');

    searchInput?.addEventListener('input', filterFurniture);
    roomFilter?.addEventListener('change', filterFurniture);
    newDesignBtn?.addEventListener('click', () => showRoomSetup());
    wallColor?.addEventListener('change', handleColorChange);
    floorColor?.addEventListener('change', handleColorChange);
    ceilingColor?.addEventListener('change', handleColorChange);
    colorPicker?.addEventListener('click', openColorPalette);
    aiRecommendations?.addEventListener('click', openAIModal);
    export3d?.addEventListener('click', () => location.href = '/3d-view');
    exportBtn?.addEventListener('click', exportDesign);
    saveBtn?.addEventListener('click', saveDesign);

    // Undo/Redo
    document.getElementById('undoBtn')?.addEventListener('click', undo);
    document.getElementById('redoBtn')?.addEventListener('click', redo);

    // Canvas drag and drop
    const canvas = document.getElementById('floorCanvas');
    canvas?.addEventListener('dragover', handleCanvasDragOver);
    canvas?.addEventListener('drop', handleCanvasDrop);
}

// Filter furniture by search and room type
function filterFurniture() {
    const search = document.getElementById('furnitureSearch')?.value.toLowerCase() || '';
    const room = document.getElementById('roomTypeFilter')?.value || '';

    const filtered = furniture.filter(item => {
        const matchSearch = item.name.toLowerCase().includes(search) || 
                          item.category.toLowerCase().includes(search);
        const matchRoom = !room || item.room_type === room;
        return matchSearch && matchRoom;
    });

    displayFurnitureCatalog(filtered);
}

// Show room setup modal
function showRoomSetup() {
    document.getElementById('roomSetupModal')?.classList.remove('hidden');
}

// Close room setup
function closeRoomSetup() {
    document.getElementById('roomSetupModal')?.classList.add('hidden');
}

// Create new design
async function createNewDesign() {
    const roomName = document.getElementById('roomName')?.value;
    const roomType = document.getElementById('roomType')?.value;
    const roomLength = parseFloat(document.getElementById('roomLength')?.value || 20);
    const roomWidth = parseFloat(document.getElementById('roomWidth')?.value || 15);
    const roomHeight = parseFloat(document.getElementById('roomHeight')?.value || 10);

    if (!roomName || !roomType) {
        alert('Please fill in all room details');
        return;
    }

    try {
        const response = await API.request('/designs/create', 'POST', {
            user_id: currentUser.id,
            room_name: roomName,
            room_type: roomType,
            room_length: roomLength,
            room_width: roomWidth,
            room_height: roomHeight
        });

        if (response.success) {
            currentDesign = response.design;
            updateRoomInfo();
            closeRoomSetup();
            redrawCanvas();
        }
    } catch (error) {
        console.error('Error creating design:', error);
    }
}

// Update room info display
function updateRoomInfo() {
    if (!currentDesign) return;

    document.getElementById('currentRoom').textContent = currentDesign.room_name;
    document.getElementById('currentSize').textContent = 
        `${currentDesign.room_length}ft x ${currentDesign.room_width}ft x ${currentDesign.room_height}ft`;
    document.getElementById('itemCount').textContent = currentDesign.items?.length || 0;
    
    const total = currentDesign.items?.reduce((sum, item) => sum + item.price, 0) || 0;
    document.getElementById('totalCost').textContent = `$${total.toFixed(2)}`;
}

// Handle furniture drag start
function handleFurnitureDragStart(e) {
    e.dataTransfer.effectAllowed = 'copy';
    e.dataTransfer.setData('furnitureId', this.dataset.furnitureId);
    e.dataTransfer.setData('furnitureName', this.dataset.furnitureName);
    e.dataTransfer.setData('furniturePrice', this.dataset.furniturePrice);
    e.dataTransfer.setData('furnitureWidth', this.dataset.furnitureWidth);
    e.dataTransfer.setData('furnitureLength', this.dataset.furnitureLength);
    e.dataTransfer.setData('furnitureImage', this.dataset.furnitureImage);
}

function handleFurnitureDragEnd(e) {
    e.dataTransfer.dropEffect = 'copy';
}

// Handle canvas drag over
function handleCanvasDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
    e.target.style.opacity = '0.8';
}

// Handle furniture drop on canvas
async function handleCanvasDrop(e) {
    e.preventDefault();
    const furnitureId = e.dataTransfer.getData('furnitureId');
    const furnitureName = e.dataTransfer.getData('furnitureName');
    const furniturePrice = parseFloat(e.dataTransfer.getData('furniturePrice'));
    const furnitureWidth = parseFloat(e.dataTransfer.getData('furnitureWidth'));
    const furnitureLength = parseFloat(e.dataTransfer.getData('furnitureLength'));

    if (!currentDesign) {
        alert('Please create a room first');
        showRoomSetup();
        return;
    }

    const canvas = document.getElementById('floorCanvas');
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    try {
        const response = await API.request(`/designs/${currentDesign.id}/add-item`, 'POST', {
            furniture_id: furnitureId,
            position_x: x,
            position_y: y,
            rotation: 0,
            scale_x: 1,
            scale_y: 1
        });

        if (response.success) {
            currentDesign = response.design;
            redrawCanvas();
            updateRoomInfo();
            saveToUndoStack();
        }
    } catch (error) {
        console.error('Error adding furniture:', error);
    }
}

// Redraw canvas with furniture items
function redrawCanvas() {
    if (!currentDesign) return;

    const canvas = document.getElementById('floorCanvas');
    const roomFloor = document.getElementById('roomFloor');

    // Update colors
    roomFloor.setAttribute('fill', currentDesign.wall_color);

    // Clear existing items
    const existingItems = canvas.querySelectorAll('.furniture-item');
    existingItems.forEach(item => item.remove());

    // Add new items
    currentDesign.items?.forEach(item => {
        addFurnitureToCanvas(item);
    });
}

// Add furniture item to canvas
function addFurnitureToCanvas(item) {
    const canvas = document.getElementById('floorCanvas');
    const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    group.setAttribute('class', 'furniture-item');
    group.setAttribute('data-item-id', item.id);
    group.setAttribute('transform', `translate(${item.position_x}, ${item.position_y}) rotate(${item.rotation})`);

    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('width', item.width * 20);
    rect.setAttribute('height', item.height * 20);
    rect.setAttribute('fill', 'rgba(59, 130, 246, 0.1)');
    rect.setAttribute('stroke', '#9ca3af');
    rect.setAttribute('stroke-width', '2');
    rect.setAttribute('rx', '4');

    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', item.width * 10);
    text.setAttribute('y', item.height * 10 + 5);
    text.setAttribute('text-anchor', 'middle');
    text.setAttribute('font-size', '12');
    text.setAttribute('fill', '#6b7280');
    text.textContent = item.furniture_name;

    group.appendChild(rect);
    group.appendChild(text);

    group.addEventListener('click', () => selectItem(item));
    group.addEventListener('mousedown', (e) => startItemDrag(e, item));

    canvas.appendChild(group);
}

// Select furniture item
function selectItem(item) {
    selectedItem = item;
    document.getElementById('selectedItemInfo').innerHTML = `
        <p><strong>Name:</strong> ${item.furniture_name}</p>
        <p><strong>Position:</strong> (${item.position_x.toFixed(0)}, ${item.position_y.toFixed(0)})</p>
        <p><strong>Size:</strong> ${item.width}ft x ${item.height}ft</p>
        <p><strong>Price:</strong> $${item.price.toFixed(2)}</p>
    `;
    document.getElementById('selectedItemControls').classList.remove('hidden');
    
    // Update canvas visualization
    const items = document.querySelectorAll('.furniture-item');
    items.forEach(el => el.classList.remove('selected'));
    document.querySelector(`[data-item-id="${item.id}"]`)?.classList.add('selected');
}

// Start dragging item
function startItemDrag(e, item) {
    if (e.button !== 0) return;
    isDragging = true;
    dragStartX = e.clientX;
    dragStartY = e.clientY;
    selectItem(item);

    const handleMove = (moveEvent) => {
        if (!isDragging) return;
        const dx = moveEvent.clientX - dragStartX;
        const dy = moveEvent.clientY - dragStartY;
        // Update position UI
    };

    const handleUp = async () => {
        isDragging = false;
        document.removeEventListener('mousemove', handleMove);
        document.removeEventListener('mouseup', handleUp);
    };

    document.addEventListener('mousemove', handleMove);
    document.addEventListener('mouseup', handleUp);
}

// Delete selected item
async function deleteSelectedItem() {
    if (!selectedItem) return;

    try {
        const response = await API.request(`/designs/item/${selectedItem.id}/remove`, 'POST');
        if (response.success) {
            currentDesign.items = currentDesign.items.filter(i => i.id !== selectedItem.id);
            selectedItem = null;
            redrawCanvas();
            updateRoomInfo();
            saveToUndoStack();
        }
    } catch (error) {
        console.error('Error deleting item:', error);
    }
}

// Handle color changes
function handleColorChange() {
    if (!currentDesign) return;

    const wallColor = document.getElementById('wallColor')?.value;
    const floorColor = document.getElementById('floorColor')?.value;
    const ceilingColor = document.getElementById('ceilingColor')?.value;

    if (wallColor || floorColor || ceilingColor) {
        updateColors(wallColor, floorColor, ceilingColor);
    }
}

// Update room colors
async function updateColors(wallColor, floorColor, ceilingColor) {
    try {
        const response = await API.request(`/designs/${currentDesign.id}/update-colors`, 'POST', {
            wall_color: wallColor || currentDesign.wall_color,
            floor_color: floorColor || currentDesign.floor_color,
            ceiling_color: ceilingColor || currentDesign.ceiling_color
        });

        if (response.success) {
            currentDesign = response.design;
            redrawCanvas();
        }
    } catch (error) {
        console.error('Error updating colors:', error);
    }
}

// Open color palette modal
function openColorPalette() {
    const modal = document.getElementById('colorPaletteModal');
    document.getElementById('paletteWallColor').value = currentDesign?.wall_color || '#FFFFFF';
    document.getElementById('paletteFloorColor').value = currentDesign?.floor_color || '#D4A574';
    document.getElementById('paletteCeilingColor').value = currentDesign?.ceiling_color || '#FFFFFF';
    modal?.classList.remove('hidden');
}

// Close color palette
function closeColorPalette() {
    document.getElementById('colorPaletteModal')?.classList.add('hidden');
}

// Apply color changes
function applyColors() {
    const wallColor = document.getElementById('paletteWallColor')?.value;
    const floorColor = document.getElementById('paletteFloorColor')?.value;
    const ceilingColor = document.getElementById('paletteCeilingColor')?.value;

    document.getElementById('wallColor').value = wallColor;
    document.getElementById('floorColor').value = floorColor;
    document.getElementById('ceilingColor').value = ceilingColor;

    updateColors(wallColor, floorColor, ceilingColor);
    closeColorPalette();
}

// Open AI recommendations modal
function openAIModal() {
    document.getElementById('aiModal')?.classList.remove('hidden');
}

// Close AI modal
function closeAIModal() {
    document.getElementById('aiModal')?.classList.add('hidden');
}

// Get AI recommendations
async function getAIRecommendations() {
    if (!currentDesign) {
        alert('Please create a room first');
        return;
    }

    const budget = parseFloat(document.getElementById('aiBudget')?.value || 5000);
    const style = document.getElementById('aiStyle')?.value || 'modern';

    try {
        const response = await API.request('/ai/recommendations', 'POST', {
            room_type: currentDesign.room_type,
            budget: budget,
            style: style
        });

        if (response.success) {
            displayAIRecommendations(response.recommendations || []);
        }
    } catch (error) {
        console.error('Error getting AI recommendations:', error);
    }
}

// Display AI recommendations
function displayAIRecommendations(recommendations) {
    const listContainer = document.getElementById('aiRecommendationsList');
    listContainer.innerHTML = '';

    if (!recommendations || recommendations.length === 0) {
        listContainer.innerHTML = '<p class="text-gray-500">No recommendations available</p>';
        return;
    }

    recommendations.forEach((rec, index) => {
        const div = document.createElement('div');
        div.className = 'bg-blue-50 p-4 rounded-lg border border-blue-200';
        div.innerHTML = `
            <h4 class="font-semibold text-gray-800">${rec.name || 'Furniture ' + (index + 1)}</h4>
            <p class="text-sm text-gray-600 mt-1">${rec.reason || 'Recommended for your space'}</p>
            ${rec.price ? `<p class="text-sm font-semibold text-green-600 mt-2">$${rec.price}</p>` : ''}
        `;
        listContainer.appendChild(div);
    });
}

// Undo functionality
function saveToUndoStack() {
    undoStack.push(JSON.parse(JSON.stringify(currentDesign)));
    redoStack = [];
}

function undo() {
    if (undoStack.length === 0) return;
    redoStack.push(JSON.parse(JSON.stringify(currentDesign)));
    currentDesign = undoStack.pop();
    redrawCanvas();
    updateRoomInfo();
}

function redo() {
    if (redoStack.length === 0) return;
    undoStack.push(JSON.parse(JSON.stringify(currentDesign)));
    currentDesign = redoStack.pop();
    redrawCanvas();
    updateRoomInfo();
}

// Save design
async function saveDesign() {
    if (!currentDesign) {
        alert('Please create a room first');
        return;
    }

    try {
        // Design is already saved via API when items are added
        alert('Design saved successfully!');
        document.getElementById('statusText').textContent = 'Design saved';
    } catch (error) {
        console.error('Error saving design:', error);
    }
}

// Export design
function exportDesign() {
    if (!currentDesign) {
        alert('No design to export');
        return;
    }

    // Export as JSON
    const dataStr = JSON.stringify(currentDesign, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `design-${currentDesign.room_name}-${new Date().getTime()}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// API helper
const API = {
    baseURL: '/api',
    
    async request(endpoint, method = 'GET', data = null) {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
            }
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, options);
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            return { error: 'Network error' };
        }
    },

    async getAllFurniture() {
        return this.request('/furniture/all', 'GET');
    },

    async getOrCreateDefaultUser() {
        return this.request('/users', 'GET');
    }
};
