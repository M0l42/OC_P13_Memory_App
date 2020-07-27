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
    let verso = "";
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
                if(response.error){
                    $(".thecard").hide();
                    $(".alert-danger").css("visibility", "visible");
                    $(".alert-danger").text(response.error);
                    $(".alert-success").css("visibility", "hidden");
                }
                else{
                    $(".front-text").text(response.recto);
                    $(".alert-success").css("visibility", "hidden");
                    $(".alert-danger").css("visibility", "hidden");
                }
            }
        });
        $(".thecard").toggleClass('thecard_rotate');
        $(this).hide();
        $("#checkMemory").val('').show()

    });

    $("#checkMemory").on('submit',function (event) {
        event.preventDefault();
        console.log("form submitted!");
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
                $(".back-text").text(response.verso);
                if (response.success === 200){
                    $(".alert-success").css("visibility", "visible");
                }
                else if (response.success === 400)
                {
                    $(".alert-danger").css("visibility", "visible");
                }
            }
        });
        $(".thecard").toggleClass('thecard_rotate');
        $(this).trigger('reset').hide();
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

    $(".change-image").change(function () {
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
    window.addEventListener("load", startupText, false);

    $(".viewMoreDeck").click(function(){
        $(".Deck-hidden").show();
        window.location.hash = '#Deck';
        $(".viewMoreDeck").hide()
    });

    $(".viewMoreQuickDeck").click(function(){
        $(".QuickDeck-hidden").show();
        window.location.hash = '#QuickDeck';
        $(".viewMoreQuickDeck").hide()
    });

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

function startupText() {
    colorTextWell = document.querySelector("#colorTextWell");
    colorTextWell.addEventListener("input", updateFirstText, false);
    colorTextWell.select();
}

function updateFirstText(event) {
    let p = document.querySelector(".thefront");

    if (p) {
        p.style.color = event.target.value;
    }
}

$(function () {
  $(document).scroll(function () {
	  let $nav = $(".navbar-fixed-top");
	  $nav.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
	});
});
