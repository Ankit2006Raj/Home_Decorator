// 3D Viewer using Three.js

let scene, camera, renderer, room3D;
let furniture3D = [];
let controls;

// Initialize 3D viewer
function init3DViewer() {
    // Scene setup
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1a1a2e);
    scene.fog = new THREE.Fog(0x1a1a2e, 50, 100);

    // Camera setup
    camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
    );
    camera.position.set(15, 10, 15);
    camera.lookAt(0, 0, 0);

    // Renderer setup
    const canvas3d = document.getElementById('canvas3d');
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true;
    canvas3d.appendChild(renderer.domElement);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(20, 20, 10);
    directionalLight.castShadow = true;
    directionalLight.shadow.mapSize.width = 2048;
    directionalLight.shadow.mapSize.height = 2048;
    scene.add(directionalLight);

    // Create room
    createRoom();

    // Add sample furniture
    addSampleFurniture();

    // Mouse controls
    setupMouseControls();

    // Handle window resize
    window.addEventListener('resize', onWindowResize);

    // Start animation loop
    animate();
}

// Create room
function createRoom() {
    const roomLength = 20;
    const roomWidth = 15;
    const roomHeight = 10;

    // Floor
    const floorGeometry = new THREE.PlaneGeometry(roomLength, roomWidth);
    const floorMaterial = new THREE.MeshStandardMaterial({
        color: 0xD4A574,
        roughness: 0.8,
        metalness: 0
    });
    const floor = new THREE.Mesh(floorGeometry, floorMaterial);
    floor.rotation.x = -Math.PI / 2;
    floor.receiveShadow = true;
    scene.add(floor);

    // Walls
    const wallMaterial = new THREE.MeshStandardMaterial({
        color: 0xFFFFFF,
        roughness: 0.9,
        metalness: 0
    });

    // Back wall
    const backWallGeometry = new THREE.PlaneGeometry(roomLength, roomHeight);
    const backWall = new THREE.Mesh(backWallGeometry, wallMaterial);
    backWall.position.z = -roomWidth / 2;
    backWall.castShadow = true;
    backWall.receiveShadow = true;
    scene.add(backWall);

    // Front wall
    const frontWall = new THREE.Mesh(backWallGeometry, wallMaterial);
    frontWall.position.z = roomWidth / 2;
    frontWall.rotation.y = Math.PI;
    frontWall.castShadow = true;
    frontWall.receiveShadow = true;
    scene.add(frontWall);

    // Left wall
    const leftWallGeometry = new THREE.PlaneGeometry(roomWidth, roomHeight);
    const leftWall = new THREE.Mesh(leftWallGeometry, wallMaterial);
    leftWall.position.x = -roomLength / 2;
    leftWall.rotation.y = Math.PI / 2;
    leftWall.castShadow = true;
    leftWall.receiveShadow = true;
    scene.add(leftWall);

    // Right wall
    const rightWall = new THREE.Mesh(leftWallGeometry, wallMaterial);
    rightWall.position.x = roomLength / 2;
    rightWall.rotation.y = -Math.PI / 2;
    rightWall.castShadow = true;
    rightWall.receiveShadow = true;
    scene.add(rightWall);

    // Ceiling
    const ceilingGeometry = new THREE.PlaneGeometry(roomLength, roomWidth);
    const ceilingMaterial = new THREE.MeshStandardMaterial({
        color: 0xFFFFFF,
        roughness: 0.9,
        metalness: 0
    });
    const ceiling = new THREE.Mesh(ceilingGeometry, ceilingMaterial);
    ceiling.position.y = roomHeight;
    ceiling.rotation.x = Math.PI / 2;
    ceiling.receiveShadow = true;
    scene.add(ceiling);

    room3D = { floor, walls: [backWall, frontWall, leftWall, rightWall], ceiling };
}

// Add sample furniture
function addSampleFurniture() {
    // Bed
    const bed = createBed();
    bed.position.set(-5, 0, 0);
    scene.add(bed);
    furniture3D.push(bed);

    // Sofa
    const sofa = createSofa();
    sofa.position.set(5, 0, -3);
    scene.add(sofa);
    furniture3D.push(sofa);

    // Table
    const table = createTable();
    table.position.set(0, 0, 5);
    scene.add(table);
    furniture3D.push(table);

    // Chair
    const chair = createChair();
    chair.position.set(2, 0, 5);
    scene.add(chair);
    furniture3D.push(chair);
}

// Create bed model
function createBed() {
    const bed = new THREE.Group();

    // Frame
    const frameGeometry = new THREE.BoxGeometry(3, 0.5, 5);
    const frameMaterial = new THREE.MeshStandardMaterial({
        color: 0x8B4513,
        roughness: 0.7,
        metalness: 0.2
    });
    const frame = new THREE.Mesh(frameGeometry, frameMaterial);
    frame.castShadow = true;
    frame.receiveShadow = true;
    bed.add(frame);

    // Mattress
    const mattressGeometry = new THREE.BoxGeometry(2.8, 0.3, 4.8);
    const mattressMaterial = new THREE.MeshStandardMaterial({
        color: 0xDEB887,
        roughness: 0.5,
        metalness: 0
    });
    const mattress = new THREE.Mesh(mattressGeometry, mattressMaterial);
    mattress.position.y = 0.4;
    mattress.castShadow = true;
    mattress.receiveShadow = true;
    bed.add(mattress);

    return bed;
}

// Create sofa model
function createSofa() {
    const sofa = new THREE.Group();

    // Main body
    const bodyGeometry = new THREE.BoxGeometry(3, 1, 1);
    const material = new THREE.MeshStandardMaterial({
        color: 0x708090,
        roughness: 0.6,
        metalness: 0
    });
    const body = new THREE.Mesh(bodyGeometry, material);
    body.position.y = 0.5;
    body.castShadow = true;
    body.receiveShadow = true;
    sofa.add(body);

    // Backrest
    const backrestGeometry = new THREE.BoxGeometry(3, 1, 0.3);
    const backrest = new THREE.Mesh(backrestGeometry, material);
    backrest.position.set(0, 1, -0.35);
    backrest.castShadow = true;
    backrest.receiveShadow = true;
    sofa.add(backrest);

    return sofa;
}

// Create table model
function createTable() {
    const table = new THREE.Group();

    // Top
    const topGeometry = new THREE.BoxGeometry(2, 0.2, 1.2);
    const woodMaterial = new THREE.MeshStandardMaterial({
        color: 0xD2691E,
        roughness: 0.5,
        metalness: 0.1
    });
    const top = new THREE.Mesh(topGeometry, woodMaterial);
    top.position.y = 0.75;
    top.castShadow = true;
    top.receiveShadow = true;
    table.add(top);

    // Legs
    for (let i = 0; i < 4; i++) {
        const legGeometry = new THREE.BoxGeometry(0.1, 0.75, 0.1);
        const leg = new THREE.Mesh(legGeometry, woodMaterial);
        leg.position.set(
            (i % 2 === 0 ? 1 : -1) * 0.9,
            0.375,
            (i < 2 ? 1 : -1) * 0.5
        );
        leg.castShadow = true;
        leg.receiveShadow = true;
        table.add(leg);
    }

    return table;
}

// Create chair model
function createChair() {
    const chair = new THREE.Group();

    // Seat
    const seatGeometry = new THREE.BoxGeometry(0.6, 0.1, 0.6);
    const material = new THREE.MeshStandardMaterial({
        color: 0x654321,
        roughness: 0.6,
        metalness: 0.1
    });
    const seat = new THREE.Mesh(seatGeometry, material);
    seat.position.y = 0.45;
    seat.castShadow = true;
    seat.receiveShadow = true;
    chair.add(seat);

    // Back
    const backGeometry = new THREE.BoxGeometry(0.6, 0.8, 0.1);
    const back = new THREE.Mesh(backGeometry, material);
    back.position.set(0, 0.85, -0.25);
    back.castShadow = true;
    back.receiveShadow = true;
    chair.add(back);

    // Legs
    for (let i = 0; i < 4; i++) {
        const legGeometry = new THREE.BoxGeometry(0.05, 0.45, 0.05);
        const leg = new THREE.Mesh(legGeometry, material);
        leg.position.set(
            (i % 2 === 0 ? 0.25 : -0.25),
            0.225,
            (i < 2 ? 0.25 : -0.25)
        );
        leg.castShadow = true;
        leg.receiveShadow = true;
        chair.add(leg);
    }

    return chair;
}

// Setup mouse controls
function setupMouseControls() {
    let isDragging = false;
    let previousMousePosition = { x: 0, y: 0 };

    renderer.domElement.addEventListener('mousedown', (e) => {
        isDragging = true;
        previousMousePosition = { x: e.clientX, y: e.clientY };
    });

    renderer.domElement.addEventListener('mousemove', (e) => {
        if (isDragging) {
            const deltaX = e.clientX - previousMousePosition.x;
            const deltaY = e.clientY - previousMousePosition.y;

            camera.position.applyAxisAngle(
                new THREE.Vector3(0, 1, 0),
                deltaX * 0.005
            );

            const up = new THREE.Vector3(0, 1, 0);
            const right = new THREE.Vector3()
                .crossVectors(camera.getWorldDirection(new THREE.Vector3()), up)
                .normalize();

            camera.position.applyAxisAngle(right, deltaY * 0.005);
            camera.lookAt(0, 5, 0);
        }

        previousMousePosition = { x: e.clientX, y: e.clientY };
    });

    renderer.domElement.addEventListener('mouseup', () => {
        isDragging = false;
    });

    renderer.domElement.addEventListener('wheel', (e) => {
        e.preventDefault();
        const direction = camera.position.clone().normalize();
        const distance = camera.position.length();
        const newDistance = e.deltaY > 0 ? distance + 1 : distance - 1;

        if (newDistance > 5 && newDistance < 50) {
            camera.position.copy(direction.multiplyScalar(newDistance));
            camera.lookAt(0, 5, 0);
        }
    });
}

// Change view
function changeView(view) {
    const distance = 25;
    switch(view) {
        case 'iso':
            camera.position.set(distance, distance * 0.75, distance);
            break;
        case 'front':
            camera.position.set(0, 7, distance * 1.5);
            break;
        case 'top':
            camera.position.set(0, distance * 1.5, 0);
            camera.up.set(0, 0, -1);
            break;
    }
    camera.lookAt(0, 5, 0);
}

// Toggle wireframe
function toggleWireframe() {
    furniture3D.forEach(item => {
        item.traverse(child => {
            if (child.material) {
                child.material.wireframe = !child.material.wireframe;
            }
        });
    });
}

// Download screenshot
function downloadScreenshot() {
    renderer.render(scene, camera);
    const link = document.createElement('a');
    link.href = renderer.domElement.toDataURL('image/png');
    link.download = `room-${new Date().getTime()}.png`;
    link.click();
}

// Go back
function goBack() {
    location.href = '/editor';
}

// Window resize
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// Animation loop
function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}

// Initialize when page loads
window.addEventListener('load', init3DViewer);
