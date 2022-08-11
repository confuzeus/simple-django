const path = require("path");
require("dotenv").config({
  path: path.resolve(process.cwd(), "appconfig.env"),
});
const { src, dest, parallel, series, watch } = require("gulp");

const autoprefixer = require("autoprefixer");
const browserSync = require("browser-sync").create();
const cssnano = require("cssnano");
const clean = require("gulp-clean");
const imagemin = require("gulp-imagemin");
const plumber = require("gulp-plumber");
const postcss = require("gulp-postcss");
const rename = require("gulp-rename");
const sass = require("gulp-sass")(require("sass"));
const gulpTerser = require("gulp-terser");

const isProd = process.env.NODE_ENV === "production";

function pathsConfig() {
  const staticSrc = `./staticSrc`;
  const vendorsRoot = "./node_modules";
  const staticDest = "./static";
  return {
    bootstrapSass: `${vendorsRoot}/bootstrap/scss`,
    vendorsJs: [
      `${vendorsRoot}/@popperjs/core/dist/umd/popper.js`,
      `${vendorsRoot}/bootstrap/dist/js/bootstrap.js`,
      `${vendorsRoot}/smooth-scroll/dist/smooth-scroll.polyfills.js`,
    ],
    icons: [`${vendorsRoot}/bootstrap-icons/bootstrap-icons.svg`],
    templates: "./templates",
    sass: `${staticSrc}/scss`,
    images: `${staticSrc}/images`,
    js: `${staticSrc}/js`,
    fonts: `${staticSrc}/fonts`,
    fontsDest: `${staticDest}/fonts`,
    cssDest: staticDest + "/css",
    jsDest: staticDest + "/js",
    imageDest: staticDest + "/images",
    iconsDest: staticDest + "/icons",
  };
}

var paths = pathsConfig();

var processCss = [autoprefixer()];

var minifyCss = [cssnano({ preset: "default" })];

function processScss() {
  let css = src(`${paths.sass}/main.scss`)
    .pipe(
      sass({
        includePaths: [paths.sass],
      }).on("error", sass.logError)
    )
    .pipe(plumber())
    .pipe(postcss(processCss))
    .pipe(rename({ suffix: ".min" }));
  if (isProd) {
    css = css.pipe(postcss(minifyCss));
  }
  return css.pipe(dest(paths.cssDest));
}

function processJs() {
  let js = src(`${paths.js}/*.js`)
    .pipe(plumber())
    .pipe(rename({ suffix: ".min" }));
  if (isProd) {
    js = js.pipe(gulpTerser());
  }
  return js.pipe(dest(paths.jsDest));
}

function processVendorJs() {
  return src(paths.vendorsJs)
    .pipe(plumber())
    .pipe(gulpTerser())
    .pipe(rename({ suffix: ".min" }))
    .pipe(dest(paths.jsDest));
}

function copyIcons() {
  return src(paths.icons).pipe(dest(paths.iconsDest));
}

function copyFonts() {
  return src(`${paths.fonts}/*`).pipe(dest(paths.fontsDest));
}

function compressImages() {
  return src(`${paths.images}/**/*.*(jpeg|jpg|png|ico|gif|svg)`)
    .pipe(
      imagemin([
        imagemin.gifsicle({ interlaced: true }),
        imagemin.mozjpeg({ quality: 70, progressive: true }),
        imagemin.optipng({ optimizationLevel: 7 }),
        imagemin.svgo({
          plugins: [{ removeViewBox: true }, { cleanupIDs: false }],
        }),
      ])
    )
    .pipe(dest(paths.imageDest));
}

function cleanDest() {
  return src([
    `${paths.cssDest}/**/*.css`,
    `${paths.jsDest}/**/*.js`,
    `${paths.imageDest}/**/*`,
    `${paths.iconsDest}/**/*`,
  ]).pipe(clean());
}

function initBrowserSync() {
  let https;

  https = (process.env.BROWSERSYNC_HTTPS || "false") !== "false";

  const proxy = `${https ? "https" : "http"}://localhost:8000`;
  browserSync.init({
    ui: {
      port: 3001,
    },
    port: 3000,
    proxy,
    open: false,
    https,
    files: [
      `${paths.cssDest}/**/*.css`,
      `${paths.jsDest}/**/*.js`,
      `${paths.templates}/**/*.html`,
    ],
  });
}

function watchPaths() {
  watch([`${paths.js}/**/*.js`], processJs);
  watch([`${paths.sass}/**/*.scss`], processScss);
}

const generateAssets = parallel(
  processScss,
  processJs,
  processVendorJs,
  compressImages,
  copyIcons,
  copyFonts
);

const dev = parallel(initBrowserSync, watchPaths);

exports.default = series(generateAssets, dev);
exports.generateAssets = generateAssets;
exports.cleanDest = cleanDest;
