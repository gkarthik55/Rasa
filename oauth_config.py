class CSOAuthConfiguration:
    def __init__(self, endpoint, client_id, client_secret, scope, grant_type, cache_name):
        self.endpoint = endpoint
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.grant_type = grant_type
        self.cache_name = cache_name

# UAT Configuration
oauth_config = CSOAuthConfiguration(
    endpoint="https://idcs-25070016ce0c4eb8b6eea18f07fe170d.identity.oraclecloud.com",
    client_id="e1d8450475c942f78a75d272d98a46b7",
    client_secret="4736c252-9902-4b58-8044-80477e889d97",
    scope="cs.dev.rest.public",
    grant_type="client_credentials",
    cache_name="cs_oauth_token"
)