function ArchiveDialog(){
    this.install()
}

ArchiveDialog.prototype.install = function(){
    var $transition = jQuery("#workflow-transition-archive_content");
    $transition.addClass('kssIgnore').click(this.onclick());
};

ArchiveDialog.prototype.onclick = function(e){
    var self = this;
    if (typeof(e) === "undefined") {
        return function(e){
            self.open_dialog();
            return false;
        };
    }
};

ArchiveDialog.prototype.open_dialog = function(){
    var w = new ArchiveDialog.Window();
    w.open();
};

ArchiveDialog.Window = function(){
    var $target = jQuery("#archive-dialog-target");
    if ($target.length === 0){
        $target = jQuery("<div>").appendTo("body").attr('id', 'archive-dialog-target');
    }
    this.target = $target;
};

ArchiveDialog.Window.prototype.open = function(){
    var self = this;
    self.dialog = jQuery(this.target).dialog({
            title:"Expire/Archive content",
            dialogClass:'archiveDialog',
            modal:true,
            resizable:true,
            width:600,
            height:400,
            open:function(ui){self._open(ui);},
            buttons:{
                    'Ok':function(e){self.handle_ok(e);},
                    'Cancel':function(e){self.handle_cancel(e);}
                    }
            }
    );
};

ArchiveDialog.Window.prototype.handle_cancel = function(e){
    this.dialog.dialog("close");
};

ArchiveDialog.Window.prototype.handle_ok = function(e){
    jQuery('.notice').remove();
    var workflow_reason = jQuery("input[name='workflow_reasons_radio']:checked").val()
    var hasErrors = false;
    if (!workflow_reason){
       jQuery("#workflow_reason_label").after("<div class='notice' style='color:Black; background-color:#FFE291; " +
                    "padding:3px'>Please select reason</div>");
        hasErrors = true;
    }
    if ((workflow_reason === 'other') && (!jQuery("input[name='workflow_other_reason']").val())){
        jQuery("input[name='workflow_other_reason']").after("<div class='notice' style='color:Black; background-color:#FFE291; " +
                    "padding:3px'>Please sepecify reason</div>");
        hasErrors = true;
    }

    if (!jQuery("input[name='workflow_archive_initiator']").val()){
       jQuery("#workflow_initiator_label").after("<div class='notice' style='color:Black; background-color:#FFE291; " +
                    "padding:3px'>Please specify initiator</div>");
        hasErrors = true;
    }
    if (hasErrors){
        jQuery(".notice").effect("pulsate", {times:3}, 2000,
                    function(){jQuery('.notice').remove();});
       return;
    }
    var $form = jQuery("form", this.target);
    $form.submit();


    this.dialog.dialog("close");
};

ArchiveDialog.Window.prototype._open = function(ui){
    var self = this;

    var base = get_base();
    var url = base + "/archive_dialog";

    jQuery(self.target).load(url, function(){

    });

};

jQuery(document).ready(function ($) {
    var ad = new ArchiveDialog();
});

