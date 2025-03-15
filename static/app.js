
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
//        $('#add-button-target').load('/add-image?image='+image);
        window.location.href=('/add-image?image='+image);
    });

    // Delete card button Click Function
    $('.delete-button').on('click', function() {
        var image = $(this).val();
//        $('#add-button-target').load('/add-image?image='+image);
        window.location.href=('/delete-card?image='+image);
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

    // Loan Calculator header text
    $('#loan-header-target').load('/loan-header/');

    // Loan Calculator plot button array Click Function
    $('.loan-plot-button').each(function(index) {
        $(this).on('click', function() {
            let payment = $('#payment').val()
            let PV = $('#PV').val()
            let rate = $('#rate').val()
            let number = $('#number').val()
            $('#loan-button-target').load('/plot-loan/?payment='+payment+'&PV='+PV+'&rate='+rate+'&number='+number);
        });
    });

}); // DOCUMENT READY FUNCTION
