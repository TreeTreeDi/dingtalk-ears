import js from '@eslint/js';
import globals from 'globals';
export default [
  js.configs.recommended,
  {
    files: ['backend/static/**/*.js'],
    languageOptions: { globals: globals.browser },
  },
];
