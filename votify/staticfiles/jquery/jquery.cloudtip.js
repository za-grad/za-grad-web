jQuery.fn.cloudtip = function(el, width){
    var _width = $(this).innerWidth();
    var cloudtip = $("<div>").html(el).addClass("cloudtip").css('width', _width);
    return $(this).html(cloudtip);
};

$(function(){
    $(document).click(function(e){
        var cloudtip = $(e.target).closest('.cloudtip');
        if (cloudtip.length === 0) {
            $('.cloudtip').remove();
        }
    });
});
