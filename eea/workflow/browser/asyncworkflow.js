function AsyncWorkflow(){
    this.handler = "@@workflow_menu";
    this.menu = jQuery("#plone-contentmenu-workflow");
    this.menuHeader = jQuery(".actionMenuHeader", this.menu);
    this.submenu = jQuery(".actionMenuContent", this.menu);
    var self = this;
    jQuery("#edit-bar").on('click',
                           "#plone-contentmenu-workflow dd a",
                           function(e){return self.handle_click(e);});
}

AsyncWorkflow.Events = {};
AsyncWorkflow.Events.WORKFLOW_MENU_REFRESHED = "ID-WORKFLOW_MENU_REFRESHED";

AsyncWorkflow.prototype.handle_click = function(e){

    // we're not sure who gets to be event target, we need the <a> link
    var $element;
    if (e.target.nodeName !== 'A') {
        $element = jQuery(e.target).parent('a');
    } else {
        $element = jQuery(e.target);
    }

    // compatibility with publishDialog and any other script that wants
    // to handle workflow action by itself
    if ($element.hasClass('kssIgnore') === true){ return true; }

    var url = $element.attr('href');
    jQuery("#plone-contentmenu-workflow .actionMenuHeader").html("<img src='" + context_url + "/eea-ajax-loader.gif' " +
                                 "alt='Changing state ...' title='Changing state ...' />");
    this.execute(url);
    /* debugger; */
    return false;
};

AsyncWorkflow.prototype.execute = function(url){
    var self = this;
    var ajaxhandler = context_url + '/' + this.handler;
    var jxhr = jQuery.post(ajaxhandler, data={'action_url':url}, success=function(data){
        var dom = jQuery(data);
        jQuery(".contentActions").html(data);
        var messages = jQuery(".contentActions .portalMessage").detach();
        jQuery("#kssPortalMessage").after(messages);
        jQuery(initializeMenus);    //we need to reinitialize menus
        jQuery(AsyncWorkflow.Events).trigger(AsyncWorkflow.Events.WORKFLOW_MENU_REFRESHED);
    }).fail(function(){
        self.menuHeader.html("Failure!");
    });
};

jQuery(document).ready(function ($) {
    var async = new AsyncWorkflow();
});
