odoo.define("wb_pos.WBSampleButton", function(require){
"use strict";
    const PosComponent = require("point_of_sale.PosComponent");
    const ProductScreen = require("point_of_sale.ProductScreen");
    const Registries = require("point_of_sale.Registries");
    const { useListener } = require("@web/core/utils/hooks");

    class WBSampleButton extends PosComponent{
        setup(){
            super.setup();
            useListener('click', this.we_sample_button_click);
        }

        async we_sample_button_click(){

//            this.showPopup("ErrorPopup", {
//                title: "Error Message",
//               body: "This is a screen simple error message.. ",
//            });
//            const { confirmed } = await this.showPopup("ConfirmPopup", {
//                title: "Confirm",
//                body: "Are you sure want to confirm !",
//            });
//            console.log("confirmation ===>", confirmed)
             const { confirmed, payload: selectedOption } = await this.showPopup("SelectionPopup", {
                title: "Select your answer !?",
                list: [ {"id":0,"label": "Yes","item": "yes"},
                        {"id":1,"label": "No","item": "no"},
                        {"id":2,"label": "Not sure","item": "not_sure"},]
             });
             console.log("confirmed ==>", confirmed);
             console.log("SelectedOption +++>", selectedOption);
        };
    }

    WBSampleButton.template = "WBSampleButton";
    ProductScreen.addControlButton({
        component: WBSampleButton,
        position: ["before", "OrderlineCustomerNoteButton"],
    });

    Registries.Component.add(WBSampleButton);

    return WBSampleButton;
});