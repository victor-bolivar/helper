# helper

## How to use it?

Within the root folder of the project you should have:

1. A `.json` with the specification of your deployment. For example:

    ```json
    {
        "type": "openstack",
        "name": "infra-1",
        "nodes": [
            {
                "name": "node",
                "count": 2,
                "imageId": "11b2c9d4-bcd0-4ac1-90cf-1346b1bff636",
                "flavorId": "8dab5489-9db9-4873-9228-63f001e984fc",
                "securityGroups": ["default"],
                "keypair": "victor",
                "roles": ["etcd", "control", "worker"],
                "networkIds": ["55779fbd-d0b6-4cb6-a206-5323256abeab"]
            }
        ]
    }
    ```

2. An `.sh` with the environment variables required for the authentication process.
For example, for Openstack, you should use use the `openrc.sh`

3. Run `python3 app.py`