// Main Home Page JavaScript

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('HomeDecorator loaded');
    initializeAnimations();
});

// Initialize animations on scroll
function initializeAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-slide-in');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.group').forEach(el => {
        observer.observe(el);
    });
}

// Toggle mobile menu
function toggleMobileMenu() {
    const nav = document.querySelector('nav');
    nav.classList.toggle('hidden');
}

// Show demo video
function showDemo() {
    alert('Demo video would play here!');
}

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({behavior: 'smooth'});
        }
    });
});

// Add animation class to feature cards when they come into view
window.addEventListener('scroll', () => {
    const cards = document.querySelectorAll('.group');
    cards.forEach(card => {
        const rect = card.getBoundingClientRect();
        if (rect.top < window.innerHeight - 100) {
            card.classList.add('animate-slide-in');
        }
    });
});

// API Helper
const API = {
    baseURL: '/api',
    
    async request(endpoint, method = 'GET', data = null) {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
            }
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, options);
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            return { error: 'Network error' };
        }
    },

    // User endpoints
    async getOrCreateDefaultUser() {
        return this.request('/users', 'GET');
    },

    // Furniture endpoints
    async getAllFurniture() {
        return this.request('/furniture/all', 'GET');
    },

    async getFurnitureByRoom(roomType) {
        return this.request(`/furniture/room/${roomType}`, 'GET');
    },

    async searchFurniture(query, roomType = null) {
        const url = `/furniture/search?q=${query}${roomType ? `&room_type=${roomType}` : ''}`;
        return this.request(url, 'GET');
    }
};

// localStorage helpers
const Storage = {
    setUser(user) {
        localStorage.setItem('user', JSON.stringify(user));
    },

    getUser() {
        return JSON.parse(localStorage.getItem('user') || '{}');
    },

    setCurrentDesign(design) {
        localStorage.setItem('currentDesign', JSON.stringify(design));
    },

    getCurrentDesign() {
        return JSON.parse(localStorage.getItem('currentDesign') || '{}');
    }
};

// Initialize default user
(async () => {
    const userResponse = await API.getOrCreateDefaultUser();
    if (userResponse.success && userResponse.user) {
        Storage.setUser(userResponse.user);
    }
})();
