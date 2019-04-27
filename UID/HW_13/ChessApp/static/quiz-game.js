var board,
  game = new Chess();

//load the game
var clean_pgn = function() {
  pgn = $('#game-pgn').text()
  splt = pgn.split('\n')
  splt.shift()
  splt.pop()
  splt[0] = splt[0].trim()
  return splt.join('\n')
}

var get_result_string = function(correct) {
  if(correct) {
    return "<img src='/static/img/correct.png' class='result-image'></img>"
  } else {
    return "<img src='/static/img/incorrect.png' class='result-image'></img>"
  }
}
var show_correct = function() {
  $('#result').html(
    get_result_string(true)
  )

}

var show_incorrect = function() {
  $('#result').html(get_result_string(false));
}

if(!game.load_pgn(clean_pgn())) {
  alert("ERROR ON GAME LOAD")
}
else {
  console.log("game loaded")
}

CURRENT_MOVE = 0
MOVES = game.history()
game.reset()
TARGET = ""
// do not pick up pieces if the game is over
// only pick up pieces for White
var onDragStart = function(source, piece, position, orientation) {
  if (game.in_checkmate() === true || game.in_draw() === true /* ||
    piece.search(/^b/) !== -1*/) {
    return false;
  }
};


var onDrop = function(source, target) {
  TARGET = target
  // see if the move is legal
  //TODO make this work
  if (MOVES[CURRENT_MOVE].includes(target))
  {
    CURRENT_MOVE ++;
  } else {
    show_incorrect()
    return 'snapback'
  }

  var move = game.move({
    from: source,
    to: target,
    promotion: 'q' // NOTE: always promote to a queen for example simplicity
  });
  // illegal move
  if (move === null) {
    CURRENT_MOVE--;
    show_incorrect()
    return 'snapback';
  }

  show_correct()

};

// update the board position after the piece snap
// for castling, en passant, pawn promotion
var onSnapEnd = function() {
  board.position(game.fen());
};

var cfg = {
  draggable: true,
  position: 'start',
  onDragStart: onDragStart,
  onDrop: onDrop,
  onSnapEnd: onSnapEnd
};
board = ChessBoard('board', cfg);
