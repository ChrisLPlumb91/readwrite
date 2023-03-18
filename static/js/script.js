/**
 * The below code executes when the page has loaded fully. The first half of it is necessary because of how the form elements
 * of the account pages are injected into the HTML, and cannot be changed in their templates. Thus, this code adds classes
 * to those elements once they have been rendered in the browser.
 * 
 * The resize event listener below is able to make changes to these pages via ids because the containers for the form are exposed
 * in the templates.
 * 
 * If the user is not on an accounts page, exceptions are avoided by using an if-else construct. The edit and add bulletin pages,
 * for instance, do not contain the same elements as the accounts pages, and so any attempts to get those elements would produce
 * errors.
 * 
 * Several pages other than the accounts page have central content sections that are small in height, and which therefore cause
 * the page footer to appear halfway up the screen. This code ensures that the footer is fixed to the bottom of the window for
 * all of these pages.
 * 
 * Toward the bottom then is code that is identical to the code in the scroll event listener after this one. There are several elements
 * which move as the user scrolls, but with only a scroll listener, reloading the page scrolled halfway down will cause these elements to
 * jump to the top of the document until the user scrolls. Using a ready listener with the exact same code prevents this. For an explanation
 * of this code, please see the comment above the scroll listener below.
 * 
 * There are also a handful of lines of code within this ready listener that are responsible for assigning the active class to links
 * in the site's navigation menu.
 * 
 * Finally, the last few lines are used to temporarily display Django messages to the user.
 */
$(document).ready(function() {  
    if (window.location.href.includes('/accounts/')) {
        var accountFooter = $('footer');
        accountFooter.addClass('position-fixed');
        accountFooter.addClass('bottom-0');

        if (window.location.href.includes('/signup/')) {
            var signUpLink = $('#sign-up-link');
            var textField = $('input[type="text"]');
            var emailField = $('input[type="email"]');
            var passwordField1 = $('input[name="password1"]');
            var passwordField2 = $('input[name="password2"]'); 

            signUpLink.addClass('active');

            textField.addClass('float-end');
            emailField.addClass('float-end');
            passwordField1.addClass('float-end');
            passwordField2.addClass('float-end');

        } else if (window.location.href.includes('/login/')) {
            var logInLink = $('#log-in-link');
            var textField = $('input[type="text"]');
            var passwordField = $('input[type="password"]');
            var rememberMe = $('label:contains("Remember Me:")');
            var parentP = $(rememberMe).parent();

            logInLink.addClass('active');

            textField.addClass('float-end');
            passwordField.addClass('float-end');

            parentP.addClass('d-block');
            parentP.addClass('text-center');
            parentP.addClass('pt-1');

        } else if (window.location.href.includes('/logout/')) {
            var logOutLink = $('#log-out-link');

            logOutLink.addClass('active');
        }
    } else if (window.location.href.includes('/edit/') || window.location.href.includes('/add')) {
        var editPageFooter = $('footer');
        editPageFooter.addClass('position-fixed');
        editPageFooter.addClass('bottom-0');

    } else if (!window.location.href.includes('/accounts/') && !window.location.href.includes('/edit/') && !window.location.href.includes('/add')) {
        
        if(!window.location.href.includes('/post/')) {
            var homePageLink = $('#home-page-link');

            homePageLink.addClass('active');
        }
        
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

        var body = $('body');
        var loggedInAs = $('#logged-in-side');
        var newBulletinButton = $('.new-bulletin-button-container');
        var rulesCard = $('.rules');
        
        var sidePanel = $(loggedInAs).outerHeight(true) + 18 + $(newBulletinButton).outerHeight(true) + $(rulesCard).outerHeight(true);
        var sidePanelAlt = $(newBulletinButton).outerHeight(true) + $(rulesCard).outerHeight(true);

        var y = $(document).scrollTop() + sidePanel;
        var yAlt = $(document).scrollTop() + sidePanelAlt; 

        var navBarHeight = $('#navbar').outerHeight(true) + 30;
        var navBarHeightAlt = $('#navbar').outerHeight(true) + 48; 
        
        var lastChild = $('#content-container-base').children().last();
        var lastBulletin = lastChild.prev(); 
        
        if ($('#pagination-nav').length) {
            lastBulletin = lastBulletin.prev();
        }

        var lastBulletinPosition = lastBulletin.position().top;
        var lastBulletinPositionBottom = lastBulletinPosition + lastBulletin.innerHeight();

        var childrenOfBody = $('body').children();
        var childrenOfSidePanel = $('#side-panel').children();

        if ($(childrenOfBody[2]).css('display') != 'block') {

            if (childrenOfSidePanel[0].getAttribute('class').includes('text-center logged-in-as')) {

                if(lastBulletinPositionBottom >= navBarHeightAlt + sidePanel) {

                    if((y - sidePanel) > navBarHeight && y < lastBulletinPositionBottom) {
                        body.removeClass('position-relative');
                        loggedInAs.removeClass('logged-in-as-fixed-bottom');
                        newBulletinButton.removeClass('button-fixed-bottom');
                        rulesCard.removeClass('rules-fixed-bottom');
                            
                        loggedInAs.addClass('logged-in-as-fixed');
                        newBulletinButton.addClass('button-fixed');
                        rulesCard.addClass('rules-fixed');
                            
                    } else if (y >= lastBulletinPositionBottom) {
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
                    }
                }        
            } else {
                if(lastBulletinPositionBottom >= navBarHeightAlt + sidePanelAlt) {
                    if((yAlt - sidePanelAlt) > navBarHeightAlt && yAlt < lastBulletinPositionBottom) {
                        body.removeClass('position-relative');
                        rulesCard.removeClass('rules-fixed-bottom-alt');
                        newBulletinButton.removeClass('button-fixed-bottom-alt');
                    
                        newBulletinButton.addClass('button-fixed-alt');
                        rulesCard.addClass('rules-fixed-alt');

                    } else if(yAlt >= lastBulletinPositionBottom) {
                        rulesCard.removeClass('rules-fixed-alt');
                        newBulletinButton.removeClass('button-fixed-alt');
                    
                        body.addClass('position-relative');
                        newBulletinButton.addClass('button-fixed-bottom-alt');
                        rulesCard.addClass('rules-fixed-bottom-alt');

                    } else {
                        rulesCard.removeClass('rules-fixed-alt');
                        newBulletinButton.removeClass('button-fixed-alt');

                    }
                }
            }
        }   
    }

    setTimeout(function () {
        let messages = document.getElementById('msg');
        let alert = new bootstrap.Alert(messages);
        alert.close();
    }, 2000);
});

/**  
 * The below code listens for scroll events, and depending on where the user has scrolled to on the page, the section of the site on the far right side
 * of most of the pages will behave differently. Once the user scrolls down to the top edge of this section, it becomes fixed to the top of the window,
 * and follows the scrollbar. Once the bottom edge of this section lines up with the bottom edge of the last element in the central content container,
 * it becomes absolutely positioned so that its bottom edge is in line with the bottom edge of that bottommost element, whether it is a bulletin on
 * the main page, or a comment on a bulletin page.
 * 
 * This code takes into account that the last element in the central section will always in fact be the modal that appears when you try to delete
 * a comment or bulletin, and that on the main page, the element before this will be the pagination container if there are more than 10 approved
 * bulletins. In other words, the last bulletin or comment will actually either be the second last element on the page, or the third last.
 * 
 * To calculate when the bottom of the side section lines up with the bottom of the last comment or bulletin, the height of said section is added
 * to the value for scrollTop, which is recalculated with every scroll event. If there are only a few bulletins on the page, the second-to-innermost
 * if prevents the classes from being set and pushing the side section to the top of the window.
 * 
 * There are two branches of this code depending on whether or not the user is logged in. When they are not logged in, the message that says,
 * "You are logged in as _____" is not displayed, and so the total height of the side section is different.
*/
$(document).scroll(function() {
    var body = $('body');
    var loggedInAs = $('#logged-in-side');
    var newBulletinButton = $('.new-bulletin-button-container');
    var rulesCard = $('.rules');
    
    var sidePanel = $(loggedInAs).outerHeight(true) + 18 + $(newBulletinButton).outerHeight(true) + $(rulesCard).outerHeight(true);
    var sidePanelAlt = $(newBulletinButton).outerHeight(true) + $(rulesCard).outerHeight(true);

    var y = $(document).scrollTop() + sidePanel;
    var yAlt = $(document).scrollTop() + sidePanelAlt; 

    var navBarHeight = $('#navbar').outerHeight(true) + 30;
    var navBarHeightAlt = $('#navbar').outerHeight(true) + 48; 
    
    var lastChild = $('#content-container-base').children().last();
    var lastBulletin = lastChild.prev(); 
    
    if ($('#pagination-nav').length) {
        lastBulletin = lastBulletin.prev();
    }

    var lastBulletinPosition = lastBulletin.position().top;
    var lastBulletinPositionBottom = lastBulletinPosition + lastBulletin.innerHeight();

    var childrenOfBody = $('body').children();
    var childrenOfSidePanel = $('#side-panel').children();

    if ($(childrenOfBody[2]).css('display') != 'block') {

        if (childrenOfSidePanel[0].getAttribute('class').includes('text-center logged-in-as')) {

            if(lastBulletinPositionBottom >= navBarHeightAlt + sidePanel) {

                if((y - sidePanel) > navBarHeight && y < lastBulletinPositionBottom) {
                    body.removeClass('position-relative');
                    loggedInAs.removeClass('logged-in-as-fixed-bottom');
                    newBulletinButton.removeClass('button-fixed-bottom');
                    rulesCard.removeClass('rules-fixed-bottom');
                        
                    loggedInAs.addClass('logged-in-as-fixed');
                    newBulletinButton.addClass('button-fixed');
                    rulesCard.addClass('rules-fixed');
                        
                } else if (y >= lastBulletinPositionBottom) {
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
                        
                }
            }        
        } else {
            if(lastBulletinPositionBottom >= navBarHeightAlt + sidePanelAlt) {

                if((yAlt - sidePanelAlt) > navBarHeightAlt && yAlt < lastBulletinPositionBottom) {
                    body.removeClass('position-relative');
                    rulesCard.removeClass('rules-fixed-bottom-alt');
                    newBulletinButton.removeClass('button-fixed-bottom-alt');
                
                    newBulletinButton.addClass('button-fixed-alt');
                    rulesCard.addClass('rules-fixed-alt');

                } else if(yAlt >= lastBulletinPositionBottom) {
                    rulesCard.removeClass('rules-fixed-alt');
                    newBulletinButton.removeClass('button-fixed-alt');
                
                    body.addClass('position-relative');
                    newBulletinButton.addClass('button-fixed-bottom-alt');
                    rulesCard.addClass('rules-fixed-bottom-alt');

                } else {
                    rulesCard.removeClass('rules-fixed-alt');
                    newBulletinButton.removeClass('button-fixed-alt');
                }
            }
        }
    }
});

/** 
 * This code listens for window resizing events. At a certain width, it truncates anchor elements within divs of the card-header class.
 * These include bulletin titles on the main page, and bulletin links in individual bulletin pages.
 * 
 * If you are on either the custom 404 or 500 pages, code is executed to dynamically adjust the height of the central container (between
 * the header and the footer) so that it never vanishes below / behind the footer. This is a copy of the code in the ready listener,
 * but unlike that, this one runs every time the user resizes the window, rather than just once after the page has loaded.
 * 
 * This listener also checks to see if you are on any of the accounts pages, e.g. login, logout, or sign up. If so, it changes the bootstrap
 * grid classes for the elements on these pages depending on the width of the window.
*/
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

/**
 * The below code attaches a click event listener to any delete buttons on either the main page or a bulletin page.
 * When clicked, these buttons open a modal that serves as a dialog box asking the user to confirm deletion of 
 * a comment or bulletin. 
 * 
 * The below code does not open the modal. It changes the text content of the modal depending on what the user
 * is attempting to delete.
 * 
 * It also changes the action attribute of the modal confirmation button's form depending on what the user
 * is attempting to delete, because the correct view needs to execute, whether it is for the deletion of a
 * comment or a bulletin.
 * 
 * On a bulletin page, the default action of said form is "{% url 'confirm_delete' bulletin.slug %}", which directs 
 * to the view which deletes bulletins. This works because the given bulletin is accessible globally throughout
 * the bulletin page template. However, the comment deleting view requires a query string to be attached
 * to the url pattern in order to execute properly. Because comment objects are only directly accessible from within
 * the for loop that is iterating through a queryset of comments, the data is assigned to the value attribute
 * of the delete button. This data is then assigned to the action attribute of the modal form.
 * 
 * On the main page, the modal is outside of the for loop that iterates through the Bulletin queryset, and so cannot
 * access any bulletins, hence the reason for the second condition in the if statement that checks to see if you
 * are on the main page.
 * 
 * Note that the modal-button class does not appear on any pages other than the main page and bulletin pages. This means
 * that this code will not execute on any of the account pages, or on the edit or add bulletin pages.
 */
if($('.modal-button').length) {
    $('.modal-button').on('click', function() {
        var type = $(this).data('type');
        var lowerCaseType = type.toLowerCase();
        var form = $('.modal-footer>form');

        $('.modal-header>h1').text(`Delete ${type}`);
        $('.modal-body>p').text(`Are you sure you want to delete your ${lowerCaseType}?`);
        
        if(type == 'Comment' || !window.location.href.includes('/post/')) {
            $(form).attr('action', $(this).attr('value'));
        }
    });
}

