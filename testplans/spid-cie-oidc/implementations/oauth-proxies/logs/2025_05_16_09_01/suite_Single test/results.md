| name | description | type | result | applicable |
|-----------|-------------|------|--------|------------|
|Does the RP's Authentication Request contain the 'code_challenge' parameter|The Authentication request is taken and the presence of the 'code_challenge' parameter is checked. If it is present, than the Authentication Request is using PKCE and is compliant with the specifications, otherwise it is not compliant.|passive|true|true|
