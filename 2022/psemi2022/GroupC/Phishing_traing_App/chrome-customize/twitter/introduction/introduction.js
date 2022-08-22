'use strict';

! function () {
    const html = chrome.runtime.getURL("twitter/introduction/introduction.html");

    $('body').wrapInner('<div class="wrapper"></div>');
    $('.wrapper').wrapInner('<div class="main-screen"></div>');
    $('.wrapper').append('<div class="side"></div>');
    $('.side').load(html)

    window.setTimeout(() => {
        document.getElementById("hukidashi-intro").src = chrome.runtime.getURL("./twitter/resources/hukidashi.jpg");
        document.getElementById("charc-intro").src = chrome.runtime.getURL("./twitter/resources/charc3.jpg");
    }, 200);
}();

function replace_url() {
    var cards1 = document.querySelectorAll('div[data-testid="card.wrapper"] div a');
    if (cards1.length == 0) {
        window.setTimeout(replace_url, 500);
        return;
    }

    for (let i = 0; i < cards1.length; i++) {
        cards1[i].setAttribute('href', 'http://127.0.0.1:5000/shindan');
    }
}
replace_url();