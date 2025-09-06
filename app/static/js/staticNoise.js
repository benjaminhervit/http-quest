// ============================
    // STATIC NOISE RENDERER (Canvas)
    // ============================
    (function(){
      const canvas = document.getElementById('noiseCanvas');
      const ctx = canvas.getContext('2d', { willReadFrequently: false });

      let w, h, id, frame = 0;
      const draw = () => {
        if (!w || !h) return;
        const imageData = ctx.createImageData(w, h);
        const buffer = new Uint32Array(imageData.data.buffer);
        for (let i = 0; i < buffer.length; i++) {
          // Random grayscale noise with alpha
          const v = Math.random() * 255 | 0;
          buffer[i] = (255   << 24) | (v << 16) | (v << 8) | (v);
        }
        ctx.putImageData(imageData, 0, 0);
      };

      const loop = () => {
        draw();
        frame = (frame + 1) % 2; // could throttle if needed
        id = setTimeout(loop, 50); // ~20 FPS for choppy TV vibe
      };

      const resize = () => {
        const dpr = Math.min(2, window.devicePixelRatio || 1);
        w = canvas.width = Math.floor(innerWidth * dpr);
        h = canvas.height = Math.floor(innerHeight * dpr);
        canvas.style.width = innerWidth + 'px';
        canvas.style.height = innerHeight + 'px';
      };

      window.addEventListener('resize', resize, { passive: true });
      resize();
      loop();

      // Respect reduced motion
      const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
      const updateMotion = () => {
        if (mq.matches) { clearTimeout(id); canvas.classList.add('low'); }
        else { canvas.classList.remove('low'); loop(); }
      };
      mq.addEventListener('change', updateMotion);
      updateMotion();
    })();