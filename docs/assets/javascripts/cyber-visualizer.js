/**
 * GhostKit Tactical 3D Visualization System
 * Creates holographic data visualizations for security modules
 */

class CyberVisualizer {
  constructor(options = {}) {
    this.containers = document.querySelectorAll(options.selector || '.cyber-viz');
    this.colorScheme = options.colorScheme || 'matrix'; // matrix, cyber, tactical
    this.rotationSpeed = options.rotationSpeed || 0.01;
    this.pulseSpeed = options.pulseSpeed || 0.02;
    this.glowIntensity = options.glowIntensity || 0.7;
    this.lineOpacity = options.lineOpacity || 0.6;
    this.depth = options.depth || 100;
    this.initDelay = options.initDelay || 300;
    
    // Initialize all visualizers
    this.initializeVisualizers();
  }
  
  initializeVisualizers() {
    // Process each container
    this.containers.forEach(container => {
      // Skip if already initialized
      if (container.dataset.initialized) return;
      container.dataset.initialized = true;
      
      // Get visualization data from data attribute or container content
      let data;
      if (container.dataset.data) {
        data = JSON.parse(container.dataset.data);
      } else {
        // Extract data from container content
        try {
          data = JSON.parse(container.textContent.trim());
          container.textContent = '';
        } catch (e) {
          console.error('Invalid visualization data', e);
          return;
        }
      }
      
      // Create visualization
      this.createVisualization(container, data);
      
      // Add intersection observer to animate when visible
      this.observeVisibility(container);
    });
  }
  
  createVisualization(container, data) {
    // Set container styles
    container.style.position = 'relative';
    container.style.height = container.dataset.height || '400px';
    container.style.width = '100%';
    container.style.overflow = 'hidden';
    container.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
    container.style.borderRadius = '8px';
    container.style.boxShadow = '0 0 20px rgba(0, 255, 70, 0.3)';
    
    // Create canvas
    const canvas = document.createElement('canvas');
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    container.appendChild(canvas);
    
    // Store canvas and data
    container.canvas = canvas;
    container.vizData = data;
    
    // Create loading animation
    const loading = document.createElement('div');
    loading.className = 'cyber-viz-loading';
    loading.style.position = 'absolute';
    loading.style.top = '50%';
    loading.style.left = '50%';
    loading.style.transform = 'translate(-50%, -50%)';
    loading.style.color = '#0F0';
    loading.style.fontFamily = 'monospace';
    loading.style.fontSize = '16px';
    loading.style.textShadow = '0 0 5px rgba(0, 255, 0, 0.7)';
    loading.textContent = 'INITIALIZING VISUALIZATION...';
    container.appendChild(loading);
    
    // Create title
    if (container.dataset.title) {
      const title = document.createElement('div');
      title.className = 'cyber-viz-title';
      title.style.position = 'absolute';
      title.style.top = '15px';
      title.style.left = '15px';
      title.style.color = '#0F0';
      title.style.fontFamily = 'monospace';
      title.style.fontSize = '14px';
      title.style.textShadow = '0 0 5px rgba(0, 255, 0, 0.7)';
      title.style.zIndex = '10';
      title.textContent = container.dataset.title;
      container.appendChild(title);
    }
  }
  
  observeVisibility(container) {
    const observer = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !container.dataset.started) {
          container.dataset.started = true;
          setTimeout(() => this.startVisualization(container), this.initDelay);
          observer.unobserve(container);
        }
      });
    }, { threshold: 0.2 });
    
    observer.observe(container);
  }
  
  getColor(index, count, alpha = 1) {
    const hue = (index / count) * 120 + 120; // 120-240 range (greens to cyans)
    return `hsla(${hue}, 100%, 50%, ${alpha})`;
  }
  
  getMatrixColor(alpha = 1) {
    return `rgba(0, 255, 70, ${alpha})`;
  }
  
  getCyberColor(index, count, alpha = 1) {
    const hue = (index / count) * 60 + 180; // 180-240 range (cyans to blues)
    return `hsla(${hue}, 100%, 50%, ${alpha})`;
  }
  
  getTacticalColor(index, count, alpha = 1) {
    const hue = (index / count) * 30; // 0-30 range (reds to oranges)
    return `hsla(${hue}, 100%, 50%, ${alpha})`;
  }
  
  getVisualizationColor(scheme, index, count, alpha = 1) {
    switch(scheme) {
      case 'matrix': return this.getMatrixColor(alpha);
      case 'cyber': return this.getCyberColor(index, count, alpha);
      case 'tactical': return this.getTacticalColor(index, count, alpha);
      default: return this.getMatrixColor(alpha);
    }
  }
  
  startVisualization(container) {
    const canvas = container.canvas;
    const data = container.vizData;
    const ctx = canvas.getContext('2d');
    const loading = container.querySelector('.cyber-viz-loading');
    
    // Remove loading indicator
    if (loading) loading.remove();
    
    // Set canvas size
    const resize = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    };
    resize();
    window.addEventListener('resize', resize);
    
    // Set visualization type
    const type = container.dataset.type || 'network';
    
    // Initialize animation variables
    let time = 0;
    let rotation = 0;
    
    // Store animation frame
    let animationFrame;
    
    // Draw function based on visualization type
    const draw = () => {
      time += 0.01;
      rotation += this.rotationSpeed;
      
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      switch(type) {
        case 'network':
          this.drawNetworkVisualization(ctx, data, time, rotation, canvas.width, canvas.height);
          break;
        case 'treemap':
          this.drawTreemapVisualization(ctx, data, time, canvas.width, canvas.height);
          break;
        case 'radar':
          this.drawRadarVisualization(ctx, data, time, rotation, canvas.width, canvas.height);
          break;
        default:
          this.drawNetworkVisualization(ctx, data, time, rotation, canvas.width, canvas.height);
      }
      
      animationFrame = requestAnimationFrame(draw);
    };
    
    // Start animation
    draw();
    
    // Store cleanup function
    container.cleanup = () => {
      cancelAnimationFrame(animationFrame);
      window.removeEventListener('resize', resize);
    };
  }
  
  drawNetworkVisualization(ctx, data, time, rotation, width, height) {
    const centerX = width / 2;
    const centerY = height / 2;
    const nodeRadius = Math.min(width, height) * 0.02;
    const nodes = data.nodes || [];
    const links = data.links || [];
    
    // Draw links
    ctx.lineWidth = 1;
    links.forEach((link, i) => {
      const source = nodes[link.source];
      const target = nodes[link.target];
      
      if (!source || !target) return;
      
      // Calculate 3D positions with rotation
      const sourceX = centerX + Math.cos(source.x + rotation) * (source.y * width * 0.4);
      const sourceY = centerY + Math.sin(source.x + rotation) * (source.y * height * 0.4);
      const targetX = centerX + Math.cos(target.x + rotation) * (target.y * width * 0.4);
      const targetY = centerY + Math.sin(target.x + rotation) * (target.y * height * 0.4);
      
      // Pulse effect
      const pulse = Math.sin(time * this.pulseSpeed * 5 + i * 0.1) * 0.5 + 0.5;
      
      // Draw link with glow
      ctx.beginPath();
      ctx.moveTo(sourceX, sourceY);
      ctx.lineTo(targetX, targetY);
      ctx.strokeStyle = this.getVisualizationColor(this.colorScheme, i, links.length, this.lineOpacity * pulse);
      ctx.shadowBlur = 5;
      ctx.shadowColor = this.getVisualizationColor(this.colorScheme, i, links.length, this.glowIntensity);
      ctx.stroke();
      ctx.shadowBlur = 0;
    });
    
    // Draw nodes
    nodes.forEach((node, i) => {
      // Calculate 3D position with rotation
      const x = centerX + Math.cos(node.x + rotation) * (node.y * width * 0.4);
      const y = centerY + Math.sin(node.x + rotation) * (node.y * height * 0.4);
      
      // Pulse effect
      const pulse = Math.sin(time * this.pulseSpeed + i * 0.2) * 0.5 + 0.5;
      const radius = nodeRadius * (node.size || 1) * (pulse * 0.3 + 0.7);
      
      // Draw node with glow
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      ctx.fillStyle = this.getVisualizationColor(this.colorScheme, i, nodes.length, 0.8);
      ctx.shadowBlur = 15;
      ctx.shadowColor = this.getVisualizationColor(this.colorScheme, i, nodes.length, this.glowIntensity);
      ctx.fill();
      ctx.shadowBlur = 0;
      
      // Draw node label if provided
      if (node.label) {
        ctx.font = '10px monospace';
        ctx.fillStyle = '#FFF';
        ctx.textAlign = 'center';
        ctx.fillText(node.label, x, y + radius + 12);
      }
    });
  }
  
  drawTreemapVisualization(ctx, data, time, width, height) {
    const items = data.items || [];
    const padding = 5;
    const maxDepth = 3;
    
    // Recursive function to draw treemap
    const drawRect = (item, x, y, w, h, depth = 0) => {
      // Pulse effect
      const pulse = Math.sin(time * this.pulseSpeed + depth * 0.5) * 0.3 + 0.7;
      
      // Draw rectangle with glow
      ctx.beginPath();
      ctx.rect(x, y, w, h);
      ctx.fillStyle = this.getVisualizationColor(this.colorScheme, depth, maxDepth, 0.2 * pulse);
      ctx.strokeStyle = this.getVisualizationColor(this.colorScheme, depth, maxDepth, 0.8 * pulse);
      ctx.lineWidth = 2;
      ctx.shadowBlur = 10;
      ctx.shadowColor = this.getVisualizationColor(this.colorScheme, depth, maxDepth, this.glowIntensity * pulse);
      ctx.stroke();
      ctx.fill();
      ctx.shadowBlur = 0;
      
      // Draw item label
      if (item.label && w > 60 && h > 30) {
        ctx.font = '12px monospace';
        ctx.fillStyle = '#FFF';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(item.label, x + w/2, y + h/2);
      }
      
      // Draw children if available and not too deep
      if (item.children && depth < maxDepth) {
        let totalSize = item.children.reduce((sum, child) => sum + (child.size || 1), 0);
        let currentX = x + padding;
        let currentY = y + padding;
        let remainingWidth = w - padding * 2;
        let remainingHeight = h - padding * 2;
        
        // Layout algorithm (simple)
        let isHorizontal = remainingWidth > remainingHeight;
        
        item.children.forEach(child => {
          const childSize = child.size || 1;
          const ratio = childSize / totalSize;
          
          let childW, childH;
          
          if (isHorizontal) {
            childW = remainingWidth * ratio;
            childH = remainingHeight;
            drawRect(child, currentX, currentY, childW, childH, depth + 1);
            currentX += childW;
          } else {
            childW = remainingWidth;
            childH = remainingHeight * ratio;
            drawRect(child, currentX, currentY, childW, childH, depth + 1);
            currentY += childH;
          }
        });
      }
    };
    
    // Start drawing from root items
    items.forEach(item => {
      const w = width * (item.size || 1);
      const h = height * (item.size || 1);
      const x = (width - w) / 2;
      const y = (height - h) / 2;
      
      drawRect(item, x, y, w, h);
    });
  }
  
  drawRadarVisualization(ctx, data, time, rotation, width, height) {
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) * 0.4;
    const categories = data.categories || [];
    const items = data.items || [];
    
    // Draw background circles
    for (let i = 1; i <= 5; i++) {
      const circleRadius = radius * (i / 5);
      
      // Pulse effect for circles
      const pulse = Math.sin(time * this.pulseSpeed + i * 0.2) * 0.2 + 0.8;
      
      ctx.beginPath();
      ctx.arc(centerX, centerY, circleRadius, 0, Math.PI * 2);
      ctx.strokeStyle = this.getVisualizationColor(this.colorScheme, i, 5, 0.2 * pulse);
      ctx.lineWidth = 1;
      ctx.stroke();
    }
    
    // Draw category lines
    if (categories.length > 0) {
      const angleStep = (Math.PI * 2) / categories.length;
      
      categories.forEach((category, i) => {
        const angle = i * angleStep + rotation;
        const x = centerX + Math.cos(angle) * radius;
        const y = centerY + Math.sin(angle) * radius;
        
        // Draw line
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(x, y);
        ctx.strokeStyle = this.getVisualizationColor(this.colorScheme, i, categories.length, 0.3);
        ctx.lineWidth = 1;
        ctx.stroke();
        
        // Draw category label
        ctx.font = '12px monospace';
        ctx.fillStyle = '#FFF';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        
        const labelX = centerX + Math.cos(angle) * (radius + 20);
        const labelY = centerY + Math.sin(angle) * (radius + 20);
        
        ctx.fillText(category.label, labelX, labelY);
      });
      
      // Draw data points
      items.forEach((item, itemIndex) => {
        const values = item.values || [];
        const points = [];
        
        // Calculate points
        values.forEach((value, i) => {
          if (i >= categories.length) return;
          
          const angle = i * angleStep + rotation;
          const distance = value * radius;
          const x = centerX + Math.cos(angle) * distance;
          const y = centerY + Math.sin(angle) * distance;
          
          points.push({ x, y });
        });
        
        // Draw area
        if (points.length > 2) {
          ctx.beginPath();
          ctx.moveTo(points[0].x, points[0].y);
          
          for (let i = 1; i < points.length; i++) {
            ctx.lineTo(points[i].x, points[i].y);
          }
          
          ctx.closePath();
          
          // Pulse effect
          const pulse = Math.sin(time * this.pulseSpeed + itemIndex * 0.5) * 0.3 + 0.7;
          
          ctx.fillStyle = this.getVisualizationColor(this.colorScheme, itemIndex, items.length, 0.2 * pulse);
          ctx.strokeStyle = this.getVisualizationColor(this.colorScheme, itemIndex, items.length, 0.8 * pulse);
          ctx.lineWidth = 2;
          ctx.shadowBlur = 10;
          ctx.shadowColor = this.getVisualizationColor(this.colorScheme, itemIndex, items.length, this.glowIntensity * pulse);
          ctx.stroke();
          ctx.fill();
          ctx.shadowBlur = 0;
        }
        
        // Draw points
        points.forEach((point, i) => {
          ctx.beginPath();
          ctx.arc(point.x, point.y, 5, 0, Math.PI * 2);
          ctx.fillStyle = this.getVisualizationColor(this.colorScheme, itemIndex, items.length, 0.9);
          ctx.fill();
        });
        
        // Draw item label if provided
        if (item.label) {
          ctx.font = '12px monospace';
          ctx.fillStyle = this.getVisualizationColor(this.colorScheme, itemIndex, items.length, 1);
          ctx.textAlign = 'left';
          ctx.textBaseline = 'middle';
          ctx.fillText(item.label, centerX + radius + 20, centerY - radius + 20 + itemIndex * 20);
        }
      });
    }
  }
  
  // Update color scheme
  setColorScheme(scheme) {
    this.colorScheme = scheme;
    return this;
  }
  
  // Initialize any new visualizers that might have been added to the page
  refresh() {
    this.containers = document.querySelectorAll('.cyber-viz');
    this.initializeVisualizers();
  }
  
  // Generate random network data (helper function)
  static generateNetworkData(nodeCount = 10, linkCount = 15) {
    const nodes = [];
    
    // Generate nodes
    for (let i = 0; i < nodeCount; i++) {
      nodes.push({
        x: Math.random() * Math.PI * 2,
        y: Math.random(),
        size: Math.random() * 0.5 + 0.5,
        label: `Node ${i+1}`
      });
    }
    
    // Generate links
    const links = [];
    for (let i = 0; i < linkCount; i++) {
      links.push({
        source: Math.floor(Math.random() * nodeCount),
        target: Math.floor(Math.random() * nodeCount)
      });
    }
    
    return { nodes, links };
  }
  
  // Generate random treemap data (helper function)
  static generateTreemapData(depth = 2, childCount = 4) {
    const generateChildren = (currentDepth) => {
      if (currentDepth <= 0) return null;
      
      const children = [];
      const count = Math.floor(Math.random() * childCount) + 2;
      
      for (let i = 0; i < count; i++) {
        children.push({
          size: Math.random() * 0.8 + 0.2,
          label: `Item ${i+1}`,
          children: generateChildren(currentDepth - 1)
        });
      }
      
      return children;
    };
    
    return {
      items: [
        {
          size: 1,
          label: 'Root',
          children: generateChildren(depth)
        }
      ]
    };
  }
  
  // Generate random radar data (helper function)
  static generateRadarData(categoryCount = 6, itemCount = 3) {
    const categories = [];
    
    // Generate categories
    for (let i = 0; i < categoryCount; i++) {
      categories.push({
        label: `Category ${i+1}`
      });
    }
    
    // Generate items
    const items = [];
    for (let i = 0; i < itemCount; i++) {
      const values = [];
      
      for (let j = 0; j < categoryCount; j++) {
        values.push(Math.random() * 0.7 + 0.3);
      }
      
      items.push({
        label: `Item ${i+1}`,
        values: values
      });
    }
    
    return { categories, items };
  }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  // Create global visualizer instance
  window.ghostKitVisualizer = new CyberVisualizer({
    selector: '.cyber-viz',
    colorScheme: 'matrix'
  });
  
  // Set up auto-generation for empty containers
  document.querySelectorAll('.cyber-viz-auto').forEach(container => {
    const type = container.dataset.type || 'network';
    let data;
    
    switch(type) {
      case 'network':
        data = CyberVisualizer.generateNetworkData();
        break;
      case 'treemap':
        data = CyberVisualizer.generateTreemapData();
        break;
      case 'radar':
        data = CyberVisualizer.generateRadarData();
        break;
      default:
        data = CyberVisualizer.generateNetworkData();
    }
    
    container.dataset.data = JSON.stringify(data);
    container.className = 'cyber-viz';
    window.ghostKitVisualizer.refresh();
  });
});
