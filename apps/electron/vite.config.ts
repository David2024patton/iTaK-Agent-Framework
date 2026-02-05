import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';

const currentDir = dirname(fileURLToPath(import.meta.url));
const rendererSource = resolve(currentDir, 'src', 'renderer');
const hooksSource = resolve(currentDir, 'src', 'hooks');
const outputPath = resolve(currentDir, 'dist', 'renderer');

export default defineConfig({
  plugins: [react()],
  root: rendererSource,
  base: './',
  build: {
    outDir: outputPath,
    emptyOutDir: true,
    rollupOptions: {
      input: resolve(rendererSource, 'index.html'),
    },
  },
  server: {
    port: 5173,
    strictPort: true,
  },
  resolve: {
    alias: {
      '@renderer': rendererSource,
      '@hooks': hooksSource,
    },
  },
});
