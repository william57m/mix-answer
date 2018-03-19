const HtmlWebpackPlugin = require('html-webpack-plugin');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');
const webpack = require('webpack');

const OUTPUT = '/home/webapp/app/output';
const SCRIPT_OUTPUT = OUTPUT + '/assets';

module.exports = {
    entry: {
        run: './app/scripts/run.js'
    },
    devtool: false,
    cache: false,
    output: {
        publicPath: 'assets/', // User by HtmlWebpackPlugin to prefix src files
        path: SCRIPT_OUTPUT,
        filename: '[name].[chunkhash].js'
    },
    resolve: {
        extensions: ['.js', '.jsx']
    },
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
                publicPath: 'assets/resources/fonts/'
            }
        }]
    },
    plugins: [
        new webpack.LoaderOptionsPlugin({
            debug: false,
            minimize: true
        }),
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: JSON.stringify('production')
            }
        }),
        new HtmlWebpackPlugin({
            template: './app/index_template.html',
            filename: OUTPUT + '/index.html',
            inject: 'html'
        }),
        new UglifyJSPlugin()
    ]
};
