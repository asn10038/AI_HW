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
  var sale = { "salespersion" : USER_NAME,
               "client" : client,
               "reams" : ream_num};
  sales.unshift(sale);
  console.log(sales);
}

// layout updates
function clear_text_boxes() {
  $('#clientInput').val('');
  $('#reamInput').val('');
}
function submit_order(){
  new_order_update();
  clear_text_boxes();
}

// Main Function
$(document).ready(function() {
  $("#newOrderButton").click(submit_order);
});
