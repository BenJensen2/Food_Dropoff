
$( document ).ready(function() {
    // redirect to restaurant detail page
    $(document).on('submit', '.navbar-searchform', function(e) {

        e.preventDefault();
        var rid = parseInt($('#navbar-rid').val());
        
        if (Number.isInteger(rid)) {
            $.ajax({
                type: 'GET',
                url: "/menu/checkRID/" + rid,
                data: $(this).serialize(),
                success: function (response) {
                    // console.log(response);
                    if (response['valid'] == false) {
                        console.log(response);
                        $('.ridcheck').html('Not a valid ID');
                        $('.navbar-searchform').trigger('reset');
                        return false;
                    } else {
                        console.log(response);
                        window.location.href = "/event/restaurant/" + rid;
                        return false;
                    }        
                },
                error: function(response) {
                    console.log(response);
                }
            })
        } else {
            console.log('not an integer');
            $('.navbar-searchform').trigger('reset');
            $('.ridcheck').html('Not a valid ID');
        }   
        return false;
    });
});

