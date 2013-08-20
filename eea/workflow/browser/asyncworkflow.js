function AsyncWorkflow(){
    this.handler = "@@workflow_menu";
    this.menu = jQuery("#plone-contentmenu-workflow");
    this.menuHeader = jQuery(".actionMenuHeader", this.menu);
    this.submenu = jQuery(".actionMenuContent", this.menu);
    var self = this;
    jQuery("#edit-bar").on('click', 
                           "#plone-contentmenu-workflow dd a", 
                           function(e){return self.handle_click(e)});
}

AsyncWorkflow.prototype.handle_click = function(e){
    var $element = jQuery(e.target);

    // compatibility with publishDialog and any other script that wants
    // to handle workflow action by itself
    if ($element.hasClass('ignoreKSS')) return true;

    var url = $element.attr('href');
    jQuery("#plone-contentmenu-workflow .actionMenuHeader").html("<img src='" + context_url + "/eea-ajax-loader.gif' " + 
                                 "alt='Changing state ...' title='Changing state ...' />");
    this.execute(url);
    return false;
}

AsyncWorkflow.prototype.execute = function(url){
    var self = this;
    var ajaxhandler = context_url + '/' + this.handler;
    var jxhr = jQuery.post(ajaxhandler, data={'action_url':url}, success=function(data){
        jQuery("#contentActionMenus").html(data);
        jQuery(initializeMenus);    //we need to reinitialize menus
        //new AsyncWorkflow();
    }).fail(function(){
        self.menuHeader.html("Failure!");
    });
}

jQuery(document).ready(function ($) {
    new AsyncWorkflow();
});

