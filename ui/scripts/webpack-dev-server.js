// Lib imports
const webpack = require('webpack');
const webpackDevServer = require('webpack-dev-server');

// Config import
const config = require('./webpack.config.dev');

// Constants
const HOST = '0.0.0.0';
const PORT = 8080;
const RELOAD_ON_CHANGE = true;
const POLL_IN_MS = 1000;

// Configuration
const options = {
    // Display options
    progress: true,
    stats: {
        colors: true,
        assets: false,
        modules: false
    },
    // Config
    hot: true,
    host: HOST,
    disableHostCheck: true,
    port: PORT,
    publicPath: '/assets/', // Path where the file are served
    contentBase: './app/', // Path to the sources
    inline: RELOAD_ON_CHANGE,
    watchOptions: {
        poll: POLL_IN_MS,
        ignored: /node_modules/
    }
};

console.log('Starting the dev web server...');
const server = new webpackDevServer(webpack(config), options);
server.listen(PORT, HOST, function (err) {
    console.log(err ? err : 'Dev server listening at', HOST + ':' + PORT);
});
