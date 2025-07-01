| name | description | type | result | applicable |
|-----------|-------------|------|--------|------------|
|Does the CLIENT ACF_Authorization response's JWT contain the 'state' parameter greater than 32 characters|The ACF_Authorization response is taken, the JWT Token in the request parameter base64url decoded and the value of the 'state' parameter must be at least 32 alphanumeric characters long. If it is not present or its length is less than 32 alphanumeric characters, then the CLIENT is not compliant with the specifications|passive|true|true|
