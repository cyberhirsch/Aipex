// Aipex front page: top 3 models per category, filtered by licence and local VRAM.
(() => {
    const state = { open: 'all', vram: 0, q: '' };
    let data = null;

    const $ = (sel) => document.querySelector(sel);
    const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
    const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

    function passes(m) {
        if (state.open === 'open' && !m.open) return false;
        if (state.vram > 0) {
            if (!m.open || m.vram_gb == null) return false;
            if (m.vram_gb > state.vram) return false;
        }
        return true;
    }

    function sourceTitle(m) {
        return m.sources.map((s) => `${data.sourceNames[s.id] || s.id}: ${s.raw} ${s.metric} → ${Math.round(s.norm)}`).join('\n');
    }

    function rowHtml(m, i) {
        const tags = [];
        if (m.open) tags.push(`<span class="tag open" title="${esc(m.license || 'Open weights')}">Open${m.license ? ' · ' + esc(m.license) : ''}</span>`);
        if (m.open && m.vram_gb != null) tags.push(`<span class="tag" title="${esc(m.vram_note || 'Estimated VRAM for local inference')}">${m.vram_gb} GB</span>`);
        if (m.sources.length === 1) tags.push(`<span class="tag" title="${esc(sourceTitle(m))}">1 source</span>`);
        else tags.push(`<span class="tag" title="${esc(sourceTitle(m))}">${m.sources.length} sources</span>`);
        const score = Math.round(m.score);
        const shown = m.score < 1 ? '<1' : score;
        return `<li class="row r${i + 1}">
            <span class="rank">${i + 1}</span>
            <span class="model"><span class="model-name" title="${esc(m.name)}">${esc(m.name)}</span><span class="model-org">${esc(m.org || '')}</span></span>
            <span class="score" title="${esc(sourceTitle(m))}">${shown}</span>
            <span class="bar"><i style="width:${Math.max(2, Math.min(100, score))}%"></i></span>
            <span class="tags">${tags.join('')}</span>
        </li>`;
    }

    function cardHtml(cat, top) {
        const srcs = [...new Set(cat.models.flatMap((m) => m.sources.map((s) => s.id)))];
        const body = top.length
            ? `<ol class="rows">${top.map(rowHtml).join('')}</ol>`
            : `<p class="card-empty">${state.vram ? `No ranked open model fits in ${state.vram} GB.` : 'No ranked open-weight model in this category.'}</p>`;
        return `<article class="card" id="${slug(cat.id)}">
            <div class="card-head"><h3 class="card-title">${esc(cat.name)}</h3><span class="card-meta">${cat.models.length} ranked</span></div>
            ${body}
            <div class="card-foot">${srcs.map((id) => esc(data.sourceNames[id] || id)).join(' · ')}</div>
        </article>`;
    }

    function render() {
        const q = state.q.trim().toLowerCase();
        const groups = new Map();
        const filtered = state.open !== 'all' || state.vram > 0;
        let hidden = 0;
        for (const cat of data.categories) {
            const hit = !q || cat.name.toLowerCase().includes(q) || cat.group.toLowerCase().includes(q) || cat.models.some((m) => m.name.toLowerCase().includes(q) || (m.org || '').toLowerCase().includes(q));
            if (!hit) continue;
            const top = cat.models.filter(passes).slice(0, 3);
            if (!top.length && filtered) { hidden++; continue; }   // a filter is on: drop categories it empties
            if (!groups.has(cat.group)) groups.set(cat.group, []);
            groups.get(cat.group).push({ cat, top });
        }
        if (!groups.size) { $('#board').innerHTML = `<p class="empty-all">Nothing matches${hidden ? ` (${hidden} categories hidden by the filter)` : ''}.</p>`; $('#groupNav').innerHTML = ''; return; }
        let html = '';
        let nav = '';
        for (const [group, items] of groups) {
            // categories with results first, empty ones last
            items.sort((a, b) => (b.top.length > 0) - (a.top.length > 0));
            const id = 'g-' + slug(group);
            nav += `<a href="#${id}">${esc(group)}<b>${items.length}</b></a>`;
            html += `<section class="group" id="${id}"><h2 class="group-title">${esc(group)}<span>${items.length} ${items.length === 1 ? 'category' : 'categories'}</span></h2><div class="grid">${items.map((x) => cardHtml(x.cat, x.top)).join('')}</div></section>`;
        }
        if (hidden) html += `<p class="hidden-note">${hidden} ${hidden === 1 ? 'category has' : 'categories have'} no ranked model that matches the filter.</p>`;
        $('#board').innerHTML = html;
        $('#groupNav').innerHTML = nav;
    }

    function bindSeg(id, key, attr) {
        $(id).addEventListener('click', (e) => {
            const b = e.target.closest('button');
            if (!b) return;
            [...$(id).children].forEach((x) => x.classList.toggle('active', x === b));
            state[key] = key === 'vram' ? Number(b.dataset[attr]) : b.dataset[attr];
            saveHash();
            render();
        });
    }

    function saveHash() {
        const p = new URLSearchParams();
        if (state.open !== 'all') p.set('open', '1');
        if (state.vram) p.set('vram', state.vram);
        history.replaceState(null, '', p.toString() ? '#' + p : location.pathname);
    }

    function loadHash() {
        const p = new URLSearchParams(location.hash.slice(1));
        if (p.get('open') === '1') state.open = 'open';
        const v = Number(p.get('vram'));
        if ([8, 24, 32].includes(v)) state.vram = v;
        document.querySelectorAll('#licenceSeg button').forEach((b) => b.classList.toggle('active', b.dataset.open === state.open));
        document.querySelectorAll('#vramSeg button').forEach((b) => b.classList.toggle('active', Number(b.dataset.vram) === state.vram));
    }

    bindSeg('#licenceSeg', 'open', 'open');
    bindSeg('#vramSeg', 'vram', 'vram');
    window.addEventListener('hashchange', () => { if (data) { state.open = 'all'; state.vram = 0; loadHash(); render(); } });
    $('#search').addEventListener('input', (e) => { state.q = e.target.value; render(); });

    fetch('data/aipex.json', { cache: 'no-cache' })
        .then((r) => r.json())
        .then((d) => {
            data = d;
            data.sourceNames = Object.fromEntries(d.sources.map((s) => [s.id, s.name]));
            $('#updated').textContent = `Data retrieved ${d.updated} · ${d.categories.length} categories · ${d.sources.length} sources.`;
            $('#sourcesList').innerHTML = 'Sources: ' + d.sources.map((s) => `<a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.name)}</a>`).join(' · ');
            loadHash();
            render();
        })
        .catch(() => { $('#board').innerHTML = '<p class="empty-all">Could not load data/aipex.json.</p>'; });
})();
