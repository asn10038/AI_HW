//CONSTANTS
var all_positions = ["Catcher",
                     "Pitcher",
                     "Designated Hitter",
                     "Centerfielder",
                     "Rightfielder",
                     "Leftfielder",
                     "First Baseman",
                     "Second Baseman",
                     "Third Baseman",
                     "Shortstop",
                     "Outfielder" ] 
var inputChecks = [
  $('#firstBasemanInput'),
  $('#secondBasemanInput'),
  $('#thirdBasemanInput'),
  $('#DHInput'),
  $('#RightfielderInput'),
  $('#LeftfieldsInput'),
  $('#CenterfielderInput'),
  $('#PitcherInput'),
  $('#CatcherInput')
]


//LOGIC
function getPositions() {

  for
}

function addPlayer() {
  fullname = $('#fullnameInput').val();
  born = $('#bornInput').val();
  bio = $('#bioInput').val();
  image_url = $('#imageURLInput').val();

  rookie_status = $('#rookieStatusInput').val();
  last_game = $('#lastGameInput').val();

  positions = getPositions();
  bats = $('#batsInput').val();
  throws = $('#throwsInput').val();
  war = $().val('#WARInput').val();

}

//LAYOUT
function install_handlers(){
  $('#addPlayerBtn').click(addPlayer);
}
//MAIN
$(document).ready(function(){
  install_handlers();
});
