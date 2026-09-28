import json, os
svg=open(os.path.join(os.path.dirname(__file__),'scene.svg')).read()
Z={
 'combles':dict(n=1,lieu='Combles & grenier',titre='Loirs & fouines',signes=['Grattements et cavalcades la nuit','Isolant tassé ou arraché','Crottes et odeur dans le grenier'],conseil='Ne bouchez pas les accès tant que l’animal est à l’intérieur.'),
 'toiture':dict(n=2,lieu='Toiture & débords de toit',titre='Guêpes & pigeons',signes=['Va-et-vient de guêpes sous les tuiles','Nid gris sous le débord de toit','Fientes et nids de pigeons'],conseil='N’approchez pas du nid et n’actionnez pas un volet où des guêpes entrent.'),
 'chambre':dict(n=3,lieu='Chambre',titre='Punaises de lit',signes=['Piqûres alignées au réveil','Petites taches noires sur le matelas','Insectes plats dans les coutures'],conseil='Ne déplacez pas vos affaires vers d’autres pièces : vous étendriez l’infestation.'),
 'plafond':dict(n=4,lieu='Faux plafond & cloisons',titre='Souris & rats',signes=['« Ça gratte dans le plafond » la nuit','Câbles ou isolant rongés','Petites crottes noires'],conseil='Notez à quelle heure et à quel endroit vous entendez les bruits : cela aide à identifier l’animal.'),
 'cuisine':dict(n=5,lieu='Cuisine',titre='Cafards & fourmis',signes=['Cafards sous l’évier ou derrière le frigo','Colonnes de fourmis vers le plan de travail','Ils reviennent malgré les bombes'],conseil='Rangez les aliments dans des boîtes fermées et ne laissez pas d’eau stagnante.'),
 'salon':dict(n=6,lieu='Salon',titre='Puces',signes=['Piqûres aux chevilles','Votre chien ou chat se gratte','Petits points noirs sur les tapis'],conseil='Traitez votre animal et le logement en même temps, sinon les puces reviennent.'),
 'cave':dict(n=7,lieu='Cave & sous-sol',titre='Rats',signes=['Sacs et cartons rongés','Traces le long des murs','Bruits et odeur d’urine'],conseil='Ne laissez pas de nourriture (croquettes, graines) accessible en cave.'),
 'arbre':dict(n=8,lieu='Arbres du jardin',titre='Chenilles & frelons',signes=['Cocons blancs dans les pins et chênes','Chenilles en file indienne au sol','Nid de frelons en hauteur'],conseil='Éloignez chiens et enfants des chenilles : leurs poils sont très urticants.'),
 'mare':dict(n=9,lieu='Jardin & terrasse',titre='Moustiques',signes=['Piqûres dès la fin de journée','Eau stagnante (soucoupes, mare)','Moustique tigre, rayé noir et blanc'],conseil='Videz chaque semaine les récipients où l’eau stagne.'),
 'pelouse':dict(n=10,lieu='Pelouse',titre='Taupes',signes=['Taupinières chaque matin','Galeries sous la pelouse','Plantes déracinées'],conseil='Les répulsifs du commerce déplacent la taupe sans l’éliminer.'),
}
html=f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Où se cachent les nuisibles ? – Eden Vert 3D</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{--orange:#EE5A1B;--orange-dark:#D44A10;--ink:#121417;--text:#2A2D33;--muted:#6A6F78;--soft:#F5F5F4;--ease:cubic-bezier(0.2,0,0,1)}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:"Barlow",system-ui,sans-serif;color:var(--text);background:#fff;-webkit-font-smoothing:antialiased}}
/* ---------- Section « maison » : autonome, à intégrer dans index.html ---------- */
.nh{{background:var(--soft);padding:clamp(56px,7vw,110px) 0;overflow:hidden}}
.nh .wrap{{max-width:1180px;margin:0 auto;padding:0 24px}}
.nh-head{{text-align:center;max-width:720px;margin:0 auto clamp(24px,4vw,44px)}}
.nh-eyebrow{{font-size:13px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);margin-bottom:10px}}
.nh-title{{font-size:clamp(28px,3.6vw,40px);font-weight:800;line-height:1.05;text-transform:uppercase;color:var(--ink);text-wrap:balance}}
.nh-title span{{color:var(--orange)}}
.nh-lead{{color:var(--muted);margin-top:12px;font-size:17px}}
.nh-grid{{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(300px,.8fr);gap:clamp(24px,4vw,56px);align-items:center}}
.house{{width:100%;height:auto;display:block;overflow:visible;filter:drop-shadow(0 30px 40px rgba(18,20,23,.12))}}
.scene{{transition:opacity .3s var(--ease)}}
.zone{{fill:var(--orange);fill-opacity:0;transition:fill-opacity .3s var(--ease);cursor:pointer}}
.zone:hover{{fill-opacity:.1}}
.zone.is-active{{fill-opacity:.2}}
.lvl{{font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;fill:#8A8E96}}
.hot{{cursor:pointer;outline:none}}
.hot .dot{{fill:var(--ink);stroke:#fff;stroke-width:2.5;transition:fill .2s var(--ease)}}
.hot text{{fill:#fff;font-weight:800;font-size:12px;text-anchor:middle;pointer-events:none}}
.hot .hit{{fill:transparent}}
.hot .ring{{fill:none;stroke:var(--orange);stroke-width:2;opacity:0;transform-box:fill-box;transform-origin:center}}
.hot:hover .dot,.hot:focus-visible .dot,.hot.is-active .dot{{fill:var(--orange)}}
.hot.is-active .ring{{opacity:1;animation:nhRing 1.8s var(--ease) infinite}}
.hot:focus-visible .ring{{opacity:1}}
@keyframes nhRing{{from{{transform:scale(.8);opacity:.9}}to{{transform:scale(1.9);opacity:0}}}}
/* fiche */
.nh-card{{background:#fff;border-radius:22px;padding:28px;box-shadow:0 0 0 1px rgb(0 0 0/.05),0 20px 50px rgb(18 20 23/.08);position:relative}}
.nh-card-top{{display:flex;align-items:center;gap:14px;margin-bottom:16px}}
.nh-num{{width:44px;height:44px;border-radius:14px;background:var(--orange);color:#fff;display:grid;place-items:center;font-weight:800;font-size:18px;flex:none}}
.nh-place{{font-size:13px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}}
.nh-pest{{font-size:26px;font-weight:800;text-transform:uppercase;color:var(--ink);line-height:1.05}}
.nh-sub{{font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--ink);margin:18px 0 10px}}
.nh-signs{{list-style:none;display:flex;flex-direction:column;gap:8px}}
.nh-signs li{{display:flex;gap:10px;align-items:flex-start;font-size:15px;line-height:1.4}}
.nh-signs li::before{{content:"";width:7px;height:7px;border-radius:50%;background:var(--orange);margin-top:7px;flex:none}}
.nh-tip{{margin-top:18px;padding:12px 14px;border-radius:12px;background:#FFF4EE;font-size:14px;line-height:1.45;color:var(--ink)}}
.nh-tip b{{color:var(--orange-dark)}}
.nh-ctas{{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px}}
.nh-btn{{display:inline-flex;align-items:center;gap:8px;padding:14px 18px;border-radius:10px;font-weight:700;font-size:13px;letter-spacing:.04em;text-transform:uppercase;text-decoration:none;transition-property:background-color,scale;transition-duration:.15s;transition-timing-function:var(--ease)}}
.nh-btn:active{{scale:.96}}
.nh-btn.primary{{background:var(--orange);color:#fff}}.nh-btn.primary:hover{{background:var(--orange-dark)}}
.nh-btn.ghost{{background:var(--soft);color:var(--ink)}}.nh-btn.ghost:hover{{background:#EAEAE8}}
.nh-nav{{display:flex;justify-content:space-between;align-items:center;margin-top:22px;padding-top:16px;border-top:1px solid #EEE}}
.nh-nav button{{border:0;background:none;font:inherit;font-weight:700;font-size:13px;color:var(--muted);cursor:pointer;padding:8px;border-radius:8px}}
.nh-nav button:hover{{color:var(--ink);background:var(--soft)}}
.nh-dots{{display:flex;gap:5px}}
.nh-dots i{{width:6px;height:6px;border-radius:50%;background:#D9DADC;transition:background-color .2s,width .2s}}
.nh-dots i.on{{background:var(--orange);width:16px;border-radius:3px}}
.nh-body{{transition:opacity .2s var(--ease),translate .2s var(--ease)}}
.nh-body.swap{{opacity:0;translate:0 6px}}
/* micro-animations */
.wp,.hn{{animation:nhBuzz 1.6s ease-in-out infinite}}.wp1,.hn1{{animation-delay:-.4s}}.wp2,.hn2{{animation-delay:-.8s}}.wp3{{animation-delay:-1.2s}}
@keyframes nhBuzz{{0%,100%{{translate:0 0}}25%{{translate:6px -5px}}50%{{translate:-3px -9px}}75%{{translate:-7px -2px}}}}
.m{{animation:nhBuzz 1.1s ease-in-out infinite}}.m1{{animation-delay:-.3s}}.m2{{animation-delay:-.6s}}.m3{{animation-delay:-.2s}}.m4{{animation-delay:-.9s}}
.tail{{transform-box:fill-box;transform-origin:100% 100%;animation:nhTail 1.4s ease-in-out infinite}}
@keyframes nhTail{{0%,100%{{rotate:0deg}}50%{{rotate:-14deg}}}}
.mouse{{animation:nhWalk 6s ease-in-out infinite}}
@keyframes nhWalk{{0%,100%{{translate:0 0}}50%{{translate:60px 0}}}}
.rat{{animation:nhScurry 5s ease-in-out infinite}}.rat2{{animation-delay:-2.5s}}
@keyframes nhScurry{{0%,100%{{translate:0 0}}40%{{translate:14px 7px}}60%{{translate:14px 7px}}}}
.roach{{animation:nhCrawl 3.2s ease-in-out infinite}}.r1{{animation-delay:-.8s}}.r2{{animation-delay:-1.6s}}.r3{{animation-delay:-2.4s}}
@keyframes nhCrawl{{0%,100%{{translate:0 0}}50%{{translate:5px 3px}}}}
.ants,.procession{{animation:nhMarch 1.2s linear infinite}}
@keyframes nhMarch{{to{{stroke-dashoffset:-11}}}}
.flea{{animation:nhJump .9s ease-out infinite}}.f1{{animation-delay:-.2s}}.f2{{animation-delay:-.5s}}.f3{{animation-delay:-.7s}}.f4{{animation-delay:-.35s}}
@keyframes nhJump{{0%,100%{{translate:0 0}}40%{{translate:2px -10px}}}}
.bb{{animation:nhCrawl 2.6s ease-in-out infinite}}.b1{{animation-delay:-.6s}}.b2{{animation-delay:-1.2s}}.b3{{animation-delay:-1.8s}}
.pigeon .head{{transform-box:fill-box;transform-origin:0 100%;animation:nhPeck 2.4s ease-in-out infinite}}.p2 .head{{animation-delay:-1.1s}}
@keyframes nhPeck{{0%,70%,100%{{rotate:0deg}}80%{{rotate:20deg}}}}
.molehill{{transform-box:fill-box;transform-origin:50% 100%;animation:nhHill 3s ease-in-out infinite}}
@keyframes nhHill{{0%,100%{{scale:1}}50%{{scale:1.08 1.15}}}}
.mole{{animation:nhWalk 7s ease-in-out infinite}}
.foliage{{transform-box:fill-box;transform-origin:50% 100%;animation:nhSway 6s ease-in-out infinite}}
@keyframes nhSway{{0%,100%{{rotate:0deg}}50%{{rotate:1.2deg}}}}
.loir .tail{{animation-duration:2s}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important;transition:none!important}}}}
/* responsive */
@media (max-width:900px){{
  .nh-grid{{grid-template-columns:1fr}}
  .house{{max-width:560px;margin:0 auto}}
}}
@media (max-width:640px){{
  .nh .wrap{{padding:0 16px}}
  .nh-card{{padding:22px 18px}}
  .nh-pest{{font-size:22px}}
  .hot .dot{{r:22px}} .hot .ring{{r:26px}} .hot .hit{{r:44px}} .hot text{{font-size:21px}}
  .nh-btn{{flex:1;justify-content:center}}
}}
</style>
</head>
<body>

<section class="nh" id="maison-nuisibles" aria-labelledby="nh-title">
  <div class="wrap">
    <header class="nh-head">
      <p class="nh-eyebrow">Diagnostic express</p>
      <h2 class="nh-title" id="nh-title">Où se cachent <span>les nuisibles</span> chez vous&nbsp;?</h2>
      <p class="nh-lead">Touchez une pièce de la maison pour découvrir les signes qui doivent vous alerter.</p>
    </header>
    <div class="nh-grid">
      <div class="nh-scene">{svg}</div>
      <article class="nh-card" aria-live="polite">
        <div class="nh-body">
          <div class="nh-card-top"><span class="nh-num">1</span><div><p class="nh-place"></p><h3 class="nh-pest"></h3></div></div>
          <p class="nh-sub">Les signes qui doivent alerter</p>
          <ul class="nh-signs"></ul>
          <p class="nh-tip"><b>Le bon réflexe&nbsp;:</b> <span></span></p>
          <div class="nh-ctas">
            <a class="nh-btn primary" href="#contact">Demander un devis</a>
            <a class="nh-btn ghost" href="tel:0184802122">01&nbsp;84&nbsp;80&nbsp;21&nbsp;22</a>
          </div>
        </div>
        <div class="nh-nav">
          <button type="button" data-step="-1" aria-label="Zone précédente">← Précédent</button>
          <div class="nh-dots" aria-hidden="true"></div>
          <button type="button" data-step="1" aria-label="Zone suivante">Suivant →</button>
        </div>
      </article>
    </div>
  </div>
</section>

<script>
(() => {{
  const DATA = {json.dumps(Z, ensure_ascii=False)};
  const keys = Object.keys(DATA);
  const root = document.getElementById('maison-nuisibles');
  const card = root.querySelector('.nh-body');
  const dots = root.querySelector('.nh-dots');
  keys.forEach(() => dots.appendChild(document.createElement('i')));
  let current = null, auto = true, timer;
  const show = (key, byUser) => {{
    if (byUser) {{ auto = false; clearInterval(timer); }}
    if (key === current) return;
    current = key;
    const d = DATA[key];
    root.querySelectorAll('.zone,.hot').forEach(el => el.classList.toggle('is-active', el.dataset.zone === key));
    [...dots.children].forEach((dot, i) => dot.classList.toggle('on', keys[i] === key));
    card.classList.add('swap');
    setTimeout(() => {{
      card.querySelector('.nh-num').textContent = d.n;
      card.querySelector('.nh-place').textContent = d.lieu;
      card.querySelector('.nh-pest').textContent = d.titre;
      card.querySelector('.nh-signs').innerHTML = d.signes.map(s => `<li>${{s}}</li>`).join('');
      card.querySelector('.nh-tip span').textContent = d.conseil;
      card.classList.remove('swap');
    }}, 160);
  }};
  root.querySelectorAll('.zone,.hot').forEach(el => {{
    el.addEventListener('click', () => show(el.dataset.zone, true));
    el.addEventListener('mouseenter', () => {{ if (matchMedia('(hover:hover)').matches) show(el.dataset.zone, true); }});
    el.addEventListener('keydown', e => {{ if (e.key === 'Enter' || e.key === ' ') {{ e.preventDefault(); show(el.dataset.zone, true); }} }});
  }});
  root.querySelectorAll('[data-step]').forEach(b => b.addEventListener('click', () => {{
    const i = (keys.indexOf(current) + +b.dataset.step + keys.length) % keys.length;
    show(keys[i], true);
  }}));
  show(keys[0]);
  // visite automatique tant que l’utilisateur n’a pas interagi (et seulement si la section est visible)
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduced) new IntersectionObserver(([en]) => {{
    clearInterval(timer);
    if (en.isIntersecting && auto) timer = setInterval(() => show(keys[(keys.indexOf(current) + 1) % keys.length]), 4500);
  }}, {{ threshold: .4 }}).observe(root);
}})();
</script>
</body>
</html>
'''
open(os.path.join(os.path.dirname(__file__),'..','maison-nuisibles.html'),'w').write(html); print('ok')
