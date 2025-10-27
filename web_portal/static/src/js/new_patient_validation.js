/* odoo-module */
odoo.define('web_portal.NewPatientForm', function(require){
'use strict';
    console.log("hello from ,client side");
var publictWidget = require('web.public.widget');

publictWidget.registry.NewPatientForm = publictWidget.Widget.extend({
    selector: '#register_new_patient',
    events: {
        'submit': '_onSubmitButton'
    },

    _onSubmitButton: function(event){
        var patientName = this.$("input[name='name']").val();
        console.log(`patientName ${patientName}`);
        if(!patientName){
            $("#alert_client_side").html("Please Enter Patient Name! ");
            $('#alert_client_side').show();
            event.preventDefault();
        }
    },
});
});