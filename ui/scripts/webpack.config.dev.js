const HtmlWebpackPlugin = require('html-webpack-plugin');
const HtmlWebpackHardDiskPlugin = require('html-webpack-harddisk-plugin');
const fs = require('fs');
const webpack = require('webpack');
const webpackOverride = fs.existsSync('./scripts/webpack.config.dev.override.js') ? require('./webpack.config.dev.override') : {};


module.exports = {
    entry: {
        run: './app/scripts/run.js'
    },
    devtool: 'source-map',
    cache: true,
    output: {
        publicPath: '/assets/',
        filename: '[name].js'
    },
    resolve: Object.assign({}, webpackOverride.resolve, {
        extensions: ['.js', '.jsx']
    }),
    module: {
        loaders: [{
            test: /\.jsx?/,
            exclude: /(node_modules)/,
            loader: 'babel-loader'
        }, {
            test: /\.scss/,
            loader: ['style-loader', 'css-loader', 'sass-loader']
        }, {
            test: /\.sass/,
            loader: ['style-loader', 'css-loader', 'sass-loader']
        }, {
            test: /\.css$/,
            loader: ['style-loader', 'css-loader']
        }, {
            test: /\.(png|jpg)$/,
            loader: 'url-loader'
        }, {
            test: /\.(eot|svg|ttf|woff(2)?)(\?[a-z0-9]+)?$/,
            loader: 'file-loader',
            options: {
                name: '[name].[ext]',
                outputPath: 'resources/fonts/',
                publicPath: '/assets/resources/fonts/'
            }
        }]
    },
    plugins: [
        new webpack.LoaderOptionsPlugin({
            debug: true,
            minimize: false
        }),
        new HtmlWebpackPlugin({
            template: './app/index_template.html',
            filename: './app/index.html',
            inject: 'html',
            alwaysWriteToDisk: true
        }),
        new HtmlWebpackHardDiskPlugin()
    ]
};
