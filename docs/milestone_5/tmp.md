```commandline
(plantswap) *[main][../PlantSwap]$ fly deploy                        
==> Verifying app config
Validating /home/raoul/Documents/Produktivität/RWTH/Semester_7/CC/PlantSwap/fly.toml
✓ Configuration is valid
--> Verified app config
Error: Could not find App "plantswap"
(plantswap) *[main][../PlantSwap]$ fly apps list 
NAME            OWNER           STATUS          LATEST DEPLOY     
connect-rust    personal        suspended       Jan 14 2024 17:05       

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
Opening https://fly.io/cli/launch/66706e696f656775716776736c347a336f36616436677978767076347279327a ...

Waiting for launch data... Done
Created app 'plantswap' in organization 'personal'
Admin URL: https://fly.io/apps/plantswap
Hostname: plantswap.fly.dev

To proceed, you must agree to the Supabase Terms of Service (https://supabase.com/terms) and Privacy Policy (https://supabase.com/privacy).

? Do you agree? Yes
Your Supabase database (plantswap-db) in ams is ready. See details and next steps with: https://fly.io/docs/reference/supabase/

Setting the following secrets on plantswap:
DATABASE_POOLER_URL: postgres://postgres.hviraqbaeccrfoxgocyz:SGKZCDK4Z2RPwNlt@fly-0-ams.pooler.supabase.com:6543/postgres
DATABASE_URL: postgres://postgres:SGKZCDK4Z2RPwNlt@db.hviraqbaeccrfoxgocyz.supabase.co:5432/postgres?sslmode=require

? Create .dockerignore from 8 .gitignore files? Yes
Created /home/raoul/Documents/Produktivität/RWTH/Semester_7/CC/PlantSwap/.dockerignore from 8 .gitignore files.
Wrote config file fly.toml
Validating /home/raoul/Documents/Produktivität/RWTH/Semester_7/CC/PlantSwap/fly.toml
✓ Configuration is valid
==> Building image
==> Building image with Depot
--> build:  (​)
[+] Building 22.7s (13/13) FINISHED                                                                                                                                                                                        
 => [internal] load build definition from Dockerfile                                                                                                                                                                  0.1s
 => => transferring dockerfile: 1.40kB                                                                                                                                                                                0.1s
 => [internal] load metadata for ghcr.io/astral-sh/uv:python3.12-bookworm-slim                                                                                                                                        1.2s
 => [internal] load .dockerignore                                                                                                                                                                                     0.1s
 => => transferring context: 884B                                                                                                                                                                                     0.1s
 => [stage-0 1/8] FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim@sha256:1d87359da9ea13a3aaf7988e70fae3118c1e351b26337830b1f6fccbf9eab6d0                                                                          1.7s
 => => resolve ghcr.io/astral-sh/uv:python3.12-bookworm-slim@sha256:1d87359da9ea13a3aaf7988e70fae3118c1e351b26337830b1f6fccbf9eab6d0                                                                                  0.0s
 => => sha256:184aff3eb8fbdeb25b5697c83adcfadb6deef75d7001234b86bd6ec2d6a610a4 249B / 249B                                                                                                                            0.1s
 => => sha256:63132b2c7e872e7fedbc801585d4f7ba03447a8bcaa6e61ea022521dcebadc12 15.66MB / 15.66MB                                                                                                                      0.4s
 => => sha256:de2a998baeb3b693572201ce82da66e97b26f2feabf01efbb4c9a952587a839d 13.65MB / 13.65MB                                                                                                                      0.2s
 => => sha256:ad5b6a1962fdac425252ec07daae642d785bd6d9c9fb9c665495ac32fb6c7346 3.32MB / 3.32MB                                                                                                                        0.2s
 => => sha256:fd674058ff8f8cfa7fb8a20c006fc0128541cbbad7f7f7f28df570d08f9e4d92 28.23MB / 28.23MB                                                                                                                      0.4s
 => => extracting sha256:fd674058ff8f8cfa7fb8a20c006fc0128541cbbad7f7f7f28df570d08f9e4d92                                                                                                                             0.7s
 => => extracting sha256:ad5b6a1962fdac425252ec07daae642d785bd6d9c9fb9c665495ac32fb6c7346                                                                                                                             0.1s
 => => extracting sha256:de2a998baeb3b693572201ce82da66e97b26f2feabf01efbb4c9a952587a839d                                                                                                                             0.3s
 => => extracting sha256:184aff3eb8fbdeb25b5697c83adcfadb6deef75d7001234b86bd6ec2d6a610a4                                                                                                                             0.0s
 => => extracting sha256:63132b2c7e872e7fedbc801585d4f7ba03447a8bcaa6e61ea022521dcebadc12                                                                                                                             0.2s
 => [internal] load build context                                                                                                                                                                                     0.2s
 => => transferring context: 258.02kB                                                                                                                                                                                 0.2s
 => [stage-0 2/8] WORKDIR /PlantSwap                                                                                                                                                                                  0.2s
 => [stage-0 3/8] RUN pip install poethepoet                                                                                                                                                                          2.5s
 => [stage-0 4/8] RUN --mount=type=cache,target=/root/.cache/uv     --mount=type=bind,source=uv.lock,target=uv.lock     --mount=type=bind,source=pyproject.toml,target=pyproject.toml     uv sync --frozen --no-inst  1.7s
 => [stage-0 5/8] ADD pyproject.toml LICENSE log_config.json README.md uv.lock ./                                                                                                                                     0.0s
 => [stage-0 6/8] ADD app app                                                                                                                                                                                         0.0s
 => [stage-0 7/8] RUN --mount=type=cache,target=/root/.cache/uv     uv sync --frozen --no-dev                                                                                                                         0.2s
 => [stage-0 8/8] RUN mkdir reports                                                                                                                                                                                   0.1s
 => exporting to image                                                                                                                                                                                               14.6s
 => => exporting layers                                                                                                                                                                                               0.4s
 => => exporting manifest sha256:61a8299b7c4517ac6553d9354b32295cfaf8f8084190007a66931b2fad54429d                                                                                                                     0.0s
 => => exporting config sha256:d81842238178cb28db43344c0052be19ed6f31d1abcd4064daa909ee4f8535b6                                                                                                                       0.0s
 => => pushing layers for registry.fly.io/plantswap:deployment-01JHKBE7DFWT7E692V6FYX9GG7@sha256:61a8299b7c4517ac6553d9354b32295cfaf8f8084190007a66931b2fad54429d                                                    11.1s
 => => pushing layer sha256:20a882825dc0f1396f4402f73f57e11d10a662cf977fd890b1027a07c8682345                                                                                                                          9.3s
 => => pushing layer sha256:cd5aa750824d2c4122dd156907d903d29398a08f329b273e1452e2316042ffab                                                                                                                         10.3s
 => => pushing layer sha256:bd9ddc54bea929a22b334e73e026d4136e5b73f5cc29942896c72e4ece69b13d                                                                                                                          7.1s
 => => pushing layer sha256:736f2b16ffb1a6952a5a25c4d1c946f789e47b5276356e0d52f8d91ceaf4ed75                                                                                                                         11.1s
 => => pushing layer sha256:e1c600fbf54fb6220989b838bcf4acdf88b9224fced7b4f6bdf4fd75caca4f71                                                                                                                          8.1s
 => => pushing layer sha256:2367ef07c00768f1fe71396351fe9b1fe692b72881e715888c9419b7f8b39ae4                                                                                                                         10.2s
 => => pushing layer sha256:184aff3eb8fbdeb25b5697c83adcfadb6deef75d7001234b86bd6ec2d6a610a4                                                                                                                          7.2s
 => => pushing layer sha256:f748a4803666b9f6af424cdeedbb2231ee2b0e5309400a95a3338b11dd081463                                                                                                                          9.9s
 => => pushing layer sha256:63132b2c7e872e7fedbc801585d4f7ba03447a8bcaa6e61ea022521dcebadc12                                                                                                                          9.2s
 => => pushing layer sha256:fd674058ff8f8cfa7fb8a20c006fc0128541cbbad7f7f7f28df570d08f9e4d92                                                                                                                         10.4s
 => => pushing layer sha256:de2a998baeb3b693572201ce82da66e97b26f2feabf01efbb4c9a952587a839d                                                                                                                         10.5s
 => => pushing layer sha256:d81842238178cb28db43344c0052be19ed6f31d1abcd4064daa909ee4f8535b6                                                                                                                          8.0s
 => => pushing layer sha256:ad5b6a1962fdac425252ec07daae642d785bd6d9c9fb9c665495ac32fb6c7346                                                                                                                          8.3s
 => => pushing manifest for registry.fly.io/plantswap:deployment-01JHKBE7DFWT7E692V6FYX9GG7@sha256:61a8299b7c4517ac6553d9354b32295cfaf8f8084190007a66931b2fad54429d                                                   3.1s
--> Build Summary:  (​)
--> Building image done
image: registry.fly.io/plantswap:deployment-01JHKBE7DFWT7E692V6FYX9GG7
image size: 100 MB

Watch your deployment at https://fly.io/apps/plantswap/monitoring

Provisioning ips for plantswap
  Dedicated ipv6: 2a09:8280:1::5f:5b58:0
  Shared ipv4: 66.241.125.252
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
  /.fly/hallpass | [fdaa:4:ab70:a7b:41:8636:7234:2]:22  

Creating a second machine to increase service availability
Finished launching new machines
-------
NOTE: The machines for [app] have services with 'auto_stop_machines = "stop"' that will be stopped when idling

-------
Checking DNS configuration for plantswap.fly.dev

Visit your newly deployed app at https://plantswap.fly.dev/

```

Having 
