import React from 'react';
import { Link } from 'react-router';

function createGameElement(game){
  return (
    <div class="game__container">
        <span class="game__body">
        <h4 class="game__header">{ game.name }</h4>
        <p>
          <button  data-action="" name="create" class="game__must">Must</button>
        </p>
        <a href="" class="game__link">Open</a>
      </span>
      {game.images ? (<img data-url={game.images[0].url} class="game__img"/>
      ) : (
          <img src="static/media/no-image.png" class="game__img" alt="no image"/>
      )}
   </div>
  );
}

export default function(props) {
  return (
    <div class="game" id="games" data-page="1">
        {props.games.map(game => createGameElement(game))}
    </div>
  );
}
