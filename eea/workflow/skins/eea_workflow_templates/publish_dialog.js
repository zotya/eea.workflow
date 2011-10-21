function getDialogButton(dialog_selector, button_name) {
    var buttons = $( dialog_selector + ' .ui-dialog-buttonpane button' );
    for ( var i = 0; i < buttons.length; ++i ) {
        var jButton = $( buttons[i] );
        if ( jButton.text() == button_name ) {
            return jButton;
        }
    }
    return null;
}


function make_publish_text(questions){
    var text = "Self-QA:    ";
    $(".question", questions).each(function(){
        var title = $("h3", this).text();
        var answer = $(":radio[checked='true']", this).val();
        var comment = $("textarea", this).val();
        if (comment.length) {
            comment += "\n";
        }
        text += title + ": " + answer + "      " + comment + "      ";
    });
    return text;
}


function set_publish_dialog(){
    $(".actionMenuContent a[title='Publish']").click(function(e){
        // this assumes a link like http://.../content_status_modify?workflow_action=quickPublish
        var transition = $(this).attr('href').split('=')[1]; 
        var target = $("<div>").appendTo("body").attr('id', 'publish-dialog-target')[0];
        $(".publishDialog").remove();

        $(target).dialog({
            title:"Confirm information before publishing",
            dialogClass:'publishDialog',
            modal:true,
            resizable:true,
            width:800,
            height:700,
            buttons:{
                "Ok":function(){
                    var questions_area = $(".questions", target);

                    // check if all required questions have been answered positively
                    var go = true;
                    $(".question", target).each(function(){
                        var q = this;
                        if ($(q).hasClass('required')){
                            var radio = $("input[value='yes']", q).get(0);
                            if (radio.checked !== true) {
                                $("h3", q).after("<div class='notice' style='color:Black; background-color:#FFE291; " + 
                                    "padding:3px'>You need to answer with Yes</div>");
                                $(".notice", q).effect("pulsate", {times:3}, 2000, function(){$('.notice', q).remove();});
                                go = false;
                                return false;
                            }
                        }
                    });
                    if (go === false){ return false; }

                    var text = make_publish_text(questions_area);
                    var form = $("form", target);
                    $("textarea#comment", target).val(text);
                    $(".questions").remove();

                    //var now = new Date();
                    //now_str = now.getFullYear() + "/" + now.getMonth() + 1 + '/' + now.getDate();
                    //form.append($("<input type='hidden' name='effective_date'>").attr('value', now_str));

                    $("input[name='workflow_action']", target).attr('value', transition);
                    form.submit();
                    $(this).dialog("close");
                    return false;
                },
                "Cancel":function(){
                    $(this).dialog("close");
                }
            },
            open:function(ui){

                     // fix this
                     //var base = $("base").attr('href') || document.baseURI || window.location.href.split("?")[0];
                     var base = window.context_url; // this is defined from main_template
                     var url = base + "/publish_dialog";

                     $(this).load(url, function(){
                         //disabling ok button
                         var okbtn = getDialogButton('.publishDialog', 'Ok');
                         okbtn.attr('disabled', 'disabled').addClass('ui-state-disabled');

                         //see if all radios have a value. When they do, activate the OK button
                         $(".questions input[type='radio']", target).change(function(){
                             var questions = $(".question", target);
                             var activated = $(":radio[checked='true']", target);
                             if (questions.length === activated.length) {
                                 var okbtn = getDialogButton('.publishDialog', 'Ok');
                                 okbtn.removeAttr('disabled').removeClass('ui-state-disabled');
                             }
                         });

                         $("#notice_emails .collapsibleHeader").click(
                             function(){
                                 $(this).parent().each(
                                     function(){
                                         var el = $(this);
                                         if (el.hasClass('expandedInlineCollapsible')) {
                                             el.removeClass('expandedInlineCollapsible').addClass('collapsedInlineCollapsible');
                                         } else {
                                             el.removeClass('collapsedInlineCollapsible').addClass('expandedInlineCollapsible');
                                         }
                                     }
                                     );
                             });

                     });
                     return false;
                 }
        });
        return false;
    });
}

$(window).load(function(){
    set_publish_dialog();
});
