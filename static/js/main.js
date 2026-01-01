// Modern interactive features and animations

// Automatically close flash messages with animation
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transform = 'translateX(100%)';
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });

    // Add sparkle effects
    addSparkleEffects();
    
    // Add floating particles
    createFloatingParticles();
});

// File size validation
function validateFileSize(input) {
    const maxSize = 100 * 1024 * 1024; // 100MB
    
    if (input.files && input.files.length > 0) {
        for (let i = 0; i < input.files.length; i++) {
            const fileSize = input.files[i].size;
            
            if (fileSize > maxSize) {
                alert('⚠️ File is too large! Maximum file size is 100MB.');
                input.value = '';
                return false;
            }
        }
    }
    
    return true;
}

// Add sparkle effects to buttons
function addSparkleEffects() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const sparkle = document.createElement('span');
            sparkle.style.position = 'absolute';
            sparkle.style.left = e.offsetX + 'px';
            sparkle.style.top = e.offsetY + 'px';
            sparkle.style.width = '10px';
            sparkle.style.height = '10px';
            sparkle.style.background = 'white';
            sparkle.style.borderRadius = '50%';
            sparkle.style.pointerEvents = 'none';
            sparkle.style.animation = 'sparkle 0.6s ease-out forwards';
            
            button.style.position = 'relative';
            button.appendChild(sparkle);
            
            setTimeout(() => sparkle.remove(), 600);
        });
    });
}

// Create floating particles background
function createFloatingParticles() {
    const container = document.querySelector('body');
    if (!container) return;
    
    const particlesContainer = document.createElement('div');
    particlesContainer.style.position = 'fixed';
    particlesContainer.style.top = '0';
    particlesContainer.style.left = '0';
    particlesContainer.style.width = '100%';
    particlesContainer.style.height = '100%';
    particlesContainer.style.pointerEvents = 'none';
    particlesContainer.style.zIndex = '0';
    particlesContainer.style.overflow = 'hidden';
    
    // Create particles
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.style.position = 'absolute';
        particle.style.width = Math.random() * 6 + 2 + 'px';
        particle.style.height = particle.style.width;
        particle.style.background = `rgba(${102 + Math.random() * 100}, ${126 + Math.random() * 100}, 234, ${Math.random() * 0.3})`;
        particle.style.borderRadius = '50%';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animation = `float ${10 + Math.random() * 20}s ease-in-out infinite`;
        particle.style.animationDelay = Math.random() * 5 + 's';
        
        particlesContainer.appendChild(particle);
    }
    
    container.insertBefore(particlesContainer, container.firstChild);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes sparkle {
        0% {
            transform: scale(0);
            opacity: 1;
        }
        100% {
            transform: scale(2);
            opacity: 0;
        }
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0) translateX(0);
        }
        25% {
            transform: translateY(-20px) translateX(10px);
        }
        50% {
            transform: translateY(-10px) translateX(-10px);
        }
        75% {
            transform: translateY(-30px) translateX(5px);
        }
    }
`;
document.head.appendChild(style);

// Add smooth scroll behavior
document.documentElement.style.scrollBehavior = 'smooth';

// File input validation
const fileInputs = document.querySelectorAll('input[type="file"]');
fileInputs.forEach(input => {
    input.addEventListener('change', function() {
        validateFileSize(this);
    });
});

// Add hover effects to file cards
document.addEventListener('DOMContentLoaded', () => {
    const fileCards = document.querySelectorAll('.file-card');
    
    fileCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
});

// Add loading animation for upload
const uploadForm = document.getElementById('uploadForm');
if (uploadForm) {
    uploadForm.addEventListener('submit', function(e) {
        const uploadBtn = document.getElementById('uploadBtn');
        if (uploadBtn && uploadBtn.textContent.includes('Upload')) {
            uploadBtn.innerHTML = `
                <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" style="animation: spin 1s linear infinite;">
                    <circle cx="12" cy="12" r="10"></circle>
                    <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
                ⏳ Uploading...
            `;
            uploadBtn.disabled = true;
            
            // Add spin animation
            const spinStyle = document.createElement('style');
            spinStyle.textContent = `
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            `;
            document.head.appendChild(spinStyle);
        }
    });
}

// Add easter egg - konami code
let konamiCode = [];
const konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];

document.addEventListener('keydown', (e) => {
    konamiCode.push(e.key);
    if (konamiCode.length > 10) konamiCode.shift();
    
    if (JSON.stringify(konamiCode) === JSON.stringify(konamiSequence)) {
        // Activate party mode!
        document.body.style.animation = 'rainbow 2s linear infinite';
        
        const partyStyle = document.createElement('style');
        partyStyle.textContent = `
            @keyframes rainbow {
                0% { filter: hue-rotate(0deg); }
                100% { filter: hue-rotate(360deg); }
            }
        `;
        document.head.appendChild(partyStyle);
        
        setTimeout(() => {
            document.body.style.animation = '';
        }, 5000);
        
        alert('🎉 Party Mode Activated! 🎊');
    }
});

