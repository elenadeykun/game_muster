import React from 'react';
import { Router, Route, browserHistory, IndexRoute } from 'react-router';

import MainLayout from './components/layouts/main-layout';
import GameListContainer from './components/containers/game-list-container'
import GameDetailsContainer from './components/containers/game-details-container'

export default (
  <Router history={browserHistory}>
  <Route component={MainLayout}>
    <Route path="/" component={GameListContainer} />
    <Route path="games">
      <IndexRoute component={GameListContainer} />
      <Route path=":gameId" component={GameDetailsContainer} />
    </Route>
    <Route path="games" component={GameListContainer}/>
  </Route>
</Router>
);
