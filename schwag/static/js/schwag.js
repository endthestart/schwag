$(document).ready(function () {
    CustomForm.init();
    NotificationActions.init();
});

var CustomForm = {
    init: function () {
        this.submitButton = $(".addcart");
        this.customForm = $("#product-options-form");

        this.bind();
    },

    bind: function () {
        var self = this;

        self.submitButton.click(function (e) {
            e.preventDefault();
            self.customForm.submit();
        });
    }
};

var NotificationActions = {
    init: function () {
        this.bind();
    },

    bind: function () {
        var self = this;

        $('.close').click(function (e) {
            e.preventDefault();
            var closeDiv = $(e.target).closest('div');
            closeDiv.hide()
        });
    }
}

Number.prototype.formatMoney = function (c, d, t) {
    var n = this,
        c = isNaN(c = Math.abs(c)) ? 2 : c,
        d = d == undefined ? "." : d,
        t = t == undefined ? "," : t,
        s = n < 0 ? "-" : "",
        i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "",
        j = (j = i.length) > 3 ? j % 3 : 0;
    return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
};

var PriceForm = function ($el) {
    this.$el = $el;
    this.$selects = this.$el.find('.product-configuration-select');
    this.$total = this.$el.find('#price');
    this.$originalPrice = parseFloat(this.$total.text());
    this.$summaryList = this.$el.find('.summary-list');
    this.enable();
};

PriceForm.prototype.enable = function () {
    this.$selects.on('change', this.onPriceChange.bind(this));
    this.$selects.trigger('change');
};

PriceForm.prototype.onPriceChange = function (event) {
    var self = this;
    var total = this.$originalPrice;
    this.$summaryList.empty();
    this.$selects.each(function () {
        total += parseFloat($(this).find("option:selected").data('price'));
        var text = $(this).find("option:selected").text().trim();
        if (text != "None")
        {
            self.$summaryList.append('<li>' + text + '</li>');
        }

    });
    this.updateTotal(total);
};

PriceForm.prototype.updateTotal = function (amount) {
    amount = Number(amount).formatMoney(2, '.', ',')

    this.$total.text(amount);
};

new PriceForm($("#product-options-form"));
