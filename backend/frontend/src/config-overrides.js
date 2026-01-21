const path = require('path');

module.exports = function override(config) {
  config.output = {
    ...config.output,
    path: path.resolve(__dirname, '../static/react'),
    publicPath: '/static/react/'
  };
  return config;
};