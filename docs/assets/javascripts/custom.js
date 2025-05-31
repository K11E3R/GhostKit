// GhostKit Advanced Interactivity Module
document.addEventListener('DOMContentLoaded', function() {
  // Terminal typing effect for elements with .typing-animation class
  function initTypeWriterEffect() {
    const elements = document.querySelectorAll('.typing-animation');
    
    elements.forEach(element => {
      const text = element.textContent;
      element.textContent = '';
      element.style.width = '0';
      
      let i = 0;
      const typeWriter = () => {
        if (i < text.length) {
          element.textContent += text.charAt(i);
          i++;
          setTimeout(typeWriter, Math.random() * 100 + 50);
        }
      };
      
      // Start typing with a slight delay
      setTimeout(typeWriter, 500);
    });
  }
  
  // Matrix rain effect for hero sections
  function createMatrixRain(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    const canvas = document.createElement('canvas');
    canvas.width = container.offsetWidth;
    canvas.height = container.offsetHeight;
    canvas.style.position = 'absolute';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.zIndex = '-1';
    canvas.style.opacity = '0.05';
    container.style.position = 'relative';
    container.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    
    // Matrix characters
    const characters = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789';
    const columns = Math.floor(canvas.width / 20);
    const drops = [];
    
    // Initialize drops
    for (let i = 0; i < columns; i++) {
      drops[i] = Math.random() * -100;
    }
    
    function draw() {
      ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      ctx.fillStyle = '#0df956';
      ctx.font = '15px monospace';
      
      for (let i = 0; i < drops.length; i++) {
        const text = characters.charAt(Math.floor(Math.random() * characters.length));
        ctx.fillText(text, i * 20, drops[i] * 20);
        
        if (drops[i] * 20 > canvas.height && Math.random() > 0.975) {
          drops[i] = 0;
        }
        
        drops[i]++;
      }
    }
    
    setInterval(draw, 35);
  }
  
  // Exploit cards interactivity
  function initExploitCards() {
    const cards = document.querySelectorAll('.exploit-card');
    
    cards.forEach(card => {
      card.addEventListener('click', function() {
        const details = this.querySelector('.exploit-card__details');
        if (details) {
          details.classList.toggle('exploit-card__details--visible');
        }
      });
    });
  }
  
  // Add 'exploit-card' class to module sections
  function enhanceModuleSections() {
    const moduleBlocks = document.querySelectorAll('h2 + p + ul, h3 + p + ul');
    
    moduleBlocks.forEach(block => {
      const parent = block.parentNode;
      const header = parent.querySelector('h2, h3');
      const description = parent.querySelector('p');
      
      if (header && description && header.textContent.includes('Module') || 
          header.textContent.includes('Exploit') || 
          header.textContent.includes('Scanner')) {
        
        const card = document.createElement('div');
        card.className = 'exploit-card';
        
        const title = document.createElement('div');
        title.className = 'exploit-card__title';
        title.textContent = header.textContent;
        
        const desc = document.createElement('div');
        desc.className = 'exploit-card__description';
        desc.innerHTML = description.innerHTML;
        
        const items = document.createElement('div');
        items.className = 'exploit-card__items';
        items.innerHTML = block.outerHTML;
        
        // Extract tags from list items
        const tags = document.createElement('div');
        tags.className = 'exploit-card__tags';
        
        const listItems = block.querySelectorAll('li');
        listItems.forEach(item => {
          if (item.textContent.includes(':')) {
            const tagText = item.textContent.split(':')[0].trim();
            const tag = document.createElement('span');
            tag.className = 'exploit-card__tag';
            tag.textContent = tagText;
            tags.appendChild(tag);
          }
        });
        
        card.appendChild(title);
        card.appendChild(tags);
        card.appendChild(desc);
        card.appendChild(items);
        
        // Replace the original elements with our card
        header.style.display = 'none';
        description.style.display = 'none';
        block.style.display = 'none';
        parent.insertBefore(card, header);
      }
    });
  }
  
  // Create terminal demos
  function createTerminalDemos() {
    const codeBlocks = document.querySelectorAll('pre > code');
    
    codeBlocks.forEach(block => {
      // Check if it contains shell/bash commands (starts with $ or #)
      const content = block.textContent;
      if (content.match(/^\s*[$#]/m)) {
        const pre = block.parentNode;
        
        // Create terminal window
        const terminal = document.createElement('div');
        terminal.className = 'terminal-window';
        
        // Terminal header
        const header = document.createElement('div');
        header.className = 'terminal-header';
        
        const buttons = document.createElement('div');
        buttons.className = 'terminal-buttons';
        
        const redBtn = document.createElement('div');
        redBtn.className = 'terminal-circle terminal-red';
        
        const yellowBtn = document.createElement('div');
        yellowBtn.className = 'terminal-circle terminal-yellow';
        
        const greenBtn = document.createElement('div');
        greenBtn.className = 'terminal-circle terminal-green';
        
        const title = document.createElement('div');
        title.className = 'terminal-title';
        title.textContent = 'GhostKit Terminal';
        
        buttons.appendChild(redBtn);
        buttons.appendChild(yellowBtn);
        buttons.appendChild(greenBtn);
        header.appendChild(buttons);
        header.appendChild(title);
        
        // Terminal body
        const body = document.createElement('div');
        body.className = 'terminal-body';
        
        // Parse the content line by line
        const lines = content.split('\n');
        lines.forEach(line => {
          if (line.match(/^\s*[$#]/)) {
            // Command line
            const prompt = document.createElement('div');
            prompt.className = 'terminal-prompt';
            prompt.textContent = line.replace(/^\s*[$#]\s*/, '');
            body.appendChild(prompt);
          } else if (line.trim()) {
            // Output line
            const output = document.createElement('div');
            output.className = 'terminal-output';
            output.textContent = line;
            body.appendChild(output);
          }
        });
        
        terminal.appendChild(header);
        terminal.appendChild(body);
        
        // Replace the original code block
        pre.parentNode.replaceChild(terminal, pre);
      }
    });
  }
  
  // Initialize progress bars
  function initProgressBars() {
    const progressElements = document.querySelectorAll('.progress-bar');
    
    progressElements.forEach(element => {
      const percentage = element.getAttribute('data-percentage') || '100';
      const fill = element.querySelector('.progress-fill');
      
      if (fill) {
        fill.style.width = percentage + '%';
      }
    });
  }
  
  // Add interaction to navigation
  function enhanceNavigation() {
    const navItems = document.querySelectorAll('.md-nav__item');
    
    navItems.forEach(item => {
      item.addEventListener('mouseenter', function() {
        this.style.transform = 'translateX(3px)';
      });
      
      item.addEventListener('mouseleave', function() {
        this.style.transform = 'translateX(0)';
      });
    });
  }
  
  // Call all initialization functions
  function initializeAll() {
    setTimeout(() => {
      initTypeWriterEffect();
      createMatrixRain('hero');
      initExploitCards();
      enhanceModuleSections();
      createTerminalDemos();
      initProgressBars();
      enhanceNavigation();
      
      // Add matrix effect to sections with 'matrix-bg' class
      document.querySelectorAll('.matrix-bg').forEach((el, i) => {
        createMatrixRain('matrix-' + i);
      });
    }, 500);
  }
  
  // Initialize on page load
  initializeAll();
  
  // Also initialize on navigation (for SPAs)
  document.addEventListener('DOMContentLoaded', initializeAll);
  
  // Custom logo animation
  const logo = document.querySelector('.md-header__button.md-logo img');
  if (logo) {
    logo.addEventListener('mouseenter', function() {
      this.style.filter = 'drop-shadow(0 0 8px var(--ghost-neon))';
      this.style.transform = 'scale(1.1)';
    });
    
    logo.addEventListener('mouseleave', function() {
      this.style.filter = '';
      this.style.transform = '';
    });
  }
});

// Add hero section to homepage
function addHeroSection() {
  const main = document.querySelector('.md-main__inner');
  const content = document.querySelector('.md-content');
  
  if (main && content && window.location.pathname.endsWith('/') || window.location.pathname.endsWith('/index.html')) {
    const hero = document.createElement('div');
    hero.id = 'hero';
    hero.className = 'ghost-hero';
    
    hero.innerHTML = `
      <div class="ghost-hero__content">
        <h1 class="ghost-hero__title typing-animation">GhostKit</h1>
        <p class="ghost-hero__subtitle">Advanced Offensive Security Framework</p>
        <div class="ghost-hero__buttons">
          <a href="getting-started/overview/" class="md-button md-button--primary">Get Started</a>
          <a href="modules/exploit_engine/" class="md-button">Explore Modules</a>
        </div>
      </div>
    `;
    
    main.insertBefore(hero, content);
  }
}

// Execute hero section addition
document.addEventListener('DOMContentLoaded', addHeroSection);
