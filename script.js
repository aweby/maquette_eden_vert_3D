/* ===================================================
   ProNuisibles – JavaScript
   =================================================== */

// === NAV SCROLL ===
const header = document.getElementById('header');
window.addEventListener('scroll', () => {
  header.classList.toggle('scrolled', window.scrollY > 40);
}, { passive: true });

// === MOBILE NAV TOGGLE ===
const navToggle = document.getElementById('navToggle');
const mobileMenu = document.getElementById('mobileMenuOverlay');
const mmBackdrop = document.getElementById('mmBackdrop');

function closeMenu() {
  if (!mobileMenu) return;
  mobileMenu.classList.remove('open');
  mmBackdrop.classList.remove('visible');
  // Attendre la fin de la transition backdrop avant de cacher
  setTimeout(() => { mmBackdrop.classList.remove('open'); }, 350);
  mobileMenu.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
  navToggle.querySelectorAll('span').forEach(s => s.removeAttribute('style'));
}

function openMenu() {
  if (!mobileMenu) return;
  mmBackdrop.classList.add('open');
  requestAnimationFrame(() => {
    mmBackdrop.classList.add('visible');
    mobileMenu.classList.add('open');
  });
  mobileMenu.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
  const spans = navToggle.querySelectorAll('span');
  spans[0].style.transform = 'rotate(45deg) translate(5px,5px)';
  spans[1].style.opacity = '0';
  spans[2].style.transform = 'rotate(-45deg) translate(5px,-5px)';
}

navToggle?.addEventListener('click', () => {
  mobileMenu.classList.contains('open') ? closeMenu() : openMenu();
});

// Fermer sur backdrop ou lien
mmBackdrop?.addEventListener('click', closeMenu);
mobileMenu?.addEventListener('click', (e) => {
  if (e.target.closest('#mobileMenuClose') || e.target.closest('a')) closeMenu();
});

// Fermer sur Escape
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeMenu(); });

// Sous-menu Prestations
function mmToggleSub(btn) {
  const isOpen = btn.getAttribute('aria-expanded') === 'true';
  const sub = document.getElementById('mmSubPrestations');
  btn.setAttribute('aria-expanded', isOpen ? 'false' : 'true');
  sub.classList.toggle('open', !isOpen);
}

// Fermer le sous-menu quand on clique sur un lien enfant
document.querySelectorAll('.mm-sub-item').forEach(a => {
  a.addEventListener('click', closeMenu);
});

/* =============================================
   HERO CANVAS – Animation nuisibles
   Particules + silhouettes qui se déplacent
   ============================================= */
(function initHeroCanvas() {
  const canvas = document.getElementById('heroCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  // Silhouettes SVG path des nuisibles (coordonnées normalisées 0–1 → canvas)
  // On dessine des formes stylisées minimalistes
  const PESTS = [
    // Rat – forme allongée avec queue
    {
      draw(cx, cy, size, angle, alpha) {
        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(angle);
        ctx.globalAlpha = alpha;
        ctx.fillStyle = '#EA5F0A';
        // Corps
        ctx.beginPath();
        ctx.ellipse(0, 0, size * 1.8, size * 0.7, 0, 0, Math.PI * 2);
        ctx.fill();
        // Tête
        ctx.beginPath();
        ctx.ellipse(size * 1.6, 0, size * 0.65, size * 0.55, 0.3, 0, Math.PI * 2);
        ctx.fill();
        // Queue (courbe)
        ctx.beginPath();
        ctx.moveTo(-size * 1.8, 0);
        ctx.quadraticCurveTo(-size * 2.8, -size * 1.2, -size * 3.5, -size * 0.4);
        ctx.strokeStyle = '#EA5F0A';
        ctx.lineWidth = size * 0.18;
        ctx.lineCap = 'round';
        ctx.globalAlpha = alpha * 0.7;
        ctx.stroke();
        // Oreille
        ctx.beginPath();
        ctx.arc(size * 1.3, -size * 0.55, size * 0.35, 0, Math.PI * 2);
        ctx.globalAlpha = alpha * 0.5;
        ctx.fillStyle = '#c44e07';
        ctx.fill();
        ctx.restore();
      },
      speed: 0.4, sizeRange: [6, 14]
    },
    // Cafard – forme ovale avec pattes
    {
      draw(cx, cy, size, angle, alpha) {
        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(angle);
        ctx.globalAlpha = alpha;
        ctx.fillStyle = '#EA5F0A';
        // Corps
        ctx.beginPath();
        ctx.ellipse(0, 0, size * 1.4, size * 0.75, 0, 0, Math.PI * 2);
        ctx.fill();
        // Tête
        ctx.beginPath();
        ctx.ellipse(size * 1.2, 0, size * 0.5, size * 0.45, 0, 0, Math.PI * 2);
        ctx.fill();
        // Pattes (3 de chaque côté)
        ctx.strokeStyle = '#EA5F0A';
        ctx.lineWidth = size * 0.12;
        ctx.lineCap = 'round';
        ctx.globalAlpha = alpha * 0.6;
        [-0.5, 0, 0.5].forEach(offset => {
          const bx = offset * size * 1.2;
          // haut
          ctx.beginPath(); ctx.moveTo(bx, -size * 0.6);
          ctx.lineTo(bx - size * 0.4, -size * 1.2); ctx.lineTo(bx - size * 0.8, -size * 0.9);
          ctx.stroke();
          // bas
          ctx.beginPath(); ctx.moveTo(bx, size * 0.6);
          ctx.lineTo(bx - size * 0.4, size * 1.2); ctx.lineTo(bx - size * 0.8, size * 0.9);
          ctx.stroke();
        });
        // Antennes
        ctx.globalAlpha = alpha * 0.5;
        ctx.beginPath(); ctx.moveTo(size * 1.5, -size * 0.2);
        ctx.quadraticCurveTo(size * 2.2, -size * 0.8, size * 2.8, -size * 0.3);
        ctx.stroke();
        ctx.beginPath(); ctx.moveTo(size * 1.5, size * 0.2);
        ctx.quadraticCurveTo(size * 2.2, size * 0.8, size * 2.8, size * 0.3);
        ctx.stroke();
        ctx.restore();
      },
      speed: 0.6, sizeRange: [5, 11]
    },
    // Araignée / punaise – corps rond avec 8 pattes
    {
      draw(cx, cy, size, angle, alpha) {
        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(angle);
        ctx.globalAlpha = alpha;
        ctx.fillStyle = '#c44e07';
        ctx.beginPath();
        ctx.arc(0, 0, size * 0.8, 0, Math.PI * 2);
        ctx.fill();
        // Tête
        ctx.fillStyle = '#EA5F0A';
        ctx.beginPath();
        ctx.arc(size * 0.9, 0, size * 0.45, 0, Math.PI * 2);
        ctx.fill();
        // 8 pattes
        ctx.strokeStyle = '#EA5F0A';
        ctx.lineWidth = size * 0.1;
        ctx.lineCap = 'round';
        ctx.globalAlpha = alpha * 0.55;
        for (let i = 0; i < 4; i++) {
          const a1 = (i / 3) * Math.PI * 0.8 - Math.PI * 0.4;
          const a2 = a1 - 0.4;
          ctx.beginPath();
          ctx.moveTo(Math.cos(a1 + Math.PI) * size * 0.7, Math.sin(a1 + Math.PI) * size * 0.7);
          ctx.lineTo(Math.cos(a1 + Math.PI) * size * 1.6, Math.sin(a1 + Math.PI) * size * 1.3);
          ctx.lineTo(Math.cos(a2 + Math.PI) * size * 2.2, Math.sin(a2 + Math.PI) * size * 1.6);
          ctx.stroke();
          ctx.beginPath();
          ctx.moveTo(Math.cos(a1) * size * 0.7, Math.sin(a1) * size * 0.7);
          ctx.lineTo(Math.cos(a1) * size * 1.6, Math.sin(a1) * size * 1.3);
          ctx.lineTo(Math.cos(a2) * size * 2.2, Math.sin(a2) * size * 1.6);
          ctx.stroke();
        }
        ctx.restore();
      },
      speed: 0.35, sizeRange: [4, 9]
    }
  ];

  // Particules lumineuses
  class Particle {
    constructor(w, h) { this.reset(w, h); }
    reset(w, h) {
      this.x = Math.random() * w;
      this.y = Math.random() * h;
      this.r = Math.random() * 1.5 + 0.3;
      this.alpha = Math.random() * 0.4 + 0.05;
      this.vx = (Math.random() - 0.5) * 0.3;
      this.vy = -(Math.random() * 0.4 + 0.1);
      this.life = 0;
      this.maxLife = Math.random() * 200 + 100;
    }
    update(w, h) {
      this.x += this.vx;
      this.y += this.vy;
      this.life++;
      if (this.life > this.maxLife || this.y < 0) this.reset(w, h);
    }
    draw(ctx) {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(234,95,10,${this.alpha * (1 - this.life / this.maxLife)})`;
      ctx.fill();
    }
  }

  // Insectes se déplaçant
  class PestSprite {
    constructor(w, h) {
      const idx = Math.floor(Math.random() * PESTS.length);
      this.type = PESTS[idx];
      this.reset(w, h, true);
    }
    reset(w, h, init = false) {
      this.w = w; this.h = h;
      const [minS, maxS] = this.type.sizeRange;
      this.size = Math.random() * (maxS - minS) + minS;
      this.speed = this.type.speed * (Math.random() * 0.8 + 0.6);
      this.alpha = Math.random() * 0.12 + 0.04;  // très discret
      // Départ depuis un bord aléatoire
      const edge = Math.floor(Math.random() * 4);
      if (edge === 0) { this.x = Math.random() * w; this.y = h + 20; }
      else if (edge === 1) { this.x = -20; this.y = Math.random() * h; }
      else if (edge === 2) { this.x = w + 20; this.y = Math.random() * h; }
      else { this.x = Math.random() * w; this.y = -20; }
      if (init) { this.x = Math.random() * w; this.y = Math.random() * h; }
      // Cible aléatoire
      this.tx = Math.random() * w;
      this.ty = Math.random() * h;
      this.angle = Math.atan2(this.ty - this.y, this.tx - this.x);
      // Légère sinuosité
      this.sinOffset = Math.random() * Math.PI * 2;
      this.sinAmp = Math.random() * 12 + 4;
      this.sinFreq = Math.random() * 0.02 + 0.01;
      this.t = 0;
    }
    update() {
      const dx = this.tx - this.x;
      const dy = this.ty - this.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 40) {
        // Nouvelle cible
        this.tx = Math.random() * this.w;
        this.ty = Math.random() * this.h;
      }
      this.angle = Math.atan2(dy, dx);
      // Déplacement sinusoïdal perpendiculaire
      const perpX = Math.cos(this.angle + Math.PI / 2);
      const perpY = Math.sin(this.angle + Math.PI / 2);
      const sin = Math.sin(this.t * this.sinFreq * 60 + this.sinOffset) * this.sinAmp * 0.02;
      this.x += Math.cos(this.angle) * this.speed + perpX * sin;
      this.y += Math.sin(this.angle) * this.speed + perpY * sin;
      this.t++;
      // Hors écran → reset
      if (this.x < -80 || this.x > this.w + 80 || this.y < -80 || this.y > this.h + 80) {
        this.reset(this.w, this.h);
      }
    }
    draw(ctx) {
      this.type.draw(this.x, this.y, this.size, this.angle, this.alpha);
    }
  }

  let W, H, particles, sprites, raf;

  function resize() {
    W = canvas.width = canvas.offsetWidth;
    H = canvas.height = canvas.offsetHeight;
    if (sprites) sprites.forEach(s => { s.w = W; s.h = H; });
  }

  function init() {
    resize();
    particles = Array.from({ length: 80 }, () => new Particle(W, H));
    // Moins de sprites sur mobile pour les perfs
    const count = window.innerWidth < 768 ? 8 : 18;
    sprites = Array.from({ length: count }, () => new PestSprite(W, H));
  }

  function loop() {
    ctx.clearRect(0, 0, W, H);

    // Fond très sombre
    ctx.fillStyle = '#0a0a0a';
    ctx.fillRect(0, 0, W, H);

    // Lueur centrale orange très subtile
    const grd = ctx.createRadialGradient(W * 0.62, H * 0.45, 0, W * 0.62, H * 0.45, W * 0.55);
    grd.addColorStop(0, 'rgba(234,95,10,0.04)');
    grd.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = grd;
    ctx.fillRect(0, 0, W, H);

    // Particules
    particles.forEach(p => { p.update(W, H); p.draw(ctx); });

    // Insectes
    sprites.forEach(s => { s.update(); s.draw(ctx); });

    raf = requestAnimationFrame(loop);
  }

  // Pause quand non visible
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) cancelAnimationFrame(raf);
    else raf = requestAnimationFrame(loop);
  });

  window.addEventListener('resize', resize, { passive: true });
  init();
  loop();
})();

/* =============================================
   CANVAS HERO 3 (même logique, canvas dédié)
   ============================================= */
(function initHeroCanvas3() {
  const canvas = document.getElementById('heroCanvas3');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let W, H, raf3;

  function resize() {
    W = canvas.width  = canvas.offsetWidth;
    H = canvas.height = canvas.offsetHeight;
  }

  function loop() {
    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = 'rgba(8,8,8,0)';
    ctx.fillRect(0, 0, W, H);
    raf3 = requestAnimationFrame(loop);
  }

  // Particules simples
  const pts = Array.from({ length: 60 }, () => ({
    x: Math.random() * 2000,
    y: Math.random() * 1200,
    r: Math.random() * 1.2 + 0.3,
    a: Math.random() * 0.25 + 0.03,
    vy: -(Math.random() * 0.3 + 0.05),
    vx: (Math.random() - 0.5) * 0.15,
  }));

  function loop2() {
    W = canvas.offsetWidth;
    H = canvas.offsetHeight;
    canvas.width = W;
    canvas.height = H;
    ctx.clearRect(0, 0, W, H);
    pts.forEach(p => {
      p.x += p.vx; p.y += p.vy;
      if (p.y < -10) { p.y = H + 10; p.x = Math.random() * W; }
      ctx.beginPath();
      ctx.arc(p.x % W, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(234,95,10,${p.a})`;
      ctx.fill();
    });
    requestAnimationFrame(loop2);
  }

  resize();
  window.addEventListener('resize', resize, { passive: true });
  loop2();
})();

/* Barre de progression hero3 */
const fillBar = document.querySelector('.h3-counter-fill');
if (fillBar) {
  const obs = new IntersectionObserver(([e]) => {
    if (e.isIntersecting) { fillBar.classList.add('animated'); obs.disconnect(); }
  }, { threshold: 0.5 });
  obs.observe(fillBar);
}

/* =============================================
   SCROLL REVEAL
   ============================================= */
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) entry.target.classList.add('visible');
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

/* =============================================
   ANIMATED COUNTERS
   ============================================= */
function animateCounter(el, target, duration = 2000) {
  let start = 0;
  const step = target / (duration / 16);
  const timer = setInterval(() => {
    start += step;
    if (start >= target) {
      el.textContent = target.toLocaleString('fr-FR');
      clearInterval(timer);
    } else {
      el.textContent = Math.floor(start).toLocaleString('fr-FR');
    }
  }, 16);
}

const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting && !entry.target.dataset.counted) {
      entry.target.dataset.counted = 'true';
      animateCounter(entry.target, parseInt(entry.target.dataset.count));
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('[data-count]').forEach(el => counterObserver.observe(el));

/* =============================================
   FAQ ACCORDION
   ============================================= */
function toggleFaq(button) {
  const item = button.parentElement;
  const isOpen = item.classList.contains('open');
  document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
  if (!isOpen) item.classList.add('open');
}

/* =============================================
   MODAL NUISIBLES
   ============================================= */
// Mise à jour brand dans les données modales
const BRAND = 'Eden Vert 3D';

const modalData = {
  rats: {
    emoji: '🐀',
    title: 'Dératisation – Rats & Souris',
    description: 'Les rats et souris causent des dégâts matériels importants et présentent des risques sanitaires graves. Ils se reproduisent à une vitesse alarmante.',
    signes: ['Crottes le long des murs', 'Bruits nocturnes (grattements, piétinements)', 'Câbles et boiseries rongés', 'Odeur forte et persistante', 'Nids faits de matières diverses'],
    solution: 'Appâts rodenticides homologués en points stratégiques + colmatage des points d\'entrée pour éviter toute réinfestation. Suivi sur 3 mois inclus.',
    garantie: '3 mois'
  },
  cafards: {
    emoji: '🪳',
    title: 'Désinsectisation – Cafards & Blattes',
    description: 'Les cafards prolifèrent très rapidement, contaminent les aliments et déclenchent des allergies. Ils véhiculent de nombreuses bactéries dangereuses.',
    signes: ['Cafards visibles la nuit', 'Odeur huileux/fétide caractéristique', 'Crottes ressemblant à du café moulu', 'Œufs (oothèques) derrière les appareils', 'Traces sombres le long des plinthes'],
    solution: 'Gel insecticide professionnel posé en zones clés + traitement liquide si nécessaire. Protocole 2 passages pour éliminer les nouvelles éclosions.',
    garantie: '3 mois'
  },
  punaises: {
    emoji: '🛏️',
    title: 'Désinsectisation – Punaises de lit',
    description: 'Les punaises de lit sont extrêmement résistantes et impossibles à éliminer sans traitement professionnel. Elles piquent la nuit et causent des troubles importants.',
    signes: ['Piqûres en ligne sur le corps', 'Taches de sang sur les draps', 'Points noirs sur le matelas et cadre', 'Odeur sucrée caractéristique', 'Mues (exuvies) translucides'],
    solution: 'Traitement thermique (56°C) et/ou traitement chimique en 2 passages. Rapport d\'intervention certifié remis à l\'issue.',
    garantie: '3 mois'
  },
  frelons: {
    emoji: '🐝',
    title: 'Désinsectisation – Frelons & Guêpes',
    description: 'Les nids de frelons représentent un danger réel pour les personnes allergiques. N\'essayez JAMAIS de les détruire vous-même.',
    signes: ['Va-et-vient intense d\'insectes', 'Nid gris (papier) sous avant-toit, en arbre ou comble', 'Bourdonnement fort et continu', 'Frelons asiatiques près des fleurs'],
    solution: 'Destruction du nid avec EPI certifié. Insecticide professionnel injecté directement dans le nid. Intervention 100% sécurisée.',
    garantie: '1 mois'
  },
  fourmis: {
    emoji: '🐜',
    title: 'Désinsectisation – Fourmis',
    description: 'Les fourmis envahissent les cuisines et contaminent les denrées. Certaines espèces (charpentières) endommagent sérieusement les boiseries.',
    signes: ['Files de fourmis dans la cuisine', 'Présence constante malgré le nettoyage', 'Sciure de bois (fourmis charpentières)', 'Fourmis près des zones humides'],
    solution: 'Gel appât sucré posé sur les pistes. Les ouvrières rapportent l\'appât à la reine, éliminant la colonie depuis la source. Résultat en 5–10 jours.',
    garantie: '3 mois'
  },
  moustiques: {
    emoji: '🦟',
    title: 'Désinsectisation – Moustiques',
    description: 'Les moustiques perturbent le quotidien et peuvent véhiculer des maladies. Le moustique tigre, espèce invasive, est désormais présent en Île-de-France.',
    signes: ['Piqûres répétées au coucher', 'Bourdonnement dans la chambre', 'Eaux stagnantes sur la propriété', 'Présence de larves dans les récipients d\'eau'],
    solution: 'Nébulisation professionnelle ULV dans les zones d\'activité + traitement des gîtes larvaires (eaux stagnantes, regards). Résultat immédiat et protection durable.',
    garantie: '2 mois'
  },
  pigeons: {
    emoji: '🐦',
    title: 'Dépigeonnisation – Pigeons & Nuisibles volants',
    description: 'Les pigeons souillent les bâtiments, propagent des maladies et dégradent les façades. Leurs fientes sont corrosives et représentent un risque sanitaire réel.',
    signes: ['Accumulation de fientes sur les rebords', 'Nids sous les toits ou dans les gouttières', 'Dégradation des façades et matériaux', 'Nuisances sonores répétées'],
    solution: 'Pose de pics inox, filets tendus, répulsifs gélatineux et systèmes électriques dissuasifs. Protection définitive et esthétique, respectueuse des oiseaux.',
    garantie: '6 mois'
  },
  chenilles: {
    emoji: '🐛',
    title: 'Traitement – Chenilles processionnaires',
    description: 'Les chenilles du pin et du chêne sont un danger réel : leurs poils urticants provoquent des réactions allergiques graves chez l\'homme et sont mortels pour les animaux.',
    signes: ['Nids blancs soyeux dans les pins ou chênes', 'Processions de chenilles en file', 'Défoliation de l\'arbre', 'Irritations cutanées après contact'],
    solution: 'Retrait manuel des nids avec EPI complet + injection de Bacillus thuringiensis (traitement biologique). Intervention préventive possible en automne pour stopper l\'infestation.',
    garantie: '1 saison'
  }
};

function openModal(type) {
  const data = modalData[type];
  if (!data) return;
  document.getElementById('modalContent').innerHTML = `
    <div class="modal-emoji">${data.emoji}</div>
    <h3>${data.title}</h3>
    <p>${data.description}</p>
    <h4>Signes d'infestation</h4>
    <ul>${data.signes.map(s => `<li>${s}</li>`).join('')}</ul>
    <h4>Notre solution</h4>
    <p>${data.solution}</p>
    <div style="display:inline-flex;align-items:center;gap:8px;background:rgba(234,95,10,0.1);color:#EA5F0A;border:1px solid rgba(234,95,10,0.25);padding:8px 16px;border-radius:50px;font-size:0.82rem;font-weight:600;margin-top:4px;">
      🛡️ Garantie ${data.garantie} incluse
    </div>
    <div class="modal-cta">
      <a href="tel:+33123456789" class="btn-primary" style="justify-content:center;border-radius:50px;padding:14px 20px;">📞 Appeler maintenant</a>
      <a href="#contact" onclick="closeModal()" style="flex:1;display:flex;align-items:center;justify-content:center;border:1px solid #333;border-radius:50px;padding:14px 20px;font-weight:600;color:#ccc;font-size:0.9rem;transition:.2s;">Devis gratuit</a>
    </div>
  `;
  document.getElementById('modalOverlay').classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  document.getElementById('modalOverlay').classList.remove('active');
  document.body.style.overflow = '';
}

document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

/* =============================================
   CONTACT FORM
   ============================================= */
function handleSubmit(e) {
  e.preventDefault();
  const btn = e.target.querySelector('.btn-form-submit');
  btn.disabled = true;
  btn.querySelector('span').textContent = 'Envoi en cours…';
  setTimeout(() => {
    e.target.style.display = 'none';
    document.getElementById('formSuccess').classList.add('show');
  }, 1200);
}

/* =============================================
   SMOOTH SCROLL
   ============================================= */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - 80, behavior: 'smooth' });
    }
  });
});

