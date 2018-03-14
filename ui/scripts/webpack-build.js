// Lib imports
const shell = require('shelljs');

// Constants
const OUTPUT_FOLDER = 'app/output';
const ASSETS_FOLDER = OUTPUT_FOLDER + '/assets';

// Remove output folder
shell.rm('-rf', OUTPUT_FOLDER);

// Create output folder
shell.mkdir('-p', OUTPUT_FOLDER);
shell.mkdir('-p', ASSETS_FOLDER);

// Copy resources to folder
shell.cp('-r', 'app/resources', 'app/output/resources');
shell.cp('-r', 'app/resources', 'app/output/assets/resources');

// Launch webpack
shell.exec('webpack --config ./scripts/webpack.config.prod.js');
