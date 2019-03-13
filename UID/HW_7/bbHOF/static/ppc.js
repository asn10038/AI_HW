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

var display_lists = function(non_ppc, ppc) {
  $('#ppc-list').empty();
  for(i in ppc) {
    html = get_ppc_list_item_html(ppc[i], i)
    $('#ppc-list').append(html);
  }

  $('#non-ppc-list').empty();
  for(i in non_ppc) {
    html = get_non_ppc_list_item_html(non_ppc[i], i)
    $('#non-ppc-list').append(html);
  }
  install_handlers();
}

var move_to_ppc = function(name) {
  $.ajax({
      type: "POST",
      url: "move_to_ppc",
      dataType : "json",
      contentType: "application/json; charset=utf-8",
      data : JSON.stringify(name),
      success: function(result){
        display_lists(result['data']['non_ppc'], result['data']['ppc'])
      },
      error: function(request, status, error){
          console.log("Error");
          console.log(request);
          console.log(status);
          console.log(error);
      }
  });
}

var move_to_non_ppc = function(name) {
  $.ajax({
      type: "POST",
      url: "move_to_non_ppc",
      dataType : "json",
      contentType: "application/json; charset=utf-8",
      data : JSON.stringify(name),
      success: function(result){
        display_lists(result['data']['non_ppc'], result['data']['ppc'])
      },
      error: function(request, status, error){
          console.log("Error");
          console.log(request);
          console.log(status);
          console.log(error);
      }
  });
}


/* Add non-ppc to ppc */
function accept_non_ppc_list_item(ui){
  element = ui.draggable[0];
  name = element.innerText;
  move_to_ppc({'name': name});

}

function accept_ppc_list_item(ui) {
  element = ui.draggable[0];
  name = element.innerText;
  move_to_non_ppc({'name': name});
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
  // initializeLists();
  // paint_lists();
  move_to_ppc({})
  install_handlers()
}

$(document).ready(function(){
  setup();
});
