class SubscriptionManager(object):
    def __init__(self, api):
        self._api = api
        self._subscriptions = {}
        self._subscription_count = 0

    def add_subscription(self, settings={}, callback=None):
        settings['subscriptionId'] = self._subscription_count

        self._subscription_count += 1

        subscription = {
            'settings': settings,
            'callback': callback,
            'active': False
        }

        return self._request_subscription(subscription)

    def remove_subscription(self, id):
        self._api.request('unsubscribe', {'subscriptionId': id})

    def run(self, id, changes, device):
        try:
            self._subscriptions[id]['callback'](changes, device);

        except:
            raise Exception('Subscription not found')

    def request_subscriptions(self):
        for id in self._subscriptions:
            subscription = self._subscriptions[id]

            if not sub['active']:
                self._request_subscription(subscription)

    def invalidate_subscriptions(self):
        for id in self._subscriptions:
            self._subscriptions[id]['active'] = False

    def remove_subscriptions(self):
        for subscription in self._subscriptions:
            self.remove_subscription(subscription)

            self._subscriptions = {}

    def _request_subscription(self, subscription):
        self._api.request('subscribe', subscription['settings'])

        subscription['active'] = True
        subscription_id = subscription['settings']['subscriptionId']

        self._subscriptions[subscription_id] = subscription

        return subscription_id
