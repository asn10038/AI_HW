//CONSTANTS
CURRENT_MOVE = 0
MOVES = []
game2 = new Chess()
game3 = new Chess()
RESPONSE = ""
CURRENT_SCORE = ""

BOARDS = []

WIN_GRAPH_MOVE_NUM = [0]
WIN_GRAPH_EVAL = [.09 ]
SCORES = {0:.09}
NEXT_EVAL = 0

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
    floatScore = parseFloat(score.split(" ")[2])
    SCORES[NEXT_EVAL] = floatScore
    update_graph_traces()

  }
}

function update_graph_traces() {
  WIN_GRAPH_MOVE_NUM = []
  WIN_GRAPH_EVAL = []
  for(var i=0; i<=NEXT_EVAL; i++) {
    WIN_GRAPH_MOVE_NUM.push(i)
    WIN_GRAPH_EVAL.push(SCORES[i])
    paint_graph()
  }
}
//fills in the traces through move x
function start_graph_update(x) {
  NEXT_EVAL = x
  score = score_next_move()
}
//randome game code
var board,
  game = new Chess();


var cfg = {
  draggable: false,
  position: 'start',
};
board = ChessBoard('board', cfg);

//simulate the game and generate of the board
function add_board(num, fen) {
  //TODO remove this safeguard
  var nextBoard = $("<div></div>").attr("id", "board-"+num)
  nextBoard.attr("class", "col-md-3 little-board")
  $('#all-boards').append(nextBoard)
  boardX = ChessBoard('board-'+num)
  boardX.position(game3.fen())
  BOARDS.push(boardX)
}

function add_boards(){
  curr_move = 0
  for (move in MOVES) {
    add_board(move, game3.fen())
    game3.move(MOVES[curr_move])
    curr_move++;
  }
}


function paint_graph(){

  var trace1 = {
  x: WIN_GRAPH_MOVE_NUM,
  y: WIN_GRAPH_EVAL,
  fill: 'tozeroy',
  type: 'scatter'
  };

  var data = [trace1];
  layout = {
    title: 'Position Evaluation',
    xaxis: {
      title: { text: "Move Number" }
    },
    yaxis: {
      title: { text: "Position Score" }
    }
  }
  Plotly.newPlot('eval-graph', data, layout, {showSendToCloud:true});


}

// new code that hopefully doesn't break everything
$(document).ready(function(){
  //start stockfish worker
  stockfish = new Worker('../static/js/stockfish.js')
  stockfish.onmessage = function(event) { parse_evaluation(event); }
  stockfish.onmessageerror = function(event) { alert("THERE WAS AN ERROR")}
  stockfish.onerror = function(event){alert("ERROR " + event.message)}

  //load the game
  if(!game.load_pgn(clean_pgn())) {
    alert("ERROR ON GAME LOAD")
  }
  else {
    console.log("game loaded")
  }
  MOVES = game.history()

  //generate all the boards
  add_boards()

  //set up the slider
  $('#all-boards').slick({
  centerMode: true,
  centerPadding: '60px',
  slidesToShow: 3,
  focusOnSelect: true,
  arrows: true,
  infinite: false,
  responsive: [
    {
      breakpoint: 768,
      settings: {
        arrows: false,
        centerMode: true,
        centerPadding: '40px',
        slidesToShow: 3
      }
    },
    {
      breakpoint: 480,
      settings: {
        arrows: false,
        centerMode: true,
        centerPadding: '40px',
        slidesToShow: 1
      }
    }
  ]
  });

  //install slider handler
  $('#all-boards').on('beforeChange', function(event, slick, currentSlide, nextSlide){
    x = nextSlide
    board.position(BOARDS[x].fen())
    start_graph_update(x)
  })

  //paint the eval graph
  paint_graph()
})
