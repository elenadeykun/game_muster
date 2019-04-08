import React from 'react';
import { Link } from 'react-router';
import PropTypes from 'prop-types';

function CreateGameElement(game){
  return (
    <div className="game__container" key={game.id}>
        <span className="game__body">
        <h4 className="game__header">{ game.name }</h4>
        <p>
         <Link to={'/games/' + game.id}>Link</Link>
          <button  data-action="" name="create" className="game__must">Must</button>
        </p>
        <a href="" className="game__link">Open</a>
      </span>
      {game.images.length > 0 ? (<img data-url={game.images[0].url} className="game__img"/>
      ) : (
          <img src="static/media/no-image.png" className="game__img" alt="no image"/>
      )}
   </div>
  );
}

export default function(props) {
  return (
    <div className="game" id="games" data-page="1">
        {props.games.map(game => CreateGameElement(game))}
    </div>
  );
}
