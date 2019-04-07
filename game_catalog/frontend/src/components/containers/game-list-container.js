import React, { Component } from 'react';
import _ from 'lodash';
import GameList from '../views/game-list';
import * as gameApi from '../../api/game-api';

class GameListContainer extends React.Component {
  constructor(props) {
   super(props);
   this.state = {games: []};
 }

  componentDidMount () {
    let component = this;
    gameApi.getGames().then(function(games){
      component.setState({games: games});
    });
  }

  render () {
    return (
      <GameList games={this.state.games} />
    );
  }
}

export default GameListContainer;
