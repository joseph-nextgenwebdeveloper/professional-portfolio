/* site.js - popups, experience tabs, contact/request switch, WhatsApp send, nav scroll-spy.
   Plain JS, no dependencies. The page still reads fine if this fails to load. */
(function () {
    'use strict';

    /* ---------------- popups (projects + services) ---------------- */
    var openOverlay = null;
    var lastTrigger = null;

    function openModal(overlay, trigger) {
        if (openOverlay) closeModal(true);
        openOverlay = overlay;
        lastTrigger = trigger || null;
        overlay.classList.add('is-open');
        document.body.classList.add('modal-open');
        var closeBtn = overlay.querySelector('.modal-close');
        if (closeBtn) closeBtn.focus({ preventScroll: true });
    }

    function closeModal(silent) {
        if (!openOverlay) return;
        openOverlay.classList.remove('is-open');
        document.body.classList.remove('modal-open');
        var wasProject = openOverlay.id.indexOf('project-') === 0;
        openOverlay = null;
        if (lastTrigger && !silent) { try { lastTrigger.focus({ preventScroll: true }); } catch (e) {} }
        lastTrigger = null;
        if (wasProject && !silent && location.hash.indexOf('#project-') === 0 && history.replaceState) {
            history.replaceState(null, '', location.pathname + location.search);
        }
    }

    document.addEventListener('click', function (e) {
        var trigger = e.target.closest('[data-modal-open]');
        if (trigger) {
            var overlay = document.getElementById(trigger.getAttribute('data-modal-open'));
            if (overlay) { e.preventDefault(); openModal(overlay, trigger); }
            return;
        }
        if (openOverlay && (e.target === openOverlay || e.target.closest('.modal-close'))) closeModal();
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeModal();
    });

    /* project popup: click a small image to view it in the main area */
    document.addEventListener('click', function (e) {
        var thumb = e.target.closest('.pm-thumb');
        if (!thumb) return;
        var card = thumb.closest('.project-modal');
        var main = card && card.querySelector('[data-pm-main]');
        if (!main) return;
        main.src = thumb.getAttribute('data-full');
        card.querySelectorAll('.pm-thumb').forEach(function (t) { t.classList.toggle('is-active', t === thumb); });
    });

    /* /projects/<slug>/ redirects to /projects/#project-<slug> -> open that popup */
    function openFromHash() {
        var h = location.hash;
        if (h.indexOf('#project-') !== 0) return;
        var overlay = document.getElementById(h.slice(1));
        if (overlay && overlay.classList.contains('modal-overlay')) openModal(overlay, null);
    }
    window.addEventListener('hashchange', openFromHash);
    openFromHash();

    /* ---------------- experience tabs ---------------- */
    document.querySelectorAll('[data-tabs]').forEach(function (root) {
        var rail = root.querySelector('.career-rail');
        var tabs = Array.prototype.slice.call(root.querySelectorAll('.career-tab'));
        var panels = Array.prototype.slice.call(root.querySelectorAll('.career-panel'));
        if (!tabs.length) return;

        function activate(tab, focus) {
            var target = tab.getAttribute('data-panel');
            tabs.forEach(function (t) {
                var on = t === tab;
                t.classList.toggle('is-active', on);
                t.setAttribute('aria-selected', on ? 'true' : 'false');
                t.tabIndex = on ? 0 : -1;
            });
            panels.forEach(function (p) { p.classList.toggle('is-active', p.id === target); });
            if (focus) tab.focus({ preventScroll: true });
            if (rail && rail.scrollWidth > rail.clientWidth + 2) {   /* phone: rail scrolls sideways */
                rail.scrollTo({ left: tab.offsetLeft - 16, behavior: 'smooth' });
            }
        }

        tabs.forEach(function (tab, i) {
            tab.addEventListener('click', function () { activate(tab, false); });
            tab.addEventListener('keydown', function (e) {
                var step = (e.key === 'ArrowDown' || e.key === 'ArrowRight') ? 1 :
                           (e.key === 'ArrowUp' || e.key === 'ArrowLeft') ? -1 : 0;
                if (!step) return;
                e.preventDefault();
                activate(tabs[(i + step + tabs.length) % tabs.length], true);
            });
        });
        activate(tabs[0], false);
    });

    /* ---------------- connect: switch between Contact and Request a Project ---------------- */
    var connect = document.querySelector('[data-connect]');
    if (connect) {
        var cTabs = Array.prototype.slice.call(connect.querySelectorAll('[data-connect-tab]'));
        var cPanels = {
            contact: document.getElementById('connect-panel-contact'),
            request: document.getElementById('connect-panel-request')
        };

        var showConnect = function (which) {
            if (!cPanels[which]) return;
            cTabs.forEach(function (t) {
                var on = t.getAttribute('data-connect-tab') === which;
                t.classList.toggle('is-active', on);
                t.setAttribute('aria-selected', on ? 'true' : 'false');
            });
            Object.keys(cPanels).forEach(function (k) { cPanels[k].classList.toggle('is-active', k === which); });
        };

        var goConnect = function (which, smooth) {
            showConnect(which);
            connect.scrollIntoView({ behavior: smooth ? 'smooth' : 'auto', block: 'start' });
        };

        cTabs.forEach(function (t) {
            t.addEventListener('click', function () { showConnect(t.getAttribute('data-connect-tab')); });
        });

        /* any link to #connect-contact / #connect-request (hero, nav, footer, bottom bar) */
        document.addEventListener('click', function (e) {
            var a = e.target.closest('a[href*="#connect-"]');
            if (!a) return;
            var url;
            try { url = new URL(a.getAttribute('href'), location.href); } catch (err) { return; }
            if (url.pathname !== location.pathname) return;          /* other page: normal navigation */
            e.preventDefault();
            var which = url.hash.replace('#connect-', '');
            goConnect(which, true);
            if (history.replaceState) history.replaceState(null, '', url.hash);
        });

        var fromHash = function () {
            if (location.hash.indexOf('#connect-') === 0) goConnect(location.hash.replace('#connect-', ''), false);
        };
        window.addEventListener('hashchange', fromHash);
        fromHash();

        /* the server re-rendered this page with form errors: bring them into view */
        if (connect.getAttribute('data-has-errors')) goConnect(connect.getAttribute('data-connect'), false);

        /* ---------- send the same form on WhatsApp instead ---------- */
        var waNumber = (connect.getAttribute('data-whatsapp') || '').replace(/\D/g, '');
        connect.querySelectorAll('[data-wa-send]').forEach(function (btn) {
            btn.addEventListener('click', function () {
                var form = btn.closest('form');
                if (!form || !waNumber) return;
                var val = function (name) {
                    var el = form.elements[name];
                    return el && el.value ? String(el.value).trim() : '';
                };
                var kind = form.getAttribute('data-wa-form');
                var lines = [];

                if (kind === 'contact') {
                    if (!val('message')) { form.elements['message'].focus(); return; }
                    lines.push('Hi Joseph, my name is ' + (val('name') || '(no name)') + '.');
                    if (val('subject')) lines.push('Topic: ' + val('subject'));
                    lines.push('', val('message'));
                    if (val('email')) lines.push('', 'Email: ' + val('email'));
                } else {
                    if (!val('details')) { form.elements['details'].focus(); return; }
                    var picked = form.querySelector('input[name="project_type"]:checked');
                    var type = picked && picked.parentNode ? picked.parentNode.textContent.trim() : '';
                    lines.push('Hi Joseph, I would like to request a project.');
                    lines.push('Name: ' + (val('name') || '-'));
                    if (val('email')) lines.push('Email: ' + val('email'));
                    if (type) lines.push('Need: ' + type);
                    var budget = form.querySelector('input[name="budget_range"]:checked');
                    var bt = budget && budget.value ? budget.parentNode.querySelector('strong') : null;
                    if (bt) lines.push('Budget: ' + bt.textContent.trim());
                    if (val('deadline')) lines.push('Timeline: ' + val('deadline'));
                    lines.push('', val('details'));
                }
                window.open('https://wa.me/' + waNumber + '?text=' + encodeURIComponent(lines.join('\n')), '_blank', 'noopener');
            });
        });
    }

    /* ---------------- nav: highlight the section you are reading ---------------- */
    if ('IntersectionObserver' in window) {
        var sections = [
            ['hero', 'top'], ['about', 'about'], ['experience', 'experience'],
            ['projects', 'projects'], ['services', 'services'], ['stack', 'stack'],
            ['connect', 'connect']
        ].map(function (pair) { return { el: document.getElementById(pair[0]), key: pair[1] }; })
         .filter(function (s) { return s.el; });

        if (sections.length > 2) {
            var links = document.querySelectorAll('#desktop-nav a[data-spy]');
            var setActive = function (key) {
                links.forEach(function (a) { a.classList.toggle('active', a.getAttribute('data-spy') === key); });
            };
            var io = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (!entry.isIntersecting) return;
                    for (var i = 0; i < sections.length; i++) {
                        if (sections[i].el === entry.target) { setActive(sections[i].key); break; }
                    }
                });
            }, { rootMargin: '-35% 0px -55% 0px' });
            sections.forEach(function (s) { io.observe(s.el); });
        }
    }

    /* ---------------- mobile menu: open/close, tap outside to close ---------------- */
    var drawer = document.getElementById('mobile-drawer');
    var navBtn = document.getElementById('mobile-toggle-btn');
    var backdrop = document.getElementById('nav-backdrop');

    function setNav(open) {
        if (!drawer || !navBtn) return;
        drawer.classList.toggle('is-open', open);
        document.body.classList.toggle('nav-open', open);
        navBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    }

    if (drawer && navBtn) {
        navBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            setNav(!drawer.classList.contains('is-open'));
        });
        /* choosing a link closes it */
        drawer.addEventListener('click', function (e) {
            if (e.target.closest('a')) setNav(false);
        });
        /* tapping anywhere outside the menu closes it */
        if (backdrop) backdrop.addEventListener('click', function () { setNav(false); });
        document.addEventListener('click', function (e) {
            if (drawer.classList.contains('is-open') && !drawer.contains(e.target) && !navBtn.contains(e.target)) setNav(false);
        });
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') setNav(false);
        });
        /* growing past the phone layout: make sure it is not left open */
        window.addEventListener('resize', function () { if (window.innerWidth >= 960) setNav(false); });
    }
})();
