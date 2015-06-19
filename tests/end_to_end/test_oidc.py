"""
Performs a request via the client with OpenID Connect enabled,
with a local OP server.
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import server_test as server_test
import client
import server

import requests
from lxml import html
from urlparse import urlparse


def get_client_key(server_url):
    """
    This function automatically performs the steps that the user would usually
    perform manually in order to obtain a token.
    """
    session = requests.session()
    # Load the login page (this request includes the redirect to the OP)
    login_page = session.get("{}/_login".format(server_url), verify=False)
    # Extract the state data from the login form
    login_tree = html.fromstring(login_page.text)
    input_tags = login_tree.iterdescendants('input')
    state = (s for s in input_tags if s.name == 'state').next().value
    # Submit the form data to the OP for verification (if verification is
    # successful, the request will redirect to a page with the key)
    data = {
        'username': 'diana',
        'password': 'krall',
        'state': state
    }
    op_location = urlparse(login_page.url).netloc
    next_url = 'https://{}/user_pass/verify'.format(op_location)
    key_page = session.post(next_url, data)
    # Extract the key from the page
    key_tree = html.fromstring(key_page.text)
    token_marker = 'Session Token '  # the token always appears after this text
    token_tag = (s for s in key_tree.iterdescendants()
                 if s.text_content().startswith(token_marker)).next()
    return token_tag.text_content()[len(token_marker):]


class TestOidc(server_test.ServerTest):

    def otherSetup(self):
        self.opServer = server.OidcOpServerForTesting()
        self.opServer.start()

    def otherTeardown(self):
        self.opServer.shutdown()

    def getServer(self):
        return server.Ga4ghServerForTesting(use_oidc=True)

    def testOidc(self):
        server_url = self.server.getUrl()
        key = get_client_key(server_url)
        c = client.ClientForTesting(server_url, flags="--key {}".format(key))
        self.runVariantSetRequest(c)
        c.cleanup()

    def runVariantSetRequest(self, c):
        self.runClientCmd(c, "variants-search -s0 -e2")
