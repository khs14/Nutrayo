import { defineConfig } from 'vite';
import { resolve, basename } from 'node:path';
import { headerHTML, filtersHTML, contactHTML, footerHTML } from './src/components/markup.js';

const PAGE_BY_FILE = { 'index.html': 'table', 'examples.html': 'examples', 'why.html': 'why', 'contact.html': 'contact', 'my-foods.html': 'mine' };

// Writes the header and filter bar into each page's HTML, so they show
// immediately instead of popping in after the JavaScript loads.
const prerenderShell = () => ({
  name: 'prerender-shell',
  transformIndexHtml: {
    order: 'pre',
    handler(html, ctx) {
      const page = PAGE_BY_FILE[basename(ctx.filename)] ?? 'table';
      return html
        .replace('<!--header-->', headerHTML(page))
        .replace('<!--filters-->', filtersHTML())
        .replace('<!--contact-->', contactHTML())
        .replace('<!--footer-->', footerHTML(page));
    },
  },
});

export default defineConfig({
  // Relative paths so the build works on GitHub Pages (/repo-name/),
  // Cloudflare Pages, Netlify or any static host without changes.
  base: './',
  plugins: [prerenderShell()],
  build: {
    rollupOptions: {
      input: {
        main: resolve(import.meta.dirname, 'index.html'),
        examples: resolve(import.meta.dirname, 'examples.html'),
        why: resolve(import.meta.dirname, 'why.html'),
        contact: resolve(import.meta.dirname, 'contact.html'),
        mine: resolve(import.meta.dirname, 'my-foods.html'),
      },
    },
  },
});
