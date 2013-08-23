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

