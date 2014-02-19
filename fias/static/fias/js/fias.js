
(function($){
    if (!window['fias']) {
        var fias = {
            onOpen: function(e) {
                var $input = $('.select2-input');

                var txt = $(this).txt();
                if (typeof txt !== 'undefined') {
                    $input.val(txt);
                    $input.select();
                }
                $input.attr('tabindex', -1);
            },

            onSelecting: function(event) {
                var preventClosing = false;
                var $input = $('.select2-input');
                var text = event.object.text;

                var t = $input.val().replace(/\s+$/g, '');
                if (t.indexOf(',', t.length - 1) == -1 && (event.object.id == null || event.object.level < 7)) {
                    preventClosing = true;
                }

                if (t.indexOf(event.object.text) != 0) {
                    if (event.object.level < 7) {
                        text += ', ';
                    } else if (event.object.id == null) {
                        text += ' ';
                    }

                    $input.val(text);
                }

                $input.focus();

                if (preventClosing) {event.preventDefault();}
                else {$input.attr('tabindex', $(this).data('select2').elementTabIndex || 0);}
            }
        };

        window.fias = fias;
    }
})(jQuery);
