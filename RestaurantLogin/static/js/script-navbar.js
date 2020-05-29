
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
                        window.location.href = "/users/restaurant/" + rid;
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

    var message_open = false;
    var scrolling = false;
    var oid = 0;
    var t;
    
    // $(".rightpane").height($(".container").height()-$(".navbar").height());
    $(".rightpane").height($(window).height()-76);
    // console.log($(".rightpane").height());
    // console.log($(".container").height());
    
    $(window).on('resize',function(){
        $(".rightpane").height($(window).height()-76);
    });
    
    // Confirm order
    $(".main").on('click', '.ajax-confirmorder', function(e) {
        e.preventDefault();
        oid = parseInt($(this).attr('orderid'));
        $.ajax({
            type: 'GET',
            url: "/messaging/" + oid + "/confirm",
            data: $(this).serialize(),
            success: function (response) {
                // console.log(response);
                $('.order_status').html(response);
                
            },
            error: function(response) {
                console.log(response);
            }
        })    
    });
    
    
    // Open messaging window and load messages
    $(".main").on('click', '.ajax-message', function() {
        oid = parseInt($(this).attr('orderid'));
        first_name = ($(this).attr('fname'));
        console.log(oid, first_name);
        headervar = "<div class='justify-content-between'>\n<span>Message " + first_name + " about order " + oid + "</span>\n<span>\n<a href='#' class='ajax-closemessage'>\n<svg class='bi bi-x-square-fill' width='1em' height='1em' viewBox='0 0 16 16' fill='currentColor' xmlns='http://www.w3.org/2000/svg'><path fill-rule='evenodd' d='M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm9.854 4.854a.5.5 0 0 0-.708-.708L8 7.293 4.854 4.146a.5.5 0 1 0-.708.708L7.293 8l-3.147 3.146a.5.5 0 0 0 .708.708L8 8.707l3.146 3.147a.5.5 0 0 0 .708-.708L8.707 8l3.147-3.146z'/></svg>\n</a>\n</span>\n</div>"
        footervar = "<form class='ajaxform-msg form-inline' action='/messaging/sendmsg' method='POST'>\n{% csrf_token %}\n<input type='hidden' name='oid' id='msgoid' value='{{one_order.id}}'>\n<div class='form-group'>\n<div class='col divtext'>\n<textarea name='message' id='txtmessage' rows='2'></textarea>\n</div>\n<button class='btn btn-dark btn-sm msgbtn' type='submit'>Send</button>\n</div>\n</form>"
        console.log(oid)
        $.ajax({
            type: 'GET',
            url: "/messaging/" + oid + "/message",
            data: $(this).serialize(),
            success: function (response) {
                // console.log(response);
                $('.rightpane-container').html(response);
                // $('.message-header').html(headervar);
                // $('.message-footer').html(footervar);
                $('.message-content').scrollTop(function() { return $('.message-content')[0].scrollHeight; });
                // $('.message-content').scrollTop(1000);
                console.log($(".message-content").height());
                console.log($(".message-content")[0].scrollHeight);
                
                
            },
            error: function(response) {
                console.log(response);
            }
        })
        $(".leftpane").animate({
            width: '73%'
        }, 0);
        $(".rightpane").animate({
            width: '25%'
        }, 0);
        message_open = true;
        t = setTimeout(reloadMessages, 10000);
    });
    
    
    
    // Check if client is scrolling
    $(function(){
        $(document).on('scroll', '.message-content', function() {
            scrolling = true;
            console.log('scrolling');
        });
    });
    
    // Reload message window every set interval (unless client is scrolling)
    function reloadMessages(){
        if (!scrolling && message_open) {
            $.ajax({
                type: 'GET',
                url: "/messaging/" + oid + "/refresh",
                data: $(this).serialize(),
                success: function (response) {
                    // console.log(response);
                    $('.message-content').html(response);
                    $('.message-content').scrollTop(function() { return $('.message-content')[0].scrollHeight; });
                    setTimeout(reloadMessages,6000);         
                },
                error: function(response) {
                    console.log(response);
                }
            })
        } else if (!message_open) {
            clearTimeout(t);
        }
        scrolling = false;
    }
    
    // Send message and reload messages
    $(document).on('submit', '.ajaxform-msg', function(e) {
        console.log('1');
        e.preventDefault();
        console.log('2');
        var txt = $('#txtmessage').val();
        console.log(txt);
        if (txt.length>0) {
            $.ajax({
                type: 'POST',
                url: "/messaging/sendmsg",
                data: $(this).serialize(),
                success: function (response) {
                    // console.log(response);
                    console.log('success');
                    $('.message-content').html(response);
                    $('.message-content').scrollTop(function() { return $('.message-content')[0].scrollHeight; });
                    console.log($(".message-content").height());
                    console.log($(".message-content")[0].scrollHeight);
                },
                error: function(response) {
                    console.log(response);
                }
            })
        } 
        scrolling=false;
        $('.ajaxform-msg').trigger('reset');
    });
    
    // Close messaging window 
    $(".main").on('click', '.ajax-closemessage', function() {
        $(".message-header").html("");
        $(".message-content").html("");
        $(".message-footer").html("")    
        $(".leftpane").animate({
            width: '100%'
        }, 0);
        $(".rightpane").animate({
            width: '0%'
        }, 0);
        message_open = false;
    });
});

