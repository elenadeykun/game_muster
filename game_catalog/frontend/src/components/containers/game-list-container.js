import React, { Component } from 'react';
import { connect } from 'react-redux';
import GameList from '../views/game-list';
import * as gameApi from '../../api/game-api';
import PropTypes from 'prop-types';
import store from '../../store';

class GameListContainer extends React.Component {
  componentDidMount () {
    gameApi.getGames();
  }

  render () {
    return (
      <GameList games={this.props.games}/>
    );
  }
}

const mapStateToProps = function(store) {
  return {
    games: store.gameState.games,
    user: store.userState.user,
  };
};


export default connect(mapStateToProps)(GameListContainer);
