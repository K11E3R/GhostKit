/**
 * GhostKit Quantum JavaScript - Unhuman Level Enhancements
 * Mode 6 Reality-Bending Interface System
 */

document.addEventListener('DOMContentLoaded', function() {
  // Initialize all quantum enhancements
  initGhostProtocol();
  initNeuromorphicElements();
  initRealityDistortion();
  initDigitalTwin();
  initQuantumContent();
  initNeuralTypewriter();
  initConsciousnessInjection();
  initBiomimeticScrolling();
  initRealityBreach();
  
  // For threat mesh visualization (if canvas exists)
  setTimeout(() => {
    const threatMeshCanvas = document.querySelector('.threat-mesh__canvas');
    if (threatMeshCanvas) {
      initThreatMesh(threatMeshCanvas);
    }
  }, 1000);
});

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
 */
function initThreatMesh(canvas) {
  // Check if three.js is available (would need to be added as dependency)
  if (typeof THREE === 'undefined') {
    console.warn('THREE.js required for threat mesh visualization');
    return;
  }
  
  // Basic three.js scene setup
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
  const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true });
  
  renderer.setSize(canvas.clientWidth, canvas.clientHeight);
  camera.position.z = 5;
  
  // Create network mesh
  const nodes = [];
  const connections = [];
  
  // Generate nodes
  for (let i = 0; i < 50; i++) {
    const geometry = new THREE.SphereGeometry(0.05, 16, 16);
    const material = new THREE.MeshBasicMaterial({ 
      color: i % 5 === 0 ? 0xff003c : 0x00ff9d,
      transparent: true,
      opacity: 0.7
    });
    
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
      const targetNode = nodes[targetIndex];
      
      // Create line connecting nodes
      const material = new THREE.LineBasicMaterial({ 
        color: 0x00ff9d,
        transparent: true,
        opacity: 0.3
      });
      
      const geometry = new THREE.BufferGeometry().setFromPoints([
        sourceNode.position,
        targetNode.position
      ]);
      
      const line = new THREE.Line(geometry, material);
      connections.push(line);
      scene.add(line);
    });
  }
  
  // Helper function to find nearest nodes
  function findNearestNodes(sourceNode, allNodes, count) {
    const distances = [];
    
    for (let i = 0; i < allNodes.length; i++) {
      if (allNodes[i] === sourceNode) continue;
      
      const distance = sourceNode.position.distanceTo(allNodes[i].position);
      distances.push({ index: i, distance: distance });
    }
    
    // Sort by distance
    distances.sort((a, b) => a.distance - b.distance);
    
    // Return indices of nearest nodes
    return distances.slice(0, count).map(d => d.index);
  }
  
  // Animation loop
  function animate() {
    requestAnimationFrame(animate);
    
    // Rotate camera around scene
    const time = Date.now() * 0.0005;
    camera.position.x = Math.sin(time) * 5;
    camera.position.z = Math.cos(time) * 5;
    camera.lookAt(scene.position);
    
    // Pulse nodes
    nodes.forEach(node => {
      node.scale.x = 1 + Math.sin(time * 3 + node.position.x) * 0.3;
      node.scale.y = 1 + Math.sin(time * 3 + node.position.y) * 0.3;
      node.scale.z = 1 + Math.sin(time * 3 + node.position.z) * 0.3;
    });
    
    renderer.render(scene, camera);
  }
  
  animate();
  
  // Handle window resize
  window.addEventListener('resize', () => {
    camera.aspect = canvas.clientWidth / canvas.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(canvas.clientWidth, canvas.clientHeight);
  });
}
