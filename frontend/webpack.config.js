const {VueLoaderPlugin} = require('vue-loader');

module.exports={
    entry: './app/main.js',
    output:{
        path: __dirname + '/public/static/js',
        filename:'bundle.js'
    },
    module:{
        rules:[
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            },
            {
                test: /\.js$/,
                exclude : /node_modules/,
                use:{
                    loader: 'babel-loader'
                }
            },
            {
                test: /\.vue$/,
                use: 'vue-loader'
            },
            {
                test: /\.s(c|a)ss$/,
                use: [
                  'vue-style-loader',
                  'css-loader',
                  {
                    loader: 'sass-loader',
                    // Requires sass-loader@^7.0.0
                    options: {
                      implementation: require('sass'),
                      fiber: require('fibers'),
                      indentedSyntax: true // optional
                    },
                    // Requires sass-loader@^8.0.0
                    options: {
                      implementation: require('sass'),
                      sassOptions: {
                        fiber: require('fibers'),
                        indentedSyntax: true // optional
                      },
                    },
                  },
                ],
            },
        ]
    },
    plugins:[
        new VueLoaderPlugin()
    ]
};