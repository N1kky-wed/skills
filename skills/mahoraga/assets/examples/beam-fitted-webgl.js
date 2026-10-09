// Hero light: one fragment shader drawing the beam, the flare where it meets the mockup's top edge, the
// white-hot sheet along that edge and the curtain of light falling past its far corner. Each part's
// cross-section was fitted to measurements of the reference frame (colour and width at many heights), then
// set in motion: light swells streaming down the beam, the flare shimmering, streaks running down the
// curtain, haze drifting past. Geometry is read from the DOM every frame (css px, hero-relative); every
// length is authored at desktop size and scaled by k = mockup width / 1024.

const VERT = 'attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}';

const FRAG = `
precision highp float;
uniform vec2 uRes;
uniform float uScale, uTime, uBoost, uK;
uniform vec3 uGeo;   // beam x, the mockup's top edge y, hero height
uniform vec2 uSpan;  // mockup left, right
uniform vec2 uMouse; // 0..1

float hash(vec2 p){ p = fract(p * vec2(443.897, 441.423)); p += dot(p, p.yx + 19.19); return fract((p.x + p.y) * p.x); }
float noise(vec2 p){
  vec2 i = floor(p), f = fract(p), u = f * f * (3. - 2. * f);
  return mix(mix(hash(i), hash(i + vec2(1., 0.)), u.x), mix(hash(i + vec2(0., 1.)), hash(i + vec2(1., 1.)), u.x), u.y);
}
float fbm(vec2 p){
  float v = 0., a = .5;
  mat2 m = mat2(1.6, 1.2, -1.2, 1.6);
  for (int i = 0; i < 4; i++){ v += a * noise(p); p = m * p; a *= .5; }
  return v;
}

void main(){
  vec2 p = vec2(gl_FragCoord.x, uRes.y - gl_FragCoord.y) / uScale;
  float bx = uGeo.x, sy = uGeo.y, hh = uGeo.z, t = uTime, k = uK;
  float dx = (p.x - bx) / k, ax = abs(dx);                 // across, from the beam (design px)
  float dn = max(p.y - sy, 0.) / k;                         // depth below the edge
  // the edge is a surface only between the mockup's ends: there light stops at it; past them it simply
  // fades the same way above and below the edge's level
  float inSpan = smoothstep(uSpan.x - 12. * k, uSpan.x + 4. * k, p.x) * smoothstep(uSpan.y + 12. * k, uSpan.y - 4. * k, p.x);
  float u = mix(abs(sy - p.y), max(sy - p.y, 0.), inSpan) / k;   // height above the edge
  float above = mix(1., 1. - smoothstep(sy - 1. * k, sy + 2. * k, p.y), inSpan);
  float lift = 1. + .25 * uBoost;                           // the hero CTA brightens everything a touch
  vec3 col = vec3(0.);

  // the mockup's outline as a rounded box (14px corners), > 0 outside, in design px
  float rr = 14. * k;
  vec2 bh = vec2((uSpan.y - uSpan.x) * .5, 800. * k);
  vec2 bq = abs(p - vec2((uSpan.x + uSpan.y) * .5, sy + bh.y)) - bh + rr;
  float sd = (length(max(bq, 0.)) + min(max(bq.x, bq.y), 0.) - rr) / k;

  // 1. smoke: big slow masses of grey-blue haze across the hero (measured off the original: mean ~21/24/36
  //    away from the beam, with real cloud contrast), lit electric blue close to the beam; drifts with the pointer
  vec2 uv = p / (640. * k) + (uMouse - .5) * vec2(.12, .06);
  vec2 q = vec2(fbm(uv + vec2(0., t * .05)), fbm(uv + vec2(5.2, 1.3) - t * .035));
  vec2 r = vec2(fbm(uv + 2.4 * q + vec2(1.7, 9.2) + t * .04), fbm(uv + 2.4 * q + vec2(8.3, 2.8) - t * .038));
  float vol = smoothstep(.34, .86, fbm(uv + 1.6 * r));      // big soft clouds with dark gaps, not marble
  col += vol * (vec3(.1, .11, .17) * (.4 + .6 * smoothstep(-700., 100., dx)) + vec3(.1, .17, .65) * exp(-ax / 190.)) * above;

  // 2. clouds of vivid blue light drifting slowly past the beam's upper half
  vec2 pu = vec2(ax / 210. - t * .035 + step(0., dx) * 4.7, p.y / (240. * k) + t * .03);
  vec2 pw = vec2(fbm(pu * 1.3 + vec2(3.1, t * .04)), fbm(pu * 1.3 + vec2(7.7, -t * .03)));
  float puff = smoothstep(.56, .95, fbm(pu + 1.7 * pw));
  col += puff * (vec3(.2, .33, 1.2) * exp(-ax / 110.) + vec3(.03, .05, .16) * exp(-ax / 200.)) * smoothstep(40., 160., u) * above;

  // 3. the beam: white core (sigma 2px at the top, 3px lower) in a blue glow decaying over 14px,
  //    swelling as light streams down it
  float grow = smoothstep(-40. * k, 190. * k, p.y);
  float stream = noise(vec2(ax * .03, p.y / k * .0045 - t * 1.3));
  float sig = mix(2., 3., grow) * (.9 + .25 * stream);
  float flick = .97 + .03 * sin(t * 7. + sin(t * 2.1) * 3.);
  float I = (.55 + .45 * grow) * flick * (1. + .45 * uBoost) * above;
  col += I * (2.2 * exp(-.5 * (ax / sig) * (ax / sig))
            + 2.9 * exp(-ax / 14.) * (.35 + .65 * grow) * (.8 + .35 * stream) * vec3(.24, .31, 1.)
            + (.05 * exp(-ax / 58.) + .03 * exp(-ax / 200.)) * vec3(.3, .3, 1.));

  // 4. the flare: a white trumpet widening into the edge, blue haze swelling toward the surface, a
  //    white-hot sheet along the edge, and the pool above it (cyan-blue toward the long side, violet
  //    toward the corner); it shimmers slowly
  float shim = .92 + .16 * noise(vec2(dx * .015, u * .02 - t * .7));
  float Rw = 153.6 * exp(-u / 45.5) * shim;
  float body = 1.324 * exp(-ax / max(Rw, .5));
  float swell = .37 * exp(-ax / (1.9e6 * exp(-u / 20.8))) * exp(-u / 115.6);
  float left = step(dx, 0.);
  float reach = dx < -380. ? exp((dx + 380.) / 76.) : 1.;
  // the glow over the edge dies out past ~-400 on the long side and within ~40px past the corner
  float span = (dx < -350. ? exp((dx + 350.) / 120.) : 1.) * exp(-max(p.x - uSpan.y, 0.) / (30. * k));
  // the sheet is measured from the mockup's rounded outline, so it wraps the far corner's arc and hands
  // over to the curtain below it
  float ripple = .9 + .1 * sin(ax / 30. - t * 2.6);
  float onEdge = smoothstep(uSpan.x - 2. * k, uSpan.x + 40. * k, p.x) * (1. - smoothstep(0., 24. * k, p.y - sy));
  float sheet = 30.3 * reach * exp(-max(sd, 0.) / (1.25 + 23.7 * exp(-ax / 53.9))) * ripple * onEdge;
  float pool = 4.15 * exp(-ax / mix(122., 478., left)) * exp(-u / 50.3);
  col += (body + (swell * vec3(0., .33, 1.) + pool * mix(vec3(.247, .035, 1.), vec3(.393, .401, 1.), left)) * span) * lift * above + sheet * lift;

  // 5. the corner: the sheet rolls over the rounded corner and falls outside the right edge as a
  //    curtain, white against the edge, a cyan fringe turning pink lower down, fanning into blue;
  //    streaks run down it like liquid
  float xo = max(sd, 0.);
  float cd = (p.y - sy) / k;
  float fl = noise(vec2(xo * .09, dn * .012 - t * 1.6));
  float wW = (3.57 + 28.5 * (1. - exp(-dn / 100.))) * (.85 + .3 * fl);
  float wG = 20.7 + .675 * dn;
  float cur = 5.07 * exp(-pow(xo / wW, 4.38));
  float fringe = 1.31 * exp(-pow((xo - 1.19 * wW) / (.551 * wW), 2.));
  vec3 fc = mix(vec3(.45, 1., 1.), vec3(1., .55, 1.), smoothstep(120., 190., dn));
  float cglow = 2.2 * exp(-xo / (max(wG - wW, 1.) * .522));
  float curtain = smoothstep(uSpan.y - 30. * k, uSpan.y - 2. * k, p.x) * smoothstep(-10., 4., cd) * (1. - smoothstep(220., 560., dn));
  col += curtain * (cur + fringe * fc + cglow * vec3(.234, .422, 1.)) * lift;

  col = 1. - exp(-col * 1.35);                        // soft highlight roll-off
  col *= 1. - smoothstep(hh - 380., hh - 20., p.y);  // hand over to the section below
  col += (hash(p + fract(t)) - .5) / 90.;             // grain, kills banding
  gl_FragColor = vec4(vec3(.035, .039, .047) + col, 1.);
}`;

export function initBeam(canvas, geometry) {
  const gl = canvas.getContext('webgl', { antialias: false, alpha: false, powerPreference: 'high-performance' });
  if (!gl) return null;
  const compile = (type, src) => {
    const s = gl.createShader(type);
    gl.shaderSource(s, src);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
    return s;
  };
  const prog = gl.createProgram();
  gl.attachShader(prog, compile(gl.VERTEX_SHADER, VERT));
  gl.attachShader(prog, compile(gl.FRAGMENT_SHADER, FRAG));
  gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(prog));
  gl.useProgram(prog);
  gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(prog, 'p');
  gl.enableVertexAttribArray(loc);
  gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  const U = Object.fromEntries(['uRes', 'uScale', 'uTime', 'uBoost', 'uK', 'uGeo', 'uSpan', 'uMouse']
    .map(n => [n, gl.getUniformLocation(prog, n)]));

  let scale = 1;
  const resize = () => {
    // everything here is soft light, so render below device resolution
    scale = Math.min(1, (window.devicePixelRatio || 1) * 0.6);
    canvas.width = Math.max(1, Math.round(canvas.clientWidth * scale));
    canvas.height = Math.max(1, Math.round(canvas.clientHeight * scale));
    gl.viewport(0, 0, canvas.width, canvas.height);
  };
  resize();

  return {
    resize,
    draw(time) {
      const g = geometry();
      gl.uniform2f(U.uRes, canvas.width, canvas.height);
      gl.uniform1f(U.uScale, scale);
      gl.uniform1f(U.uTime, time);
      gl.uniform1f(U.uBoost, g.boost);
      gl.uniform1f(U.uK, g.k);
      gl.uniform3f(U.uGeo, g.beamX, g.surfaceY, g.height);
      gl.uniform2f(U.uSpan, g.left, g.right);
      gl.uniform2f(U.uMouse, g.mouseX, g.mouseY);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
    },
  };
}
