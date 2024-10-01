(function ($) {
    $('#click-button').change(function () {
        if (this.checked) {
            $('.popup-image').show(function () {
                setTimeout(function () {
                    $(".popup-image").fadeOut(2000);
                }, 6000);
            });

            $('.audiofile')[0].play();

        } else {
            $('.popup-image').hide();
        }
    });
})(jQuery)