window.isMobile = {
    Android: function() {
        return navigator.userAgent.match(/Android/i);
    },
    BlackBerry: function() {
        return navigator.userAgent.match(/BlackBerry/i);
    },
    iOS: function() {
        return navigator.userAgent.match(/iPhone|iPad|iPod/i);
    },
    Opera: function() {
        return navigator.userAgent.match(/Opera Mini/i);
    },
    Windows: function() {
        return navigator.userAgent.match(/IEMobile/i);
    },
    any: function() {
        return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
    }
};

var chunk_size = 36;

var VotifyLogin = {
    require_login: function() {
        $.getJSON('/accounts/login/test/', function(data){
            if (!data.result) {
                window.location.href = '/accounts/login/?next=' + window.location.href;
            }
        });
    }
};

window.Votify = {
    Login: VotifyLogin,
    Messages: {
        add: function(msg) {
            $('.alert-holder').html(_.template($('#alert-template').html(), {'msg': msg}));
        }
    }
};

window.IdeaSmallBox = {
    current_offset: 0,
    loading: false,
    config: {
        load: {
            load_create_link: false,
            order: 'top'
        },
        cols_no: 3
    },
    get_filter: function() {
        var self = IdeaSmallBox;
        var filter = '';
        if (self.config.load.load_create_link && self.current_offset === 0)
            filter += '&load_create_link=1';
        if (self.config.load.filter_district_id)
            filter += '&filter_district_id=' + self.config.load.filter_district_id;
        if (self.config.load.filter_category_id)
            filter += '&filter_category_id=' + self.config.load.filter_category_id;
        if (self.config.load.filter_user_id)
            filter += '&filter_user_id=' + self.config.load.filter_user_id;
        if (self.config.load.order)
            filter += '&order=' + self.config.load.order;
        if (self.config.load.template)
            filter += '&template=' + self.config.load.template;
        return filter;
    },
    holder_selector: '.idea-small-box-list-holder',
    get_holder: function() {
        return $(this.holder_selector);
    },
    clear: function() {
        var holder = IdeaSmallBox.get_holder();

        window.last_scroll_position = 0;
        IdeaSmallBox.current_offset = 0;
        holder.empty();

        if ($('body').innerWidth() < 768) {
            IdeaSmallBox.config.cols_no = 1;
        }

        var span_size = 12 / IdeaSmallBox.config.cols_no;

        for (var i=0; i<IdeaSmallBox.config.cols_no; i++) {
            holder.append($('<div>').addClass('span' + span_size + ' col' + i));
        }
    },
    load: function(clear) {
        if (!IdeaSmallBox.loading) {
            if (clear) {
                IdeaSmallBox.clear();
            }
            IdeaSmallBox.loading = true;
            $.getJSON("/prijedlozi/list/?offset=" + IdeaSmallBox.current_offset + IdeaSmallBox.get_filter(), function(data){
                for (var i=0; i < data.length; i++) {
                    IdeaSmallBox.get_holder().find('.col' + (i % IdeaSmallBox.config.cols_no)).append(data[i]);
                }
                if (data.length < chunk_size) {
                    $('.idea-small-box-list-load-more').hide();
                }
                IdeaSmallBox.current_offset++;
                IdeaSmallBox.loading = false;
                $('body').trigger('idea_list_loaded');
            });
        }
    }
};

window.NewsSmallBox = {
    current_offset: 0,
    loading: false,
    config: {
        cols_no: 3
    },
    holder_selector: '.news-small-box-list-holder',
    get_holder: function() {
        return $(this.holder_selector);
    },
    clear: function() {
        var self = this;
        var holder = self.get_holder();

        window.last_scroll_position = 0;
        self.current_offset = 0;
        holder.empty();

        if ($('body').innerWidth() < 768) {
            self.config.cols_no = 1;
        }

        var span_size = 12 / self.config.cols_no;

        for (var i=0; i<self.config.cols_no; i++) {
            holder.append($('<div>').addClass('span' + span_size + ' col' + i));
        }
    },
    load: function(clear) {
        var self = this;
        if (!self.loading) {
            if (clear) {
                self.clear();
            }
            self.loading = true;
            $.getJSON("/novosti/list/?offset=" + self.current_offset, function(data){
                for (var i=0; i < data.length; i++) {
                    self.get_holder().find('.col' + (i % self.config.cols_no)).append(data[i]);
                }
                if (data.length < chunk_size) {
                    $('.news-small-box-list-load-more').hide();
                }
                self.current_offset++;
                self.loading = false;
            });
        }
    }
};

window.MemberSmallBox = {
    current_offset: 0,
    loading: false,
    config: {
        cols_no: 3
    },
    holder_selector: '.member-small-box-list-holder',
    get_holder: function() {
        return $(this.holder_selector);
    },
    clear: function() {
        var self = this;
        var holder = self.get_holder();

        window.last_scroll_position = 0;
        self.current_offset = 0;
        holder.empty();

        if ($('body').innerWidth() < 768) {
            self.config.cols_no = 1;
        }

        var span_size = 12 / self.config.cols_no;

        for (var i=0; i<self.config.cols_no; i++) {
            holder.append($('<div>').addClass('span' + span_size + ' col' + i));
        }
    },
    load: function(clear) {
        var self = this;
        if (!self.loading) {
            if (clear) {
                self.clear();
            }
            self.loading = true;
            $.getJSON("/korisnici/list/ajax/?offset=" + self.current_offset, function(data){
                for (var i=0; i < data.length; i++) {
                    var data_html = $(data[i]);
                    var title_el = data_html.find('.title');
                    title_el.text((self.current_offset * chunk_size + i + 1) + ". " + title_el.text());
                    self.get_holder().find('.col' + (i % self.config.cols_no)).append(data_html);
                }
                if (data.length < chunk_size) {
                    $('.member-small-box-list-load-more').hide();
                }
                self.current_offset++;
                self.loading = false;
            });
        }
    }
};

window.last_scroll_position = 0;
$(window).scroll(function () {
    if (($(window).height() + $(window).scrollTop() >= $(document).height() - 600) && last_scroll_position <= $(window).scrollTop() ){
        last_scroll_position = $(window).scrollTop();
        $('.idea-small-box-list-load-more .load-more').click();
        $('.news-small-box-list-load-more .load-more').click();
        $('.member-small-box-list-load-more .load-more').click();
    }
});

$(document).on('click', '.idea-small-box-list-load-more .load-more', function(e){
    IdeaSmallBox.load();
    return false;
});

$(document).on('click', '.news-small-box-list-load-more .load-more', function(e){
    NewsSmallBox.load();
    return false;
});

$(document).on('click', '.member-small-box-list-load-more .load-more', function(e){
    MemberSmallBox.load();
    return false;
});

Array.prototype.rotate = function(n) {
    while (this.length && n < 0) n += this.length;
    this.push.apply(this, this.splice(0, n));
    return this;
};

function selectShadow(){
    $('.select-shadow').each(function(){
        var self = $(this);

        var $shadow = $('<div>', {
            css: {
                'position': 'absolute',
                'left':     self.offset().left,
                'top':      self.offset().top,
                'width':    self.outerWidth(),
                'height':   self.outerHeight(),
                '-webkit-box-shadow': '1px 2px 5px rgba(230, 230, 230, 0.75)',
                '-moz-box-shadow': '1px 2px 5px rgba(230, 230, 230, 0.75)',
                'box-shadow': '1px 2px 5px rgba(230, 230, 230, 0.75)',
                'z-index':  -1
            }
        }).appendTo(self.parent());
    });
}

$(function(){
    selectShadow();
});

window.add_right_content_bg = function() {
    var holder = $('.sidebar_smallbox_holder');
    var bg = $('<div>')
        .addClass('content-right-bg')
        .css({
            height: holder.closest('.container').innerHeight() + 120
        });
    holder
        .css('position', 'relative')
        .append(bg);

    return bg;
};


$(function(){
    $('.get-mobile-footer .btn-mobile-send').click(function(){
        var mobile = $('.get-mobile-footer .get-mobile-input').val();
        if (mobile && mobile !== '') {
            $.postJSON('/korisnici/mobile_form_handler/', {'mobile': mobile}, function(data){
                if (data.success) {
                    $('.get-mobile-footer .get-mobile-input').val('');
                }
                $('.get-mobile-footer .get-mobile-msg').text(data.msg);
            });
        } else {
            $('.get-mobile-footer .get-mobile-msg').text('Upišite broj mobitela.');
        }
        return false;
    });

    $('.get-mobile-footer .get-mobile-input').keypress(function(e){
        if (e.which == 13) {
            $('.get-mobile-footer .btn-mobile-send').click();
        }
    });
});


$(function(){

    $(document).on('click', '.alert .close', function(e){
        $(this).closest('.alert').fadeOut(400, function(){
            $(this).remove();
        });
        return false;
    });

    if (isMobile.any()) {
        $('.sidebar-right').remove();
    }

    $('.sidebar-right .give-idea').hover(
        function(){
            $(this).stop();
            $(this).animate({left: '-310px'}, 150);
        },
        function(){
            $(this).stop();
            $(this).animate({left: '0px'}, 150);
        }
    );

    var bann_holder = $('.banner-holder .banner');
    var footer_top = $('.footer .top');
    var create_idea_banner = $('.create-idea-banner');
    var bann_holder_f_size_px = parseInt(bann_holder.css('font-size'));
    var footer_top_f_size_px = parseInt(footer_top.css('font-size'));
    var create_idea_banner_px = parseInt(create_idea_banner.css('font-size'));

    function resize_font() {
        var win_width = $(window).width();
        var ratio = parseFloat(win_width)/1905;
        bann_holder.css('font-size', ratio * bann_holder_f_size_px + 'px');
        footer_top.css('font-size', ratio * footer_top_f_size_px + 'px');
        create_idea_banner.css('font-size', ratio * create_idea_banner_px + 'px');
    }

    $(window).resize(resize_font);
    resize_font();
});
