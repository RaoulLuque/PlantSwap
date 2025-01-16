# Deploying the Application to the Cloud

As a cloud provider, we chose [fly.io](https://fly.io), a relatively small player that initially offered a great [free-tier](https://fly.io/docs/about/pricing/#discontinued-plans). Unfortunately, this tier is no longer available to new accounts. However, since I had previously used fly.io for a [Connect Four bot](https://connect-rust.fly.dev/) written in Rust, my account remains on the old free-tier.

The decision to use fly.io was not solely based on monetary considerations. Deployment with fly.io is straightforward and seamless, as demonstrated below. Additionally, it offers excellent Docker support and straightforward continuous deployment integration with GitHub Actions, as described in [Continuous Deployment Using GitHub Actions](continuous_deployment_using_github_actions.md). However, fly.io’s relatively small ecosystem does come with some limitations, such as fewer features and potential risks related to security or the possibility of the service being discontinued as we have discussed in class as well.

Despite these drawbacks, fly.io proved to be an excellent choice for this project due to the free-tier benefits for hosting both the application and a PostgreSQL database.

## Evaluation Criteria

The criteria used to choose the platform-as-a-service (PaaS) were cost efficiency, ease of deployment, scalability, and reliability and security. Fly.io was evaluated against other services such as Heroku and AWS Elastic Beanstalk. Heroku, while offering a developer-friendly experience, has a free-tier that was recently restricted, similar to fly.io. Therefore, Heroku’s pricing is higher compared to fly.io, making it less appealing for this project’s budget constraints. AWS Elastic Beanstalk offers a more feature-rich environment with greater scalability and ecosystem support, but the complexity of setup and management, combined with the lack of a meaningful free-tier, made it less suitable for this project’s requirements.

Fly.io’s integration with Docker and its simplicity in setup provided a significant advantage over both Heroku and AWS Elastic Beanstalk. While Heroku also supports Docker, its reliance on buildpacks can sometimes introduce limitations. AWS Elastic Beanstalk’s Docker support, though comprehensive, requires more manual configuration, which could increase deployment time and effort. Fly.io strikes a balance between ease of use and functionality for containerized applications, which was a key deciding factor. Of course, also the existing experience and good results using fly.io proved to be a deciding factor in chosing a cloud provider.

Regarding why we even chose a IaaS (as which fly.io technically counts), the setup is really easy. We just containerize our application and know it will exactly the same as on our local machine (running docker engine). Furthermore, we are not committed to a specific platform, language or framework, since we can simply change our entire backend if necessary and the container will wrap that application so that the users would not even notice a change.

## Setting up fly

[Fly.io](fly.io) has an own CLI tool which can be used to deploy applications. The documentation can be found [here](https://fly.io/docs/flyctl/) and the installation is as easy as running
```commandline
curl -L https://fly.io/install.sh | sh
```
on linux. After having then added the binary to the PATH variable of your shell, you are ready to go. 

Since I already had an existing account I could login into the CLI tool using
`fly auth login`. Similar to how they handle other configuration and login processes, this opens a browser where one can simply log in and this login is transferred to the CLI tool.

## Deploying the application

Fly.io uses fly.toml files to configure the deployment of an application. As a Rust and therefore Cargo user, this is of course known terrain. I simply reused the configuration from my last app which made sure I would comply with all the constraints on the free tier. The configuration file can be found in the repository [here](../../fly.toml) (this is usually not recommended, we need it for the continuous deployment using GitHub Actions however) and looks as follows:

```toml
app = 'plantswap'
primary_region = 'ams'

[build]
dockerfile = 'Dockerfile'

[http_service]
internal_port = 8000
force_https = true
auto_stop_machines = 'stop'
auto_start_machines = true
min_machines_running = 0
processes = ['app']

[[vm]]
cpu_kind = "shared"
cpus = 1
memory_mb = 256
```

First off, we set the metadata information, that is, the application name and the primary region the app will be hosted in which is europe in this case. Fly.io does not have that many servers, especially in europe, therefore ams (amsterdam) was the best choice. After that in the `[build]` section we specify the dockerfile we want to use as the basis for our application. We simply use the Dockerfile from this repository. One could also provide a link to an image registry or something similar, but we want to always use the most recent version of the app which is why we will be (re)building the image on every deployment of the app. The next section contains the information for the http service. That is, the exposed port and some information on the machines used. This is interesting because fly has great auto scaling capabilities. That is, if no request has been made for some times, all machines will shut down because we have set the number of minimum machines to 0. That has the implication of the startup process taking longer if there is a request after a long time were there has not been a request, which is not a problem for us however.

At last, we specify the type of vm we want for our service. We use a shared cpu with a memory of 256mb, which is relatively little but sufficient for our purposes and what is included in the legacy free tier.

Having created our fly.toml file, we are ready to deploy the application. As explained in the [documentation](https://fly.io/docs/launch/deploy/) this can be done using the `fly deploy` command. However, if the app is not registered yet, this will yield an error as can be seen in the following.

```commandline
(plantswap) *[main][../PlantSwap]$ fly deploy                        
==> Verifying app config
Validating /home/raoul/Documents/Produktivität/RWTH/Semester_7/CC/PlantSwap/fly.toml
✓ Configuration is valid
--> Verified app config
Error: Could not find App "plantswap"
```

Therefore, we first had to run the [`fly launch`](https://fly.io/docs/reference/fly-launch/) command once. Doing so, we were prompted if we wanted to use the existing fly.toml file from the current directory and whether we wanted to tweak the settings before proceeding. We said yes in order to add a postgres database to our application. We did this using the [Supabase](https://supabase.com/) provider, which has a collaboration with fly.io such that it is integrated into the services of fly.io and has a free tier allowing for one free database (which still works). The result of using the `fly launch` command can be seen in the following. 
```commandline
(plantswap) *[main][../PlantSwap]$ fly launch   
An existing fly.toml file was found for app plantswap
? Would you like to copy its configuration to the new app? Yes
Using build strategies '[the "Dockerfile" dockerfile]'. Remove [build] from fly.toml to force a rescan
Creating app in /home/raoul/Documents/Produktivität/RWTH/Semester_7/CC/PlantSwap
We're about to launch your app on Fly.io. Here's what you're getting:

Organization: Raoul Luqué             (fly launch defaults to the personal org)
Name:         plantswap                (from your fly.toml)
Region:       Amsterdam, Netherlands   (from your fly.toml)
App Machines: shared-cpu-1x, 256MB RAM (from your fly.toml)
Postgres:     <none>                   (not requested)
Redis:        <none>                   (not requested)
Tigris:       <none>                   (not requested)

? Do you want to tweak these settings before proceeding? Yes
Opening https://fly.io/cli/launch/hidden

Waiting for launch data... Done
Created app 'plantswap' in organization 'personal'
Admin URL: https://fly.io/apps/plantswap
Hostname: plantswap.fly.dev

To proceed, you must agree to the Supabase Terms of Service (https://supabase.com/terms) and Privacy Policy (https://supabase.com/privacy).

? Do you agree? Yes
Your Supabase database (plantswap-db) in ams is ready. See details and next steps with: https://fly.io/docs/reference/supabase/

Setting the following secrets on plantswap:
DATABASE_POOLER_URL: hidden
DATABASE_URL: hidden

? Create .dockerignore from 8 .gitignore files? Yes
Created /home/raoul/Documents/Produktivität/RWTH/Semester_7/CC/PlantSwap/.dockerignore from 8 .gitignore files.
Wrote config file fly.toml
Validating /home/raoul/Documents/Produktivität/RWTH/Semester_7/CC/PlantSwap/fly.toml
✓ Configuration is valid
==> Building image
==> Building image with Depot
--> build:  (​)
[+] Building 22.7s (13/13) FINISHED                                                           
 => [internal] load build definition from Dockerfile                                           
 => => transferring dockerfile: 1.40kB                                                        
 => [internal] load metadata for ghcr.io/astral-sh/uv:python3.12-bookworm-slim                 
 => [internal] load .dockerignore                                                             
 => => transferring context: 884B                                                             
 => [stage-0 1/8] FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim@sha256:1d87359da9ea13a3aaf7988e70fae3118c1e351b26337830b1f6fccbf9eab6d0    
 => => resolve ghcr.io/astral-sh/uv:python3.12-bookworm-slim@sha256:1d87359da9ea13a3aaf7988e70fae3118c1e351b26337830b1f6fccbf9eab6d0    
 => => sha256:184aff3eb8fbdeb25b5697c83adcfadb6deef75d7001234b86bd6ec2d6a610a4 249B / 249B    
 => => sha256:63132b2c7e872e7fedbc801585d4f7ba03447a8bcaa6e61ea022521dcebadc12 15.66MB / 15.66MB 
 => => sha256:de2a998baeb3b693572201ce82da66e97b26f2feabf01efbb4c9a952587a839d 13.65MB / 13.65MB
 => => sha256:ad5b6a1962fdac425252ec07daae642d785bd6d9c9fb9c665495ac32fb6c7346 3.32MB / 3.32MB
 => => sha256:fd674058ff8f8cfa7fb8a20c006fc0128541cbbad7f7f7f28df570d08f9e4d92 28.23MB / 28.23MB 
 => => extracting sha256:fd674058ff8f8cfa7fb8a20c006fc0128541cbbad7f7f7f28df570d08f9e4d92     
 => => extracting sha256:ad5b6a1962fdac425252ec07daae642d785bd6d9c9fb9c665495ac32fb6c7346     
 => => extracting sha256:de2a998baeb3b693572201ce82da66e97b26f2feabf01efbb4c9a952587a839d     
 => => extracting sha256:184aff3eb8fbdeb25b5697c83adcfadb6deef75d7001234b86bd6ec2d6a610a4     
 => => extracting sha256:63132b2c7e872e7fedbc801585d4f7ba03447a8bcaa6e61ea022521dcebadc12     
 => [internal] load build context                                                             
 => => transferring context: 258.02kB                                                         
 => [stage-0 2/8] WORKDIR /PlantSwap                                                          
 => [stage-0 3/8] RUN pip install poethepoet                                                  
 => [stage-0 4/8] RUN --mount=type=cache,target=/root/.cache/uv     --mount=type=bind,source=uv.lock,target=uv.lock     --mount=type=bind,source=pyproject.toml,target=pyproject.toml     uv sync --frozen --no-inst  1.7s
 => [stage-0 5/8] ADD pyproject.toml LICENSE log_config.json README.md uv.lock ./             
 => [stage-0 6/8] ADD app app                                                                 
 => [stage-0 7/8] RUN --mount=type=cache,target=/root/.cache/uv     uv sync --frozen --no-dev  
 => [stage-0 8/8] RUN mkdir reports                                                           
 => exporting to image                                                                        
 => => exporting layers                                                                       
 => => exporting manifest sha256:61a8299b7c4517ac6553d9354b32295cfaf8f8084190007a66931b2fad54429d                     
 => => exporting config sha256:d81842238178cb28db43344c0052be19ed6f31d1abcd4064daa909ee4f8535b6                     
 => => pushing layers for registry.fly.io/plantswap:deployment-01JHKBE7DFWT7E692V6FYX9GG7@sha256:61a8299b7c4517ac6553d9354b32295cfaf8f8084190007a66931b2fad54429d                           
 => => pushing layer sha256:20a882825dc0f1396f4402f73f57e11d10a662cf977fd890b1027a07c8682345  
 => => pushing layer sha256:cd5aa750824d2c4122dd156907d903d29398a08f329b273e1452e2316042ffab  
 => => pushing layer sha256:bd9ddc54bea929a22b334e73e026d4136e5b73f5cc29942896c72e4ece69b13d  
 => => pushing layer sha256:736f2b16ffb1a6952a5a25c4d1c946f789e47b5276356e0d52f8d91ceaf4ed75  
 => => pushing layer sha256:e1c600fbf54fb6220989b838bcf4acdf88b9224fced7b4f6bdf4fd75caca4f71  
 => => pushing layer sha256:2367ef07c00768f1fe71396351fe9b1fe692b72881e715888c9419b7f8b39ae4  
 => => pushing layer sha256:184aff3eb8fbdeb25b5697c83adcfadb6deef75d7001234b86bd6ec2d6a610a4  
 => => pushing layer sha256:f748a4803666b9f6af424cdeedbb2231ee2b0e5309400a95a3338b11dd081463  
 => => pushing layer sha256:63132b2c7e872e7fedbc801585d4f7ba03447a8bcaa6e61ea022521dcebadc12  
 => => pushing layer sha256:fd674058ff8f8cfa7fb8a20c006fc0128541cbbad7f7f7f28df570d08f9e4d92  
 => => pushing layer sha256:de2a998baeb3b693572201ce82da66e97b26f2feabf01efbb4c9a952587a839d  
 => => pushing layer sha256:d81842238178cb28db43344c0052be19ed6f31d1abcd4064daa909ee4f8535b6  
 => => pushing layer sha256:ad5b6a1962fdac425252ec07daae642d785bd6d9c9fb9c665495ac32fb6c7346  
 => => pushing manifest for hidden                        
--> Build Summary:  (​)
--> Building image done
image: hidden
image size: 100 MB

Watch your deployment at https://fly.io/apps/plantswap/monitoring

Provisioning ips for plantswap
  Dedicated ipv6: hidden
  Shared ipv4: hidden
  Add a dedicated ipv4 with: fly ips allocate-v4

This deployment will:
 * create 2 "app" machines

No machines in group app, launching a new machine

WARNING The app is not listening on the expected address and will not be reachable by fly-proxy.
You can fix this by configuring your app to listen on the following addresses:
  - 0.0.0.0:8080
Found these processes inside the machine with open listening sockets:
  PROCESS        | ADDRESSES                            
-----------------*--------------------------------------
  /.fly/hallpass | hidden

Creating a second machine to increase service availability
Finished launching new machines
-------
NOTE: The machines for [app] have services with 'auto_stop_machines = "stop"' that will be stopped when idling

-------
Checking DNS configuration for plantswap.fly.dev

Visit your newly deployed app at https://plantswap.fly.dev/
```

As can be, we built the image of the dockerfile and pushed it to the registry of fly.io. Furthermore, after launching the application, at the end of the logs, the app was not listening on the expected address. This was due to the fact that I had provided the wrong port in the fly.toml

However, there was another problem.

## Connecting to the database

Somehow, we had to make sure that the fly hosted application would connect to the database hosted by supabase. This could be done with the provided IPv6/IPv4 addresses of the database. However, we would have to somehow pass these arguments to the application. For this, fly has a [secrets feature](https://fly.io/docs/apps/secrets/) which securely stores secrets for a fly application and automatically injects these as environment variables into the containers when deploying.

Using this feature and the `fly secrets set` CLI, we were able to set the postgres connection details and the details of the first superuser for the application/database.

Having fixed these issues, the result of running `fly deploy` now looked like this (truncated)

```commandline
--- snipped ---
image: hidden
image size: 100 MB

Watch your deployment at https://fly.io/apps/plantswap/monitoring

-------
Updating existing machines in 'plantswap' with rolling strategy

-------
 ✔ Cleared lease for hidden
-------
Checking DNS configuration for plantswap.fly.dev

Visit your newly deployed app at https://plantswap.fly.dev/
```

That is, our application is now reachable at [https://plantswap.fly.dev/](https://plantswap.fly.dev/) or rather at [ttps://plantswap.fly.dev/docs](ttps://plantswap.fly.dev/docs) (for interactive openAPI documentation of the application) 🎉.

Using the dashboard provided by fly.io we can now see the status of our application, check the number of machines running the application and the data usage and other metrics/statistics as well as the logs of the individual machines. The following screenshot shows the dashboard.

![dashboard.png](dashboard.png)

At last, we want to note that the current setup of the app with 1 machine and 1 database instance is of course not the best for real production. Instead it is a proof-of-concept and was chosen mostly due to its cost effectiveness. However, fly.io also offers great [scalability options](https://fly.io/docs/launch/scale-count/), where one can automatically scale the number of machines up and down depending on the demand. This of course integrates great with our setup, since we can have multiple instances of the app running in parallel and sending separate requests to the database if necessary. At some point, the database will become a bottleneck of course, but for a start this could be a viable setup (the database can also be scaled using [supabase](https://supabase.com/)).

## Testing the application

As discused in previous milestones, one can reach an interactive API documentation of the app at [https://plantswap.fly.dev/docs](https://plantswap.fly.dev/docs). Using this, we were able to create an account, log-in using OAuth2 and then successfully create a plant ad. This can be seen in the following screenshot:

![plant_ad.png](plant_ad.png)

Regarding the main functionality, we were able to create another account, to create another plant add in order to then use the id of the previously created plant (which anyone could retrieve via the `/Plants/` endpoint as well) to create a trade request. Peak PlantSwap 🌟🪴

![trade_request.png](trade_request.png)