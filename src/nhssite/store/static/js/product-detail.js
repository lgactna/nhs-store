$("input[name='quantity']").on('input', function() {
    var units = $("input[name='quantity']").val()
    $("#total-price").text("$"+(unit_price*units).toFixed(2))
});
