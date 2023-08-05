import json
import os
import webbrowser
from urllib.parse import urlencode

import aiohttp
from hubble.utils.api_utils import get_base_url
from hubble.utils.config import config
from requests.compat import urljoin


class Auth:
    @staticmethod
    def get_auth_token():
        """Get user auth token.

        .. note:: We first check `JINA_AUTH_TOKEN` environment variable.
          if token is not None, use env token. Otherwise, we get token from config.
        """
        token_from_env = os.environ.get('JINA_AUTH_TOKEN')
        return token_from_env if token_from_env else config.get('auth_token')

    @staticmethod
    async def login(**kwargs):
        api_host = get_base_url()
        auth_info = None
        async with aiohttp.ClientSession(trust_env=True) as session:
            kwargs['provider'] = kwargs.get('provider', 'jina-login')

            async with session.get(
                url=urljoin(
                    api_host,
                    'user.identity.proxiedAuthorize?{}'.format(urlencode(kwargs)),
                ),
            ) as response:
                async for line in response.content:
                    item = json.loads(line.decode('utf-8'))
                    event = item['event']
                    if event == 'redirect':
                        print('Open the following link in your browser:')
                        print(item['data']['redirectTo'])
                        webbrowser.open(item['data']['redirectTo'])
                    elif event == 'authorize':
                        if item['data']['code'] and item['data']['state']:
                            auth_info = item['data']
                        else:
                            print(
                                '🚨 Authentication failed: {}'.format(
                                    item['data']['error_description']
                                )
                            )
                    elif event == 'error':
                        print('🚨 Authentication failed: {}'.format(item['data']))
                    else:
                        print('🚨 Unknown event: {}'.format(event))

        if auth_info is None:
            return

        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.post(
                url=urljoin(api_host, 'user.identity.grant.auto'),
                data=auth_info,
            ) as response:
                response.raise_for_status()
                json_response = await response.json()
                token = json_response['data']['token']

                config.set('auth_token', token)
                print('🔐 Successfully login to Jina Ecosystem!')

    @staticmethod
    async def logout():
        api_host = get_base_url()

        async with aiohttp.ClientSession(trust_env=True) as session:
            session.headers.update({'Authorization': f'token {Auth.get_auth_token()}'})

            async with session.post(
                url=urljoin(api_host, 'user.session.dismiss')
            ) as response:
                json_response = await response.json()
                if json_response['code'] == 401:
                    print('🔓 You are not logged in. No need to logout.')
                elif json_response['code'] == 200:
                    print('🔓 You have successfully logged out.')
                    config.delete('auth_token')
                else:
                    print(f'🚨 Failed to logout. {json_response["message"]}')
