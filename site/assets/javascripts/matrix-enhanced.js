/**
 * GhostKit Enhanced Matrix Background System
 * Advanced cyberpunk visual effects with depth perception and adaptive density
 */

class MatrixParticleSystem {
  constructor(options = {}) {
    this.canvas = options.canvas || document.createElement('canvas');
    this.ctx = this.canvas.getContext('2d');
    this.width = options.width || window.innerWidth;
    this.height = options.height || window.innerHeight;
    this.density = options.density || 1.0; // Controls particle density
    this.speed = options.speed || 1.0; // Controls fall speed
    this.symbolSize = options.symbolSize || 14;
    this.fadeLength = options.fadeLength || 1.3; // Controls trail length
    this.layerCount = options.layerCount || 3; // Depth layers for 3D effect
    this.colorScheme = options.colorScheme || 'matrix'; // 'matrix', 'cyber', 'tactical'
    
    // Setup
    this.canvas.width = this.width;
    this.canvas.height = this.height;
    this.particles = [];
    this.lastTime = 0;
    this.symbolSet = '01GH05TK1+*><)(?/\\{}[]!@#$%^&ABCDEFJIJLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
    
    // Initialize particle system
    this.init();
    
    // Setup resize handler
    window.addEventListener('resize', () => this.resize());
  }
  
  init() {
    // Clear existing particles
    this.particles = [];
    
    // Calculate columns
    const columns = Math.floor(this.width / this.symbolSize) * this.density;
    
    // Create particles in layers for depth effect
    for (let layer = 0; layer < this.layerCount; layer++) {
      const layerSpeed = 1 + (layer / this.layerCount) * this.speed;
      const layerOpacity = 0.5 + (layer / this.layerCount) * 0.5;
      
      for (let i = 0; i < columns * (layer + 1) / this.layerCount; i++) {
        this.particles.push({
          x: Math.random() * this.width,
          y: Math.random() * this.height,
          speed: (Math.random() * 2 + 1) * layerSpeed,
          opacity: layerOpacity,
          length: Math.floor(Math.random() * 15 + 5) * this.fadeLength,
          layer: layer,
          symbols: []
        });
        
        // Pre-generate symbols for each particle
        for (let j = 0; j < 20; j++) {
          this.particles[this.particles.length - 1].symbols.push(
            this.symbolSet.charAt(Math.floor(Math.random() * this.symbolSet.length))
          );
        }
      }
    }
  }
  
  resize() {
    this.width = window.innerWidth;
    this.height = window.innerHeight;
    this.canvas.width = this.width;
    this.canvas.height = this.height;
    this.init();
  }
  
  getColor(opacity, layer) {
    switch(this.colorScheme) {
      case 'matrix':
        return `rgba(0, 255, 70, ${opacity})`;
      case 'cyber':
        return `rgba(0, ${120 + layer * 45}, ${180 + layer * 25}, ${opacity})`;
      case 'tactical':
        return `rgba(${180 + layer * 25}, ${20 + layer * 10}, ${20 + layer * 5}, ${opacity})`;
      default:
        return `rgba(0, 255, 70, ${opacity})`;
    }
  }
  
  update(deltaTime) {
    this.ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
    this.ctx.fillRect(0, 0, this.width, this.height);
    
    // Sort particles by layer for proper depth drawing
    this.particles.sort((a, b) => a.layer - b.layer);
    
    this.particles.forEach(particle => {
      // Draw the particle
      for (let i = 0; i < particle.length; i++) {
        const y = particle.y - i * this.symbolSize;
        if (y < 0) continue;
        
        // Calculate opacity based on position in the stream
        const opacity = ((particle.length - i) / particle.length) * particle.opacity;
        
        // Get symbol for this position (randomly change occasionally)
        const symbolIndex = i % particle.symbols.length;
        if (Math.random() < 0.01) {
          particle.symbols[symbolIndex] = this.symbolSet.charAt(
            Math.floor(Math.random() * this.symbolSet.length)
          );
        }
        
        // Draw the symbol
        this.ctx.fillStyle = this.getColor(opacity, particle.layer);
        this.ctx.font = `${this.symbolSize}px monospace`;
        this.ctx.fillText(
          particle.symbols[symbolIndex],
          particle.x,
          y
        );
      }
      
      // Update particle position
      particle.y += particle.speed * deltaTime * 0.05;
      
      // Reset particle if it's gone off screen
      if (particle.y - particle.length * this.symbolSize > this.height) {
        particle.y = 0;
        particle.x = Math.random() * this.width;
        // Occasionally change the length
        if (Math.random() < 0.1) {
          particle.length = Math.floor(Math.random() * 15 + 5) * this.fadeLength;
        }
      }
    });
  }
  
  animate(timestamp) {
    if (!this.lastTime) this.lastTime = timestamp;
    const deltaTime = timestamp - this.lastTime;
    this.lastTime = timestamp;
    
    this.update(deltaTime);
    requestAnimationFrame(this.animate.bind(this));
  }
  
  start() {
    this.canvas.style.position = 'fixed';
    this.canvas.style.top = '0';
    this.canvas.style.left = '0';
    this.canvas.style.width = '100%';
    this.canvas.style.height = '100%';
    this.canvas.style.zIndex = '-1';
    this.canvas.style.pointerEvents = 'none';
    
    document.body.prepend(this.canvas);
    requestAnimationFrame(this.animate.bind(this));
    
    return this;
  }
  
  // Additional methods for external control
  setDensity(density) {
    this.density = density;
    this.init();
    return this;
  }
  
  setSpeed(speed) {
    this.speed = speed;
    return this;
  }
  
  setColorScheme(scheme) {
    this.colorScheme = scheme;
    return this;
  }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  // Create global matrix instance
  window.ghostKitMatrix = new MatrixParticleSystem({
    density: 0.8,
    speed: 1.2,
    colorScheme: 'matrix'
  }).start();
  
  // Adjust matrix density based on page scroll position
  window.addEventListener('scroll', () => {
    const scrollPercent = window.scrollY / (document.body.scrollHeight - window.innerHeight);
    const newDensity = 0.6 + scrollPercent * 0.8; // Increase density as user scrolls
    window.ghostKitMatrix.setDensity(newDensity);
  });
  
  // Easter egg: keyboard sequence "ghost" changes color scheme
  let keySequence = '';
  document.addEventListener('keydown', (e) => {
    keySequence += e.key.toLowerCase();
    keySequence = keySequence.slice(-5); // Keep only last 5 keys
    
    if (keySequence === 'ghost') {
      // Cycle through color schemes
      const schemes = ['matrix', 'cyber', 'tactical'];
      const currentIndex = schemes.indexOf(window.ghostKitMatrix.colorScheme);
      const nextIndex = (currentIndex + 1) % schemes.length;
      window.ghostKitMatrix.setColorScheme(schemes[nextIndex]);
      
      // Show easter egg notification
      const notification = document.createElement('div');
      notification.textContent = `COLOR SCHEME: ${schemes[nextIndex].toUpperCase()}`;
      notification.style.position = 'fixed';
      notification.style.bottom = '20px';
      notification.style.right = '20px';
      notification.style.background = 'rgba(0,0,0,0.8)';
      notification.style.color = '#0f0';
      notification.style.padding = '10px 15px';
      notification.style.borderRadius = '5px';
      notification.style.fontFamily = 'monospace';
      notification.style.zIndex = '9999';
      notification.style.boxShadow = '0 0 10px rgba(0,255,70,0.7)';
      
      document.body.appendChild(notification);
      setTimeout(() => notification.remove(), 3000);
    }
  });
});
