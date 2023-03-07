$(window).resize(function() {
    if ($(window).innerWidth() <= 767) {
        var cardHeaderTitles = $('.card-header>a');
        console.log(cardHeaderTitles);
        cardHeaderTitles.addClass('title-ellipsis');
    }
});

$(document).scroll(function() {
    var body = $('body');
    var loggedInAs = $('.logged-in-as');
    var newBulletinButton = $('.new-bulletin-button-container');
    var rulesCard = $('.rules');
    
    var sidePanel = $(loggedInAs).outerHeight(true) + $(newBulletinButton).outerHeight(true) + $(rulesCard).outerHeight(true);
    var sidePanelAlt = $(newBulletinButton).outerHeight(true) + $(rulesCard).outerHeight(true);
    var childrenOfSidePanel = $('#side-panel').children();
    var y = $(document).scrollTop() + sidePanel;
    var yAlt = $(document).scrollTop() + sidePanelAlt; 
    var navBarHeight = $('#navbar').outerHeight(true) + 30; 
    
    var lastChild = $('#content-container-base').children().last();
    var lastChildPosition = lastChild.position().top;
    var lastChildHeightWithoutBottomMargin = lastChild.innerHeight() + parseInt(lastChild.css('margin-top'));
    var lastChildPositionBottom = lastChildPosition + lastChildHeightWithoutBottomMargin;

    var childrenOfBody = $('body').children();

    if ($(childrenOfBody[2]).css('display') == 'block') {

    } else {
        if (childrenOfSidePanel[0].getAttribute('class').includes('text-center logged-in-as')) {
            if((y - sidePanel) > navBarHeight && y < lastChildPositionBottom) {
                body.removeClass('position-relative');
                loggedInAs.removeClass('logged-in-as-fixed-bottom');
                newBulletinButton.removeClass('button-fixed-bottom');
                rulesCard.removeClass('rules-fixed-bottom');
                    
                loggedInAs.addClass('logged-in-as-fixed');
                newBulletinButton.addClass('button-fixed');
                rulesCard.addClass('rules-fixed');
                    
                document.addClass('me-2');
            } else if (y >= lastChildPositionBottom) {
                loggedInAs.removeClass('logged-in-as-fixed');
                newBulletinButton.removeClass('button-fixed');
                rulesCard.removeClass('rules-fixed');
                
                body.addClass('position-relative');
                loggedInAs.addClass('logged-in-as-fixed-bottom');
                newBulletinButton.addClass('button-fixed-bottom');
                rulesCard.addClass('rules-fixed-bottom');
            } else {
                loggedInAs.removeClass('logged-in-as-fixed');
                newBulletinButton.removeClass('button-fixed');
                rulesCard.removeClass('rules-fixed');
                    
                document.removeClass('me-2');
            }
        } else {
            if((yAlt - sidePanelAlt) > navBarHeight && yAlt < lastChildPositionBottom) {
                console.log('fixing side panel');
                body.removeClass('position-relative');
                rulesCard.removeClass('rules-fixed-bottom-alt');
                newBulletinButton.removeClass('button-fixed-bottom-alt');
            
                newBulletinButton.addClass('button-fixed-alt');
                rulesCard.addClass('rules-fixed-alt');
                document.addClass('me-2');
            } else if(yAlt >= lastChildPositionBottom) {
                rulesCard.removeClass('rules-fixed-alt');
                newBulletinButton.removeClass('button-fixed-alt');
            
                body.addClass('position-relative');
                newBulletinButton.addClass('button-fixed-bottom-alt');
                rulesCard.addClass('rules-fixed-bottom-alt');
            } else {
                rulesCard.removeClass('rules-fixed-alt');
                newBulletinButton.removeClass('button-fixed-alt');
                document.removeClass('me-2');
            }
        }
    }
});
        
        
if (window.location.href.includes('/accounts/')) {
    var footer = $('footer');
    var textField = $('input[type="text"]');
    var passwordField = $('input[type="password"]');
    var emailField = $('input[type="email"]');

    var rememberMe = $('label:contains("Remember Me:")');
    var parentP = $(rememberMe).parent();

    footer.addClass('position-fixed');
    footer.addClass('bottom-0');
    textField.addClass('float-end');
    passwordField.addClass('float-end');
    emailField.addClass('float-end');

    parentP.addClass('d-block');
    parentP.addClass('text-center');
    parentP.addClass('pt-1');

} else {
    footer.removeClass('position-fixed');
    footer.removeClass('bottom-0');
    textField.removeClass('float-end');
    passwordField.addClass('float-end');
    emailField.addClass('float-end');

    parentP.removeClass('d-block');
    parentP.removeClass('text-center');
    parentP.removeClass('pt-1');
}

