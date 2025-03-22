
$(document).ready(function(){ // DOCUMENT READY FUNCTION

    // Loan Calculator header text
    $('#loan-header-target').load('/loan-header/');

    // Weather data
    $('#weather-target').load('/weather');

    // Clock button
    $('.clock-button').on('click', function() {
        var image = $(this).attr('id');
        $('#clock-button-target').load('/thumb?image='+image);
    });

    // Set Zipcode button
    $('.set-zip-button').on('click', function() {
        let zip = $('#zip').val()
        $('#weather-target').load('/weather?zip='+zip);
    });

    //Barometer Reset Button
    $(".reset-barometer-button").click(function(){
        let zip = $('#zip').val();
        $("#weather-target").load('/weather?reset=True&zip='+zip);
    })

    // Edit card UPDATE button array
    $('.update-button').each(function(index) {
        $(this).on('click', function() {
        var image = $(this).attr('id');
        window.location.href=('/card-edit?image='+image);
        });
    });

    // Image Selector
    $('#name').on('change', function() {
        var image = $(this).val();
        window.location.href=('/card-edit?image='+image);
    });

    // Add button
    $('.add-button').on('click', function() {
        var image = $(this).attr('id');
        window.location.href=('/add-image?image='+image);
    });

    // Delete card button
    $('.delete-button').on('click', function() {
        var image = $(this).val();
        window.location.href=('/delete-card?image='+image);
    });

    // View card button array
    $('.view-button').each(function(index) {
        $(this).on('click', function() {
        var image = $(this).attr('id');
        window.location.href=('/card-view?image='+image);
        });
    });

    // Edit card button array
    $('.edit-button').each(function(index) {
        $(this).on('click', function() {
        var image = $(this).attr('id');
        window.location.href=('/card-edit?image='+image);
        });
    });

    // Loan Calculator plot button
    $('.loan-plot-button').each(function(index) {
        $(this).on('click', function() {
            let payment = $('#payment').val()
            let PV = $('#PV').val()
            let rate = $('#rate').val()
            let number = $('#number').val()
             window.location.href=('/plot_loan?P='+payment+'&PV='+PV+'&r='+rate+'&n='+number);
        });
    });

}); // DOCUMENT READY FUNCTION
