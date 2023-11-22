# spid-cie-oidc testplan

## Adding support for your RP

### Integration

#### Step 0: Understanding the environment

All the spid-cie-oidc implementations in this repo are tested by means of [spid-cie-oidc-django](https://github.com/italia/spid-cie-oidc-django) which features an OP, TA, and RP that will be used as testbeds to execute the tests. Your RP will have to be integrated into this environment, and the original RP can be optionally removed.

The spid-cie-oidc-django environment is run by means of a docker-compose yaml, which starts all the containers. You will need to add your RP to the compose file and set it to use a proxy that is used for testing. More details will be provided later in this guide.

#### Step 1: Create folder structure

To add support for an RP, you have to adhere to the folder structure of the repo as described [here](../README.md#folder-structure). To start, you can use the [template folder](./implementations/template/) that we created with the basic folders and files needed.

> Tip: if you plan to do a pull request to this repo with support for your RP, please add to the .gitignore all the unnecessary files and, if possible, downlaod at-the-moment the sources needed to build your Docker image in the build_and_run.sh script instead of pushing them to the repo. Otherwise, you could use a submodule if your sources are in a git repo.

#### Step 2: Add your RP container to the compose file

If you have a Docker image hosted on a Docker registry, just use it inside the [docker-compose.yml](./implementations/template/docker-compose.yml) file. Otherwise, if you need to build an image locally, please provide the steps to do that in the [build_and_run.sh](./implementations/template/build_and_run.sh) script, and use the builded container inside the [docker-compose.yml](./implementations/template/docker-compose.yml) file.

Either way you choose, you now need to redirect all the traffic in your container to the proxy hosted on port 8080 on the container burpsuite. To do this, there are commands available on the template's compose that install redsocks and forward the packets to/from the default OP and TA to the proxy.

> Note: A debian base image is suggested in order for the default proxy forwarding to work. You can use other base images, but you will need to redirect all the outgoing traffic to localhost:8002 and localhost:8000 (OP and TA) to burpsuite:8080, which is the proxy we are using. If the proxy forwarding doesn't work, some tests will not be executed.

> Warning: The port exposed by your RP can be any, but avoid 8080, 8001, 8000, and 8002. By default, it is 8005.

#### Step 3: RP on-boarding

Do the on-boarding process

- generate your RP jwks
- register the RP on the [TA](http://trust-anchor.org:8000/admin/spid_cie_oidc_authority/federationdescendant/add)
- set "name", "sub" and "jwks" with the values shown in the previous step
- set isActive to true
- create new profile on the [TA](http://trust-anchor.org:8000/admin/spid_cie_oidc_authority/federationentityassignedprofile/add/)
- set this RP as Descendant
- set "SPID Public SP" as Profile
- set the Federation Entity as Issuer
- after the creation, review the profiles and copy the trust marks into your RP
- complete RP on-boarding
- go to `your-rp:port/.well-known/openid-federation?format=json` endpoint and verify trust_marks are exposed

> steps taken from [spid-cie-oidc-java](https://github.com/italia/spid-cie-oidc-java/blob/main/examples/relying-party-spring-boot/README.md)

Your RP should now be working with the spid-cie-oidc-django OP. Try a SSO login from your RP to the OP with the credentials "user" and "oidcuser".

### Adapt tests to your RP

#### Step 4: Create a custom session

You should write a session for your RP. The session is a list of actions that the browser will need to do to complete authentication on your RP. This is needed to trigger all the messages that will be intercepted by the proxy.

You can start from an existing session, such as [s_CIE](implementations/spid-cie-oidc-django/input/mig-t/sessions/s_CIE) of spid-cie-oidc-django, and change the part of your RP.

> if you need more details on how to write a session, check [this section](https://github.com/stfbk/mig-t/blob/main/doc/language.md#session-track-user-actions) of the mig-t documentation

> if you plan to push your RP to the mig repo, please put the session inside the `input/mig-t/sessions/` folder.

#### Step 5: Edit message definition

For the tests to work, you will need to edit the [msg_def.json](./implementations/template/config/mig-t/msg_def.json) file and edit it according to your RP. This step will be automated in future releases, but it is now needed for the tests to work properly. In the template file, you will find comments "// TODO" where you need to replace **your-rp-url** and **your-rp-port** with your RP one. Following is a brief description of each one:

line 61

```
"contains": "your-rp-url:your-rp-port"
```

line 156

```
"check regex": "/fetch\\?sub=http://your-rp-url:your-rp-port" // TODO
```

> Warning: in line 156, please escape each regex-recognized symbol in your input with \\\\

line 222

```
"check regex": "/federation_fetch_endpoint\\?iss=http://your-rp-url:your-rp-port&sub=http://trust-anchor.org:8000"
```

line 244

```
"check regex": "/federation_fetch_endpoint\\?iss=http://your-rp-url:your-rp-port&sub=http://subject-aggregator.org:8004"
```

#### Step 6: Execute generate_mr.sh

You can now execute [generate_mr.sh](./implementations/template/generate_mr.sh) script, that will generate the tests inside the [tests folder](./implementations/template/input/mig-t/tests/).

If the tests are not generated, check that the folder [templates](./implementations/template/config/testplan-to-mr/templates/) is present. Otherwise, copy its content from the [spid-cie-oidc-django templates folder](./implementations/spid-cie-oidc-django/config/testplan-to-mr/templates).
<https://github.com/stfbk/mig/tree/new-rp/testplans/spid-cie-oidc/implementations/spid-cie-oidc-java>
