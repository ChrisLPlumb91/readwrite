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

    if (window.location.href.includes('/accounts/')) {
        var accountFormContainer = $('.account-form-container');
        var infoContainer = $('.info-container');
        if ($(window).innerWidth() <= 1650 && $(window).innerWidth() > 1110) {
            accountFormContainer.removeClass('col-4');
            accountFormContainer.removeClass('offset-4');
            accountFormContainer.removeClass('col-8');
            accountFormContainer.removeClass('offset-2');
            accountFormContainer.addClass('col-6');
            accountFormContainer.addClass('offset-3');
        } else if ($(window).innerWidth() <= 1110 && $(window).innerWidth() > 830) {
            accountFormContainer.removeClass('col-4');
            accountFormContainer.removeClass('offset-4');
            accountFormContainer.removeClass('col-6');
            accountFormContainer.removeClass('offset-3');
            accountFormContainer.removeClass('col-10');
            accountFormContainer.removeClass('offset-1');
            accountFormContainer.addClass('col-8');
            accountFormContainer.addClass('offset-2');
        } else if ($(window).innerWidth() <= 830) {
            accountFormContainer.removeClass('col-4');
            accountFormContainer.removeClass('offset-4');
            accountFormContainer.removeClass('col-6');
            accountFormContainer.removeClass('offset-3');
            accountFormContainer.removeClass('col-8');
            accountFormContainer.removeClass('offset-2');
            accountFormContainer.addClass('col-10');
            accountFormContainer.addClass('offset-1');
        } else {
            accountFormContainer.removeClass('col-6');
            accountFormContainer.removeClass('offset-3');
            accountFormContainer.addClass('col-4');
            accountFormContainer.addClass('offset-4');
        }

        if ($(window).innerWidth() <= 600 && $(window).innerWidth() > 450) {
            infoContainer.removeClass('col-6');
            infoContainer.removeClass('offset-3');
            infoContainer.removeClass('col-10');
            infoContainer.removeClass('offset-1');
            infoContainer.addClass('col-8');
            infoContainer.addClass('offset-2');
        } else if ($(window).innerWidth() <= 450) {
            infoContainer.removeClass('col-8');
            infoContainer.removeClass('offset-2');
            infoContainer.addClass('col-10');
            infoContainer.addClass('offset-1');
        } else {
            infoContainer.removeClass('col-8');
            infoContainer.removeClass('offset-2');
            infoContainer.removeClass('col-10');
            infoContainer.removeClass('offset-1');
            infoContainer.addClass('col-6');
            infoContainer.addClass('offset-3');
        }
    }

});

$(document).scroll(function() {
    var body = $('body');
    // The logged in message that appears at the top of the page when the width is small enough is actually the first element of two that has this class, so loggedInAs actually contains a HTMLCollection.
    // The second element ([1]) is the one that is needed here.
    var loggedInAs = $('#logged-in-side');
    var newBulletinButton = $('.new-bulletin-button-container');
    var rulesCard = $('.rules');
    
    // combined height of side-panel contents when logged in
    var sidePanel = $(loggedInAs).outerHeight(true) + 18 + $(newBulletinButton).outerHeight(true) + $(rulesCard).outerHeight(true);
    // combined height of side-panel contents when not logged in
    var sidePanelAlt = $(newBulletinButton).outerHeight(true) + $(rulesCard).outerHeight(true);

    // Distance from the top edge of the window when fully scrolled up to the top edge of the window when scrolled down any amount.
    // Adding the height of side-panel when logged in (y), or when logged out (yAlt)
    var y = $(document).scrollTop() + sidePanel;
    var yAlt = $(document).scrollTop() + sidePanelAlt; 

    // Height of the navbar plus 30px because of the 48px top margin on the container-fluid that contains everything (bulletins, side-panel, etc.)
    var navBarHeight = $('#navbar').outerHeight(true) + 30;
    var navBarHeightAlt = $('#navbar').outerHeight(true) + 48; 
    
    // content-container-base is the col-9 container that holds the bulletin list. This line gets the last child of that container, which is actually the modal used when deleting...
    var lastChild = $('#content-container-base').children().last();
    // Therefore, the prev() method is used to get the sibling just before the modal, which should be the last bulletin on the page.
    var lastBulletin = lastChild.prev(); 
    
    if ($('#pagination-nav').length) {
        lastBulletin = lastBulletin.prev();
        console.log(lastBulletin);
    }

    // This line gets the position in pixels of the last child of content-container-base. "top" is the position in the document of the topmost edge of content-container-base.
    // The real top edge of this element is 16 pixels after position().top because of its 16px top margin, but I have deliberately not added 16 to position().top, and am including
    // said margin.
    var lastBulletinPosition = lastBulletin.position().top;
    
    // The inner height ignores margin / padding etc. so here, it is getting the true height of the last child of content-container-base. I am adding the top margin to that height.
    var lastBulletinHeightWithoutBottomMargin = lastBulletin.innerHeight() + parseInt(lastBulletin.css('margin-top')); 
    // Finally, this line gets the true bottom position (minus the bottom margin) of said last child by adding the height-with-top-margin gotten above to the top position of it.
    // In other words, lastChildPositionBottom is the y-coordinate of the actual bottom edge of the last child (not including its bottom margin).
    var lastBulletinPositionBottom = lastBulletinPosition + lastBulletinHeightWithoutBottomMargin;

    // All the direct children of the body element - [0]: container-fluid (displays messages), [1]: navbar, [2]: logged-in-as-top-container (only if page width falls to a certain amount)
    // Otherwise, child [2] is another container-fluid. 
    // Note that logged-in-as-top-container is always the 3rd child of the body, it's just that until the page width falls to a certain amount, its display is none, rather than block.
    // In other words, setting display to none doesn't remove the element from the DOM, it just makes it dimensionless and invisible.
    var childrenOfBody = $('body').children();

    // All the direct children of side-panel - [0]: logged-in-as, [1]: new-bulletin-button-container, [2]: rules
    var childrenOfSidePanel = $('#side-panel').children();

    // This initial if checks to see if the display of the 3rd child of the body element is block. This will be the case when the window width decreases enough
    // that the logged in text and new bulletin button appear at the top of the page, rather than the side. At this point, the display of child 3 changes from none to block.
    if ($(childrenOfBody[2]).css('display') == 'block') {

    } else {
        if (childrenOfSidePanel[0].getAttribute('class').includes('text-center logged-in-as')) { // This if is checking to see if the logged in message is part of the side-panel, which it will be only if you are logged in.
            if((y - sidePanel) > navBarHeight && y < lastBulletinPositionBottom) { // If scrollTop's height without the side-panel height is greater than the height of the nav bar, and is less than the y-coordinate position of the bottom of the last bulletin.
                body.removeClass('position-relative');
                loggedInAs.removeClass('logged-in-as-fixed-bottom');
                newBulletinButton.removeClass('button-fixed-bottom');
                rulesCard.removeClass('rules-fixed-bottom');
                    
                loggedInAs.addClass('logged-in-as-fixed');
                newBulletinButton.addClass('button-fixed');
                rulesCard.addClass('rules-fixed');
                    
                document.addClass('me-2');
            } else if (y >= lastBulletinPositionBottom) { // if y (scrollTop + side-panel height) is greater than or equal to the bottom of the last bulletin's y-coordinate, the side-panel becomes fixed to the bottom.
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
        } else { // This else executes if the logged in message is not part of side-panel (meaning you aren't logged in).
            if((yAlt - sidePanelAlt) > navBarHeightAlt && yAlt < lastBulletinPositionBottom) {
                body.removeClass('position-relative');
                rulesCard.removeClass('rules-fixed-bottom-alt');
                newBulletinButton.removeClass('button-fixed-bottom-alt');
            
                newBulletinButton.addClass('button-fixed-alt');
                rulesCard.addClass('rules-fixed-alt');
                document.addClass('me-2');
            } else if(yAlt >= lastBulletinPositionBottom) {
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
        
$(document).ready(function() {
    if (window.location.href.includes('/accounts/')) {
        var accountFooter = $('footer');
        accountFooter.addClass('position-fixed');
        accountFooter.addClass('bottom-0');

        if (window.location.href.includes('/signup/')) {
            var textField = $('input[type="text"]');
            var emailField = $('input[type="email"]');
            var passwordField1 = $('input[name="password1"]');
            var passwordField2 = $('input[name="password2"]'); 

            textField.addClass('float-end');
            emailField.addClass('float-end');
            passwordField1.addClass('float-end');
            passwordField2.addClass('float-end');

        } else if (window.location.href.includes('/login/')) {
            var textField = $('input[type="text"]');
            var passwordField = $('input[type="password"]');
            var rememberMe = $('label:contains("Remember Me:")');
            var parentP = $(rememberMe).parent();

            textField.addClass('float-end');
            passwordField.addClass('float-end');

            parentP.addClass('d-block');
            parentP.addClass('text-center');
            parentP.addClass('pt-1');

        } 
    } else if (window.location.href.includes('/edit/') || window.location.href.includes('/add')) {
        var editPageFooter = $('footer');
        editPageFooter.addClass('position-fixed');
        editPageFooter.addClass('bottom-0');

    } else if (!window.location.href.includes('/accounts/') && !window.location.href.includes('/edit/') && !window.location.href.includes('/add')) {
        var errorPageFooter = $('footer');
        var navbarHeader = $('.navbar');

        var contentHeight = $(document).innerHeight() - $(errorPageFooter).outerHeight(true) - $(navbarHeader).outerHeight(true);  

        if ($('#404-container').length) {
            var PageNotFoundContainer = $('#404-container');
            var row = $('#404-container>div');

            $(PageNotFoundContainer).height(contentHeight);
            $(row).height(contentHeight);

            errorPageFooter.addClass('position-fixed');
            errorPageFooter.addClass('bottom-0');
        } else if ($('#500-container').length) {
            var InternalServerErrorContainer = $('#500-container');
            var row = $('#500-container>div');

            $(InternalServerErrorContainer).height(contentHeight);
            $(row).height(contentHeight);

            errorPagefooter.addClass('position-fixed');
            footer.addClass('bottom-0');
        } else {
            errorPageFooter.removeClass('position-fixed');
            errorPageFooter.removeClass('bottom-0');
        }
    }
});


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

        if (!window.location.href.includes('/post/') || !window.location.href.includes('/accounts/')) {
            $(form).attr('action', $(this).attr('value'));
        }
    });
}

