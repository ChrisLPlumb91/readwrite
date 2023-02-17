$(document).scroll(function() {
    var y = $(document).scrollTop();    
    var rulescard = $('.rules');
    var coldiv = $('div>.col-3');
    
    if(y > 195 && y < 848)  {
        coldiv.removeClass('position-relative');
        rulescard.removeClass('rules-fixed-bottom');
        rulescard.addClass('rules-fixed');
        document.addClass('me-2');
    } else if(y >= 848) {
        rulescard.removeClass('rules-fixed');
        coldiv.addClass('position-relative');
        rulescard.addClass('rules-fixed-bottom');
    } else {
        rulescard.removeClass('rules-fixed');
        document.removeClass('me-2');
    }
});