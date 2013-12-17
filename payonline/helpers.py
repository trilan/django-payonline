class DataProxy(object):

    aliases = {
        'datetime': 'DateTime',
        'transaction_id': 'TransactionID',
        'order': 'OrderId',
        'amount': 'Amount',
        'currency': 'Currency',
        'provider': 'Provider',
        'order_id': 'OrderId',
        'card_holder': 'CardHolder',
        'cart_number': 'CardNumber',
        'country': 'Country',
        'city': 'City',
        'address': 'Address',
        'Phone': 'phone',
        'wm_trans_id': 'WmTransId',
        'wm_inv_id': 'WmInvId',
        'wm_id': 'WmId',
        'wm_purse': 'WmPurse',
        'ip_address': 'IpAddress',
        'ip_country': 'IpCountry',
        'bin_country': 'BinCountry',
    }

    def __init__(self, data):
        self.data = data

    def __getitem__(self, name):
        if name in self.aliases:
            name = self.aliases[name]
        return self.data[name]

    def get(self, name, default=None):
        if name in self.aliases:
            name = self.aliases[name]
        return self.data.get(name, default)
