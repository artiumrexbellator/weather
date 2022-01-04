$( "#load" ).click(function() {
    if($("#date").val().length!=0)
        window.location="/home?station="+$("#station").val()+"&date="+$("#date").val()
});

$( "#download" ).click(function() {
    window.location="/download?station="+$(this).attr("station")+"&date="+$(this).attr("date")
});