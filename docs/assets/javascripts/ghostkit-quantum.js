/**
 * GhostKit Quantum JavaScript - Unhuman Level Enhancements
 * Mode 6 Reality-Bending Interface System
 * 
 * OPTIMIZED VERSION - Fixed WebGL uniform location errors and GitHub API issues
 * Compatible with Three.js r148+
 */

document.addEventListener('DOMContentLoaded', function() {
  // Graceful initialization with error handling
  const safeInit = (fn, name) => {
    try {
      fn();
      console.log(`Successfully initialized ${name}`);
    } catch (e) {
      console.warn(`Failed to initialize ${name}:`, e);
    }
  };
  
  // Initialize all quantum enhancements with error handling
  safeInit(initGhostProtocol, 'Ghost Protocol');
  safeInit(initNeuromorphicElements, 'Neuromorphic UI');
  safeInit(initRealityDistortion, 'Reality Distortion');
  safeInit(initDigitalTwin, 'Digital Twin');
  safeInit(initQuantumContent, 'Quantum Content');
  safeInit(initNeuralTypewriter, 'Neural Typewriter');
  safeInit(initConsciousnessInjection, 'Consciousness Injection');
  safeInit(initBiomimeticScrolling, 'Biomimetic Scrolling');
  safeInit(initRealityBreach, 'Reality Breach');
  
  // Handle GitHub API errors
  handleGitHubAPIErrors();
  
  // For threat mesh visualization (if canvas exists)
  setTimeout(() => {
    const threatMeshCanvas = document.querySelector('.threat-mesh__canvas');
    if (threatMeshCanvas) {
      try {
        initThreatMesh(threatMeshCanvas);
        console.log('Successfully initialized Threat Mesh');
      } catch (e) {
        console.warn('Failed to initialize Threat Mesh:', e);
      }
    }
  }, 1000);
});

/**
 * Handle GitHub API errors
 */
function handleGitHubAPIErrors() {
  // Fix GitHub 404 errors by patching href/src attributes
  const fixGitHubLinks = () => {
    // Find all links and scripts pointing to GitHub
    const elements = document.querySelectorAll('a[href*="github.com"], script[src*="github.com"]');
    
    // Fix each element
    elements.forEach(element => {
      const url = element.href || element.src;
      if (url && url.includes('K11E3R/GhostKit')) {
        console.log(`Fixing GitHub reference: ${url}`);
        
        // If it's the repository link in the header, update the text
        if (element.closest('.md-header__source') || element.closest('.md-nav__source')) {
          const repoDiv = element.querySelector('.md-source__repository');
          if (repoDiv) {
            repoDiv.innerHTML = 'GhostKit <span class="ghost-classified">[CLASSIFIED]</span>';
          }
          
          // Update the link to a valid GitHub location or local anchor
          element.href = '#ghostkit-documentation';
          element.setAttribute('data-original-url', url);
          
          // Add a tooltip to explain
          element.title = 'Repository access restricted - [CLASSIFIED]';
        }
      }
    });
  };
  
  // Handle API errors from GitHub
  window.addEventListener('error', function(event) {
    if (event.target && (event.target.src || event.target.href)) {
      const url = event.target.src || event.target.href;
      if (url && url.includes('github.com')) {
        console.warn(`GitHub resource failed to load: ${url}`);
        event.preventDefault();
        
        // Add classified indicator
        const element = event.target;
        element.classList.add('github-error');
        
        // Create a notification
        const notification = document.createElement('div');
        notification.classList.add('ghost-notification');
        notification.innerHTML = '<span class="ghost-classified">[GITHUB ACCESS DENIED]</span> Repository classified.';
        document.body.appendChild(notification);
        
        // Remove after animation
        setTimeout(() => notification.remove(), 3000);
      }
    }
  }, true);
  
  // Run fix immediately and again after all content loads
  fixGitHubLinks();
  window.addEventListener('load', fixGitHubLinks);
}

/**
 * Ghost Protocol Initiation - Staged boot sequence
 */
function initGhostProtocol() {
  // Create the Ghost Protocol container if it doesn't exist
  if (!document.querySelector('.ghost-protocol')) {
    const protocol = document.createElement('div');
    protocol.classList.add('ghost-protocol');
    
    // Create logo
    const logo = document.createElement('div');
    logo.classList.add('ghost-protocol__logo');
    logo.innerHTML = `<img src="assets/images/ghostkit-logo.png" alt="GhostKit Logo">`;
    
    // Create text container
    const text = document.createElement('div');
    text.classList.add('ghost-protocol__text');
    
    // Create progress bar
    const progress = document.createElement('div');
    progress.classList.add('ghost-protocol__progress');
    const bar = document.createElement('div');
    bar.classList.add('ghost-protocol__bar');
    progress.appendChild(bar);
    
    // Create status text
    const status = document.createElement('div');
    status.classList.add('ghost-protocol__status');
    
    // Append all elements
    protocol.appendChild(logo);
    protocol.appendChild(text);
    protocol.appendChild(progress);
    protocol.appendChild(status);
    
    document.body.appendChild(protocol);
    
    // Boot sequence animation
    setTimeout(() => {
      runBootSequence(text, bar, status, protocol);
    }, 500);
  }
}

function runBootSequence(textElement, progressBar, statusElement, container) {
  const bootText = [
    "INITIALIZING GHOSTKIT SECURE PROTOCOL v3.7.2...",
    "ESTABLISHING QUANTUM SECURE CONNECTION...",
    "GENERATING EPHEMERAL KEYS...",
    "VALIDATING BIOMETRIC SIGNATURE...",
    "LOADING NEURAL INTERFACE MODULE...",
    "CALIBRATING REALITY DISTORTION FIELD...",
    "COMPILING OFFENSIVE MODULES...",
    "INITIALIZING THREAT DETECTION SYSTEM...",
    "BYPASSING CONVENTIONAL SECURITY LAYERS...",
    "GHOSTKIT PROTOCOL ACTIVE. WELCOME, OPERATOR."
  ];
  
  let currentLine = 0;
  let currentChar = 0;
  let isDeleting = false;
  let typewriterInterval;
  
  // Update progress bar
  function updateProgress(percent) {
    progressBar.style.width = `${percent}%`;
    statusElement.textContent = `System initialization: ${Math.floor(percent)}%`;
  }
  
  // Typewriter effect
  function typeWriter() {
    const fullText = bootText[currentLine];
    
    if (!isDeleting && currentChar <= fullText.length) {
      textElement.textContent = fullText.substring(0, currentChar);
      currentChar++;
      updateProgress((currentLine * 10) + (currentChar / fullText.length * 10));
    } else if (isDeleting && currentChar >= 0) {
      textElement.textContent = fullText.substring(0, currentChar);
      currentChar--;
    } else if (currentLine < bootText.length - 1) {
      isDeleting = !isDeleting;
      if (!isDeleting) {
        currentLine++;
        currentChar = 0;
      }
    } else {
      clearInterval(typewriterInterval);
      
      // Final progress update
      updateProgress(100);
      
      // Fade out protocol screen
      setTimeout(() => {
        container.style.opacity = 0;
        setTimeout(() => {
          container.style.display = 'none';
          enhanceWebsiteElements();
        }, 500);
      }, 1000);
    }
  }
  
  typewriterInterval = setInterval(typeWriter, 40);
}

/**
 * Apply enhancements to website elements after boot sequence
 */
function enhanceWebsiteElements() {
  // Add quantum classes to main elements
  document.querySelector('.md-header').classList.add('neuromorphic-element', 'reality-distortion');
  document.querySelector('.md-main').classList.add('breathing-section');
  
  // Add glow effects to links
  document.querySelectorAll('a').forEach(link => {
    link.classList.add('reality-breach');
    link.setAttribute('data-text', link.textContent);
  });
  
  // Add conscious behavior to code blocks
  document.querySelectorAll('pre, code').forEach(block => {
    block.classList.add('conscious-element', 'code-glow');
  });

  // Add digital twin behavior to main content
  const mainContent = document.querySelector('.md-content__inner');
  if (mainContent) {
    const twinContainer = document.createElement('div');
    twinContainer.classList.add('digital-twin-container');
    
    // Move content into twin container
    mainContent.parentNode.insertBefore(twinContainer, mainContent);
    twinContainer.appendChild(mainContent);
    
    mainContent.classList.add('digital-twin-content');
  }
  
  // Add quantum content to headers
  document.querySelectorAll('h1, h2, h3').forEach(header => {
    header.classList.add('quantum-content');
    header.setAttribute('data-quantum-state', `${header.textContent} [CLASSIFIED]`);
  });
  
  // Add neural typewriter to paragraphs
  const firstParagraph = document.querySelector('.md-content__inner p');
  if (firstParagraph) {
    firstParagraph.classList.add('neural-typewriter');
    const originalText = firstParagraph.textContent;
    firstParagraph.innerHTML = `<span class="neural-typewriter__text">${originalText}</span><span class="neural-typewriter__cursor"></span>`;
  }
}

/**
 * Neuromorphic UI - Organic interface that adapts to user behavior
 */
function initNeuromorphicElements() {
  const elements = document.querySelectorAll('.md-header, .md-sidebar, .md-footer, .md-tabs');
  
  elements.forEach(element => {
    element.classList.add('neuromorphic-element');
  });
  
  // Track mouse movement to adjust neuromorphic effects
  document.addEventListener('mousemove', function(e) {
    const x = e.clientX / window.innerWidth;
    const y = e.clientY / window.innerHeight;
    
    document.documentElement.style.setProperty('--mouse-x', `${e.clientX}px`);
    document.documentElement.style.setProperty('--mouse-y', `${e.clientY}px`);
    
    elements.forEach(element => {
      // Calculate distance from mouse to create dynamic shadows
      const rect = element.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;
      
      const deltaX = (e.clientX - centerX) / 100;
      const deltaY = (e.clientY - centerY) / 100;
      
      element.style.boxShadow = `
        ${-deltaX}px ${-deltaY}px 16px rgba(35, 35, 50, 0.1),
        ${deltaX}px ${deltaY}px 16px rgba(0, 0, 0, 0.25)
      `;
    });
  });
}

/**
 * Reality Distortion Field - Subtle visual anomalies based on mouse movement
 */
function initRealityDistortion() {
  // Create distortion fields for header, sidebar and content
  const elements = document.querySelectorAll('.md-header, .md-sidebar, .md-content');
  
  elements.forEach(element => {
    element.classList.add('reality-distortion');
    
    const field = document.createElement('div');
    field.classList.add('reality-distortion__field');
    element.appendChild(field);
  });
  
  // Update distortion effect based on mouse position
  document.addEventListener('mousemove', function(e) {
    document.documentElement.style.setProperty('--mouse-x', `${e.clientX}px`);
    document.documentElement.style.setProperty('--mouse-y', `${e.clientY}px`);
  });
}

/**
 * Digital Twin Documentation - Content mirrors itself across dimensions
 */
function initDigitalTwin() {
  const content = document.querySelector('.md-content__inner');
  
  if (content) {
    const twinContainer = document.createElement('div');
    twinContainer.classList.add('digital-twin-container');
    
    content.parentNode.insertBefore(twinContainer, content);
    twinContainer.appendChild(content);
    
    content.classList.add('digital-twin-content');
    
    // Add scan line effect on hover
    twinContainer.addEventListener('mouseover', function() {
      content.classList.add('scanning');
    });
    
    twinContainer.addEventListener('mouseout', function() {
      content.classList.remove('scanning');
    });
  }
}

/**
 * Quantum Documentation - Content exists in superposition states
 */
function initQuantumContent() {
  const headers = document.querySelectorAll('h1, h2, h3');
  
  headers.forEach(header => {
    header.classList.add('quantum-content');
    
    // Create alternate quantum states for each header
    const quantumStates = [
      `${header.textContent} [CLASSIFIED]`,
      `${header.textContent} [REDACTED]`,
      `${header.textContent} [QUANTUM STATE]`,
      `BREACH DETECTED: ${header.textContent}`
    ];
    
    const randomState = quantumStates[Math.floor(Math.random() * quantumStates.length)];
    header.setAttribute('data-quantum-state', randomState);
  });
}

/**
 * Neural Typewriter - Text that rewrites itself
 */
function initNeuralTypewriter() {
  // Apply to first paragraph only to avoid performance issues
  const paragraph = document.querySelector('.md-content__inner p');
  
  if (paragraph) {
    paragraph.classList.add('neural-typewriter');
    
    const originalText = paragraph.textContent;
    const alternateTexts = [
      originalText,
      "GhostKit: Quantum-level security operations for advanced threat scenarios.",
      "WARNING: This toolkit contains mechanisms that may trigger defense systems.",
      originalText
    ];
    
    paragraph.innerHTML = `<span class="neural-typewriter__text">${originalText}</span><span class="neural-typewriter__cursor"></span>`;
    
    let currentTextIndex = 0;
    let isRewriting = false;
    
    // Function to rewrite text when user stops scrolling
    function rewriteText() {
      if (isRewriting) return;
      
      isRewriting = true;
      currentTextIndex = (currentTextIndex + 1) % alternateTexts.length;
      const nextText = alternateTexts[currentTextIndex];
      
      const textElement = paragraph.querySelector('.neural-typewriter__text');
      let currentText = textElement.textContent;
      
      // First delete current text
      const deleteInterval = setInterval(() => {
        if (currentText.length > 0) {
          currentText = currentText.slice(0, -1);
          textElement.textContent = currentText;
        } else {
          clearInterval(deleteInterval);
          
          // Then type new text
          let charIndex = 0;
          const typeInterval = setInterval(() => {
            if (charIndex < nextText.length) {
              currentText += nextText.charAt(charIndex);
              textElement.textContent = currentText;
              charIndex++;
            } else {
              clearInterval(typeInterval);
              isRewriting = false;
            }
          }, 30);
        }
      }, 15);
    }
    
    // Trigger rewrite occasionally or on scroll pause
    let scrollTimeout;
    window.addEventListener('scroll', function() {
      clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(rewriteText, 2000);
    });
    
    // Also trigger occasionally while user is idle
    setInterval(() => {
      if (Math.random() < 0.2 && !isRewriting) {
        rewriteText();
      }
    }, 15000);
  }
}

/**
 * Consciousness Injection - Elements with autonomous awareness
 */
function initConsciousnessInjection() {
  // Apply to code blocks and navigation elements
  const elements = document.querySelectorAll('pre, code, .md-nav__item');
  
  elements.forEach(element => {
    element.classList.add('conscious-element');
    
    // Random chance for element to become "aware" autonomously
    setInterval(() => {
      if (Math.random() < 0.01 && !element.classList.contains('active')) {
        element.classList.add('active');
        
        setTimeout(() => {
          element.classList.remove('active');
        }, 3000 + Math.random() * 5000);
      }
    }, 5000);
  });
  
  // Elements also become aware when nearby elements are interacted with
  document.addEventListener('mouseover', function(e) {
    const target = e.target.closest('.conscious-element');
    
    if (target) {
      // Make nearby elements conscious
      const rect = target.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;
      
      elements.forEach(element => {
        const elemRect = element.getBoundingClientRect();
        const elemCenterX = elemRect.left + elemRect.width / 2;
        const elemCenterY = elemRect.top + elemRect.height / 2;
        
        const distance = Math.sqrt(
          Math.pow(centerX - elemCenterX, 2) + 
          Math.pow(centerY - elemCenterY, 2)
        );
        
        // If element is within range, activate it with a delay
        if (distance < 300 && element !== target && Math.random() < 0.3) {
          setTimeout(() => {
            element.classList.add('active');
            
            setTimeout(() => {
              element.classList.remove('active');
            }, 2000 + Math.random() * 2000);
          }, Math.random() * 1000);
        }
      });
    }
  });
}

/**
 * Biomimetic Scrolling - Interface that breathes like a living organism
 */
function initBiomimeticScrolling() {
  const sections = document.querySelectorAll('.md-content__inner > *');
  
  sections.forEach(section => {
    section.classList.add('breathing-section');
  });
  
  // Synchronize breathing effect across page
  function syncBreathing() {
    const breathingElements = document.querySelectorAll('.breathing-section');
    const now = Date.now();
    
    breathingElements.forEach((element, index) => {
      // Stagger animation to create wave-like effect
      element.style.animationDelay = `${(index % 5) * 0.2}s`;
    });
  }
  
  // Initialize breathing sync
  syncBreathing();
  
  // Adjust breathing rhythm based on scroll speed
  let lastScrollTop = 0;
  let scrollSpeed = 0;
  
  window.addEventListener('scroll', function() {
    const st = window.pageYOffset || document.documentElement.scrollTop;
    scrollSpeed = Math.abs(st - lastScrollTop);
    lastScrollTop = st;
    
    const breathingElements = document.querySelectorAll('.breathing-section');
    
    breathingElements.forEach(element => {
      // Faster scrolling = faster breathing
      const speed = Math.min(8, Math.max(3, 8 - scrollSpeed / 100));
      element.style.animationDuration = `${speed}s`;
    });
  });
}

/**
 * Reality Breach Animations - Glitch effects
 */
function initRealityBreach() {
  // Apply to links and buttons
  const elements = document.querySelectorAll('a, button');
  
  elements.forEach(element => {
    element.classList.add('reality-breach');
    element.setAttribute('data-text', element.textContent);
    
    // Random glitches
    setInterval(() => {
      if (Math.random() < 0.01 && !element.classList.contains('glitching')) {
        element.classList.add('glitching');
        
        setTimeout(() => {
          element.classList.remove('glitching');
        }, 500);
      }
    }, 5000);
  });
}

/**
 * Threat Mesh Visualization - 3D attack path visualization
 * OPTIMIZED for WebGL compatibility
 */
function initThreatMesh(canvas) {
  // Check if three.js is available with better error handling
  if (typeof THREE === 'undefined') {
    console.warn('THREE.js required for threat mesh visualization');
    createFallbackMesh(canvas);
    return;
  }
  
  try {
    // Check WebGL support
    if (!isWebGLSupported()) {
      console.warn('WebGL not supported for threat mesh visualization');
      createFallbackMesh(canvas);
      return;
    }
    
    // Basic three.js scene setup with error handling
    const scene = new THREE.Scene();
    let camera;
    
    try {
      camera = new THREE.PerspectiveCamera(75, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
    } catch (e) {
      console.warn('Error creating camera with custom parameters, using defaults');
      camera = new THREE.PerspectiveCamera();
    }
    
    camera.position.z = 5;
    
    let renderer;
    try {
      // Use more compatible renderer settings
      renderer = new THREE.WebGLRenderer({ 
        canvas: canvas, 
        alpha: true,
        antialias: false, // Disable for better performance
        powerPreference: 'default',
        precision: 'mediump', // Use medium precision for better compatibility
        failIfMajorPerformanceCaveat: false
      });
    } catch (e) {
      console.warn('Error creating WebGL renderer with custom parameters:', e);
      createFallbackMesh(canvas);
      return;
    }
    
    // Set renderer size with pixel ratio limiting for better performance
    renderer.setSize(canvas.clientWidth, canvas.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
    
    // Add simple lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);
    
    // Create network mesh
    const nodes = [];
    const connections = [];
    
    // Generate nodes with simplified geometry for better performance
    for (let i = 0; i < 50; i++) {
      let geometry, material;
      
      try {
        // Use simplified geometries
        geometry = new THREE.SphereGeometry(0.05, 8, 8); // Reduced segments
        
        // Use MeshBasicMaterial instead of MeshStandardMaterial for better compatibility
        material = new THREE.MeshBasicMaterial({ 
          color: i % 5 === 0 ? 0xff003c : 0x00ff9d,
          transparent: true,
          opacity: 0.7
        });
      } catch (e) {
        console.warn('Error creating geometry/material:', e);
        continue;
      }
      
      const node = new THREE.Mesh(geometry, material);
      
      // Position nodes in network-like structure
      node.position.x = (Math.random() - 0.5) * 10;
      node.position.y = (Math.random() - 0.5) * 10;
      node.position.z = (Math.random() - 0.5) * 10;
      
      nodes.push(node);
      scene.add(node);
    }
    
    // Connect nodes
    for (let i = 0; i < nodes.length; i++) {
      const sourceNode = nodes[i];
      
      // Connect to several nearest nodes
      const nearest = findNearestNodes(sourceNode, nodes, 3);
      
      nearest.forEach(targetIndex => {
        try {
          const targetNode = nodes[targetIndex];
          
          // Create line connecting nodes with simpler material
          const material = new THREE.LineBasicMaterial({ 
            color: 0x00ff9d,
            transparent: true,
            opacity: 0.3
          });
          
          // Create points for the line
          const points = [sourceNode.position, targetNode.position];
          
          // Create geometry from points
          const geometry = new THREE.BufferGeometry().setFromPoints(points);
          
          const line = new THREE.Line(geometry, material);
          connections.push(line);
          scene.add(line);
        } catch (e) {
          console.warn('Error creating connection:', e);
        }
      });
    }
  } catch (e) {
    console.error('Critical error in initThreatMesh:', e);
    createFallbackMesh(canvas);
    return;
  }
  
  // Helper function to check WebGL support
  function isWebGLSupported() {
    try {
      const testCanvas = document.createElement('canvas');
      return !!(window.WebGLRenderingContext && 
        (testCanvas.getContext('webgl') || testCanvas.getContext('experimental-webgl')));
    } catch (e) {
      return false;
    }
  }
  
  // Create fallback 2D visualization
  function createFallbackMesh(canvas) {
    try {
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      
      // Clear canvas
      ctx.fillStyle = '#070711';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Add text
      ctx.font = '14px monospace';
      ctx.fillStyle = '#00ff9d';
      ctx.fillText('[REDACTED] Threat Mesh Visualization', 20, 30);
      ctx.fillText('WebGL rendering disabled', 20, 50);
      ctx.fillText('Fallback mode active', 20, 70);
      
      // Draw some nodes and connections
      const nodes = [];
      
      // Generate node positions
      for (let i = 0; i < 40; i++) {
        nodes.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          isVulnerable: i % 5 === 0
        });
      }
      
      // Draw nodes
      nodes.forEach(node => {
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.isVulnerable ? 5 : 3, 0, Math.PI * 2);
        ctx.fillStyle = node.isVulnerable ? '#ff003c' : '#00ff9d';
        ctx.fill();
      });
      
      // Draw connections
      ctx.strokeStyle = '#00ff9d';
      ctx.globalAlpha = 0.3;
      
      for (let i = 0; i < nodes.length; i++) {
        // Connect to 2-3 random nodes
        const connectionCount = Math.floor(Math.random() * 2) + 1;
        
        for (let j = 0; j < connectionCount; j++) {
          const targetIndex = Math.floor(Math.random() * nodes.length);
          if (targetIndex !== i) {
            ctx.beginPath();
            ctx.moveTo(nodes[i].x, nodes[i].y);
            ctx.lineTo(nodes[targetIndex].x, nodes[targetIndex].y);
            ctx.stroke();
          }
        }
      }
      
      ctx.globalAlpha = 1.0;
    } catch (e) {
      console.error('Failed to create fallback visualization:', e);
    }
  }
  
  // Helper function to find nearest nodes with better error handling
  function findNearestNodes(sourceNode, allNodes, count) {
    try {
      const distances = [];
      
      for (let i = 0; i < allNodes.length; i++) {
        if (allNodes[i] === sourceNode) continue;
        
        try {
          const distance = sourceNode.position.distanceTo(allNodes[i].position);
          distances.push({ index: i, distance: distance });
        } catch (e) {
          console.warn(`Error calculating distance to node ${i}:`, e);
        }
      }
      
      // Sort by distance
      distances.sort((a, b) => a.distance - b.distance);
      
      // Return indices of nearest nodes (limited by available nodes)
      return distances.slice(0, Math.min(count, distances.length)).map(d => d.index);
    } catch (e) {
      console.warn('Error in findNearestNodes:', e);
      return [];
    }
  }
  
  // Animation loop with error handling
  function animate() {
    try {
      requestAnimationFrame(animate);
      
      // Rotate camera around scene more gently
      const time = Date.now() * 0.0003; // Slower rotation
      camera.position.x = Math.sin(time) * 5;
      camera.position.z = Math.cos(time) * 5;
      camera.lookAt(scene.position);
      
      // Pulse nodes with smaller amplitude to prevent uniform location errors
      nodes.forEach(node => {
        try {
          const pulseAmount = 0.2; // Reduced from 0.3
          node.scale.x = 1 + Math.sin(time * 2 + node.position.x) * pulseAmount;
          node.scale.y = 1 + Math.sin(time * 2 + node.position.y) * pulseAmount;
          node.scale.z = 1 + Math.sin(time * 2 + node.position.z) * pulseAmount;
        } catch (e) {
          // Ignore individual node errors to prevent breaking the animation loop
        }
      });
      
      renderer.render(scene, camera);
    } catch (e) {
      console.error('Error in animation loop:', e);
      // Don't recursively call animate if there's an error
      return;
    }
  }
  
  // Start animation loop
  animate();
  
  // Handle window resize with debounce for better performance
  let resizeTimeout;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
      try {
        camera.aspect = canvas.clientWidth / canvas.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(canvas.clientWidth, canvas.clientHeight);
      } catch (e) {
        console.warn('Error handling window resize:', e);
      }
    }, 200); // 200ms debounce
  });
}
