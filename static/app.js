
$(document).ready(function(){ // DOCUMENT READY FUNCTION

    //   Cards Display
//   $('#cards-target').load('/cards');

//    // Thumbnail Display
//   var x = $('#image').val();
//   $('#thumb-target').load('/thumb?image='+x);

//    // Add image button click function
//   var x = $('#image').val();
//   $('#add-button-target').load('/add-image?image='+x);


    // Add button Click Function
    $('.add-button').on('click', function() {
        var image = $(this).attr('id');
        $('#add-button-target').load('/add-image?image='+image);
    });

    // View card button array Click Function
    $('.view-button').each(function(index) {
        $(this).on('click', function() {
        var image = $(this).attr('id');
        window.location.href=('/card-view?image='+image+'&new_image='+image);
        });
    });

    // Edit card button array Click Function
    $('.edit-button').each(function(index) {
        $(this).on('click', function() {
        var image = $(this).attr('id');
        window.location.href=('/card-edit?image='+image);
        });
    });


  //View Button Click Function
  $("#view-button-unique").click(function(){
     window.location.href=('/card-view/');
  })

}); // DOCUMENT READY FUNCTION