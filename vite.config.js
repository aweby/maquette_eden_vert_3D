import { defineConfig } from 'vite';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));

/**
 * Serveur de dev pour les pages HTML statiques + chargement du module toolbar.
 * Le build utilise une entrée minimale : ce dépôt n’est pas une app bundlée classique.
 */
export default defineConfig({
  root: '.',
  appType: 'mpa',
  build: {
    rollupOptions: {
      input: { _toolbar_probe: resolve(__dirname, 'src/dev-21st-toolbar.ts') },
    },
    outDir: 'dist',
    emptyOutDir: true,
  },
});
