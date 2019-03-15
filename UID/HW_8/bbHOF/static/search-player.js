//CONTSANTS

//logic functions
function get_result_row_odd_html(img_url,
                             fullname,
                             WAR,
                             born,
                             id) {
  return "<div class='row odd-row result-row'>" +
    "<div class='search_image col-md-2'>" +
      "<img class='result-image' src='" + img_url + "'></img>" +
    "</div>" +
    "<div class='col-md-3'>" +
    "<a class='result-name' href='/view_item/" + id + "'" +">" +
      fullname + "</a>" +
    "</div>" +
    "<div class='col-md-1'>" + "<span class='bold'>" +
      WAR + "</span>" +
    "</div>" +
    "<div class='col-md-5'>" +
      born +
    "</div>" +
    "</div>"
}

function get_result_row_even_html(img_url,
                             fullname,
                             WAR,
                             born,
                             id) {
  return "<div class='row even-row result-row'>" +
    "<div class='search_image col-md-2'>" +
      "<img class='result-image' src='" + img_url + "'></img>" +
    "</div>" +
    "<div class='col-md-3'>" +
    "<a class='result-name' href='/view_item/" + id + "'" +">" +
      fullname + "</a>" +
    "</div>" +
    "<div class='col-md-1'>" + "<span class='bold'>" +
      WAR + "</span>" +
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
    get_html = (i%2==0 ? get_result_row_even_html : get_result_row_odd_html)
    html = get_html(results[i]['image_url'],
                               results[i]['full_name'],
                               results[i]['WAR'],
                               results[i]['rookie_status'],
                               results[i]['id'])
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
        players = result['data']['players'];
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
function install_handlers2(){
  $('#searchButton').click(search);
}
//Main
$(document).ready(function(){
  install_handlers2();
});
