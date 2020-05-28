// registration validator
$(".ajaxform-reg").submit(function(e) {
    e.preventDefault();
    var form = $(this);
    var restaurant_name = $("#restaurant_name").val();
    var cuisine = $("#cuisine").val();
    var address = $("#address").val();
    var city = $("#city").val();
    var state = $("#state").val();
    var zip_code = $("#zip_code").val();
    var first_name = $("#first_name").val();
    var last_name = $("#last_name").val();
    var email = $("#email").val();
    var phone_number = $("#phone_number").val();
    var password = $("#password").val();
    var confirmpw = $("#confirmpw").val();
    var output = 0;

    $('.errrestaurant_name').html('');
    $('.errcuisine').html('');
    $('.erraddress').html('');
    $('.errcity').html('');
    $('.errstate').html('');
    $('.errzip_code').html('');
    $('.errfirst_name').html('');
    $('.errlast_name').html('');
    $('.erremail').html('');
    $('.errphone_number').html('');
    $('.errpassword').html('');
    $('.errconfirmpw').html('');


    if (restaurant_name.length < 2) {
        output +=1;
        $('.errrestaurant_name').html('<p>Restaurant name must be at least 2 characters in length2</p>');
    }
    if (cuisine.length < 4) {
        output +=1;
        $('.errcuisine').html('<p>Cuisine must be at least 4 characters in length2</p>');
    }
    if (address.length < 5) {
        output +=1;
        $('.erraddress').html('<p>Street address must be at least 5 characters in length2</p>');
    }
    if (city.length < 3) {
        output +=1;
        $('.errcity').html('<p>City must be at least 3 characters in length2</p>');
    }
    if (state.length != 2) {
        output +=1;
        $('.errstate').html('<p>Choose state from the dropdown2</p>');
    }
    if (String(zip_code).length != 5) {
        output +=1;
        $('.errzip_code').html('<p>Enter a 5-digit zip code2</p>');
    }
    if (first_name.length < 2) {
        output +=1;
        $('.errfirst_name').html('<p>First name must be at least 2 characters long2</p>');
    }
    if (last_name.length < 3) {
        output +=1;
        $('.errlast_name').html('<p>Last name must be at least 2 characters long2</p>');
    }

    if (!emailregex(email)) {
        output +=1;
        $('.erremail').html('<p>Please enter a valid email address2</p>');
    } 

    if (String(phone_number).length != 10) {
        output +=1;
        $('.errphone_number').html('<p>Enter a valid phone number with area code without dashes, parentheses or spaces2</p>');
    }

    if (!passwordregex(password)) {
        output +=1;
        $('.errpassword').html('<p>Password must be between 8-20 characters in length and must contain at least one number2</p>');
    }
    
    if (password != confirmpw) {
        output +=1;
        $('.errconfirmpw').html('<p>Passwords do not match - please confirm password again2</p>');
    }

    $.ajax({
        type: 'GET',
        url: "/restaurantlogin/ajax-regval",
        data: {"email": email, "rid": -9},
        success: function (response) {
            if (response["used"]) {
                output +=1;
                $('.erremail').html('<p>An account already exists for this email2</p>');
            }
        
            if (output > 0) {
                return false;
            } else {
                form.unbind('submit').submit();
            } 
        },
        error: function(response) {
            console.log(response);
            return false;        
            // if (output > 0) {
            //     return false;
            // } else {
            //     form.unbind('submit').submit();
            // } 
        }
    })
});


// login validator
$(".ajaxform-login").submit(function(e) {
    e.preventDefault();
    var form = $(this);
    $('.loginfail').html('');

    $.ajax({
        type: 'POST',
        url: "/restaurantlogin/ajax-logval",
        data: $(this).serialize(),
        success: function (response) {
            if (!response["match"]) {
                $('.loginfail').html('<p>Incorrect email or password2</p>');
                return false
            } 
            else {
                form.unbind('submit').submit();
            }
        },
        error: function(response) {
            console.log(response);
        }
    })

});


// edit validator
$(".ajaxform-edit").submit(function(e) {
    e.preventDefault();
    var form = $(this);
    var cuisine = $("#cuisine").val();
    var address = $("#address").val();
    var city = $("#city").val();
    var state = $("#state").val();
    var zip_code = $("#zip_code").val();
    var first_name = $("#first_name").val();
    var last_name = $("#last_name").val();
    var email = $("#email").val();
    var phone_number = $("#phone_number").val();
    var password = $("#password").val();
    var confirmpw = $("#confirmpw").val();
    var restaurant_id = $('.ajaxform-edit').attr('resid');
    console.log(restaurant_id);
    var output = 0;

    $('.errcuisine').html('');
    $('.erraddress').html('');
    $('.errcity').html('');
    $('.errstate').html('');
    $('.errzip_code').html('');
    $('.errfirst_name').html('');
    $('.errlast_name').html('');
    $('.erremail').html('');
    $('.errphone_number').html('');
    $('.errpassword').html('');
    $('.errconfirmpw').html('');


    if (cuisine.length < 4) {
        output +=1;
        $('.errcuisine').html('<p>Cuisine must be at least 4 characters in length2</p>');
    }
    if (address.length < 5) {
        output +=1;
        $('.erraddress').html('<p>Street address must be at least 5 characters in length2</p>');
    }
    if (city.length < 3) {
        output +=1;
        $('.errcity').html('<p>City must be at least 3 characters in length2</p>');
    }
    if (state.length != 2) {
        output +=1;
        $('.errstate').html('<p>Choose state from the dropdown2</p>');
    }
    if (String(zip_code).length != 5) {
        output +=1;
        $('.errzip_code').html('<p>Enter a 5-digit zip code2</p>');
    }
    if (first_name.length < 2) {
        output +=1;
        $('.errfirst_name').html('<p>First name must be at least 2 characters long2</p>');
    }
    if (last_name.length < 3) {
        output +=1;
        $('.errlast_name').html('<p>Last name must be at least 2 characters long2</p>');
    }

    if (!emailregex(email)) {
        output +=1;
        $('.erremail').html('<p>Please enter a valid email address2</p>');
    } 

    if (String(phone_number).length != 10) {
        output +=1;
        $('.errphone_number').html('<p>Enter a valid phone number with area code without dashes, parentheses or spaces2</p>');
    }

    if (password.length > 0 && !passwordregex(password)) {
        output +=1;
        $('.errpassword').html('<p>Password must be between 8-20 characters in length and must contain at least one number2</p>');
    }
    
    if (password != confirmpw) {
        output +=1;
        $('.errconfirmpw').html('<p>Passwords do not match - please confirm password again2</p>');
    }

    $.ajax({
        type: 'GET',
        url: "/restaurantlogin/ajax-regval",
        data: {"email": email, "rid": restaurant_id},
        success: function (response) {
            if (response["used"]) {
                output +=1;
                $('.erremail').html('<p>An account already exists for this email2</p>');
            }
        
            if (output > 0) {
                return false;
            } else {
                form.unbind('submit').submit();
            } 
        },
        error: function(response) {
            console.log(response);
            return false;        
            // if (output > 0) {
            //     return false;
            // } else {
            //     form.unbind('submit').submit();
            // } 
        }
    })
});


function emailregex(email) {
    var re= /^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$/;
    return re.test(email);
}

function passwordregex(password) {
    var re2= /^(?=.*\d)[a-zA-Z\d]{8,20}$/;
    return re2.test(password);
}