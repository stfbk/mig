| name | description | type | result | applicable |
|-----------|-------------|------|--------|------------|
|Does the OP contain the correct type of code parameter on redirect in a successful authentication|In order to check if the OP correctly handles a successful authentication request, a correct request is sent by a client and the behavior of the OP is analyzed. In particular, the client must be redirected to its redirect_uri and the redirect must have 'code' as query parameter and it must be a UUID.|passive|false|true|
