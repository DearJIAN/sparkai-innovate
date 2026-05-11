/**
 * SparkAI Skill Test Landing Page - Interactive Script
 * Skills applied: frontend-design, ui-ux-pro-max, design-taste-frontend
 */

(function () {
  'use strict';

  // ============================================
  // Smooth Scroll to Section
  // ============================================
  window.scrollToSection = function (sectionId) {
    const element = document.getElementById(sectionId);
    if (!element) return;

    const offset = 80;
    const elementPosition = element.getBoundingClientRect().top + window.pageYOffset;
    const offsetPosition = elementPosition - offset;

    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });
  };

  // ============================================
  // Skill Card Interaction
  // ============================================
  function initSkillCards() {
    const cards = document.querySelectorAll('.skill-card');

    cards.forEach(function (card) {
      card.addEventListener('click', function () {
        const isActive = card.classList.contains('active');

        // Toggle active state
        if (isActive) {
          card.classList.remove('active');
        } else {
          card.classList.add('active');
        }

        // Add a subtle scale feedback on click
        card.style.transform = 'scale(0.98)';
        setTimeout(function () {
          card.style.transform = '';
        }, 150);
      });

      // Keyboard accessibility
      card.setAttribute('tabindex', '0');
      card.setAttribute('role', 'button');
      card.setAttribute('aria-pressed', 'false');

      card.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          card.click();
        }
      });

      card.addEventListener('focus', function () {
        card.style.outline = '2px solid var(--color-accent)';
        card.style.outlineOffset = '4px';
      });

      card.addEventListener('blur', function () {
        card.style.outline = '';
        card.style.outlineOffset = '';
      });
    });
  }

  // ============================================
  // Scroll Reveal Animation (IntersectionObserver)
  // ============================================
  function initScrollReveal() {
    const revealElements = document.querySelectorAll('.skill-card, .verify-item, .section-header');

    revealElements.forEach(function (el) {
      el.classList.add('reveal');
    });

    const observerOptions = {
      root: null,
      rootMargin: '0px 0px -50px 0px',
      threshold: 0.1
    };

    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    revealElements.forEach(function (el) {
      observer.observe(el);
    });
  }

  // ============================================
  // Navbar Scroll Effect
  // ============================================
  function initScrollEffects() {
    let lastScrollY = window.scrollY;
    let ticking = false;

    function updateScrollEffects() {
      const scrollY = window.scrollY;

      // Add subtle parallax to hero background
      const heroBg = document.querySelector('.hero-bg');
      if (heroBg && scrollY < window.innerHeight) {
        heroBg.style.transform = 'translateY(' + (scrollY * 0.3) + 'px)';
      }

      lastScrollY = scrollY;
      ticking = false;
    }

    window.addEventListener('scroll', function () {
      if (!ticking) {
        requestAnimationFrame(updateScrollEffects);
        ticking = true;
      }
    }, { passive: true });
  }

  // ============================================
  // Button Ripple Effect
  // ============================================
  function initRippleEffect() {
    const buttons = document.querySelectorAll('.btn');

    buttons.forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        const rect = btn.getBoundingClientRect();
        const ripple = document.createElement('span');
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        ripple.style.cssText = [
          'position: absolute',
          'width: ' + size + 'px',
          'height: ' + size + 'px',
          'left: ' + x + 'px',
          'top: ' + y + 'px',
          'background: rgba(255,255,255,0.3)',
          'border-radius: 50%',
          'transform: scale(0)',
          'animation: rippleEffect 0.6s ease-out',
          'pointer-events: none'
        ].join(';');

        btn.style.position = 'relative';
        btn.style.overflow = 'hidden';
        btn.appendChild(ripple);

        setTimeout(function () {
          ripple.remove();
        }, 600);
      });
    });

    // Add ripple keyframes dynamically
    const style = document.createElement('style');
    style.textContent = [
      '@keyframes rippleEffect {',
      '  to { transform: scale(2.5); opacity: 0; }',
      '}'
    ].join('\n');
    document.head.appendChild(style);
  }

  // ============================================
  // Verify Item Hover Enhancement
  // ============================================
  function initVerifyItems() {
    const items = document.querySelectorAll('.verify-item');

    items.forEach(function (item, index) {
      item.style.transitionDelay = (index * 50) + 'ms';
    });
  }

  // ============================================
  // Console Greeting
  // ============================================
  function initConsoleGreeting() {
    console.log('%c SparkAI Skill Test ', 'background: linear-gradient(135deg, #0ea5e9, #6366f1); color: #fff; font-size: 20px; font-weight: bold; padding: 10px 20px; border-radius: 8px;');
    console.log('%cSkills successfully loaded and applied.', 'color: #0ea5e9; font-size: 14px;');
    console.log('%cGenerated files: index.html, styles.css, script.js, DESIGN.md, SKILL_USAGE_LOG_TEST.md', 'color: #475569; font-size: 12px;');
  }

  // ============================================
  // Initialize All
  // ============================================
  function init() {
    initSkillCards();
    initScrollReveal();
    initScrollEffects();
    initRippleEffect();
    initVerifyItems();
    initConsoleGreeting();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
