
$(document).ready(function(){ // DOCUMENT READY FUNCTION

    // Edit card UPDATE button array Click Function
    $('.update-button').each(function(index) {
        $(this).on('click', function() {
        var image = $(this).attr('id');
        window.location.href=('/card-edit?image='+image);
        });
    });

    // Image Selector onchange Function
    $('#name').on('change', function() {
        var image = $(this).val();
        window.location.href=('/card-edit?image='+image);
    });

    // Add button Click Function
    $('.add-button').on('click', function() {
        var image = $(this).attr('id');
        $('#add-button-target').load('/add-image?image='+image);
    });

    // View card button array Click Function
    $('.view-button').each(function(index) {
        $(this).on('click', function() {
        var image = $(this).attr('id');
        window.location.href=('/card-view?image='+image);
        });
    });

    // Edit card button array Click Function
    $('.edit-button').each(function(index) {
        $(this).on('click', function() {
        var image = $(this).attr('id');
        window.location.href=('/card-edit?image='+image);
        });
    });

}); // DOCUMENT READY FUNCTION

