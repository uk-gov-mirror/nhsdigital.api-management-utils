import re
from typing import List


def apigee_apps_to_product_map(apps_list: List[dict], product_filter: str = None):

    result = dict()

    not_matched = []

    for app in apps_list:

        credentials = app.get('credentials', [])

        for cred in credentials:

            api_products = cred.get('apiProducts', [])

            for product in api_products:
                api_product = product['apiproduct']
                if product_filter and not re.match(product_filter, api_product):
                    not_matched.append(api_product)
                    continue

                if api_product not in result:
                    result[api_product] = []

                result[api_product].append(
                    dict(
                        appId=app["appId"],
                        appName=app["name"],
                        developerId=app["developerId"],
                        consumerKey=cred["consumerKey"],
                        apiproduct=api_product
                     )
                )
    for product in sorted(set(not_matched)):
        print(f'did not match: {product}')
    return result


def apigee_products_to_api_map(products: List[dict], proxy_filter: str = None):

    result = dict()

    not_matched = []

    for product in products:

        proxies = product.get('proxies', [])

        for proxy in proxies:

            if proxy_filter and not re.match(proxy_filter, proxy):
                not_matched.append(proxy)
                continue

            if proxy not in result:
                result[proxy] = []

            result[proxy].append(product['name'])

    for proxy in sorted(set(not_matched)):
        print(f'did not match: {proxy}')
    return result


def apigee_remove_proxy_from_product(product: dict, proxy_to_remove):
    product["proxies"] = [
        p for p in product.get("proxies", [])
        if p != proxy_to_remove
    ]
    return product


class FilterModule:

    @staticmethod
    def filters():
        return {
            # jinja2 overrides
            'apigee_apps_to_product_map': apigee_apps_to_product_map,
            'apigee_products_to_api_map': apigee_products_to_api_map,
            'apigee_remove_proxy_from_product': apigee_remove_proxy_from_product
        }