| name | description | type | result | applicable |
|-----------|-------------|------|--------|------------|
|Does the OP contain iss set to the its identifier on redirect in a successful authentication|In order to check if the OP correctly handles a successful authentication request, a correct request is sent by a client and the behavior of the OP is analyzed. In particular, the client must be redirected to its redirect_uri and the redirect must have 'iss' as query parameter set to the OP's identifier|passive|false|true|
