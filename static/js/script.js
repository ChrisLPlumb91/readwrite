$(document).scroll(function() {
    var y = $(document).scrollTop();    
    var rulesCard = $('.rules');
    var newBulletinButton = $('.button-container');
    var coldiv = $('div>.col-3');
    
    if(y > 195 && y < 848)  {
        coldiv.removeClass('position-relative');
        rulesCard.removeClass('rules-fixed-bottom');
        newBulletinButton.removeClass('button-fixed-bottom');
        rulesCard.addClass('rules-fixed');
        newBulletinButton.addClass('button-fixed');
        document.addClass('me-2');
    } else if(y >= 848) {
        rulesCard.removeClass('rules-fixed');
        newBulletinButton.removeClass('button-fixed');
        coldiv.addClass('position-relative');
        newBulletinButton.addClass('button-fixed-bottom');
        rulesCard.addClass('rules-fixed-bottom');
    } else {
        rulesCard.removeClass('rules-fixed');
        newBulletinButton.removeClass('button-fixed');
        document.removeClass('me-2');
    }
});
