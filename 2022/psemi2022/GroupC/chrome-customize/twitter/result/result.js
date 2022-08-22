'use strict';

! function(){
    const html = chrome.runtime.getURL("twitter/result/result.html");

    $('body').wrapInner('<div class="wrapper"></div>');
    $('.wrapper').wrapInner('<div class="main-screen"></div>');
    $('.wrapper').append('<div class="side"></div>');
    $('.side').load(html)

    window.setTimeout(() => {
        document.getElementById("hukidashi-result").src = chrome.runtime.getURL("./twitter/resources/hukidashi.jpg");
        document.getElementById("charc-result").src = chrome.runtime.getURL("./twitter/resources/charc.png");
    }, 200);
}();

function replace_url(){
    var cards1 = document.querySelectorAll('div[data-testid="card.wrapper"] div a');
    if(cards1.length == 0) {
        //The node we need does not exist yet.
        //Wait 500ms and try again
        window.setTimeout(replace_url, 500);
        return;
    }
    
    for ( let i = 0;i < cards1.length; i++){
        cards1[i].setAttribute('href', 'http://127.0.0.1:5000/shindan');
     }
}
replace_url();