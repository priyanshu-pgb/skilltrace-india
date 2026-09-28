/**
 * SkillBridge - Animation & Micro-Interactions System
 * Honors prefers-reduced-motion
 */

document.addEventListener('DOMContentLoaded', () => {
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  initCircularProgress(prefersReducedMotion);
  initCountUp(prefersReducedMotion);
  initCardStagger(prefersReducedMotion);
});

/**
 * Animated SVG Circular Progress Rings
 */
function initCircularProgress(reducedMotion) {
  const circles = document.querySelectorAll('.circle-bar');
  circles.forEach(circle => {
    const score = parseFloat(circle.dataset.score || 0);
    const radius = circle.r.baseVal.value;
    const circumference = 2 * Math.PI * radius;

    circle.style.strokeDasharray = `${circumference} ${circumference}`;
    circle.style.strokeDashoffset = circumference;

    const offset = circumference - (score / 100) * circumference;

    if (reducedMotion) {
      circle.style.strokeDashoffset = offset;
    } else {
      setTimeout(() => {
        circle.style.strokeDashoffset = offset;
      }, 200);
    }
  });
}

/**
 * Smooth Count-Up for Stat Numbers
 */
function initCountUp(reducedMotion) {
  const countElements = document.querySelectorAll('.count-up');
  
  countElements.forEach(el => {
    const target = parseFloat(el.dataset.target || el.textContent || 0);
    const isFloat = el.dataset.isFloat === 'true';
    const suffix = el.dataset.suffix || '';
    const prefix = el.dataset.prefix || '';

    if (reducedMotion) {
      el.textContent = `${prefix}${isFloat ? target.toFixed(1) : Math.round(target)}${suffix}`;
      return;
    }

    let start = 0;
    const duration = 1200; // ms
    const stepTime = 20; // 50 fps
    const totalSteps = duration / stepTime;
    const increment = target / totalSteps;

    const timer = setInterval(() => {
      start += increment;
      if (start >= target) {
        start = target;
        clearInterval(timer);
      }
      el.textContent = `${prefix}${isFloat ? start.toFixed(1) : Math.round(start)}${suffix}`;
    }, stepTime);
  });
}

/**
 * Card Stagger Reveal
 */
function initCardStagger(reducedMotion) {
  if (reducedMotion) return;

  const cards = document.querySelectorAll('.stagger-fade');
  cards.forEach((card, idx) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(12px)';
    card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';

    setTimeout(() => {
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, 80 * idx);
  });
}
