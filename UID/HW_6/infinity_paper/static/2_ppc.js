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

//utility function
function get_index_from_id(string){
  return string.split("-")[1]
}

// logic Functions
function initializeLists(){
  nonPpcEmployees = employees.slice();
  ppcEmployees = [];
}

function swap_non_ppc(index) {
  ppcEmployees.push(nonPpcEmployees[index]);
  nonPpcEmployees.splice(index, 1);

}


function swap_ppc(index) {
  nonPpcEmployees.push(ppcEmployees[index]);
  ppcEmployees.splice(index, 1);
}

// layout Functions
function get_ppc_list_item_html(name, i) {
  return '<div class="row list-item ppc-list-item"  id="ppc-' + i + '">' +
    '<div>' +
      name +
    '</div>' +
  '</div>'
}

function get_non_ppc_list_item_html(name, i) {
  return '<div class="row list-item non-ppc-list-item"  id="nonppc-' + i + '">' +
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
    html = get_non_ppc_list_item_html(nonPpcEmployees[i], i)
    $('#non-ppc-list').append(html);
  }
}

function paint_lists() {
  paint_ppc_list();
  paint_non_ppc_list();
}

function paint_handled_lists() {
  paint_lists();
  install_list_handlers();
}

/* Add non-ppc to ppc */
function accept_non_ppc_list_item(ui){
  element = ui.draggable[0];
  index = get_index_from_id(element.id);
  swap_non_ppc(index);
  paint_handled_lists();
}

function accept_ppc_list_item(ui) {
  element = ui.draggable[0];
  index = get_index_from_id(element.id);
  swap_ppc(index);
  paint_handled_lists();
}

function install_list_handlers() {
  $(".list-item").draggable({
    revert: "invalid",
    stack: ".container"
  });

  $(".list-item").hover(function() {
    $(this).addClass('is-draggable');
  },
  function() {
    $(this).removeClass('is-draggable');
  });

}

function install_handlers() {
    install_list_handlers();
    // make the list items draggable
    $("#ppc-list-header").droppable({
      drop: function(event, ui) {
        accept_non_ppc_list_item(ui)
      },
      accept: ".non-ppc-list-item",
      classes: { "ui-droppable-active" : "drop-here",
                  "ui-droppable-hover" : "target-selected" }
    });
    $("#non-ppc-list-header").droppable({
      drop: function(event, ui) {
        accept_ppc_list_item(ui)
      },
      accept: ".ppc-list-item",
      classes: { "ui-droppable-active" : "drop-here",
                  "ui-droppable-hover" : "target-selected" }
    });
}
// Main
function setup(){
  initializeLists();
  paint_lists();
  install_handlers()
}

$(document).ready(function(){
  setup();
});
