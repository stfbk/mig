| name | description | type | result | applicable |
|-----------|-------------|------|--------|------------|
|Does the AS correctly contain the code parameter on redirect in a successful authentication|In order to check if the AS correctly handles a successful authentication request, a correct request is sent by a client and the behavior of the OP is analyzed. In particular, the client must be redirected to its redirect_uri and the redirect must have 'code' as query parameter|passive|true|true|
