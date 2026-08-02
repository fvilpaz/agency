/* =====================================================================
   QREA'S AGENCY — Interacciones
   ===================================================================== */
(function () {
  'use strict';
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Header sticky ---------- */
  var header = document.getElementById('header');
  if (header) {
    function onScroll() {
      if (window.scrollY > 40) header.classList.add('is-stuck');
      else header.classList.remove('is-stuck');
    }
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- Menú móvil ---------- */
  var toggle = document.getElementById('navToggle');
  var nav = document.getElementById('nav');
  if (toggle && nav) {
    function closeNav() {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Abrir menú');
      document.body.classList.remove('no-scroll');
    }
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
      document.body.classList.toggle('no-scroll', open);
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) closeNav();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) { closeNav(); toggle.focus(); }
    });
  }

  /* ---------- Reveal on scroll ---------- */
  var reveals = Array.prototype.slice.call(document.querySelectorAll('.reveal'));
  if (reduceMotion || !('IntersectionObserver' in window)) {
    reveals.forEach(function (el) { el.classList.add('is-visible'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add('is-visible'); io.unobserve(entry.target); }
      });
    }, { threshold: 0.14, rootMargin: '0px 0px -8% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Scrollspy (nav activo) ---------- */
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.nav__link'));
  var sections = navLinks
    .map(function (l) { var id = l.getAttribute('href'); return id && id.charAt(0) === '#' ? document.querySelector(id) : null; })
    .filter(Boolean);
  if ('IntersectionObserver' in window && sections.length) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var id = '#' + entry.target.id;
          navLinks.forEach(function (l) { l.classList.toggle('is-active', l.getAttribute('href') === id); });
        }
      });
    }, { threshold: 0.5 });
    sections.forEach(function (s) { spy.observe(s); });
  }

  /* ---------- Año footer ---------- */
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  /* ---------- Formulario (validación + envío placeholder) ---------- */
  var form = document.getElementById('contactForm');
  var msg = document.getElementById('formMsg');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      msg.className = 'form__msg';
      msg.textContent = '';

      if (!form.checkValidity()) {
        var firstInvalid = form.querySelector(':invalid');
        msg.textContent = 'Revisa los campos obligatorios marcados con *.';
        msg.classList.add('err');
        if (firstInvalid) firstInvalid.focus();
        return;
      }

      var fd = new FormData(form);
      var data = {};
      fd.forEach(function(value, key) {
        if (key === 'mejora') {
          if (!data.mejoras) data.mejoras = [];
          data.mejoras.push(value);
        } else {
          data[key] = value;
        }
      });
      if (!data.mejoras) data.mejoras = [];
      data.privacidad = !!fd.get('consent');

      fetch('/contacto', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      .then(function(r) { return r.json(); })
      .then(function(res) {
        if (res.ok) {
          msg.textContent = res.message;
          msg.classList.add('ok');
          form.reset();
        } else {
          msg.textContent = 'Ha ocurrido un error. Por favor inténtalo de nuevo.';
          msg.classList.add('err');
        }
      })
      .catch(function() {
        msg.textContent = 'Error de conexión. Por favor inténtalo de nuevo.';
        msg.classList.add('err');
      });
    });
  }

  /* ---------- WhatsApp flotante ----------
     Para activarlo: define el número real abajo y se mostrará el botón. */
  var WHATSAPP_NUMBER = ''; // ej. '34600000000' (sin +, sin espacios)
  if (WHATSAPP_NUMBER) {
    var wa = document.getElementById('waFloat');
    if (wa) {
      var text = encodeURIComponent('Hola, quiero hablar sobre mi negocio de hostelería y conocer cómo puede ayudarme QREA\'S Agency.');
      wa.href = 'https://wa.me/' + WHATSAPP_NUMBER.replace(/\s/g, '') + '?text=' + text;
      wa.classList.add('is-active');
    }
  }

  /* ---------- Custom Cursor ---------- */
  var cursorDot = document.querySelector('.cursor-dot');
  var cursorOutline = document.querySelector('.cursor-outline');
  if (cursorDot && cursorOutline && window.matchMedia("(pointer: fine)").matches) {
    document.body.classList.add('has-custom-cursor');
    window.addEventListener('mousemove', function(e) {
      cursorDot.style.left = e.clientX + 'px';
      cursorDot.style.top = e.clientY + 'px';
      
      // Añadimos un pequeño delay al outline usando setTimeout para un efecto más fluido
      setTimeout(function() {
        cursorOutline.style.left = e.clientX + 'px';
        cursorOutline.style.top = e.clientY + 'px';
      }, 50);
    });

    document.querySelectorAll('a, button, input, textarea, select').forEach(function(el) {
      el.addEventListener('mouseenter', function() {
        cursorDot.style.transform = 'translate(-50%, -50%) scale(1.5)';
        cursorDot.style.backgroundColor = 'transparent';
        cursorDot.style.border = '1px solid var(--gold)';
        cursorOutline.style.transform = 'translate(-50%, -50%) scale(1.5)';
        cursorOutline.style.backgroundColor = 'rgba(181, 150, 91, 0.15)';
      });
      el.addEventListener('mouseleave', function() {
        cursorDot.style.transform = 'translate(-50%, -50%) scale(1)';
        cursorDot.style.backgroundColor = 'var(--gold)';
        cursorDot.style.border = 'none';
        cursorOutline.style.transform = 'translate(-50%, -50%) scale(1)';
        cursorOutline.style.backgroundColor = 'transparent';
      });
    });
  }
})();
