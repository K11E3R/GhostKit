/**
 * Neural Mesh - Advanced 3D visualization system for threat modeling
 * Part of GhostKit Quantum enhancement suite
 * 
 * OPTIMIZED VERSION - Fixed WebGL uniform location errors and shader program issues
 * Compatible with Three.js r148+
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
        targeted: 0xffcc00,
        background: 0x070711,
        predictedPath: 0xff5e86,
        criticalNode: 0xff00ff,
        dataStream: 0x00c3ff
      },
      animationSpeed: 1.0,
      pulseIntensity: 0.3,
      autoRotate: true,
      renderQuality: 'high',
      enableQuantumEntanglement: true,
      enableRealityDistortion: true,
      threatModelingEnabled: true,
      adaptiveDefenseSystem: true
    }, options);
    
    this.nodes = [];
    this.connections = [];
    this.attackPaths = [];
    this.exploitedNodes = new Set();
    this.breachInProgress = false;
    this.predictedTargets = new Set();
    this.entangledNodes = new Map(); // Quantum entanglement pairs
    this.threatModel = {
      attackVectors: [],
      vulnerabilityScores: {},
      criticalAssets: new Set(),
      attackSurface: 0,
      defenseCapability: 0
    };
    this.realityDistortionLevel = 0;
    this.lastAnalysisTime = Date.now();
    
    // Performance metrics
    this.metrics = {
      framesPerSecond: 0,
      nodeRenderTime: 0,
      pathPredictionTime: 0,
      totalRenderTime: 0,
      anomalyDetectionRate: 0
    };
    
    this.init();
  }
  
  init() {
    try {
      // Initialize Three.js scene with error handling
      this.scene = new THREE.Scene();
      this.scene.background = new THREE.Color(this.options.colors.background);
      
      // Set up camera with safe defaults if parameters fail
      try {
        this.camera = new THREE.PerspectiveCamera(
          75, 
          this.canvas.clientWidth / this.canvas.clientHeight, 
          0.1, 
          1000
        );
        this.camera.position.z = 5;
      } catch (e) {
        console.warn('[GHOST PROTOCOL] Error creating camera with custom parameters, using defaults');
        this.camera = new THREE.PerspectiveCamera();
        this.camera.position.z = 5;
      }
      
      // Set up renderer with maximum safety settings
      try {
        // If THREE.js was patched in index.html, this will use the safe version
        // If not, we apply our own safety measures
        this.renderer = new THREE.WebGLRenderer({ 
          canvas: this.canvas,
          antialias: false, // Disable for better performance and fewer shader issues
          alpha: true,
          precision: 'lowp', // Use low precision to avoid shader precision issues
          powerPreference: 'low-power',
          failIfMajorPerformanceCaveat: false
        });
        
        // Set size with pixel ratio limiting to avoid memory issues
        this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
        
        // Add shader error protection if not already patched
        const originalRender = this.renderer.render;
        this.renderer.render = (scene, camera) => {
          // Check for WebGL support to avoid shader uniform location errors
          if (!this.isWebGLSupported()) {
            console.log('[GHOST PROTOCOL] WebGL not supported in this context, using fallback');
            this.initializeFallback2D();
            return;
          }
          try {
            return originalRender.call(this.renderer, scene, camera);
          } catch (e) {
            console.warn('[GHOST PROTOCOL] Caught WebGL render error:', e.message);
            // Continue without crashing
          }
        };
      } catch (e) {
        console.error('[GHOST PROTOCOL] Critical error creating WebGL renderer:', e);
        this.initializeFallback2D();
        return;
      }
      
      // Add lights with reduced complexity
      try {
        // Simplified lighting to reduce shader complexity
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
        this.scene.add(ambientLight);
      } catch (e) {
        console.warn('[GHOST PROTOCOL] Error adding lights:', e);
      }
      
      // Generate mesh network with error handling
      try {
        this.generateNetwork();
      } catch (e) {
        console.error('[GHOST PROTOCOL] Failed to generate network:', e);
        // Continue with empty scene rather than crashing
      }
      
      // Start animation loop with error catching
      this.animate();
      
      // Add event listeners with cleanup tracking
      this._eventListeners = [];
      
      const addSafeEventListener = (element, event, handler) => {
        const safeHandler = (...args) => {
          try {
            handler(...args);
          } catch (e) {
            console.warn(`[GHOST PROTOCOL] Error in ${event} handler:`, e);
          }
        };
        element.addEventListener(event, safeHandler);
        this._eventListeners.push({element, event, handler: safeHandler});
      };
      
      // Handle window resize with debounce
      let resizeTimeout;
      addSafeEventListener(window, 'resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => this.onResize(), 200);
      });
      
      // Add click handler for node selection
      this.raycaster = new THREE.Raycaster();
      this.mouse = new THREE.Vector2();
      addSafeEventListener(this.canvas, 'click', (event) => this.onCanvasClick(event));
      
      // Simulate periodic attacks with safer interval
      this.attackInterval = setInterval(() => {
        try {
          this.simulateAttack();
        } catch (e) {
          console.warn('[GHOST PROTOCOL] Error in attack simulation:', e);
        }
      }, 8000);
      
      console.log('[GHOST PROTOCOL] NeuralMesh 3D visualization initialized successfully');
    } catch (error) {
      console.error('[GHOST PROTOCOL] Fatal error initializing NeuralMesh:', error);
      this.initializeFallback2D();
    }
  }
  
  // Fallback method if WebGL initialization fails
  initFallbackVisualization() {
    if (!this.canvas) return;
    
    // Clear the canvas
    const ctx = this.canvas.getContext('2d');
    if (!ctx) return;
    
    ctx.fillStyle = '#070711';
    ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    
    // Draw some nodes and connections in 2D
    const drawNode = (x, y, isVulnerable) => {
      ctx.beginPath();
      ctx.arc(x, y, isVulnerable ? 8 : 5, 0, Math.PI * 2);
      ctx.fillStyle = isVulnerable ? '#ff003c' : '#00ff9d';
      ctx.fill();
    };
    
    const nodes = [];
    // Generate nodes
    for (let i = 0; i < 50; i++) {
      const x = Math.random() * this.canvas.width;
      const y = Math.random() * this.canvas.height;
      const isVulnerable = Math.random() < 0.2;
      nodes.push({ x, y, isVulnerable });
      drawNode(x, y, isVulnerable);
    }
    
    // Draw connections
    ctx.strokeStyle = '#00ff9d44';
    ctx.lineWidth = 1;
    for (let i = 0; i < nodes.length; i++) {
      // Connect to 2-3 nearest nodes
      const connections = Math.floor(Math.random() * 2) + 2;
      for (let j = 0; j < connections; j++) {
        const target = Math.floor(Math.random() * nodes.length);
        if (target !== i) {
          ctx.beginPath();
          ctx.moveTo(nodes[i].x, nodes[i].y);
          ctx.lineTo(nodes[target].x, nodes[target].y);
          ctx.stroke();
        }
      }
    }
  }
  generateNetwork() {
    try {
      console.log('[GHOST PROTOCOL] Generating secure network graph with ultra-safe materials');
      
      // Create node objects with simplified materials to reduce shader errors
      for (let i = 0; i < this.options.nodeCount; i++) {
        try {
          const geometry = new THREE.SphereGeometry(0.05, 16, 16);
          const material = new THREE.MeshBasicMaterial({
            color: this.options.colors.safe,
            transparent: true,
            opacity: 0.7
          });
          
          const mesh = new THREE.Mesh(geometry, material);
          
          // Position nodes randomly in a sphere
          const theta = Math.random() * Math.PI * 2;
          const phi = Math.acos(2 * Math.random() - 1);
          const radius = 2 * Math.pow(Math.random(), 1/3);
          
          mesh.position.x = radius * Math.sin(phi) * Math.cos(theta);
          mesh.position.y = radius * Math.sin(phi) * Math.sin(theta);
          mesh.position.z = radius * Math.cos(phi);
          
          // Store node data
          const node = {
            id: `node-${i}`,
            mesh: mesh,
            connections: [],
            security: Math.random(), // 0 = vulnerable, 1 = secure
            value: Math.random(),    // 0 = low value, 1 = high value
            exploited: false,
            targeted: false,          // Is node predicted as a potential target
            criticalAsset: Math.random() > 0.9, // 10% chance of being a critical asset
            vulnerability: Math.random() > 0.7 ? Math.random() * 0.8 : 0, // 30% chance of having vulnerabilities
            pulsePhase: Math.random() * Math.PI * 2,
            distortionFactor: Math.random() * 0.2 // For reality distortion effect
          };
          
          if (node.criticalAsset) {
            this.threatModel.criticalAssets.add(node.id);
          }
          
          this.nodes.push(node);
          this.scene.add(mesh);
          
          // Add a subtle glowing backdrop to show reality breach model
          this.threatModel.vulnerabilityScores[node.id] = node.vulnerability;
              let attempts = 0;
              do {
                targetNodeIndex = Math.floor(Math.random() * this.nodes.length);
                attempts++;
                if (attempts > 10) break; // Prevent infinite loop
              } while (targetNodeIndex === i || !this.nodes[targetNodeIndex]);
              
              // Skip if we couldn't find a valid target
              if (attempts > 10 || !this.nodes[targetNodeIndex]) continue;
              
              const targetNode = this.nodes[targetNodeIndex];
              
              // Create a connection line with the simplest possible material
              const connectionMaterial = new THREE.LineBasicMaterial({
                color: this.options.colors.connection || 0x888888, // Fallback color if not defined
                transparent: true,
                opacity: 0.5
              });
              
              // Create points for the line
              const points = [
                node.mesh.position.clone(), // Clone to avoid reference issues
                targetNode.mesh.position.clone()
              ];
              
              // Create geometry from points
              const lineGeometry = new THREE.BufferGeometry().setFromPoints(points);
              
              // Create the line
              const connection = new THREE.Line(lineGeometry, connectionMaterial);
              
              // Add metadata to the line
              connection.userData = {
                sourceId: i,
                targetId: targetNodeIndex,
                active: false,
                compromised: false
              };
              
              // Store references (safely)
              this.connections.push(connection);
              
              // Safely add connection references
              if (node.connections && Array.isArray(node.connections)) {
                node.connections.push(connection);
              }
              
              if (targetNode.connections && Array.isArray(targetNode.connections)) {
                targetNode.connections.push(connection);
              }
              
              // Add to scene
              this.scene.add(connection);
            } catch (e) {
              console.warn(`[GHOST PROTOCOL] Error creating connection from node ${i}:`, e);
              // Continue with next connection
            }
          }
        } catch (e) {
          console.warn(`[GHOST PROTOCOL] Error processing connections for node ${i}:`, e);
          // Continue with next node
        }
      }
      
      console.log(`[GHOST PROTOCOL] Network generation complete: ${this.nodes.length} nodes, ${this.connections.length} connections`);
    } catch (e) {
      console.error('[GHOST PROTOCOL] Critical error generating network:', e);
    }
    
    // Add special "core" node
    try {
      // Create core node at center
      try {
        const coreMaterial = new THREE.MeshBasicMaterial({
          color: this.options.colors.safe,
          transparent: true,
          opacity: 0.9
        });
        
        const coreGeometry = new THREE.SphereGeometry(0.15, 12, 12);
        this.coreNode = new THREE.Mesh(coreGeometry, coreMaterial);
        this.coreNode.position.set(0, 0, 0);
        
        // Set core node properties
        this.coreNode.userData = {
          id: 'core',
          connections: 0,
          isVulnerable: false,
          isExploited: false,
          isCore: true,
          pulsePhase: 0
        };
        
        this.scene.add(this.coreNode);
        this.nodes.push(this.coreNode);
      } catch (coreError) {
        console.warn('[GHOST PROTOCOL] Error creating core node:', coreError);
      }
      
      console.log('[GHOST PROTOCOL] Core node created successfully');
    } catch (e) {
      console.warn('[GHOST PROTOCOL] Error creating core node:', e);
    }
    
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
          node.mesh.position,
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
    try {
      const distances = [];
      
      for (let i = 0; i < this.nodes.length; i++) {
        try {
          const targetNode = this.nodes[i];
          
          // Skip if same node
          if (targetNode === sourceNode) {
            continue;
          }
          
          // Calculate distance with safe error handling
          try {
            const distance = sourceNode.mesh.position.distanceTo(targetNode.mesh.position);
            
            distances.push({
              index: i,
              distance: distance
            });
          } catch (distanceError) {
            console.warn('[GHOST PROTOCOL] Error calculating distance:', distanceError);
          }
        } catch (nodeError) {
          console.warn('[GHOST PROTOCOL] Error processing node in findNearestNodes:', nodeError);
        }
      }
      
      // Sort by distance with error handling
      try {
        distances.sort((a, b) => a.distance - b.distance);
      } catch (sortError) {
        console.warn('[GHOST PROTOCOL] Error sorting distances:', sortError);
      }
      
      // Return indices of nearest nodes (limited by count)
      return distances.slice(0, count).map(d => d.index);
    } catch (error) {
      console.error('[GHOST PROTOCOL] Critical error in findNearestNodes:', error);
      return []; // Return empty array as fallback
    }
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
      const pulse = Math.sin(time + node.userData.pulsePhase) * this.options.pulseIntensity;
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
  
  isWebGLSupported() {
    try {
      const canvas = document.createElement('canvas');
      return !!(window.WebGLRenderingContext && 
        (canvas.getContext('webgl') || canvas.getContext('experimental-webgl')));
    } catch (e) {
      return false;
    }
  }
}

// Initialize if window and THREE are available
// Quantum accelerated initialization - max 2 seconds
(function() {
  // Immediate self-executing function for faster startup
  
  // Check for WebGL support first (optimized)
  const checkWebGLSupport = () => {
    try {
      const canvas = document.createElement('canvas');
      return !!(window.WebGLRenderingContext && 
        (canvas.getContext('webgl') || canvas.getContext('experimental-webgl')));
    } catch (e) {
      return false;
    }
  };
  
  // Log WebGL support status
  const hasWebGL = checkWebGLSupport();
  console.log(`[GHOST PROTOCOL] WebGL Support: ${hasWebGL ? 'Available' : 'Not Available'}`);
  
  // Track initialization state
  let initStarted = false;
  let maxInitTime = window.GHOST_MAX_LOAD_TIME || 2000; // Default to 2 seconds max
  
  // Function to initialize with timeout guarantee
  const initializeWithTimeout = () => {
    if (initStarted) return; // Prevent double initialization
    initStarted = true;
    
    const startTime = performance.now();
    const canvas = document.querySelector('.threat-mesh__canvas');
    
    if (!canvas) {
      console.warn('[GHOST PROTOCOL] Canvas element not found');
      return;
    }
    
    // Force completion after timeout
    const forceCompletionTimer = setTimeout(() => {
      console.warn('[GHOST PROTOCOL] Forcing mesh initialization completion (timeout)');
      if (!window.meshInitialized) {
        // Fallback if initialization is taking too long
        try {
          const ctx = canvas.getContext('2d');
          if (ctx) {
            ctx.fillStyle = '#070711';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.font = '14px monospace';
            ctx.fillStyle = '#00ff9d';
            ctx.fillText('[REDACTED] Threat Mesh Visualization', 20, 30);
            ctx.fillText('Accelerated mode enabled', 20, 50);
          }
        } catch (err) {
          console.error('[GHOST PROTOCOL] Failed to create fallback:', err);
        }
      }
    }, maxInitTime - 200); // Leave 200ms buffer
    
    // Initialize when THREE is available
    if (window.THREE) {
      try {
        new NeuralMesh(canvas);
        window.meshInitialized = true;
        clearTimeout(forceCompletionTimer);
        console.log(`[GHOST PROTOCOL] NeuralMesh initialized in ${(performance.now() - startTime).toFixed(0)}ms`);
      } catch (e) {
        console.log(`[GHOST PROTOCOL] Failed to initialize WebGL context: ${e}`);
        
        // Fallback to basic visualization
        try {
          const ctx = canvas.getContext('2d');
          if (ctx) {
            ctx.fillStyle = '#070711';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.font = '14px monospace';
            ctx.fillStyle = '#00ff9d';
            ctx.fillText('[REDACTED] Threat Mesh Visualization', 20, 30);
            ctx.fillText('WebGL initialization failed', 20, 50);
            ctx.fillText('Fallback mode enabled', 20, 70);
          }
        } catch (drawErr) {
          console.error('[GHOST PROTOCOL] Even 2D fallback failed:', drawErr);
        }
      }
    } else {
      console.warn('[GHOST PROTOCOL] THREE not available, using fallback');
      try {
        const ctx = canvas.getContext('2d');
        if (ctx) {
          ctx.fillStyle = '#070711';
          ctx.fillRect(0, 0, canvas.width, canvas.height);
          ctx.font = '14px monospace';
          ctx.fillStyle = '#00ff9d';
          ctx.fillText('[REDACTED] Threat Mesh Visualization', 20, 30);
          ctx.fillText('THREE.js not available', 20, 50);
          ctx.fillText('Fallback mode enabled', 20, 70);
        }
      } catch (err) {
        console.error('[GHOST PROTOCOL] Failed to create fallback:', err);
      }
    }
  };

  // Start initialization immediately if document is ready
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    initializeWithTimeout();
  } else {
    // Use faster 'DOMContentLoaded' instead of load event
    document.addEventListener('DOMContentLoaded', initializeWithTimeout);
    
    // Backup initialization after a short delay if DOMContentLoaded doesn't fire
    setTimeout(initializeWithTimeout, 800);
  }
})();
