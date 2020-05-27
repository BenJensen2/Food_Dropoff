
var message_open = false;
var scrolling = false;
var oid = 0;
var t;

$(".rightpane").height($(".container").height()-$(".header").height());

$(window).on('resize',function(){
    $(".rightpane").height($(".container").height()-$(".header").height());
});

// Confirm order
$(".main").on('click', '.ajax-confirmorder', function() {
    // e.preventDefault();
    oid = parInt($(this).attr('orderid'));
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
    oid = parInt($(this).attr('orderid'));
    $.ajax({
        type: 'GET',
        url: "/messaging/" + oid + "/message",
        data: $(this).serialize(),
        success: function (response) {
            // console.log(response);
            $('.rightpane-container').html(response);
            $('.message-content').scrollTop(function() { return $('.message-content').scrollHeight; });            
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
    t = setTimeout(reloadMessages, 4000);
});


// Check if client is scrolling
$(function(){
    $(".main").on('scroll', '.message-content', function() {
        scrolling = true;
    });
});

// Reload message window every set interval (unless client is scrolling)
function reloadMessages(){
    if (!scrolling && message_open) {
        $.ajax({
            type: 'GET',
            url: "/messaging/" + oid + "/message",
            data: $(this).serialize(),
            success: function (response) {
                // console.log(response);
                $('.rightpane-container').html(response);
                $('.message-content').scrollTop(function() { return $('.message-content').scrollHeight; });
                setTimeout(reloadMessages,4000);         
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
$(".main").on('submit', '.ajaxform-msg', function(e) {
    e.preventDefault();
    var txt = $('#message').val();
    if (len(txt)>0) {
        $.ajax({
            type: 'POST',
            url: "/messaging/sendmsg",
            data: $(this).serialize(),
            success: function (response) {
                // console.log(response);
                $('.rightpane-container').html(response);
                $('.message-content').scrollTop(function() { return $('.message-content').scrollHeight; });
            },
            error: function(response) {
                console.log(response);
            }
        })
    }
    scrolling=false;
    $("#message").trigger('reset');
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


