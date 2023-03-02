$(document).scroll(function() {
    var y = $(document).scrollTop();  
    var rulesCard = $('.rules');
    var newBulletinButton = $('.new-bulletin-button-container');
    var loggedInAs = $('.logged-in-as')
    var body = $('body');
    var scrollTopHeightLimit = $(document).outerHeight(true) - ($('#bulletin-card-1').outerHeight(true) * 4 + $('footer').outerHeight(true) + 170);
    
    if(y > 195 && y <= scrollTopHeightLimit)  {
        body.removeClass('position-relative');
        rulesCard.removeClass('rules-fixed-bottom');
        newBulletinButton.removeClass('button-fixed-bottom');
        loggedInAs.removeClass('logged-in-as-fixed-bottom');

        rulesCard.addClass('rules-fixed');
        newBulletinButton.addClass('button-fixed');
        loggedInAs.addClass('logged-in-as-fixed');
        document.addClass('me-2');
    } else if(y > scrollTopHeightLimit) {
        rulesCard.removeClass('rules-fixed');
        newBulletinButton.removeClass('button-fixed');
        loggedInAs.removeClass('logged-in-as-fixed');

        body.addClass('position-relative');
        loggedInAs.addClass('logged-in-as-fixed-bottom');
        newBulletinButton.addClass('button-fixed-bottom');
        rulesCard.addClass('rules-fixed-bottom');
    } else {
        rulesCard.removeClass('rules-fixed');
        newBulletinButton.removeClass('button-fixed');
        loggedInAs.removeClass('logged-in-as-fixed');
        document.removeClass('me-2');
    }      
});

// let form = $('#comment-like-form')

// $('button').one('mouseup', function(event) {
//     console.log('Liking/Unliking...')
//     form = $(this).parent();
//     form.submit();    
//     event.preventDefault();
// })

// $('form').on('submit', function(e) {
//     console.log('Submitting form...');
// })

// $('#comment-liked').one('click', function(event) {
//     console.log('Submitting form and unliking...');
//     form.submit();
// })


