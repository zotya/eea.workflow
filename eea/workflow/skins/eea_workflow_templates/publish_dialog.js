
function getDialogButton(dialog_selector, button_name) {
    var res = null;
    (function($) {
        var buttons = $(dialog_selector + ' .ui-dialog-buttonpane button' );
        for ( var i = 0; i < buttons.length; ++i ) {
            var jButton = $( buttons[i] );
            if ( jButton.text() == button_name ) {
                res = jButton[0];
                return;
            }
        }
        return;
    })(jQuery);
    return res;
}


function make_publish_text(questions){
 return (function($) {
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
})(jQuery);
}


function set_publish_dialog(){
(function($) {
    $("#workflow-transition-publish").attr('class', "kssIgnore");
    $("#plone-contentmenu-workflow dd.actionMenuContent a").click(function(e){
        if ($(this).attr('id') != "workflow-transition-publish") {
            var href = $(this).attr('href');
            var re = new RegExp("workflow_action=(.*)");
            var action = href.match(re)[1];
            var formaction = $('base').attr('href') + '/content_status_modify';
            var form = "<form id='publish_form' method='POST' action='" + formaction + "'>";
            form += "<input name='workflow_action' type='hidden' value='" + action + "'/>";
            form += "</form>";
            $('body').append(form);
            $("#publish_form").submit();

            return false;
        }

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

                     var base = $("base").attr('href') || document.baseURI || window.location.href.split("?")[0];
                     var url = base + "/publish_dialog";

                     $(this).load(url, function(){
                         var base_url = $(".metadata .context_url").text();
                         $("#workflow-emails-placeholder").load(base_url + '/workflow_emails', function(){
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
                         //see if all radios have a value. When they do, activate the OK button
                         $(".questions input[type='radio']", target).change(function(){
                             var questions = $(".question", target);
                             var activated = $(":radio[checked='true']", target);
                             var okbtn = getDialogButton('.publishDialog', 'Ok');
                             if (questions.length === activated.length) {
                                 $(okbtn).removeAttr('disabled').removeClass('ui-state-disabled');
                             } else {
                                 $(okbtn).attr('disabled', 'disabled').addClass('ui-state-disabled');
                             }
                         });

                     });
                     //
                     //disabling ok button
                     var okbtn = getDialogButton('.publishDialog', 'Ok');
                     $(okbtn).attr('disabled', 'disabled').addClass('ui-state-disabled');

                     return false;
                 }
        });
        return false;
    });
})(jQuery);
}

var disableWorkflowKSS = function(){
    var rules = kukit.engine.getRules();
    jQuery(rules).each(function(){
            var selector = this.kssSelector.css;
            if (selector == "#plone-contentmenu-workflow dd.actionMenuContent a") {
                this.actions.content = {};
            }
            if (selector == "#plone-contentmenu-workflow dd.actionMenuContent a.kssIgnore") {
                this.actions.content = {};
            }
    });
};

jQuery(document).ready(function ($) {

  set_publish_dialog();
  $("#workflow-transition-fake_publish").click(function(){
      alert("This item is not ready to be published");
      return false;
  });

  // We need to wait for kukit to be initialized
  jQuery(document).oneTime(1000, "disable-kss", function(){
    disableWorkflowKSS();
  });

});
