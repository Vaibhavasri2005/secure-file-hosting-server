// Modern interactive features

// Automatically close flash messages
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
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

// File management functions
function toggleStar(filename) {
    fetch('/star/' + filename, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        });
}

// File sharing function
function shareFile(filename) {
    const shareUrl = window.location.origin + '/download/' + filename;
    if (navigator.share) {
        navigator.share({
            title: 'Share File',
            text: 'Check out this file: ' + filename,
            url: shareUrl
        });
    } else {
        navigator.clipboard.writeText(shareUrl);
        alert('📋 Link copied to clipboard!');
    }
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

