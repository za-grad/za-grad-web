(function($){

    $(document).on('click', '.btn-disapprove', function(ev) {

        ev.stopPropagation();
        ev.preventDefault();

        var current_el = $(this);
        var confirmed_action = true;

        var should_prompt = current_el.attr('data-should-prompt');

        if (typeof should_prompt !== 'undefined' && should_prompt !== false){
            var message = "Are you sure?";
            if (should_prompt !== "")
                message = should_prompt;
            confirmed_action = prompt('Jesi siguran da želiš obustaviti prijedlog?\nNapiši razlog.');
        }

        var redirect_url = current_el.data('redirect-url');
        if (confirmed_action)
            $.postJSON(current_el.attr('href'), {'reason': confirmed_action}, function(data){
                if (redirect_url)
                    location.href = redirect_url;
                else
                    location.reload();
            });

        return false;

    });

}(django.jQuery));
