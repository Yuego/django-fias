'use strict';

(function($){

    var addrs = [
        'Республика Дагестан, с. Кванхидатли',
        'Астраханская область, Енотаевский район, с. Ленино, ул.Степная',
        'Респ. Казахстан, Атырауская обл., с. Ганюшкино, ул. Кошекбаева',
        'Астраханская обл., п. Верхний Баскунчак, пер. Октябрьский',
    ];

    $(function(){
        var $input = $("input[data-autocomplete='address']");

        $input.autocomplete({
            minLength: 1,
            source: $input.data('source'),
            select: function(event, ui){
                console.log([event, ui]);
            },
            focus: function(event, ui){
                console.log('Focus');
            }
        });

    });



}(jQuery));
