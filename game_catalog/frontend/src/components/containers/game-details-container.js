import React, { Component } from 'react';
import _ from 'lodash';
import GameDetails from '../views/game-details';
import * as gameApi from '../../api/game-api';
import PropTypes from 'prop-types';

class GameDetailsContainer extends React.Component {
  constructor(props) {
   super(props);
   this.state = {game: []};
  }

  componentDidMount () {
    let component = this;
    let gameId = this.props.params.gameId;
    gameApi.getGame(gameId).then(function(game){
      component.setState({game: game});
    });
  }

  render () {
    return (
      <GameDetails {...this.state}/>
    );
  }
}

export default GameDetailsContainer;
