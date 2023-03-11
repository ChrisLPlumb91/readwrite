$(window).resize(function() {
    var cardHeaderTitles = $('.card-header>a');

    if ($(window).innerWidth() <= 767) {
        cardHeaderTitles.addClass('title-ellipsis');
    } else {
        cardHeaderTitles.removeClass('title-ellipsis');
    }

    if($('#404-container').length) {
        var footer = $('footer');
        var navbarHeader = $('.navbar');
        var contentContainer = $('#404-container');
        var row = $('404-container>div');

        var contentHeight = $(document).innerHeight() - $(footer).outerHeight(true) - $(navbarHeader).outerHeight(true);
        
        $(contentContainer).height(contentHeight);
        $(row).height(contentHeight);
    } else if($('#500-container').length) {
        var footer = $('footer');
        var navbarHeader = $('.navbar');
        var contentContainer = $('#500-container');
        var row = $('500-container>div');

        var contentHeight = $(document).innerHeight() - $(footer).outerHeight(true) - $(navbarHeader).outerHeight(true);
        
        $(contentContainer).height(contentHeight);
        $(row).height(contentHeight);
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
}

$(document).ready(function() {
    var footer = $('footer');
    var navbarHeader = $('.navbar');

    var contentHeight = $(document).innerHeight() - $(footer).outerHeight(true) - $(navbarHeader).outerHeight(true);  

    if($('#404-container').length) {
        var PageNotFoundContainer = $('#404-container');
        var row = $('#404-container>div');

        $(PageNotFoundContainer).height(contentHeight);
        $(row).height(contentHeight);

        footer.addClass('position-fixed');
        footer.addClass('bottom-0');
    } else if($('#500-container').length) {
        var InternalServerErrorContainer = $('#500-container');
        var row = $('#500-container>div');

        $(InternalServerErrorContainer).height(contentHeight);
        $(row).height(contentHeight);

        footer.addClass('position-fixed');
        footer.addClass('bottom-0');
    } else {
        footer.removeClass('position-fixed');
        footer.removeClass('bottom-0');
    }
})

if($('.modal-button').length) {
    $('.modal-button').on('click', function() {
        var type = $(this).data('type');
        var lowerCaseType = type.toLowerCase();
        var form = $('.modal-footer>form');

        $('.modal-header>h1').text(`Delete ${type}`);
        $('.modal-body>p').text(`Are you sure you want to delete your ${lowerCaseType}?`);

        if(type == 'Comment') {
            $(form).attr('action', $(this).attr('value'));
        }
    });
}

