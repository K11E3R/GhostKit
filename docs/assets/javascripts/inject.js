// GhostKit CSS/JS Injector
document.addEventListener('DOMContentLoaded', function() {
  // Inject our custom CSS
  function injectStylesheet(href) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = href;
    document.head.appendChild(link);
  }
  
  // Inject our custom JS
  function injectScript(src) {
    const script = document.createElement('script');
    script.src = src;
    document.body.appendChild(script);
  }
  
  // Inject all custom assets
  injectStylesheet('/assets/stylesheets/custom.css');
  injectStylesheet('/assets/stylesheets/hero.css');
  injectScript('/assets/javascripts/custom.js');
  
  // Add a digital noise overlay to the entire site
  const noiseOverlay = document.createElement('div');
  noiseOverlay.classList.add('noise-overlay');
  document.body.appendChild(noiseOverlay);
  
  // Add CSS for the noise overlay directly
  const noiseStyle = document.createElement('style');
  noiseStyle.textContent = `
    .noise-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-image: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3QUcCgYcJ3FYUQAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBkLmUHAAAExElEQVRo3u2aTWxUVRTHf/e+N6XfMEOnpdNiSfoRQkUlJCIhIX7FuDJGFy5caIwuDAsWxpUrV27YmBAXLggGQ2JcqFFBKCgfrVZb2tLOVDs40w9mhjLMvHevizc9jG3pgE3f6Dvj4r177pv7O+f8z/+ccy8SQghMj/8BpASZHtNASJDpMQ2EZP0IPp8PKeX/8uOHhx9w5cp3fL99Jz+f+5FMOsUjK1by4kuvUbWwikLR4cz3J+js6KSrs4NcNs1jzVsA2Pniy6xZW0N9YyOZ1DQ93d1kjGmOHDrIkSMHmZoYQ5F95ZfnEAIcx8G2bRYtWkR7ezuNjY0cPLCft9/6J9LCwkL279/P5s2bCQaDdN++w+VLF3mrZSf19Q/T3naWlpYdHPv6KPGJMSpvCTIhBFobuF0akpKS0lJWrq7h6aef4Yc/2qYcmZlBa20GdYRSkMlYdHR28fTTz5JKpejsuE5bWxtTkxMIIRDCyR/HOe7xPsH09DTB4lI62to48u3XDN4fHOeZTQ0ASmYhE5yYsIhEhnjggQDl5WX09Nwml81is9k8JEVIgFRSMjQ8TDAYZPHixaQzGTZs2MDtO3cJBYNIodBag9Zora2b1mowxsAwJkePHePQ0YOMjYyCcJRy4+yCXZI8TYvF9+nq7CSdtgiFQpSUlFJaWkrvvbt4PG4KCtzEJyf59ddfWLF8BQMDA5w5c5qvvjzAqlWreGLrVppqarnVfhOttTOcK1JrbXV1dYlwOIzH4yEej3Pu3Dmqq6vJZDLMnz+f9evX09fXx9mzZ/F6vbz44gtMTSdZs3YtKMnZs2cpLy/j+ede4MTJE0xNTiCE1vqWUCQSEWNjY8yZMwdjDLFYjPHxcXw+H1pr5s6dS21tLV1dXWQyGaqqqigqKkIpRXX1KrTWXLlyhbKyMqrXr+fa9WsMDw9hjOGR+vpxjzuflYXDYe69916i0SiGmw3F2NgYRUVFSCmxbZtgMMjGjRvp7+8nEolQVVWFz+cjm82STCYxxvD777+xePESautq+eXST8iioqKM2+0W586dIxaL4ff7qaiooLe3l0QiQWFhIUopbNsmFAqxZcsWkskkN27coLa2lvvuu4/R0VGSySR+v5/r169x+fJl/P4AtbW1xMbH0Vprt9Y6HYlEXNu2bROhUIiqqioikQjJZJKamhqUUtzvLt+bN2/S0tJCJBKhurqasrIyJiYmiMViGGP45JNP2Ld3L8FQiPXr1qGNQSmFVBKXyyW+OHxECCEEQgipmY26tTYYbdBarLU2WJYl9u37WC3wB5ibr1lz9xVCINJ5CDnHbIdnWRZ79uxRgVAplZWVeXdXXl7uzOy2bbvwgMORo4cF8/z4/P7t+f66t39MbfDC8mmbO6sLTjtnXdCczcwKAkEwGKS/v18vWbLkB6/X+05FRYXftu28r1t+T6VSx3p7ezvb2trMunXrVDqdxu12I+WfXy/nLmTOXUznJv65MSmEkAghsSwLj8eDUkq73e5MUVFRxrbtE0op8fnnn4uysjIVj8dxuVy4XK7Z9zWL8z9nZgPzL3zdsixM3rlSCOEKBAL+QCBwn9vtftPj8bwxNDREcXExHo8HIcSsYOTMZ2+XIhccUsq/XO7MtUE5N1LO9fhfDCnl7CqLv7nW+Q/JN3GWBN8Y9AAAAABJRU5ErkJggg==");
      pointer-events: none;
      z-index: 9999;
      opacity: 0.03;
    }
  `;
  document.head.appendChild(noiseStyle);
});
