$(function () {

    var $content_url=$('.field-content_url');
    var $content_word=$('.field-content_word');
    var $is_jump=$('input[name=is_jump]');
    var switch_editor=function (is_jump) {
        if(is_jump){
            $content_url.show();
            $content_word.hide();
        }
        else {
            $content_url.hide();
            $content_word.show();
        }
    };
    $is_jump.on('click',function () {
        switch_editor($(this).is(':checked'));
    });
    switch_editor($is_jump.is(':checked'));

});