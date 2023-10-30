# spid-cie-oidc testplan

## Adding support for your Relying Party

### Step 0: Understanding the environment

All the spid-cie-oidc implementations in this repo are tested by means of [spid-cie-oidc-django](https://github.com/italia/spid-cie-oidc-django) which features an OpenID Provider, Trust Anchor and Relying Party, that will be used as testbed to execute the tests. Your Relying Party will have to be integrated into this enviroment, and the original relying party can be optionally removed.

The spid-cie-oidc-django environment is ran by means of a docker-compose yaml, which starts all the containers. You will need to add your RP in the compose file, and set it to use a proxy which is used for the testing. More details will be provided later in this guide.

### Step 1: Create folder structure

To add support for an RP you have to adhere to the folder structure of the repo as described [here](../README.md#folder-structure). To start, you can use the [template folder](./implementations/template/) that we created with the basic folders and files needed.

> Tip: if you plan to do a pull request to this repo whith the support for your RP, please add to the .gitignore all the unnecessary files, and, if possible, downlaod at-the-moment the sources needed to build your Docker image in the build_and_run.sh script instead of pushing them to the repo. Otherwise you could use a submodule if your sources are in a git repo.  

### Step 2: Add your RP container in compose file

If you have a Docker image hosted on a Docker registry, just use it inside the [docker-compose.yml](./implementations/template/docker-compose.yml) file. Otherwise, if you need to build an image locally, please provide the steps to do that in the [build_and_run.sh](./implementations/template/build_and_run.sh) script, and use the builded container inside the [docker-compose.yml](./implementations/template/docker-compose.yml) file.  

Either way you choose, you now need to redirect all the traffic of your container to the proxy hosted on port 8080 on the container burpsuite. To do this, there are already two environment variables set on the template compose settings, this sometimes work, but depends on if your implementation is taking system-wide proxy variables in consideration.

> Note: A debian base image is suggested in order for the default proxy forwarding to work. You can use other base images, but you will need to redirect all the outgoing traffic to localhost:8002 and localhost:8000 (OP and TA) to burpsuite:8080, which is the proxy we are using. If the proxy fordwarding doesn't work, some tests will not be executed.

> Warning: The port exposed by your RP can be any but avoid 8080, 8001, 8000, 8002. By default it is 8005.

### Step 3: Rrelying Party on-boarding

Do the on-boarding process

- generate your relying party jwks
- register the relying party on the [Trust Anchor](http://trust-anchor.org:8000/admin/spid_cie_oidc_authority/federationdescendant/add)
  - set "name", "sub" and "jwks" with values shown in previous step
  - set isActive to true
- create new profile on the [Trust Anchor](http://trust-anchor.org:8000/admin/spid_cie_oidc_authority/federationentityassignedprofile/add/)
  - set this relying party as Descendant
  - set "SPID Public SP" as Profile
  - set the Federation Entity as Issuer
- after the creation review the profiles and copy the trust marks into your RP
- complete relying party on-boarding
  - go to `your-rp:port/.well-known/openid-federation?format=json` endpoint and verify trust_marks are exposed

> steps taken from [spid-cie-oidc-java](https://github.com/italia/spid-cie-oidc-java/blob/main/examples/relying-party-spring-boot/README.md)

Your RP should now be working with the spid-cie-oidc-django OP, try a SSO login from your RP to the OP with the credentials "user" "oidcuser".

### Step 4: Create custom session track

TODO: explain how to write session track and add it to input/mig-t/sessions

### Step 5: Edit message definition

For the tests to work, you will need to edit the [msg_def.json](./implementations/template/config/mig-t/msg_def.json) file, and edit it according to your RP. This step will be automated in future releases, but it is now needed for the tests to work propely. In the template file you will find comments "// TODO" where you need to replace **your-rp-url** and **your-rp-port** with your RP one. Following is a brief description of each one:

line 61

```
"contains": "your-rp-url:your-rp-port"
```

line 156

```
"check regex": "/fetch\\?sub=http://your-rp-url:your-rp-port" // TODO
```

> Warning: in line 156 please escape each regex recognized symbol in your input with \\\\

line 222

```
"check regex": "/federation_fetch_endpoint\\?iss=http://your-rp-url:your-rp-port&sub=http://trust-anchor.org:8000"
```

line 244

```
"check regex": "/federation_fetch_endpoint\\?iss=http://your-rp-url:your-rp-port&sub=http://subject-aggregator.org:8004"
```

### Step 6: Execute generate_mr.sh

You can now execute the [generate_mr.sh](./implementations/template/generate_mr.sh) script, that will generate the tests inside [tests folder](./implementations/template/input/mig-t/tests/).

If the tests are not generated, check that the folder [templates](./implementations/template/config/testplan-to-mr/templates/) is present. Otherwise, copy its content from the [spid-cie-oidc-django templates folder](./implementations/spid-cie-oidc-django/config/testplan-to-mr/templates).
