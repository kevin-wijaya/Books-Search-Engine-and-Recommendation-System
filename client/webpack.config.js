const path = require('path');
const webpack = require('webpack');
const TerserPlugin = require('terser-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');

const PROD = JSON.parse(process.env.PROD_ENV || false);

module.exports = {
    mode: PROD ? 'production' : 'development',
    watch: !PROD,
    entry: './src/index.js',
    output: {
        path: path.resolve(__dirname, '.dist'),
        filename: PROD ? 'bundle.min.js' : 'bundle.js'
    },
    optimization: {
        minimize: PROD,
        minimizer: [
            new TerserPlugin({ parallel: true })
        ],
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
        }),
        new HtmlWebpackPlugin({
            inject: false,
            template: './src/index.html', 
            minify: {
                collapseWhitespace: true,
                removeComments: true,
                removeRedundantAttributes: true,
                useShortDoctype: true,
                removeEmptyAttributes: true,
                removeStyleLinkTypeAttributes: true,
                keepClosingSlash: true,
                minifyJS: true,
                minifyCSS: true,
                minifyURLs: true,
            },
        }),
    ],
}