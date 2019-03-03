//CONSTANTS

var USER_NAME = "Frank Foo"

//Utility functions
function LOG(text){
  console.log(text);
}

// Logic Functions

function get_sale_html(sale, id) {
  return '<div class="row">' +
    '<div class="col-md-2">' +
      sale.salesperson +
    '</div>' +
    '<div class="col-md-3">' +
      sale.client +
    '</div>' +
    '<div class="col-md-1">' +
      sale.reams +
    '</div>' +
    '<div class="col-md-1">' +
      '<button class="deleteButton" id="' + id + '"> x </button>' +
    '</div>' +
  '</div>'
}

// layout updates
var display_sales_list = function(sales) {
  $('#salesList').empty();
  for (i in sales) {
    $('#salesList').append(get_sale_html(sales[i], sales[i]['id']))
  }
  //install delete button handler
  $(".deleteButton").click(do_delete_sale);
}

var save_sale = function(new_sale) {
  var data_to_save = new_sale
  $.ajax({
      type: "POST",
      url: "add_sale",
      dataType : "json",
      contentType: "application/json; charset=utf-8",
      data : JSON.stringify(data_to_save),
      success: function(result){
        LOG(result['data'])
        display_sales_list(result['data']['sales']);
        $('#clientInput').focus();
        //reconfig autocomplete
        clients = result['data']['clients'];
        setup_autocomplete(clients);
      },
      error: function(request, status, error){
          console.log("Error");
          console.log(request);
          console.log(status);
          console.log(error);
      }
  });
}

var delete_sale = function(id) {
  // delete a specific sale
  var data_to_delete = {'id' : id}
  $.ajax({
      type: "POST",
      url: "delete_sale",
      dataType : "json",
      contentType: "application/json; charset=utf-8",
      data : JSON.stringify(data_to_delete),
      success: function(result){
        display_sales_list(result['data']['sales']);
      },
      error: function(request, status, error){
          console.log("Error");
          console.log(request);
          console.log(status);
          console.log(error);
      }
  });
}

function clear_text_boxes() {
  $('#clientInput').val('');
  $('#reamInput').val('');
}

function setup_autocomplete(clients) {
    $('#clientInput').autocomplete({
      source: clients
    });
}

function get_clients_from_sales(sales) {
  res = []
  for ( i in sales) {
    res.push(sales[i]['client'])
  }
  return res
}

function handled_empty_field() {
  var textboxes = [$('#clientInput'), $('#reamInput')];
  var names = ['Client Input', 'Ream Input'];
  for( i in textboxes ) {
    if(textboxes[i].val() == '' || textboxes[i].val() == null) {
      alert(names[i] + ' is empty');
      textboxes[i].focus();
      return true;
    }
  }
  return false;
}

function handled_invalid_number() {
  var reamVal = $('#reamInput').val();
  if( isNaN(reamVal) || !isFinite(reamVal))
  {
    alert('Invalid number in ream input');
    $('#reamInput').focus();
    return true;
  }
  return false;
}

function do_delete_sale(){
  var index = this.id;
  delete_sale(index);
}

function do_save_sale() {
  if(handled_empty_field() || handled_invalid_number())
    return;

  var client = $('#clientInput').val();
  var ream_num = $('#reamInput').val();
  var sale = { "salesperson" : USER_NAME,
               "client" : client,
               "reams" : ream_num};
  clear_text_boxes();
  save_sale(sale);
}

function install_handlers(){

  $("#newOrderButton").click(do_save_sale);
  $(".deleteButton").click(do_delete_sale);
  $('#reamInput').keydown(function(e) {
    if(e.keyCode == 13) {
      do_save_sale();
    }
  });
}

// Main Functions
function setup() {
  install_handlers();
  save_sale({})
}

$(document).ready(function() {
  setup();
});
