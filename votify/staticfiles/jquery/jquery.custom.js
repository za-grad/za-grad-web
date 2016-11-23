(function($){
    $.extend({
        postJSON: function(url, data, callback_fn) {
            $.ajax({
                type: 'POST',
                data: JSON.stringify(data),
                contentType: "application/json",
                url: url,
                success: function(data) {
                    if (data.message) {
                        Votify.Messages.add(data.message);
                    }
                    callback_fn(data);
                }
            });
        }
    });

    $(function(){
        $('a[data-method="post"]').on('click', function(ev) {

            ev.stopPropagation();
            ev.preventDefault();

            var current_el = $(this);
            var confirmed_action = true;

            var should_prompt = current_el.attr('data-should-prompt');

            if (typeof should_prompt !== 'undefined' && should_prompt !== false){
                var message = "Are you sure?";
                if (should_prompt !== "")
                    message = should_prompt;
                confirmed_action = confirm(message);
            }

            var redirect_url = current_el.data('redirect-url');
            if (confirmed_action)
                $.postJSON(current_el.attr('href'), {}, function(data){
                    if (redirect_url)
                        location.href = redirect_url;
                    else
                        location.reload();
                });

        });
    });

    $(function(){
        $(document).ajaxSend(function(event, xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = $.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            function sameOrigin(url) {
                // url could be relative or scheme relative or absolute
                var host = document.location.host; // host + port
                var protocol = document.location.protocol;
                var sr_origin = '//' + host;
                var origin = protocol + sr_origin;
                // Allow absolute or scheme relative URLs to same origin
                return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                    (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                    // or any other URL that isn't scheme relative or absolute i.e relative.
                    !(/^(\/\/|http:|https:).*/.test(url));
            }
            function safeMethod(method) {
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            }

            if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        });
    });

    $.fn.cloudtip = function(el, width){
        var current_el = $(this);
        var _width = current_el.innerWidth();
        var cloudtip = $("<div>").html(el).addClass("cloudtip").css({'width': _width, 'display': 'none'});
        current_el.html(cloudtip);
        cloudtip.fadeIn();
        return current_el;
    };

    $(function(){
        $(document).click(function(e){
            var cloudtip = $(e.target).closest('.cloudtip');
            if (cloudtip.length === 0) {
                $('.cloudtip').fadeOut(function(){
                    $(this).remove();
                });
            }
        });
    });

    $.ajaxSetup({ cache: false });


})(jQuery || django.jQuery);
