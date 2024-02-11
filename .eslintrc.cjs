module.exports = {
  parserOptions: {
    parser: "@babel/eslint-parser",
    requireConfigFile: false,
    ecmaVersion: 2022,
    sourceType: "module",
  },
  extends: ["eslint:recommended", "prettier"],
  env: {
    browser: true,
    node: true,
  },
  plugins: ["import", "prettier"],
};
