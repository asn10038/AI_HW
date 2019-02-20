// Models
var employees = [
"Phyllis",
"Angela",
"Dwight",
"Oscar",
"Creed",
"Pam",
"Jim",
"Stanley",
"Michael",
"Kevin",
"Kelly"
]
var ppcEmployees = []
var nonPpcEmployees = []

// logic Functions
function initializeLists(){
  nonPpcEmployees = employees.slice();
  ppcEmployees = [];
}


// layout Functions
function get_ppc_list_item_html(name, i) {
  return '<div class="row list-item"  id="ppc-' + i + '">' +
    '<div>' +
      name +
    '</div>' +
  '</div>'
}

function get_non_ppc_list_item_html(name, i) {
  return '<div class="row list-item"  id="non-ppc-' + i + '">' +
    '<div>' +
      name +
    '</div>' +
  '</div>'
}

function paint_ppc_list()
{
  $('#ppc-list').empty();
  for(i in ppcEmployees) {
    html = get_ppc_list_item_html(ppcEmployees[i], i)
    $('#ppc-list').append(html);
  }
}

function paint_non_ppc_list() {
  $('#non-ppc-list').empty();
  for(i in nonPpcEmployees) {
    html = get_ppc_list_item_html(nonPpcEmployees[i], i)
    $('#non-ppc-list').append(html);
  }
}

function paint_lists() {
  // paint_ppc_list();
  paint_non_ppc_list();
}

// Main
function setup(){
  initializeLists();
  paint_lists();
}

$(document).ready(function(){
  setup();
});
