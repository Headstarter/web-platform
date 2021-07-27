$( document ).ready(function() {
    $(".vertical-centration").each((index, element) => {
        console.log(element);
        $(element).attr("style","padding-top:calc(50vh - " + (2 * $(".rd-navbar").height()) + "px - " + ($(element.children[0]).height()/2) + "px);");
    });
});