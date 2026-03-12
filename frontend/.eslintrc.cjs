module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
    'plugin:react/recommended', // Include recommended rules for React
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parser: '@typescript-eslint/parser',
  plugins: ['react-refresh', 'react', '@typescript-eslint'],
  settings: {
    react: {
      version: 'detect', // Automatically detect the react version
    },
  },
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
    'react/prop-types': 'off',
    'no-unused-vars': 'warn',
    '@typescript-eslint/no-unused-vars': ['warn'], // Use TypeScript-specific rule
    '@typescript-eslint/explicit-function-return-type': 'warn', // Enforce explicit return types
    '@typescript-eslint/no-explicit-any': 'warn', // Discourage use of 'any'
    '@typescript-eslint/explicit-module-boundary-types': 'warn', // Enforce explicit types for module boundaries
    '@typescript-eslint/no-non-null-assertion': 'warn', // Discourage non-null assertions
    '@typescript-eslint/consistent-type-imports': 'warn', // Enforce consistent type imports
    'no-restricted-syntax': [
      'error',
      {
        selector: 'CallExpression[callee.name="require"]',
        message: 'Use import instead of require',
      },
    ],
    'no-var': 'error', // Disallow var, use let and const instead
    'prefer-const': 'warn', // Prefer const over let where possible
    'prefer-arrow-callback': 'warn', // Prefer arrow functions as callbacks
    'react/jsx-filename-extension': [1, { extensions: ['.tsx'] }], // Enforce .tsx extension for JSX
    'react/jsx-uses-react': 'off', // Not needed with React 17+ (new JSX transform)
    'react/react-in-jsx-scope': 'off', // Not needed with React 17+ (new JSX transform)
  },
  overrides: [
    {
      files: ['*.ts', '*.tsx'],
      rules: {
        // Additional rules specific to TypeScript files
      },
    },
    {
      files: ['*.js', '*.jsx'],
      rules: {
        'no-restricted-syntax': [
          'error',
          {
            selector: 'Program',
            message:
              'JavaScript files are not allowed. Use TypeScript instead.',
          },
        ],
      },
    },
  ],
};
