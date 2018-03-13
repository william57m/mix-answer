import React from 'react';
import ReactDOM from 'react-dom';
import Router from './router';
require('../styles/main.scss');

ReactDOM.render(
  <Router />,
  document.getElementById('app')
);
