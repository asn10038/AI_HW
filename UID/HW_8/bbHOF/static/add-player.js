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
  '#CatcherInput',
  '#PitcherInput',
  '#DHInput',
  '#CenterfielderInput',
  '#RightfielderInput',
  '#LeftfielderInput',
  '#firstBasemanInput',
  '#secondBasemanInput',
  '#thirdBasemanInput',
  '#ShortstopInput',
  '#OutfielderInput'
]

var generalInputs = [
  '#fullnameInput',
  '#bornInput',
  '#bioInput',
  '#imageURLInput',
  '#rookieStatusInput',
  '#lastGameInput',
  '#batsInput',
  '#throwsInput',
  '#WARInput'
]

//LOGIC

function inputError() {
  alert("input error")
}
function getPositions() {
  positions = []
  for (var i in inputChecks) {
    if($(inputChecks[i]).is(':checked')){
      positions.push(all_positions[i])
    }
  }
  console.log(positions)
}

function safeInput(){
  var positionChecked = false;
  WARVal = $('#WARInput').val()
  if( isNaN(WARVal) || !isFinite(WARVal)) {
    console.log('war val not valid')
    return false;
  }

  for(var i in generalInputs) {
    if ($(generalInputs[i]).val() == ''){
      console.log(generalInputs[i])
      return false
    }
  }
  for(var i in inputChecks) {
    console.log(inputChecks[i])
    if($(inputChecks[i]).is(':checked')) {
      positionChecked = true;
      console.log('position is checked')
      break;
    }
  }
  if (!positionChecked) {
    console.log('no positions checked')
    return false;
  }
  return true;
}
function clearInputs() {
  for (var i in inputChecks)
    $(inputChecks[i]).prop('checked', false)
  for (var i in generalInputs)
    $(generalInputs[i]).val('');
}

function addPlayer() {
  if(!safeInput())
    return inputError();

  fullname = $('#fullnameInput').val();
  born = $('#bornInput').val();
  bio = $('#bioInput').val();
  image_url = $('#imageURLInput').val();

  rookie_status = $('#rookieStatusInput').val();
  last_game = $('#lastGameInput').val();

  positions = getPositions();
  bats = $('#batsInput').val();
  throws = $('#throwsInput').val();
  war = $('#WARInput').val();

  player = {
    'fullname' : fullname,
    'born' : born,
    'bio' : bio,
    'image_url' : image_url,
    'rookie_status' : rookie_status,
    'last_game' : last_game,
    'positions' : positions,
    'bats' : bats,
    'throws' : throws,
    'WAR' : war
  }
  $.ajax({
      type: "POST",
      url: "add_item",
      dataType : "json",
      contentType: "application/json; charset=utf-8",
      data : JSON.stringify(player),
      success: function(result){
        console.log(result['data'])

        //reconfig autocomplete
        newPlayerLink = result['data']['link-to-view'];
        console.log(newPlayerLink)
        $('#newPlayerLink').attr('href', newPlayerLink)
        $('#newPlayerLink').text(newPlayerLink)
        $('#successAdd').show()
        // clearInputs()
      },
      error: function(request, status, error){
          $('#failAdd').show()
          console.log("Error");
          console.log(request);
          console.log(status);
          console.log(error);
      }
  });
  return player
}

//LAYOUT

function install_handlers(){
  $('#successAdd').hide()
  $('#failAdd').hide()
  $("#closeSuccessAlert").click(function() {
      $('#successAdd').hide()
  })
  $("#closeFailAlert").click(function() {
      $('#failAdd').hide()
  })

  $('#addPlayerBtn').click(addPlayer);
}
//MAIN
$(document).ready(function(){
  install_handlers();
});
