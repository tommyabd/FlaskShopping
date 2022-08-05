var $window = $(window);

$(document).ready(function() {

    $(".animate-redirect a[href^='#']").click(function(e) {
        e.preventDefault();

        var position = $($(this).attr("href")).offset().top;

        $("body, html").animate({
            scrollTop: position
        }, 1000);
    });

    // scroll to top
    $window.on('scroll', function() {
        if ($(this).scrollTop() > 500) {
            $(".scroll-to-top").fadeIn(400);

        } else {
            $(".scroll-to-top").fadeOut(400);
        }
    });

    $(".scroll-to-top").on('click', function(event) {
        event.preventDefault();
        $("html, body").animate({
            scrollTop: 0
        }, 600);
    });

    $('.countup').counterUp({
        delay: 50,
        time: 2000
    });  

    // Current Year
    $('.current-year').text(new Date().getFullYear());

});