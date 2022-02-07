# oktaparty
This project seeks to remedy some of the missing features in Okta.

- Group Management
- Querying User and Group Information

## Configuration
Copy .env.example to .env and change the values.

These are the Environmental Variables if you would like to deploy to Kubernetes or otherwise.

### Okta Group Profile
In order to keep our source of truth as Okta, we will use profile attributes for Group information.

Add the following attributes to control User's ability to join, leave, or see Groups:

["allowJoin", "allowLeave", "hidden"]

<img src="https://user-images.githubusercontent.com/474463/152597822-3fee7db9-d1ab-43ef-b531-a385035e849f.png" style="width:50%">

<img src="https://user-images.githubusercontent.com/474463/152621124-c926f9a9-28c6-450d-a8e3-869573309ed6.png" style="width:50%">

### Developer Environment
Install Docker and Docker Compose then run

```docker-compose up```
