let scene, camera, renderer, controls;
let avatar, mouth;
let clock = new THREE.Clock();
let smokeParticles = [];

function init(){
  const container = document.getElementById('three');
  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.setPixelRatio(devicePixelRatio);
  container.appendChild(renderer.domElement);

  scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x061625, 0.012);

  camera = new THREE.PerspectiveCamera(50, container.clientWidth/container.clientHeight, 0.1, 100);
  camera.position.set(0, 1.2, 3.2);

  controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;

  const hemi = new THREE.HemisphereLight(0x77aaff, 0x080820, 0.7);
  scene.add(hemi);
  const dir = new THREE.DirectionalLight(0xffffff, 0.8);
  dir.position.set(5, 10, 7);
  scene.add(dir);

  // Floor
  const g = new THREE.CylinderGeometry(5, 5, 0.1, 64);
  const m = new THREE.MeshStandardMaterial({ color: 0x0b1b2b, metalness: 0.2, roughness: 0.8 });
  const floor = new THREE.Mesh(g, m);
  floor.position.y = -1;
  scene.add(floor);

  // Smoke particles
  const loaderTex = new THREE.TextureLoader();
  loaderTex.load('/assets/smoke.png', (tex)=>{
    const geo = new THREE.PlaneGeometry(2,2);
    const mat = new THREE.PointsMaterial({ size: 1.6, map: tex, transparent: true, depthWrite: false, color: 0x66aaff });
    for(let i=0;i<40;i++){
      const mesh = new THREE.Points(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3()]), mat.clone());
      mesh.position.set((Math.random()-0.5)*2, -1 + Math.random()*2, (Math.random()-0.5)*2);
      smokeParticles.push(mesh);
      scene.add(mesh);
    }
  });

  // Load avatar or fallback sphere
  const gltfLoader = new THREE.GLTFLoader();
  gltfLoader.load('/assets/avatar.glb', (gltf)=>{
    avatar = gltf.scene;
    avatar.traverse((o)=>{ if(o.isMesh){ o.castShadow=true; o.receiveShadow=true; } });
    scene.add(avatar);
    avatar.position.set(0,-1,0);
    // Try to find a mouth bone by name hints
    mouth = avatar.getObjectByName('Mouth') || avatar.getObjectByName('jaw') || avatar.getObjectByName('Jaw');
    if(!mouth){
      // Create simple mouth surrogate
      const geo = new THREE.BoxGeometry(0.2,0.05,0.1);
      const mat = new THREE.MeshStandardMaterial({ color: 0x88ccff, metalness:0.8, roughness:0.2 });
      mouth = new THREE.Mesh(geo, mat);
      mouth.position.set(0, 0.9, 0.5);
      avatar.add(mouth);
    }
  }, undefined, ()=>{
    const sphere = new THREE.Mesh(new THREE.SphereGeometry(0.8, 48, 48), new THREE.MeshStandardMaterial({ color: 0xa0cfff, metalness: 1, roughness: 0.2 }));
    sphere.position.set(0, -0.2, 0);
    avatar = new THREE.Group();
    avatar.add(sphere);
    mouth = new THREE.Mesh(new THREE.BoxGeometry(0.4,0.06,0.1), new THREE.MeshStandardMaterial({ color: 0xffffff }));
    mouth.position.set(0, 0.6, 0.7);
    avatar.add(mouth);
    scene.add(avatar);
  });

  window.addEventListener('resize', ()=>{
    renderer.setSize(container.clientWidth, container.clientHeight);
    camera.aspect = container.clientWidth/container.clientHeight;
    camera.updateProjectionMatrix();
  });

  animate();
}

let visemeQueue = [];
function animateVisemes(visemes){
  visemeQueue = visemes.slice();
}

function tickMouth(dt){
  if(!mouth) return;
  if(visemeQueue.length===0){ mouth.scale.y = THREE.MathUtils.lerp(mouth.scale.y || 1, 1, 0.1); return; }
  const now = performance.now();
  if(!tickMouth._start){ tickMouth._start = now; }
  const elapsed = now - tickMouth._start;
  const current = visemeQueue[0];
  if(elapsed >= current.time){
    // Simple mapping to openness
    const map = { 'BMP':0.3, 'FV':0.25, 'TD':0.2, 'SZ':0.2, 'KG':0.22, 'A':0.6, 'O':0.55, 'U':0.5, 'I':0.4, 'E':0.45, 'CH':0.35, 'SH':0.35, 'NG':0.2, 'L':0.3, 'R':0.3, 'Y':0.25, 'N':0.2, 'H':0.2, 'REST':0.1 };
    const openness = map[current.viseme] || 0.2;
    mouth.scale.y = 1 + openness;
    visemeQueue.shift();
  }
}

function animate(){
  requestAnimationFrame(animate);
  const dt = clock.getDelta();
  controls.update();
  // smoke drift
  for(const s of smokeParticles){ s.position.y += dt*0.2; s.material.opacity = Math.max(0, (1.5 - (s.position.y+1))/1.5); if(s.position.y>2){ s.position.y = -1; } }
  tickMouth(dt);
  renderer.render(scene, camera);
}

init();
window.animateVisemes = animateVisemes;
