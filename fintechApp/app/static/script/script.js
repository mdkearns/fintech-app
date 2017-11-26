function pageScript(){
    if(window.location.pathname == "/app/reports/" || window.location.pathname == "/app/reports_search/"){
        $('#content-container').css("padding-left", "0");
    }
    
    $(function() {
        $('input[name="daterange"]').daterangepicker({
            timePicker: true,
            timePickerIncrement: 30,
            locale: {
                format: 'MM/DD/YYYY h:mm A'
            }
        });
    });
}