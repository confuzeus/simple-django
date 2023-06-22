module.exports = {
  parserOptions: {
    parser: "@babel/eslint-parser",
    requireConfigFile: false,
    ecmaVersion: 2022,
    sourceType: "module",
  },
  extends: ["eslint:recommended", "plugin:prettier/recommended"],
  env: {
    browser: true,
  },
  plugins: ["import", "prettier"],
  rules: {
    "prettier/prettier": [
      "error",
      {
        singleQuote: false,
        trailingComma: "all",
        allowParens: "always",
        printwidth: 170,
        semi: true,
      },
    ],
  },
};
