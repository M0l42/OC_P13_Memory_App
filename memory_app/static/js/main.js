function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

$(document).ready(function() {
    $("#next").click(function() {
        $.ajax({
            url: '',
            type: 'get',
            data: {
                button_text: $(this).text(),
                next: true,
                rotate: false,
            },
            success: function(response) {
                // $('#seconds').append('<li>' + response.secondes + '</li>');
                console.log(response.error)
                if(response.error){
                    $(".thecard").hide()
                    $(".alert-danger").show();
                    $(".alert-danger").text(response.error);
                    $(".alert-success").hide();
                }
                else{
                    $(".thefront").text(response.recto);
                    $(".theback").text(response.verso);
                    $(".alert-success").hide();
                    $(".alert-danger").hide();
                }
            }
        });
        $(".thecard").toggleClass('thecard_rotate');
        $(this).hide();
        $("#checkMemory").show()
    });

    $("#checkMemory").on('submit',function (event) {
        event.preventDefault();
        console.log("form submitted!")
        $.ajaxSetup({
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        });
        $.ajax({
            url: '',
            type: 'POST',
            data: {
                form_text: $('#post-text').val(),
            },
            success: function(response) {
                // $('#seconds').append('<li>' + response.secondes + '</li>');
                $(".thefront").text(response.recto);
                $(".theback").text(response.verso);
                console.log(response.error)
                if (response.success === 200){
                    $(".alert-success").show();
                }
                else if (response.success === 400)
                {
                    $(".alert-danger").show();
                }
            }
        });
        $(".thecard").toggleClass('thecard_rotate');
        $(this).hide();
        $("#next").show()
    });

    let max_fields = 10; //Maximum allowed input fields
    let wrapper    = $(".wrapper"); //Input fields wrapper
    let add_button = $(".add_fields"); //Add button class or ID
    let x = 1; //Initial input field is set to 1

    //group add limit
    var maxGroup = 10;

    //add more fields group
    $(".addMore").click(function(){
        if($('body').find('.fieldGroup').length < maxGroup){
            var fieldHTML = '<div class="form-group fieldGroup">'+$(".fieldGroupCopy").html()+'</div>';
            $('body').find('.fieldGroup:last').after(fieldHTML);
        }else{
            alert('Maximum '+maxGroup+' groups are allowed.');
        }
    });

    //remove fields group
    $("body").on("click",".remove",function(){
        $(this).parents(".fieldGroup").remove();
    });

    $(".form-control").change(function () {
        $.ajax({
            url: '',
            type: 'GET',
            data: {
                image: this.value,
            },
            success: function(response) {
                if (response.image){
                    let image = '../../../static/img/deck/' + response.image;
                    $(".thefront").css("background-image", "url('" + image + "')");
                }
                else {
                    $(".thefront").css({"background-image":"none"});
                }
            }
        });
    });

    window.addEventListener("load", startup, false);
});

function startup() {
    colorWell = document.querySelector("#colorWell");
    colorWell.addEventListener("input", updateFirst, false);
    colorWell.select();
}

function updateFirst(event) {
    let p = document.querySelector(".thefront");

    if (p) {
        p.style.background = event.target.value;
    }
}