//CONTSANTS

//logic functions
function get_result_row_html(img_url,
                             fullname,
                             WAR,
                             born,
                             id) {
  return "<div class='row result-row'>" +
    "<div class='col-md-2'>" +
      "<img src='" + img_url + "'></img>" +
    "</div>" +
    "<div class='col-md-3'>" +
      fullname +
    "</div>" +
    "<div class='col-md-1'>" +
      WAR +
    "</div>" +
    "<div class='col-md-5'>" +
      born +
    "</div>" +
    "</div>"
}

function paint_results(results) {
  $('#resultsDiv').empty()
  for (i in results) {
    console.log(results[i])
    html = get_result_row_html(results[i]['image_url'],
                               results[i]['full_name'],
                               results[i]['WAR'],
                               results[i]['born'])
    $('#resultsDiv').append(html);
  }
}

function search() {
  query = $('#searchBar').val()
  $.ajax({
      type: "POST",
      url: "search",
      dataType : "json",
      contentType: "application/json; charset=utf-8",
      data : JSON.stringify(query),
      success: function(result){
        players= result['data']['players'];
        console.log(players)
        paint_results(players)
      },
      error: function(request, status, error){
          console.log("Error");
          console.log(request);
          console.log(status);
          console.log(error);
      }
  });
}
// layout functions
function install_handlers(){
  $('#searchButton').click(search);
}
//Main
$(document).ready(function(){
  install_handlers();
});
