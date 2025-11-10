odoo.define('wb_pos.pos_restrict_payment', function (require) {
    'use strict';

    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    const ErrorPopup = require('point_of_sale.ErrorPopup');
    const rpc = require('web.rpc')

    const RestrictPaymentButton = (ProductScreen) => class extends ProductScreen {

        async _getFreeProductQty(productId){
            const locationId = this.env.pos.default_location_src_id;
            console.log('Location ',locationId);
            const quants = await rpc.query({
                model: 'stock.quant',
                method: 'search_read',
                domain: [['product_id', '=', productId], ['location_id', '=', locationId]],
                fields: ['id', 'location_id','product_id','quantity', 'reserved_quantity'],
            });
            console.log('quants',quants)
            const freeQty = quants.reduce((sum, q) => sum + (q.quantity - q.reserved_quantity), 0);
            return freeQty;
        }


        async _onClickPay() {
            const order = this.env.pos.get_order();
            for (const line of order.get_orderlines()) {
                const product = line.get_product();
                const qtyOrdered = line.get_quantity();
                const qtyAvailable = await this._getFreeProductQty(product.id) || 0;

                console.log(`product => ${product}, order => ${qtyOrdered}, available ${qtyAvailable}`)

                if (this.env.pos.no_negative_sale && qtyOrdered > qtyAvailable) {
                    await this.showPopup('ErrorPopup', {
                        title: this.env._t('Insufficient Stock'),
                        body: this.env._t(
                            `Product "${product.display_name}" has only ${qtyAvailable} units available, but you ordered ${qtyOrdered}.`
                        ),
                    });
                    return; // stop payment flow
                }
            }

            // continue normal payment flow
            await super._onClickPay();
        }
    };

    Registries.Component.extend(ProductScreen, RestrictPaymentButton);

    return RestrictPaymentButton;
});
