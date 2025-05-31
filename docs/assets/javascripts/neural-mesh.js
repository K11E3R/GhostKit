/**
 * Neural Mesh - Advanced 3D visualization system for threat modeling
 * Part of GhostKit Quantum enhancement suite
 */

class NeuralMesh {
  constructor(canvasElement, options = {}) {
    this.canvas = canvasElement;
    this.options = Object.assign({
      nodeCount: 80,
      connectionLimit: 4,
      colors: {
        safe: 0x00ff9d,
        vulnerable: 0xff003c,
        exploited: 0xff9d00,
        background: 0x070711
      },
      animationSpeed: 1.0,
      pulseIntensity: 0.3,
      autoRotate: true,
      renderQuality: 'high'
    }, options);
    
    this.nodes = [];
    this.connections = [];
    this.attackPaths = [];
    this.exploitedNodes = new Set();
    this.breachInProgress = false;
    
    this.init();
  }
  
  init() {
    // Initialize Three.js scene
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(this.options.colors.background);
    
    // Set up camera
    this.camera = new THREE.PerspectiveCamera(
      75, 
      this.canvas.clientWidth / this.canvas.clientHeight, 
      0.1, 
      1000
    );
    this.camera.position.z = 5;
    
    // Set up renderer
    this.renderer = new THREE.WebGLRenderer({ 
      canvas: this.canvas,
      antialias: this.options.renderQuality === 'high',
      alpha: true
    });
    this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight);
    this.renderer.setPixelRatio(window.devicePixelRatio);
    
    // Add ambient light
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    this.scene.add(ambientLight);
    
    // Add point light
    const pointLight = new THREE.PointLight(0xffffff, 0.8);
    pointLight.position.set(5, 5, 5);
    this.scene.add(pointLight);
    
    // Generate mesh network
    this.generateNetwork();
    
    // Start animation loop
    this.animate();
    
    // Handle window resize
    window.addEventListener('resize', () => this.onResize());
    
    // Add click handler for node selection
    this.raycaster = new THREE.Raycaster();
    this.mouse = new THREE.Vector2();
    this.canvas.addEventListener('click', (event) => this.onCanvasClick(event));
    
    // Simulate periodic attacks
    setInterval(() => this.simulateAttack(), 8000);
  }
  
  generateNetwork() {
    // Create node objects
    for (let i = 0; i < this.options.nodeCount; i++) {
      // Node geometry based on type
      const isVulnerable = Math.random() < 0.2;
      const geometry = new THREE.SphereGeometry(
        isVulnerable ? 0.08 : 0.05, 
        16, 
        16
      );
      
      // Node material
      const material = new THREE.MeshPhongMaterial({
        color: isVulnerable ? this.options.colors.vulnerable : this.options.colors.safe,
        emissive: isVulnerable ? this.options.colors.vulnerable : this.options.colors.safe,
        emissiveIntensity: 0.3,
        transparent: true,
        opacity: 0.8,
        shininess: 30
      });
      
      // Create mesh
      const node = new THREE.Mesh(geometry, material);
      
      // Position in 3D space - cluster formation
      const angle = Math.random() * Math.PI * 2;
      const radius = 2 + Math.random() * 3;
      const height = (Math.random() - 0.5) * 4;
      
      node.position.x = Math.cos(angle) * radius;
      node.position.y = height;
      node.position.z = Math.sin(angle) * radius;
      
      // Add metadata
      node.userData = {
        id: i,
        type: isVulnerable ? 'vulnerable' : 'safe',
        connections: 0,
        pulseOffset: Math.random() * Math.PI * 2,
        exploited: false,
        importance: Math.random()
      };
      
      this.nodes.push(node);
      this.scene.add(node);
    }
    
    // Create connections between nodes
    for (let i = 0; i < this.nodes.length; i++) {
      const sourceNode = this.nodes[i];
      
      // Find nearest nodes to connect with
      const nearestNodes = this.findNearestNodes(sourceNode, this.options.connectionLimit);
      
      nearestNodes.forEach(targetIndex => {
        const targetNode = this.nodes[targetIndex];
        
        // Skip if connection already exists
        if (this.connectionExists(sourceNode.userData.id, targetNode.userData.id)) {
          return;
        }
        
        // Connection color based on vulnerability
        const isVulnerablePath = 
          sourceNode.userData.type === 'vulnerable' || 
          targetNode.userData.type === 'vulnerable';
        
        // Create line material
        const material = new THREE.LineBasicMaterial({
          color: isVulnerablePath ? this.options.colors.vulnerable : this.options.colors.safe,
          transparent: true,
          opacity: isVulnerablePath ? 0.4 : 0.2,
          linewidth: isVulnerablePath ? 2 : 1
        });
        
        // Create line geometry
        const points = [
          sourceNode.position,
          targetNode.position
        ];
        const geometry = new THREE.BufferGeometry().setFromPoints(points);
        
        // Create line and add to scene
        const connection = new THREE.Line(geometry, material);
        
        // Add metadata
        connection.userData = {
          source: sourceNode.userData.id,
          target: targetNode.userData.id,
          vulnerable: isVulnerablePath,
          active: false,
          trafficIntensity: 0
        };
        
        this.connections.push(connection);
        this.scene.add(connection);
        
        // Update node connection count
        sourceNode.userData.connections++;
        targetNode.userData.connections++;
      });
    }
    
    // Add special "core" node
    const coreGeometry = new THREE.OctahedronGeometry(0.2, 1);
    const coreMaterial = new THREE.MeshPhongMaterial({
      color: this.options.colors.safe,
      emissive: this.options.colors.safe,
      emissiveIntensity: 0.5,
      transparent: true,
      opacity: 0.9,
      shininess: 80
    });
    
    this.coreNode = new THREE.Mesh(coreGeometry, coreMaterial);
    this.coreNode.position.set(0, 0, 0);
    this.coreNode.userData = {
      id: this.nodes.length,
      type: 'core',
      connections: 0,
      pulseOffset: 0,
      exploited: false,
      importance: 1.0
    };
    
    this.nodes.push(this.coreNode);
    this.scene.add(this.coreNode);
    
    // Connect vulnerable nodes to core
    this.nodes.forEach(node => {
      if (node.userData.type === 'vulnerable' && node !== this.coreNode) {
        // Create line material
        const material = new THREE.LineBasicMaterial({
          color: this.options.colors.vulnerable,
          transparent: true,
          opacity: 0.15,
          linewidth: 1
        });
        
        // Create line geometry
        const points = [
          node.position,
          this.coreNode.position
        ];
        const geometry = new THREE.BufferGeometry().setFromPoints(points);
        
        // Create line and add to scene
        const connection = new THREE.Line(geometry, material);
        
        // Add metadata
        connection.userData = {
          source: node.userData.id,
          target: this.coreNode.userData.id,
          vulnerable: true,
          active: false,
          trafficIntensity: 0
        };
        
        this.connections.push(connection);
        this.scene.add(connection);
        
        // Update node connection count
        node.userData.connections++;
        this.coreNode.userData.connections++;
      }
    });
  }
  
  findNearestNodes(sourceNode, count) {
    const distances = [];
    
    for (let i = 0; i < this.nodes.length; i++) {
      const targetNode = this.nodes[i];
      
      // Skip if same node
      if (targetNode === sourceNode) {
        continue;
      }
      
      // Calculate distance
      const distance = sourceNode.position.distanceTo(targetNode.position);
      
      distances.push({
        index: i,
        distance: distance
      });
    }
    
    // Sort by distance
    distances.sort((a, b) => a.distance - b.distance);
    
    // Return indices of nearest nodes (limited by count)
    return distances.slice(0, count).map(d => d.index);
  }
  
  connectionExists(sourceId, targetId) {
    return this.connections.some(connection => {
      return (
        (connection.userData.source === sourceId && connection.userData.target === targetId) ||
        (connection.userData.source === targetId && connection.userData.target === sourceId)
      );
    });
  }
  
  animate() {
    requestAnimationFrame(() => this.animate());
    
    const time = Date.now() * 0.001;
    
    // Rotate scene if auto-rotate is enabled
    if (this.options.autoRotate) {
      this.scene.rotation.y = time * 0.1 * this.options.animationSpeed;
    }
    
    // Animate nodes
    this.nodes.forEach(node => {
      // Pulse effect
      const pulse = Math.sin(time + node.userData.pulseOffset) * this.options.pulseIntensity;
      const basePulse = 1 + pulse * 0.2;
      
      // Different animation for different node types
      if (node.userData.type === 'core') {
        // Core node rotates
        node.rotation.x += 0.01 * this.options.animationSpeed;
        node.rotation.y += 0.02 * this.options.animationSpeed;
        
        // Core node pulses
        node.scale.set(basePulse, basePulse, basePulse);
      } else if (node.userData.exploited) {
        // Exploited nodes pulse more dramatically
        const exploitPulse = basePulse * 1.2;
        node.scale.set(exploitPulse, exploitPulse, exploitPulse);
        
        // Exploited nodes glow more intensely
        node.material.emissiveIntensity = 0.7 + pulse * 0.3;
      } else {
        // Normal nodes have subtle pulse
        node.scale.set(basePulse, basePulse, basePulse);
        
        // Adjust emissive intensity based on pulse
        node.material.emissiveIntensity = 0.3 + pulse * 0.1;
      }
    });
    
    // Animate connections
    this.connections.forEach(connection => {
      if (connection.userData.active) {
        // Animate active connections (being used in attack)
        connection.material.opacity = 0.6 + Math.sin(time * 5) * 0.4;
        
        // Traffic animation
        connection.userData.trafficIntensity += 0.05 * this.options.animationSpeed;
        if (connection.userData.trafficIntensity > 1) {
          connection.userData.trafficIntensity = 0;
        }
      } else {
        // Normal connections
        connection.material.opacity = connection.userData.vulnerable ? 0.4 : 0.2;
      }
    });
    
    // Render scene
    this.renderer.render(this.scene, this.camera);
  }
  
  onResize() {
    // Update camera and renderer when canvas size changes
    this.camera.aspect = this.canvas.clientWidth / this.canvas.clientHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight);
  }
  
  onCanvasClick(event) {
    // Calculate mouse position in normalized device coordinates
    const rect = this.canvas.getBoundingClientRect();
    this.mouse.x = ((event.clientX - rect.left) / this.canvas.clientWidth) * 2 - 1;
    this.mouse.y = -((event.clientY - rect.top) / this.canvas.clientHeight) * 2 + 1;
    
    // Update raycaster
    this.raycaster.setFromCamera(this.mouse, this.camera);
    
    // Find intersections with nodes
    const intersects = this.raycaster.intersectObjects(this.nodes);
    
    if (intersects.length > 0) {
      const selectedNode = intersects[0].object;
      
      // Trigger node selection
      this.selectNode(selectedNode);
    }
  }
  
  selectNode(node) {
    // If we're already in a breach simulation, cancel it
    if (this.breachInProgress) {
      this.resetAttack();
      return;
    }
    
    // Only vulnerable nodes can be directly exploited
    if (node.userData.type !== 'vulnerable' && node.userData.type !== 'core') {
      return;
    }
    
    // Start breach animation from this node
    this.startAttack(node);
  }
  
  startAttack(startNode) {
    this.breachInProgress = true;
    this.exploitedNodes.clear();
    
    // Reset any active connections
    this.connections.forEach(connection => {
      connection.userData.active = false;
    });
    
    // Mark starting node as exploited
    startNode.userData.exploited = true;
    startNode.material.color.set(this.options.colors.exploited);
    startNode.material.emissive.set(this.options.colors.exploited);
    this.exploitedNodes.add(startNode.userData.id);
    
    // Start attack propagation
    this.propagateAttack(startNode);
  }
  
  propagateAttack(currentNode) {
    // Find connections from this node
    const nodeConnections = this.connections.filter(connection => {
      return (
        connection.userData.source === currentNode.userData.id ||
        connection.userData.target === currentNode.userData.id
      );
    });
    
    // Activate these connections
    nodeConnections.forEach(connection => {
      connection.userData.active = true;
      connection.material.color.set(this.options.colors.exploited);
      
      // Get the target node ID (the one that isn't the current node)
      const targetId = connection.userData.source === currentNode.userData.id
        ? connection.userData.target
        : connection.userData.source;
      
      // Skip if target already exploited
      if (this.exploitedNodes.has(targetId)) {
        return;
      }
      
      // Find the target node
      const targetNode = this.nodes.find(node => node.userData.id === targetId);
      
      // Delay before propagating to this node
      const delay = 500 + Math.random() * 1000;
      
      setTimeout(() => {
        // Mark target as exploited
        targetNode.userData.exploited = true;
        targetNode.material.color.set(this.options.colors.exploited);
        targetNode.material.emissive.set(this.options.colors.exploited);
        this.exploitedNodes.add(targetId);
        
        // Continue propagation
        this.propagateAttack(targetNode);
      }, delay);
    });
    
    // If this is the core node, trigger breach completion
    if (currentNode.userData.type === 'core') {
      setTimeout(() => {
        this.onCoreBreach();
      }, 1000);
    }
  }
  
  resetAttack() {
    this.breachInProgress = false;
    
    // Reset nodes
    this.nodes.forEach(node => {
      node.userData.exploited = false;
      
      const color = node.userData.type === 'vulnerable'
        ? this.options.colors.vulnerable
        : this.options.colors.safe;
      
      node.material.color.set(color);
      node.material.emissive.set(color);
    });
    
    // Reset connections
    this.connections.forEach(connection => {
      connection.userData.active = false;
      
      const color = connection.userData.vulnerable
        ? this.options.colors.vulnerable
        : this.options.colors.safe;
      
      connection.material.color.set(color);
    });
  }
  
  onCoreBreach() {
    // Core breach effects
    this.coreNode.material.emissiveIntensity = 1.0;
    
    // Radial shockwave effect
    const shockwave = document.createElement('div');
    shockwave.classList.add('neural-mesh-shockwave');
    this.canvas.parentNode.appendChild(shockwave);
    
    // Remove shockwave after animation
    setTimeout(() => {
      shockwave.remove();
      this.resetAttack();
    }, 2000);
  }
  
  simulateAttack() {
    // Only start a new attack if one isn't already in progress
    if (this.breachInProgress) {
      return;
    }
    
    // Find a random vulnerable node
    const vulnerableNodes = this.nodes.filter(node => 
      node.userData.type === 'vulnerable' && !node.userData.exploited
    );
    
    if (vulnerableNodes.length > 0) {
      const randomIndex = Math.floor(Math.random() * vulnerableNodes.length);
      const startNode = vulnerableNodes[randomIndex];
      
      this.startAttack(startNode);
    }
  }
}

// Initialize if window and THREE are available
document.addEventListener('DOMContentLoaded', function() {
  setTimeout(() => {
    const canvas = document.querySelector('.threat-mesh__canvas');
    if (canvas && window.THREE) {
      new NeuralMesh(canvas);
    }
  }, 2000); // Delay to ensure DOM and Three.js are fully loaded
});
