/**
 * GhostKit Tactical Enhancement System
 * Master loader that integrates all cyberpunk UI enhancements
 */

class GhostKitTactical {
  constructor() {
    this.isInitialized = false;
    this.features = {
      matrix: true,
      terminal: true,
      visualizer: true,
      effects: true,
      sound: false // Default off to avoid surprising users
    };
    
    // Initialize when DOM is loaded
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.initialize());
    } else {
      this.initialize();
    }
  }
  
  initialize() {
    if (this.isInitialized) return;
    this.isInitialized = true;
    
    console.log('🔮 GhostKit Tactical UI System Initializing...');
    
    // Add tactical CSS overrides
    this.injectStyles();
    
    // Initialize components
    this.initializeComponents();
    
    // Apply code highlighting enhancements
    this.enhanceCodeBlocks();
    
    // Add sound toggle in footer
    this.addSoundToggle();
    
    // Add cyberpunk header animation
    this.addHeaderAnimation();
    
    // Handle user preferences
    this.loadUserPreferences();
    
    console.log('🔮 GhostKit Tactical UI System Ready');
  }
  
  injectStyles() {
    const style = document.createElement('style');
    style.textContent = `
      /* GhostKit Tactical UI Overrides */
      :root {
        --md-primary-fg-color: #1a1a1a;
        --md-primary-fg-color--light: #303030;
        --md-primary-fg-color--dark: #0f0f0f;
        --md-accent-fg-color: #00ff66;
        --md-typeset-a-color: #00cc66;
      }
      
      /* Cyberpunk aesthetic overrides */
      body {
        background-color: #0a0a0a !important;
        color: #e0e0e0 !important;
      }
      
      /* Neon text effects */
      .md-header__topic {
        text-shadow: 0 0 5px rgba(0, 255, 102, 0.8) !important;
      }
      
      .md-nav__title {
        color: #00ff66 !important;
        text-shadow: 0 0 5px rgba(0, 255, 102, 0.5) !important;
      }
      
      h1, h2, h3, h4, h5, h6 {
        color: #00ff99 !important;
        text-shadow: 0 0 8px rgba(0, 255, 102, 0.5) !important;
      }
      
      /* Tactical borders and separators */
      .md-main {
        background: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.95));
      }
      
      .md-sidebar {
        background-color: rgba(0, 0, 0, 0.7) !important;
        backdrop-filter: blur(5px);
      }
      
      .md-nav {
        background-color: transparent !important;
      }
      
      /* Code blocks */
      .highlight pre {
        background-color: rgba(0, 20, 10, 0.7) !important;
        border: 1px solid rgba(0, 255, 102, 0.3) !important;
        box-shadow: 0 0 10px rgba(0, 255, 102, 0.2) !important;
      }
      
      /* Glowing buttons */
      .md-button {
        background-color: rgba(0, 50, 20, 0.5) !important;
        border: 1px solid rgba(0, 255, 102, 0.5) !important;
        color: #00ff66 !important;
        text-shadow: 0 0 5px rgba(0, 255, 102, 0.5) !important;
        transition: all 0.3s ease !important;
      }
      
      .md-button:hover {
        background-color: rgba(0, 80, 40, 0.7) !important;
        box-shadow: 0 0 15px rgba(0, 255, 102, 0.7) !important;
        transform: translateY(-2px) !important;
      }
      
      /* Terminal demo containers */
      .terminal-demo {
        margin: 20px 0;
        border-radius: 5px;
        overflow: hidden;
      }
      
      /* Visualization containers */
      .cyber-viz {
        margin: 20px 0;
        border-radius: 5px;
        overflow: hidden;
      }
      
      /* Glow effect on hover for navigation */
      .md-nav__link:hover {
        color: #00ff66 !important;
        text-shadow: 0 0 8px rgba(0, 255, 102, 0.8) !important;
      }
      
      /* Animated footer */
      .md-footer {
        background: linear-gradient(90deg, #0a0a0a, #0a1a0a, #0a0a0a) !important;
        background-size: 600% 600% !important;
        animation: gradientShift 10s ease infinite !important;
      }
      
      @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
      }
      
      /* Sound toggle button */
      .sound-toggle {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 100;
        background-color: rgba(0, 0, 0, 0.7);
        border: 1px solid rgba(0, 255, 102, 0.5);
        color: #00ff66;
        padding: 5px 10px;
        border-radius: 5px;
        font-family: monospace;
        font-size: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        opacity: 0.5;
      }
      
      .sound-toggle:hover {
        opacity: 1;
        box-shadow: 0 0 10px rgba(0, 255, 102, 0.7);
      }
      
      /* Scroll bar customization */
      ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
      }
      
      ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.3);
      }
      
      ::-webkit-scrollbar-thumb {
        background: rgba(0, 255, 102, 0.5);
        border-radius: 4px;
      }
      
      ::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 255, 102, 0.8);
      }
      
      /* Custom header animation */
      .cyber-header-glow {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        background: radial-gradient(circle at 50% 50%, rgba(0, 255, 102, 0.15), transparent 70%);
        opacity: 0;
        animation: pulseGlow 8s ease-in-out infinite;
      }
      
      @keyframes pulseGlow {
        0% { opacity: 0; }
        50% { opacity: 0.5; }
        100% { opacity: 0; }
      }
    `;
    
    document.head.appendChild(style);
  }
  
  initializeComponents() {
    // Load scripts dynamically
    const scripts = [
      { src: 'assets/javascripts/matrix-enhanced.js', feature: 'matrix' },
      { src: 'assets/javascripts/terminal-demo.js', feature: 'terminal' },
      { src: 'assets/javascripts/cyber-visualizer.js', feature: 'visualizer' }
    ];
    
    scripts.forEach(script => {
      if (this.features[script.feature]) {
        const scriptEl = document.createElement('script');
        scriptEl.src = script.src;
        document.body.appendChild(scriptEl);
      }
    });
    
    // Convert code blocks with terminal class to terminal demos
    document.querySelectorAll('pre.terminal').forEach(pre => {
      pre.classList.add('terminal-demo');
    });
    
    // Set up auto-visualizers where needed
    document.querySelectorAll('.cyber-viz-placeholder').forEach(placeholder => {
      placeholder.classList.add('cyber-viz-auto');
    });
  }
  
  enhanceCodeBlocks() {
    // Add glowing effect to code highlighting
    document.querySelectorAll('pre code').forEach(codeBlock => {
      if (codeBlock.className.includes('language-')) {
        codeBlock.parentElement.classList.add('enhanced-code');
        
        // Add terminal-like header
        const language = codeBlock.className.split('language-')[1].split(' ')[0];
        const header = document.createElement('div');
        header.className = 'code-header';
        header.innerHTML = `
          <div class="code-buttons">
            <span></span><span></span><span></span>
          </div>
          <div class="code-title">${language.toUpperCase()}</div>
        `;
        
        codeBlock.parentElement.insertBefore(header, codeBlock);
      }
    });
  }
  
  addSoundToggle() {
    const toggle = document.createElement('div');
    toggle.className = 'sound-toggle';
    toggle.textContent = '🔇 SOUND: OFF';
    toggle.title = 'Toggle sound effects';
    
    toggle.addEventListener('click', () => {
      this.features.sound = !this.features.sound;
      toggle.textContent = this.features.sound ? '🔊 SOUND: ON' : '🔇 SOUND: OFF';
      
      // Save preference
      localStorage.setItem('ghostkit-sound', this.features.sound ? 'on' : 'off');
      
      // Update terminal sound setting if available
      if (window.ghostKitTerminal) {
        window.ghostKitTerminal.playSound = this.features.sound;
      }
    });
    
    document.body.appendChild(toggle);
  }
  
  addHeaderAnimation() {
    const header = document.querySelector('.md-header');
    if (header) {
      const glowEffect = document.createElement('div');
      glowEffect.className = 'cyber-header-glow';
      header.appendChild(glowEffect);
    }
  }
  
  loadUserPreferences() {
    // Load sound preference
    const soundPref = localStorage.getItem('ghostkit-sound');
    if (soundPref === 'on') {
      this.features.sound = true;
      document.querySelector('.sound-toggle').textContent = '🔊 SOUND: ON';
      
      // Update terminal sound setting if available
      if (window.ghostKitTerminal) {
        window.ghostKitTerminal.playSound = true;
      }
    }
  }
}

// Initialize the tactical enhancement system
window.ghostKitTactical = new GhostKitTactical();
