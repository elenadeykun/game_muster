import React from 'react';

function CreateImagesSection(images){
  const imageItems = images.images.map((image) =>
    <img key={image.url} data-url={image.url} className="screen-img" alt="pacman"/>
  );

  return (
    <div>
       <h4 className="game-description__title">Screenshots</h4>
       <div> {imageItems} </div>
     </div>
  );
}

function CreateDetailsSection(game){
  game = game.game;
  const genres = game.genres.map((genre) =>
                  <span className="toast"> {genre.name} </span>
                );
  const platforms = game.platforms.map((genre) =>
                    <span className="toast"> {genre.name} </span>
                  );
  return (
    <div className="description__section">
      { (game.users_rating > 0 || game.critics_rating > 0) &&
        <h4 className="game-description__title">Rating</h4>
      }
      { game.users_rating > 0 &&
        <div className="game-description__rating">
          <span>Users</span>
          <span className="game-description__views">{game.users_rating}
          ({game.users_views} views)</span>
        </div>
      }
      { game.critics_rating > 0 &&
        <div className="game-description__rating critics-rating">
          <span>Critics</span>
          <span className="game-description__views">{game.critics_rating}
          ({game.critics_views} views)</span>
        </div>
      }
      { game.genres.length > 0 &&
        <div>
          <h4 class="game-description__title">Genres</h4>
          {genres}
        </div>
      }
      { game.platforms.length > 0 &&
        <div>
          <h4 class="game-description__title">Platforms</h4>
          {platforms}
        </div>
      }

      </div>
    );
}

export default function(props) {
  const game = props.game;

  return (
    <div className="game-article">
      <h3 className="game-article__header">{props.game.name}</h3>
      <div className="game-description">
          <div className="game-description__section main-game-section">
              <h4 className="game-description__title">Description</h4>
              { game.description && (game.description.length > 0)
                ? ( <p> { game.description } </p>
              ):(
                  <p> No information available yet.</p>
              )}

              { game.release_date &&
                  <div>
                    <h4 className="game-description__title">Release Date</h4>
                    <p>{ game.release_date }</p>
                  </div>
              }

              { game.images && game.images.length > 0 &&
                <CreateImagesSection images={game.images}/>
              }

          </div>
          <CreateDetailsSection game={game}/>
       </div>
     </div>
  );
}
