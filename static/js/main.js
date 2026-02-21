// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {
    initAnimations();
    initFormEnhancements();
    initAutoHideFlashMessages();
    initSmoothScroll();
    initQuizSelector();
});

/**
 * Initialize page animations
 */
function initAnimations() {
    // Stagger animation for cards
    const cards = document.querySelectorAll('.glass-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(15px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.8s ease';
            card.style.opacity = '2';
            card.style.transform = 'translateY(10px))';
        }, index * 100);
    });
    
    // Add hover glow effect to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.7s ease';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transition = 'all 0.7s ease';
        });
    });
}

/**
 * Enhance form inputs with focus effects
 */
function initFormEnhancements() {
    const inputs = document.querySelectorAll('.form-input');
    
    inputs.forEach(input => {
        // Add focus animation
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
            this.parentElement.style.transition = 'transform 0.3s ease';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
        
        // Add shake animation on error
        if (input.classList.contains('error')) {
            input.style.animation = 'shake 0.5s';
        }
    });
}

/**
 * Auto-hide flash messages after 5 seconds
 */
function initAutoHideFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            message.style.opacity = '0';
            message.style.transform = 'translateX(100%)';
            
            setTimeout(() => {
                message.remove();
            }, 500);
        }, 5000);
    });
}

/**
 * Smooth scroll for anchor links
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href.startsWith('#')) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

/**
 * Shake animation for errors
 */
function shakeElement(element) {
    element.style.animation = 'none';
    setTimeout(() => {
        element.style.animation = 'shake 0.5s';
    }, 10);
}

// Add shake animation to CSS dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
        20%, 40%, 60%, 80% { transform: translateX(10px); }
    }
`;
document.head.appendChild(style);

/**
 * Format time in MM:SS format
 */
function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

/**
 * Create particle effect (for landing page)
 */
function createParticles() {
    const particlesContainer = document.querySelector('.particles');
    if (!particlesContainer) return;
    
    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            position: absolute;
            width: ${Math.random() * 4 + 1}px;
            height: ${Math.random() * 4 + 1}px;
            background: rgba(0, 217, 255, ${Math.random() * 0.5 + 0.3});
            border-radius: 50%;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            animation: float ${Math.random() * 10 + 10}s infinite ease-in-out;
            animation-delay: ${Math.random() * 5}s;
        `;
        particlesContainer.appendChild(particle);
    }
    
    // Add float animation
    const floatStyle = document.createElement('style');
    floatStyle.textContent = `
        @keyframes float {
            0%, 100% {
                transform: translate(0, 0) scale(1);
                opacity: 0.3;
            }
            50% {
                transform: translate(${Math.random() * 100 - 50}px, ${Math.random() * 100 - 50}px) scale(1.5);
                opacity: 1;
            }
        }
    `;
    document.head.appendChild(floatStyle);
}

// Initialize particles on landing page
if (document.querySelector('.landing-container')) {
    createParticles();
}

/**
 * Handle quiz option selection with visual feedback
 */
document.addEventListener('change', function(e) {
    if (e.target.type === 'radio' && e.target.name === 'option') {
        const optionItem = e.target.closest('.option-item');
        if (optionItem) {
            // Remove selected class from all options
            document.querySelectorAll('.option-item').forEach(item => {
                item.classList.remove('selected');
            });
            
            // Add selected class to current option
            optionItem.classList.add('selected');
        }
    }
});

/**
 * Prevent form submission on Enter key in code editor
 */
const codeEditor = document.getElementById('code-input');
if (codeEditor) {
    codeEditor.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.ctrlKey) {
            // Allow Ctrl+Enter for new line
            return;
        }
    });
}

/**
 * Add loading state to buttons on form submit
 */
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function() {
        const submitButton = this.querySelector('button[type="submit"]');
        if (submitButton && !submitButton.disabled) {
            submitButton.disabled = true;
            submitButton.style.opacity = '0.6';
            submitButton.textContent = submitButton.textContent + '...';
        }
    });
});

/**
 * Add ripple effect to buttons
 */
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            left: ${x}px;
            top: ${y}px;
            transform: scale(0);
            animation: ripple 0.6s ease-out;
            pointer-events: none;
        `;
        
        this.style.position = 'relative';
        this.style.overflow = 'hidden';
        this.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    });
});

// Add ripple animation
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(rippleStyle);

/**
 * Add intersection observer for scroll animations
 */
if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });
    
    document.querySelectorAll('.glass-card').forEach(card => {
        observer.observe(card);
    });
}

/**
 * Toggle active styles in quiz selector with reactive filtering
 */
function initQuizSelector() {
    // State management - single source of truth
    let selectedLanguage = '';
    let selectedLevel = '';

    const languageLabels = document.querySelectorAll('.language-pill');
    const levelLabels = document.querySelectorAll('.level-badge');
    const languageInputs = document.querySelectorAll('input[name="language"]');
    const levelInputs = document.querySelectorAll('input[name="level"]');
    const catalogSection = document.getElementById('quiz-catalog');
    const catalogCards = document.querySelectorAll('[data-language][data-level]');
    const selectedPanel = document.querySelector('.selected-quiz-panel');
    const form = document.querySelector('.quiz-select-form');
    const submitButton = form?.querySelector('button[type="submit"]');

    /**
     * Update language selection
     */
    const updateLanguage = (lang) => {
        selectedLanguage = lang;
        languageLabels.forEach(label => {
            const labelLang = label.dataset.language;
            if (labelLang === lang) {
                label.classList.add('active');
                label.querySelector('input').checked = true;
            } else {
                label.classList.remove('active');
                label.querySelector('input').checked = false;
            }
        });
        updateUI();
    };

    /**
     * Update level selection
     */
    const updateLevel = (level) => {
        selectedLevel = level;
        levelLabels.forEach(label => {
            const labelLevel = label.dataset.level;
            if (labelLevel === level) {
                label.classList.add('active');
                label.querySelector('input').checked = true;
            } else {
                label.classList.remove('active');
                label.querySelector('input').checked = false;
            }
        });
        updateUI();
    };

    /**
     * Update UI based on current selections
     */
    const updateUI = () => {
        const hasSelection = selectedLanguage && selectedLevel;

        // Show/hide catalog section
        catalogSection.style.display = hasSelection ? 'none' : 'block';

        // Update selected panel visibility and content
        if (hasSelection) {
            // Find the matching quiz card and highlight it
            catalogCards.forEach(card => {
                if (card.dataset.language === selectedLanguage && card.dataset.level === selectedLevel) {
                    // Extract quiz info from the card
                    const title = card.querySelector('h4')?.textContent || 'Selected Track';
                    const description = card.querySelector('p')?.textContent || '';
                    const durationText = card.querySelector('[data-duration]')?.textContent || 
                                        card.textContent.match(/(\d+)m/)?.[1] || '0';
                    const questionsText = card.querySelector('[data-questions]')?.textContent || 
                                         card.textContent.match(/(\d+)Q/)?.[1] || '0';
                    
                    // Parse duration and questions count from catalog card
                    const meta = card.querySelector('.catalog-meta');
                    const durationMatch = meta?.textContent.match(/(\d+)/)?.[1] || '0';
                    const questionsMatch = meta?.textContent.match(/(\d+)(?=Q)/)?.[1] || '0';

                    // Update selected panel
                    selectedPanel.innerHTML = `
                        <div class="quiz-meta">
                            <div>
                                <h3>${title}</h3>
                                <p>${description}</p>
                            </div>
                            <div class="meta-stats">
                                <span>⏱ ${durationMatch} mins</span>
                                <span>📋 ${questionsMatch} questions</span>
                            </div>
                        </div>
                    `;
                }
            });

            // Enable submit button
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.style.opacity = '1';
            }
        } else {
            // Show default message
            selectedPanel.innerHTML = '<p class="missing-quiz">Select a language and level to begin.</p>';
            
            // Disable submit button
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.style.opacity = '0.5';
            }
        }
    };

    /**
     * Attach event listeners to language pills
     */
    languageLabels.forEach(label => {
        label.addEventListener('click', (e) => {
            updateLanguage(label.dataset.language);
        });
    });

    /**
     * Attach event listeners to level badges
     */
    levelLabels.forEach(label => {
        label.addEventListener('click', (e) => {
            updateLevel(label.dataset.level);
        });
    });

    /**
     * Also handle form submission - ensure both are selected
     */
    if (form) {
        form.addEventListener('submit', (e) => {
            if (!selectedLanguage || !selectedLevel) {
                e.preventDefault();
                flash('Please select both a language and difficulty level.', 'error');
            }
        });
    }

    // Initialize UI on page load
    updateUI();
}

/**
 * Fisher-Yates Shuffle Algorithm
 * Randomizes an array in-place efficiently
 * @param {Array} array - The array to shuffle
 * @returns {Array} - The shuffled array (same reference)
 */
function fisherYatesShuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        // Swap elements at positions i and j
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

/**
 * Create a shallow copy of an array and shuffle it
 * Does NOT modify the original array
 * @param {Array} array - The array to shuffle
 * @returns {Array} - A new shuffled array
 */
function getShuffledCopy(array) {
    if (!Array.isArray(array)) {
        return array;
    }
    const copy = [...array];
    return fisherYatesShuffle(copy);
}
