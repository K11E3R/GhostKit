/**
 * GhostKit Terminal Demo System
 * Realistic command line simulation with typing effects and syntax highlighting
 */

class TerminalDemoSystem {
  constructor(options = {}) {
    this.containers = document.querySelectorAll(options.selector || '.terminal-demo');
    this.typeSpeed = options.typeSpeed || [30, 90]; // [min, max] typing speed in ms
    this.errorRate = options.errorRate || 0.01; // Chance of typing errors for realism
    this.cursorBlinkRate = options.cursorBlinkRate || 500; // Cursor blink rate in ms
    this.commandDelay = options.commandDelay || [500, 1200]; // Delay between commands
    this.initDelay = options.initDelay || 800; // Initial delay before starting
    this.correctionDelay = options.correctionDelay || 200; // Delay before correcting typos
    this.highlightSyntax = options.highlightSyntax !== undefined ? options.highlightSyntax : true;
    this.playSound = options.playSound !== undefined ? options.playSound : true;
    
    // Load sound effects if enabled
    if (this.playSound) {
      this.keySound = new Audio();
      this.keySound.src = options.keySoundSrc || 'data:audio/mp3;base64,SUQzAwAAAABHeFRBTEIAAAABAAAAVENPTgAAAAEAAABUUEUxAAAABAAAAFRJVDIAAAABAAAAVFJDSwAAAAEAAABUWUVSAAAABAAAAFRDT00AAAABAAAAVFNVAAAABAAAAFRZRVIAAAAEAAAA//tQxAAAAAAAAAAAAAAAAAAAAAAAWGluZwAAAA8AAAACAAAEYgD///////////////////////////////////////////8AAAA8TEFNRTMuMTAwAwEAAAAAAAAAABRAJAXwQQABPAAABGKIla0EAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//tAxAAABlgnphGCABDdD/T80AABOAAAH0JqRZMwAkCdIjSA6EImQxMxdFTkMzKpzJwoQILgpjIlA2NWZK+qf8w8LxvQZBQRQgQy1mKMcZuLwZgQHogA7gkHEDA8lmX/1x2EImhELFhQ8ZVav+L86f/+nTp+dOn5w4cf/UYGAwN9vt9D8bDAZQGxN9/MUxBMQU1FMy4xMDBVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV';
      this.keySound.volume = 0.15;
      this.errorSound = new Audio();
      this.errorSound.src = options.errorSoundSrc || 'data:audio/mp3;base64,SUQzAwAAAABHeFRBTEIAAAABAAAAVENPTgAAAAEAAABUUEUxAAAABAAAAFRJVDIAAAABAAAAVFJDSwAAAAEAAABUWUVSAAAABAAAAFRDT00AAAABAAAAVFNVAAAABAAAAFRZRVIAAAAEAAAA//tQxAAAAAAAAAAAAAAAAAAAAAAAWGluZwAAAA8AAAACAAAEYgD///////////////////////////////////////////8AAAA8TEFNRTMuMTAwAwEAAAAAAAAAABRAJAXwQQABPAAABGKIla0EAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//tAxAAABT0XXnmCABLGlysswQAIxRGVsRVJkSQeEMUMaGc4JhkKAJCSNZmSH8CoDgmAcDgLAQWTVjItRKV+ZgiBYCQeB4+UJ//WcLyb/oE4CUTHqzn//XGYdf/1xmHXg+D4Ph+D4IAgCAIH/+CAIAgfggf/4IAgcEAQOCAIH/+CAIAgCBwQBAAAAMQU1FMy4xMDBVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV';
      this.errorSound.volume = 0.2;
      this.returnSound = new Audio();
      this.returnSound.src = options.returnSoundSrc || 'data:audio/mp3;base64,SUQzAwAAAABHeFRBTEIAAAABAAAAVENPTgAAAAEAAABUUEUxAAAABAAAAFRJVDIAAAABAAAAVFJDSwAAAAEAAABUWUVSAAAABAAAAFRDT00AAAABAAAAVFNVAAAABAAAAFRZRVIAAAAEAAAA//tQxAAAAAAAAAAAAAAAAAAAAAAAWGluZwAAAA8AAAACAAAGDgD///////////////////////////////////////////8AAAA8TEFNRTMuMTAwAwEAAAAAAAAAABRAJAdwQQABPAAABg5CFbMKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//tAxAAABOknShGCABGek/OMkwAEQAiIEJCMiYhEyJSRDgTIlImVRMi//91RZMifUWTIlInREUxEZRFjsRGURbr/+iLdEREQodxYdHf/5cWnR0dHcWFhQsKP/8KFhYdHR0dyh3//QsU6Oh0dxQoUKP/4oUKHR3FD/+h0f/9Cp0f/0P//lCgo//5Q6Ov//KFBQUFBQUFOgsLCwsLCwpMQU1FMy4xMDBVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV';
      this.returnSound.volume = 0.25;
    }
    
    // Initialize all terminal demos
    this.initializeTerminals();
  }
  
  initializeTerminals() {
    // Process each terminal container
    this.containers.forEach(container => {
      // Skip if already initialized
      if (container.dataset.initialized) return;
      container.dataset.initialized = true;
      
      // Get demo script from data attribute or container content
      let script;
      if (container.dataset.script) {
        script = JSON.parse(container.dataset.script);
      } else {
        // Extract script from pre-formatted text
        const scriptText = container.textContent.trim();
        container.textContent = '';
        script = this.parseScript(scriptText);
      }
      
      // Create terminal UI
      this.createTerminalUI(container, script);
      
      // Add intersection observer to start demo when visible
      this.observeVisibility(container);
    });
  }
  
  parseScript(text) {
    // Parse raw text into command/response pairs
    const lines = text.split('\\n');
    const script = [];
    let currentCommand = '';
    let currentResponse = [];
    let isInCommand = true;
    
    lines.forEach(line => {
      if (line.startsWith('$ ')) {
        // If we were building a previous command/response, save it
        if (currentCommand) {
          script.push({
            command: currentCommand,
            response: currentResponse.join('\\n')
          });
        }
        // Start new command
        currentCommand = line.substring(2);
        currentResponse = [];
        isInCommand = false;
      } else {
        if (isInCommand) {
          currentCommand += '\\n' + line;
        } else {
          currentResponse.push(line);
        }
      }
    });
    
    // Add the last command/response
    if (currentCommand) {
      script.push({
        command: currentCommand,
        response: currentResponse.join('\\n')
      });
    }
    
    return script;
  }
  
  createTerminalUI(container, script) {
    // Set container styles
    container.style.fontFamily = 'monospace, "Courier New", Courier';
    container.style.backgroundColor = 'rgba(0, 0, 0, 0.85)';
    container.style.color = '#0F0';
    container.style.padding = '15px';
    container.style.borderRadius = '5px';
    container.style.boxShadow = '0 0 15px rgba(0, 255, 0, 0.3)';
    container.style.overflow = 'auto';
    container.style.maxHeight = '500px';
    container.style.position = 'relative';
    
    // Create terminal header
    const header = document.createElement('div');
    header.style.borderBottom = '1px solid rgba(0, 255, 0, 0.3)';
    header.style.paddingBottom = '8px';
    header.style.marginBottom = '10px';
    header.style.display = 'flex';
    header.style.justifyContent = 'space-between';
    header.style.alignItems = 'center';
    
    // Terminal buttons
    const buttons = document.createElement('div');
    ['#FF5F56', '#FFBD2E', '#27C93F'].forEach(color => {
      const button = document.createElement('span');
      button.style.display = 'inline-block';
      button.style.width = '12px';
      button.style.height = '12px';
      button.style.borderRadius = '50%';
      button.style.backgroundColor = color;
      button.style.marginRight = '6px';
      buttons.appendChild(button);
    });
    
    // Terminal title
    const title = document.createElement('div');
    title.textContent = container.dataset.title || 'GhostKit Terminal';
    title.style.color = '#0F0';
    
    header.appendChild(buttons);
    header.appendChild(title);
    container.appendChild(header);
    
    // Create terminal content area
    const content = document.createElement('div');
    content.className = 'terminal-content';
    content.style.lineHeight = '1.4';
    content.style.whiteSpace = 'pre-wrap';
    content.style.wordBreak = 'break-all';
    container.appendChild(content);
    
    // Store script and content element
    container.script = script;
    container.content = content;
  }
  
  observeVisibility(container) {
    const observer = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !container.dataset.started) {
          container.dataset.started = true;
          this.runScript(container);
          observer.unobserve(container);
        }
      });
    }, { threshold: 0.3 });
    
    observer.observe(container);
  }
  
  // Get random delay within range
  getRandomDelay(range) {
    return Math.floor(Math.random() * (range[1] - range[0] + 1)) + range[0];
  }
  
  // Type a character with realistic errors
  async typeCharacter(content, char, cursor) {
    // Chance to make a typing error
    if (Math.random() < this.errorRate) {
      const errorChar = 'abcdefghijklmnopqrstuvwxyz'[Math.floor(Math.random() * 26)];
      content.textContent = content.textContent.slice(0, -1) + errorChar + cursor;
      
      if (this.playSound) {
        this.errorSound.currentTime = 0;
        this.errorSound.play();
      }
      
      // Wait and then correct the error
      await new Promise(resolve => setTimeout(resolve, this.correctionDelay));
      content.textContent = content.textContent.slice(0, -2) + cursor;
      await new Promise(resolve => setTimeout(resolve, this.correctionDelay));
    }
    
    // Type the actual character
    content.textContent = content.textContent.slice(0, -1) + char + cursor;
    
    if (this.playSound && char !== '') {
      this.keySound.currentTime = 0;
      this.keySound.play();
    }
  }
  
  // Run the terminal script
  async runScript(container) {
    const script = container.script;
    const content = container.content;
    const cursor = '█';
    
    // Initial prompt
    content.textContent = '$ ' + cursor;
    await new Promise(resolve => setTimeout(resolve, this.initDelay));
    
    // Process each command/response pair
    for (let i = 0; i < script.length; i++) {
      const item = script[i];
      
      // Type command
      for (let j = 0; j < item.command.length; j++) {
        await this.typeCharacter(content, item.command[j], cursor);
        await new Promise(resolve => setTimeout(resolve, this.getRandomDelay(this.typeSpeed)));
      }
      
      // Press enter
      if (this.playSound) {
        this.returnSound.currentTime = 0;
        this.returnSound.play();
      }
      
      // Wait before showing response
      await new Promise(resolve => setTimeout(resolve, this.commandDelay[0]));
      
      // Show command response
      let responseHtml = item.response;
      
      // Apply syntax highlighting if enabled
      if (this.highlightSyntax) {
        responseHtml = this.highlightSyntax(item.response);
      }
      
      content.textContent = content.textContent.slice(0, -1); // Remove cursor
      content.innerHTML += '\\n' + responseHtml + '\\n$ ' + cursor;
      
      // Scroll to bottom
      container.scrollTop = container.scrollHeight;
      
      // Delay before next command
      await new Promise(resolve => setTimeout(resolve, this.getRandomDelay(this.commandDelay)));
    }
    
    // Blink cursor at end
    let cursorVisible = true;
    const blinkInterval = setInterval(() => {
      cursorVisible = !cursorVisible;
      content.textContent = content.textContent.slice(0, -1) + (cursorVisible ? cursor : ' ');
    }, this.cursorBlinkRate);
    
    // Clean up after 60 seconds of blinking
    setTimeout(() => clearInterval(blinkInterval), 60000);
  }
  
  // Basic syntax highlighting for common command outputs
  highlightSyntax(text) {
    // Replace with syntax highlighting
    return text
      // IP addresses
      .replace(/\b(?:\d{1,3}\.){3}\d{1,3}\b/g, '<span style="color:#5AF;">$&</span>')
      // URLs and paths
      .replace(/(https?:\/\/[^\s]+)/g, '<span style="color:#5FF;">$1</span>')
      .replace(/\/[\w\/\.-]+/g, '<span style="color:#5FF;">$&</span>')
      // Numbers and sizes
      .replace(/\b\d+\b/g, '<span style="color:#F55;">$&</span>')
      .replace(/\b\d+[KMG]B\b/g, '<span style="color:#F55;">$&</span>')
      // Command output headers
      .replace(/^([A-Z][A-Z\s]+:)/gm, '<span style="color:#FF5;">$1</span>')
      // Success messages
      .replace(/(success|succeeded|completed)/gi, '<span style="color:#5F5;">$1</span>')
      // Error and warning messages
      .replace(/(error|failed|warning|vulnerable)/gi, '<span style="color:#F55;">$1</span>')
      // JSON/YAML keys
      .replace(/"([^"]+)":/g, '<span style="color:#FF5;">"$1"</span>:')
      // Brackets and braces
      .replace(/[\[\]{}()]/g, '<span style="color:#AAF;">$&</span>');
  }
  
  // Initialize any new terminal demos that might have been added to the page
  refresh() {
    this.containers = document.querySelectorAll('.terminal-demo');
    this.initializeTerminals();
  }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  // Create global terminal demo instance
  window.ghostKitTerminal = new TerminalDemoSystem({
    selector: '.terminal-demo',
    playSound: true
  });
  
  // Convert <pre class="terminal"> blocks into interactive demos
  document.querySelectorAll('pre.terminal').forEach(pre => {
    const container = document.createElement('div');
    container.className = 'terminal-demo';
    container.dataset.title = pre.dataset.title || 'GhostKit Terminal';
    
    // Get content and remove $ prompt if present
    const content = pre.textContent;
    
    // Replace pre with terminal demo
    pre.parentNode.replaceChild(container, pre);
    
    // Create script from content
    const script = [
      { command: content.split('\\n')[0].replace(/^\$ /, ''), response: content.split('\\n').slice(1).join('\\n') }
    ];
    
    // Set up terminal demo
    container.dataset.script = JSON.stringify(script);
    window.ghostKitTerminal.initializeTerminals();
  });
});
