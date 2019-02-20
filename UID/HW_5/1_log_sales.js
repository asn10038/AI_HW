//CONSTANTS

var USER_NAME = "Frank Foo"
var clients = [
      "Shake Shack",
      "Toast",
      "Computer Science Department",
      "Teacher's College",
      "Starbucks",
      "Subsconsious",
      "Flat Top",
      "Joe's Coffee",
      "Max Caffe",
      "Nussbaum & Wu",
      "Taco Bell",
];

var sales = [
	{
		"salesperson": "James D. Halpert",
		"client": "Shake Shack",
		"reams": 100
	},
	{
		"salesperson": "Stanley Hudson",
		"client": "Toast",
		"reams": 400
	},
	{
		"salesperson": "Michael G. Scott",
		"client": "Computer Science Department",
		"reams": 1000
	},
]


//Utility functions
function LOG(text){
  console.log(text);
}

// Logic Functions

function make_page(clientList) {
  console.log(clientList);
}

function new_order_update(){
  var client = $('#clientInput').val();
  var ream_num = $('#reamInput').val();
  var sale = { "salesperson" : USER_NAME,
               "client" : client,
               "reams" : ream_num};
  sales.unshift(sale);

  // add client to the client list if not exist
  if (clients.indexOf(client) < 0) {
    clients.push(client);
  }
  console.log(sales);
}

function get_sale_html(sale, i) {
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
      '<button class="deleteButton" id="' + i + '"> x </button>' +
    '</div>' +
  '</div>'
}

function delete_order(index) {
  sales.splice(index, 1);
}

// layout updates
function paint_order_list() {
  /* This is probably inefficient */
  $('#salesList').empty();
  for ( i in sales) {
    $('#salesList').append(get_sale_html(sales[i], i));
  }
}

function clear_text_boxes() {
  $('#clientInput').val('');
  $('#reamInput').val('');
}

function setup_autocomplete() {
    $('#clientInput').autocomplete({
      source: clients
    });
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

function submit_order(){
  // error checking
  if(handled_empty_field() || handled_invalid_number())
    return;

  new_order_update();
  clear_text_boxes();
  paint_handled_order_list();
  $('#clientInput').focus();
}

function do_delete_order(){
  var index = this.id;
  delete_order(index);
  paint_handled_order_list();
}

function install_handlers(){
  $("#newOrderButton").click(submit_order);
  $(".deleteButton").click(do_delete_order);
  $('#reamInput').keydown(function(e) {
    if(e.keyCode == 13) {
      submit_order();
    }
  });
}

function paint_handled_order_list() {
  paint_order_list();
  $(".deleteButton").click(do_delete_order);
}

// Main Functions
function setup() {
  setup_autocomplete();
  paint_order_list();
  install_handlers();
}
$(document).ready(function() {
  setup();
});
