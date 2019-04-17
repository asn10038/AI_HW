//CONSTANTS
CURRENT_MOVE = 0
MOVES = []
game2 = new Chess()
RESPONSE = ""
CURRENT_SCORE = ""

// new code that hopefully won't fuck the old code
function clean_pgn() {
  pgn = $('#game-pgn').text()
  splt = pgn.split('\n')
  splt.shift()
  splt.pop()
  splt[0] = splt[0].trim()
  return splt.join('\n')
}

function make_next_move() {
  game2.move(MOVES[CURRENT_MOVE])
  //board.position(game.fen())
  CURRENT_MOVE++
  board.position(game2.fen())
}

function score_next_move() {
  stockfish.postMessage("position fen " + board.fen())
  stockfish.postMessage("eval")
  return 0
}

function parse_evaluation(event) {
  resp = event.data
  RESPONSE += resp
  if(RESPONSE.indexOf("Total Evaluation") != -1) {
    score = RESPONSE.substring(RESPONSE.indexOf("Total Evaluation"))
    CURRENT_SCORE = score
    RESPONSE = ""
    $("#scratch").text(CURRENT_SCORE)
  }
}
//randome game code
var board,
  game = new Chess();

// do not pick up pieces if the game is over
// only pick up pieces for White
var onDragStart = function(source, piece, position, orientation) {
  if (game.in_checkmate() === true || game.in_draw() === true ||
    piece.search(/^b/) !== -1) {
    return false;
  }
};

var makeRandomMove = function() {
  var possibleMoves = game.moves();

  // game over
  if (possibleMoves.length === 0) return;

  var randomIndex = Math.floor(Math.random() * possibleMoves.length);
  game.move(possibleMoves[randomIndex]);
  board.position(game.fen());
};

var onDrop = function(source, target) {
  // see if the move is legal
  var move = game.move({
    from: source,
    to: target,
    promotion: 'q' // NOTE: always promote to a queen for example simplicity
  });

  // illegal move
  if (move === null) return 'snapback';

  // make random legal move for black
  window.setTimeout(makeRandomMove, 250);
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




// new code that hopefully doesn't break everything
$(document).ready(function(){
  //stockfish worker
  stockfish = new Worker('../static/js/stockfish.js')
  stockfish.onmessage = function(event) { parse_evaluation(event); }
  stockfish.onmessageerror = function(event) { alert("THERE WAS AN ERROR")}
  stockfish.onerror = function(event){alert("ERROR " + event.message)}
  //game stuff
  if(!game.load_pgn(clean_pgn())) {
    alert("ERROR ON GAME LOAD")
  }
  else {
    console.log("game loaded")
  }
  MOVES = game.history()
  $('#next').click(function() {
    make_next_move();
    score = score_next_move();
  })
})
