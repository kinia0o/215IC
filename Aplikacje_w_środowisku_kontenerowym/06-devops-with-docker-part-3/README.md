# DevOps with Docker (part 3)
### Kinga Wierzbicka 215IC_B2 22677

This part introduces production-ready practices such as container optimization and deployment pipelines. We'll also familiarize ourselves with other container orchestration solutions. By the end of this part you are able to:

* Critically examine the images that you pull

* Trim the container size and image build time via *multiple* methods such as multi-stage builds.

* Automatically deploy containers

Shortcut to exercises:
* [Exercises 3.1-3.4](#exercises-31-34)
* [Exercise 3.5](#exercise-35)
* [Exercise 3.6](#exercise-36)
* [Exercise 3.7](#exercise-37)
* [Exercises 3.8 - 3.10](#exercises-38---310)
* [Exercise 3.11](#exercise-311)

---

# Official Images and trust

We've focused on using Docker as a tool to solve various types of problems. Meanwhile we have decided to push some of the issues until later and completely ignored others.

The goal for this part is to look into some of the best container practices and improve our processes.

In [part 1](/part-1/section-3#exercises-15---16), we mentioned how the [Alpine Linux](https://www.alpinelinux.org/) image is much smaller than Ubuntu, but we didn't dive any reasoning why we might pick one over the other.

On top of that, we have been running the applications as [root](https://en.wikipedia.org/wiki/Superuser), i.e. the super user, which is potentially dangerous.

## Look into official images

Which version is considered to be the "official" version is up to the maintainers of [Docker Official Images](https://github.com/docker-library/official-images) to decide. The [official images repository](https://github.com/docker-library/official-images) contains a library of images considered official. They are introduced into the library by regular pull request processes. The extended process for verifying an image is described in the repository README.

Many of the most well-known projects are maintained under the [docker-library](https://github.com/docker-library) organization. Those include images such as Postgres and Python. 
However, many of them are included in the library but are managed by a separate organization, like Ubuntu and [Node.js](https://github.com/nodejs/docker-node)

Let's look into the Ubuntu image on [Docker Hub](https://hub.docker.com/r/library/ubuntu/) and trace the process.

The description/readme says:

    What's in this image?

     This image is built from official rootfs tarballs provided by Canonical
     (see dist-* tags at https://git.launchpad.net/cloud-images/+oci/ubuntu-base).

We can see that the image is built from <https://git.launchpad.net/cloud-images/+oci/ubuntu-base>.

Let's take a closer look at Ubuntu to verify where it comes from. If you click the Dockerfile link of <https://hub.docker.com/r/_/ubuntu/> you'll be given a json file instead of the Dockerfile contents. The digest seems to contain the valid digest for a single architecture version listed on Docker Hub (amd64). But after downloading it and checking the digest `docker pull ubuntu:22.04 && docker image ls --digests` the result does not match up.

We find a Dockerfile from the repository [here](https://git.launchpad.net/cloud-images/+oci/ubuntu-base/tree/Dockerfile?h=jammy-22.04). We can increase trust that it's the same as the image we downloaded with `image history`:

```console
$ docker image history --no-trunc ubuntu:22.04
```

The output from image history matches with the directives specified in the Dockerfile. If this isn't enough, we could also build the image ourselves.

The first line states that the image starts FROM a **special** image "scratch" that is just empty. Then a file `ubuntu-*-oci-$LAUNCHPAD_BUILD_ARCH-root.tar.gz` is added to the root from the same [directory](https://git.launchpad.net/cloud-images/+oci/ubuntu-base/tree/?h=jammy-22.04).

Notice how the file is not extracted at any point. The `ADD` instruction [documentation](https://docs.docker.com/engine/reference/builder/#add) states that "If src is a local tar archive in a recognized compression format (identity, gzip, bzip2 or xz) then it is unpacked as a directory."

We could verify the checksums of the file if we were interested. For the Ubuntu image automation from the launchpad takes care of creating the PRs to docker-library and the maintainers of the official images repository verify the PRs.

You can also visit the Docker Hub page for the image tag itself, which shows the layers and warns about potential security issues. You can see how many different problems it finds [here](https://hub.docker.com/layers/library/ubuntu/22.04/images/sha256-b2175cd4cfdd5cdb1740b0e6ec6bbb4ea4892801c0ad5101a81f694152b6c559?context=explore).

Now we have learned that the build processes are open and we can verify it if we have the need. In addition, we learned that there's nothing that makes the "official" images special.

#### "You can't trust code that you did not totally create yourself."
###### - Ken Thompson (1984, Reflections on Trusting Trust)

---

# Deployment pipelines

[CI/CD](https://en.wikipedia.org/wiki/CI/CD) pipeline (sometimes called deployment pipeline) is a corner stone of DevOps.
According to [Gitlab](https://about.gitlab.com/topics/ci-cd/):

  _CI/CD automates much or all of the manual human intervention traditionally needed to get new code from a commit into production. With a CI/CD pipeline, development teams can make changes to code that are then automatically tested and pushed out for delivery and deployment. Get CI/CD right and downtime is minimized and code releases happen faster._

Let us now see how one can set up a deployment pipeline that can be used to automatically deploy containerized software to _any_ machine. So every time you commit the code in your machine, the pipeline builds the image and starts it up in the server.

Since we cannot assume that everyone has access to their own server, we will demonstrate the pipeline using _a local machine_ as the development target, but the exactly same steps can be used for a virtual machine in the cloud (such as one provided by [Hetzner](https://www.hetzner.com/cloud)) or even Raspberry Pi.

We will use [GitHub Actions](https://github.com/features/actions) to build an image and push the image to Docker Hub, and then use a project called [Watchtower](https://containrrr.dev/watchtower/) to automatically pull and restart the new image in the target machine.

As an example, we will look repository [https://github.com/docker-hy/docker-hy.github.io](https://github.com/docker-hy/docker-hy.github.io), that is, the material of this course.

As was said [GitHub Actions](https://github.com/features/actions) is used to implement the first part of the deployment pipeline. The [documentation](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions) gives the following overview:

_GitHub Actions is a continuous integration and continuous delivery (CI/CD) platform that allows you to automate your build, test, and deployment pipeline. You can create workflows that build and test commit and every pull request to your repository, or deploy merged pull requests to production._

The [project](https://github.com/docker-hy/docker-hy.github.io) defines a _workflow_ with GitHub Actions that builds a Docker image and pushes it to Docker Hub every time the code is pushed to the GitHub repository.

Let us now see how the workflow definition looks. It is stored in the file _deploy.yml_ inside the _.github/workflows_ directory:

```yaml
name: Release DevOps with Docker # Name of the workflow

# On a push to the branch named master
on:
  push:
    branches:
      - master

# Job called build runs-on ubuntu-latest
jobs:
  deploy:
    name: Deploy to GitHub Pages
    # we are not interested in this job

  publish-docker-hub:
    name: Publish image to Docker Hub
    runs-on: ubuntu-latest
    steps:
    # Checkout to the repository
    - uses: actions/checkout@v2

    # We need to login so we can later push the image without issues.
    - name: Login to Docker Hub
      uses: docker/login-action@v1
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}
    # Builds devopsdockeruh/docker-hy.github.io
    - name: Build and push
      uses: docker/build-push-action@v2
      with:
        push: true
        tags: devopsdockeruh/coursepage:latest
```

The [workflow](https://docs.github.com/en/actions/using-workflows) has two  [jobs](https://docs.github.com/en/actions/using-jobs/using-jobs-in-a-workflow), we are now interested in the one that is called _publish-docker-hub_. The other job, called _deploy_ takes care of deploying the page as a GitHub page.

A job consists of a series of [steps](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idsteps). Each step is a small operation or _action_ that does its part of the whole. The steps are the following

- [actions/checkout@v2](https://github.com/actions/checkout) is used to check out the code from the repository
- [docker/login-action@v1](https://github.com/docker/login-action) is used to log in to Docker Hub
- [docker/build-push-action@v2](https://github.com/docker/build-push-action) is used to build the image and push it to Docker Hub

The first action was one of the ready-made actions that GitHub provides. The latter two are official actions offered by Docker. See [here](https://github.com/marketplace/actions/build-and-push-docker-images) for more info about the official Docker GitHub Actions.

Before the workflow will work, two [secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) should be added to the GitHub repository: `DOCKERHUB_TOKEN` and `DOCKERHUB_USERNAME`. This is done by opening the repository in the browser and first pressing *Settings* then *Secrets*. The `DOCKERHUB_TOKEN` can be created in Docker Hub from the  *Account Settings / Security*.

GitHub Actions are doing only the "first half" of the deployment pipeline: they are ensuring that every push to GitHub is built to a Docker image which is then pushed to Docker Hub.

The other half of the deployment pipeline is implemented by a containerized service called [Watchtower](https://github.com/containrrr/watchtower) which is an open-source project that automates the task of updating images. Watchtower will pull the source of the image (in this case Docker Hub) for changes in the containers that are running. The container that is running will be updated and automatically restarted when a new version of the image is pushed to Docker Hub. Watchtower respects tags e.g. q container using ubuntu:22.04 will not be updated unless a new version of ubuntu:22.04 is released.

:::tip Security reminder: Docker Hub accessing your computer

Note that now anyone with access to your Docker Hub also has access to your PC through this. If they push a malicious update to your application, Watchtower will happily download and start the updated version.

:::

Watchtower can be run eg. using the following Docker Compose file:

```yaml
version: "3.8"

services:
  watchtower:
    image: containrrr/watchtower
    environment:
      -  WATCHTOWER_POLL_INTERVAL=60 # Poll every 60 seconds
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    container_name: watchtower
```

One needs to be careful when starting Watchtower with _docker compose up_,  since it will try to update **every** image running the machine. The [documentation](https://containrrr.github.io/watchtower/) describes how this can be prevented.

## Exercises 3.1-3.4

:::info Exercise 3.1: Your pipeline

  Create now a similar deployment pipeline for a simple Node.js/Express app found
[here](https://github.com/docker-hy/material-applications/tree/main/express-app).

  Either clone the project or copy the files to your own repository. Set up a similar deployment pipeline (or the "first half") using GitHub Actions that was just described. Ensure that a new image gets pushed to Docker Hub every time you push the code to GitHub (you may eg. change the message the app shows).

Note that there is an important change that you should make to the above workflow configuration, the branch should be named _main_:

```yaml
name: Release Node.js app

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # ...
```

The earlier example still uses the old GitHub naming convention and calls the main branch _master_.

Some of the actions that the above example uses are a bit outdated, so go through the documentation

- [actions/checkout](https://github.com/actions/checkout)
- [docker/login-action](https://github.com/docker/login-action)
- [docker/build-push-action](https://github.com/docker/)

and use the most recent versions in your workflow.

Keep an eye on the GitHub Actions page to see that your workflow is working:

![Github Actions page](/img/3/gha.png)

Ensure also from Docker Hub that your image gets pushed there.

Next, run your image locally in detached mode, and ensure that you can access it with the browser.

Now set up and run the [Watchtower](https://github.com/containrrr/watchtower) just as described above.

You might do these two in a single step in a shared Docker Compose file.

Now your deployment pipeline is set up! Ensure that it works:
- make a change to your code
- commit and push the changes to GitHub
- wait for some time (the time it takes for GitHub Action to build and push the image plus the Watchtower poll interval)
- reload the browser to ensure that Watchtower has started the new version (that is, your changes are visible)

  Submit a link to the repository with the config.

:::

[Link to my repository](https://github.com/kinia0o/new-workflow/tree/main)

Success of action creating new image after push on github:

![screen1](screeny/e1s1.png)

Success of pull new image and update container by Watchtower:

![screen1s2](screeny/e1s2.png)

:::info Exercise 3.2: A deployment pipeline to a cloud service

  In [Exercise 1.16](/part-1/section-6#exercises-115-116) you deployed a containerized app to a cloud service.

  Now it is time to improve your solution by setting up a deployment pipeline for it so that every push to GitHub results in a new deployment to the cloud service.

  You will most likely find a ready-made GitHub Action that does most of the heavy lifting your you... Google is your friend!

  Submit a link to the repository with the config. The repository README should have a link to the deployed application.

:::

:::info Exercise 3.3: Scripting magic

  Create a now script/program that downloads a repository from GitHub, builds a Dockerfile located in the root and then publishes it into the Docker Hub.

  You can use any scripting or programming language to implement the script. Using [shell script](https://www.shellscript.sh/) might make the next exercise a bit easier... and do not worry if you have not done a shell script earlier, you do not need much for this exercise and Google helps.

  The script could eg. be designed to be used so that as the first argument it gets the GitHub repository and as the second argument the Docker Hub repository. Eg. when run as follows

  ```bash
  ./builder.sh mluukkai/express_app mluukkai/testing
  ```

  the script clones <https://github.com/mluukkai/express_app>, builds the image, and pushes it to Docker Hub repository mluukkai/testing

:::

builder.sh:

```
#!/bin/bash

# Sprawdzenie, czy podano dwa argumenty
if [ "$#" -ne 2 ]; then
    echo "Niepoprawne argumenty - poprawne użycie: ./builder.sh <GitHub_repo> <DockerHub_repo>"
    exit 1
fi

# Pobranie argumentów
GITHUB_REPO=$1
DOCKERHUB_REPO=$2

# Pobranie nazwy repozytorium (ostatnia część ścieżki)
REPO_NAME=$(basename "$GITHUB_REPO")

# Klonowanie repozytorium
echo "Klonowanie repozytorium: https://github.com/$GITHUB_REPO.git"
git clone "https://github.com/$GITHUB_REPO.git"

# Przejście do katalogu repozytorium
cd "$REPO_NAME" || { echo "Błąd: katalog $REPO_NAME nie istnieje!"; exit 1; }

# Budowanie obrazu Dockera
echo "Budowanie obrazu Dockera: $DOCKERHUB_REPO:latest"
docker build -t "$DOCKERHUB_REPO:latest" .

# Logowanie do Docker Hub
echo "Logowanie do Docker Hub"
docker login

# Wysłanie obrazu do Docker Hub
echo "Wysyłanie obrazu: $DOCKERHUB_REPO:latest"
docker push "$DOCKERHUB_REPO:latest"

echo "Zakończono pomyślnie! ^^"
```
![screen3s1](screeny/e3s1.png)

Successful pushed image:

![screen3s2](screeny/e3s2.png)


:::info Exercise 3.4: Building images from inside of a container

As seen from the Docker Compose file, the Watchtower uses a volume to [docker.sock](https://stackoverflow.com/questions/35110146/can-anyone-explain-docker-sock) socket to access the Docker daemon of the host from the container:

  ```yaml
services:
  watchtower:
    image: containrrr/watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    # ...
```

   In practice this means that Watchtower can run commands on Docker the same way we can "command" Docker from the cli with _docker ps_, _docker run_ etc.

  We can easily use the same trick in our own scripts! So if we mount the _docker.sock_ socket to a container, we can use the command _docker_ inside the container, just like we are using it in the host terminal!

Dockerize now the script you did for the previous exercise. You can use images from [this repository](https://hub.docker.com/_/docker) to run Docker inside Docker!

Your Dockerized could be run like this (the command is divided into many lines for better readability, note that copy-pasting a multiline command does not work):

```
docker run -e DOCKER_USER=mluukkai \
  -e DOCKER_PWD=password_here \
  -v /var/run/docker.sock:/var/run/docker.sock \
  builder mluukkai/express_app mluukkai/testing
```

Note that now the Docker Hub credentials are defined as environment variables since the script needs to log in to Docker Hub for the push.

Submit the Dockerfile and the final version of your script.

  Hint: you quite likely need to use [ENTRYPOINT](https://docs.docker.com/engine/reference/builder/#entrypoint) in this Exercise.
  See [Part 1](/part-1/section-4) for more.

:::

Modified script builder.sh:

```
#!/bin/bash

# Sprawdzenie, czy podano dwa argumenty
if [ "$#" -ne 2 ]; then
    echo "Niepoprawne argumenty - poprawne użycie: ./builder.sh <GitHub_repo> <DockerHub_repo>"
    exit 1
fi

# Pobranie argumentów
GITHUB_REPO=$1
DOCKERHUB_REPO=$2

# Pobranie nazwy repozytorium (ostatnia część ścieżki)
REPO_NAME=$(basename "$GITHUB_REPO")

# Klonowanie repozytorium
echo "Klonowanie repozytorium: https://github.com/$GITHUB_REPO"
echo "$GITHUB_USER:$GITHUB_TOKEN"
git clone "https://$GITHUB_USER:$GITHUB_TOKEN@github.com/$GITHUB_REPO"

# Przejście do katalogu repozytorium
cd "$REPO_NAME" || { echo "Błąd: katalog $REPO_NAME nie istnieje!"; exit 1; }

# Budowanie obrazu Dockera
echo "Budowanie obrazu Dockera: $DOCKERHUB_REPO:latest"
docker build -t "$DOCKERHUB_REPO:latest" .

# Logowanie do Docker Hub
echo "Logowanie do Docker Hub jako $DOCKER_USER"
echo "$DOCKER_PWD" | docker login -u "$DOCKER_USER" --password-stdin || { echo "Błąd logowania"; exit 1; }

# Wysłanie obrazu do Docker Hub
echo "Wysyłanie obrazu: $DOCKERHUB_REPO:latest"
docker push "$DOCKERHUB_REPO:latest"

echo "Zakończono pomyślnie! ^^"
```

Dockerfile:

```
# Obraz bazowy Dockera
FROM docker:latest

# Instalacja Gita, bo jest wymagany do klonowania repozytoriów
RUN apk add --no-cache git

# Skopiowanie skryptu do obrazu oraz nadanie mu uprawnień
WORKDIR /app
COPY builder.sh /app/builder.sh
RUN chmod +x /app/builder.sh

# Ustawienie skryptu jako domyślnego polecenia ENTRYPOINT
ENTRYPOINT ["sh", "/app/builder.sh"]
```

commands:

```
docker build -t builder .
docker run -e DOCKER_USER=kiianeee -e GITHUB_USER=kinia0o -e GITHUB_TOKEN=<mój_token> -v /var/run/docker.sock:/var/run/docker.sock builder kinia0o/new-workflow kiianeee/new2
```
![screen4s1](screeny/e4s1.png)

Part 2:

![screen4s2](screeny/e4s2.png)

Successful pushed image:

![screen4s3](screeny/e4s3.png)


---

# Using a non-root user

Let's get back to the yt-dlp application, that we for last time worked with it [Part 2](http://localhost:8000/part-2/1-migrating-to-docker-compose#volumes-in-docker-compose).

The application could, in theory, escape the container due to a bug in Docker or Linux kernel. To mitigate this security issue we will add a non-root user to our container and run our process with that user. Another option would be to map the root user to a high, non-existing user id on the host with https://docs.docker.com/engine/security/userns-remap/, and can be used in case you must use root within the container.

The Dockerfile that we did in [Part 1](/part-1/section-4) was this:

```dockerfile
FROM ubuntu:22.04

WORKDIR /mydir

RUN apt-get update && apt-get install -y curl python3
RUN curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
RUN chmod a+x /usr/local/bin/yt-dlp

ENTRYPOINT ["/usr/local/bin/yt-dlp"]
```

We will add a user called _appuser_ with the following command

```dockerfile
RUN useradd -m appuser
```

After that we change the user with the directive [USER](https://docs.docker.com/engine/reference/builder/#user) - so all commands after this line will be executed as our new user, including the `CMD` and `ENTRYPOINT`.

```dockerfile
FROM ubuntu:22.04

WORKDIR /mydir

RUN apt-get update && apt-get install -y curl python3
RUN curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
RUN chmod a+x /usr/local/bin/yt-dlp

RUN useradd -m appuser
USER appuser

ENTRYPOINT ["/usr/local/bin/yt-dlp"]
```

The `WORKDIR` is renamed to /usr/videos since it makes more sense as the videos will be downloaded there. When we run this image without bind mounting our local directory:

```console
$ docker  run yt-dlp https://www.youtube.com/watch?v=XsqlHHTGQrw

... 

[info] XsqlHHTGQrw: Downloading 1 format(s): 22
[download] Unable to open file: [Errno 13] Permission denied: 'Master’s Programme in Computer Science ｜ University of Helsinki [XsqlHHTGQrw].mp4.part'. Retrying (1/3)...
[download] Unable to open file: [Errno 13] Permission denied: 'Master’s Programme in Computer Science ｜ University of Helsinki [XsqlHHTGQrw].mp4.part'. Retrying (2/3)...
[download] Unable to open file: [Errno 13] Permission denied: 'Master’s Programme in Computer Science ｜ University of Helsinki [XsqlHHTGQrw].mp4.part'. Retrying (3/3)...

ERROR: unable to open for writing: [Errno 13] Permission denied: 'Master’s Programme in Computer Science ｜ University of Helsinki [XsqlHHTGQrw].mp4.part'
```

We'll see that our `appuser` user has no access to write to the container filesystem. This can be fixed with `chown` or not fix it at all, if the intented usage is to always have a `/mydir` mounted from the host. By mounting the directory the application works as intended.

If we want to give the `appuser` permission to write inside the container, the permission change must be done when we are still executing as root, that is, before the directive `USER` is used to change the user:

```dockerfile
FROM ubuntu:22.04

# ...

WORKDIR /mydir

# create the appuser
RUN useradd -m appuser

# change the owner of current dir to appuser
RUN chown appuser .

# now we can change the user
USER appuser

ENTRYPOINT ["/usr/local/bin/yt-dlp"]
```

## Exercise 3.5

:::caution Mandatory Exercise 3.5

  In exercises [1.12](/part-1/section-6#exercises-111-114) and [1.13](/part-1/section-6#exercises-111-114) we created Dockerfiles for both [frontend](https://github.com/docker-hy/material-applications/tree/main/example-frontend) and [backend](https://github.com/docker-hy/material-applications/tree/main/example-backend).

  Security issues with the user being a root are serious for the example frontend and backend as the containers for web services are supposed to be accessible through the Internet.

  Make sure the containers start their processes as non-root user.

  The backend image is based on [Alpine Linux](https://www.alpinelinux.org/), which does not support the command `useradd`. Google will surely help you a way to create a user in an `alpine` based image.

  Submit the Dockerfiles.

:::

Dockerfile dla backend:

```
FROM golang:1.16-alpine
WORKDIR /usr/src/app
COPY . .

# Tworzenie użytkownika i grupy w Alpine
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Nadanie uprawnień do katalogu roboczego
RUN chown -R appuser:appgroup /usr/src/app

# Przełączenie na użytkownika nie-root
USER appuser

EXPOSE 8080
ENV REQUEST_ORIGIN=http://localhost:5000
RUN go build

# Uruchomienie aplikacji jako użytkownik nie-root
CMD ["./server"]
```

Dockerfile dla frontend:

```
FROM node:14

# Tworzenie użytkownika
RUN useradd -m appuser

WORKDIR /usr/src/app
COPY . .
EXPOSE 5000
ENV REACT_APP_BACKEND_URL=http://localhost:8080
RUN npm install
RUN npm run build
RUN npm install -g serve

# Przełączenie na użytkownika nie-root
USER appuser

CMD ["serve", "-s", "-l", "5000", "build"]
```

commands:

```
docker build . -t backend
docker run -p 8080:8080 --name back backend
docker build . -t frontend
docker run -p 5000:5000 --name front frontend
```

backend:

![screen5s1](screeny/e5s1.png)

frontend:

![screen5s2](screeny/e5s2.png)

On [http://localhost:5000](http://localhost:5000):

![screen5s3](screeny/e5s3.png)

---

# Optimizing the image size

A small image size has many advantages, firstly, it takes much less time to pull a small image from the registry. Another thing is the security: the bigger your image is the larger the surface area for an attack it has.

The following tutorial on "Building Small Containers" from Google is an excellent video to showcase the importance of optimizing your Dockerfiles:

<p>
<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/wGz_cbtCiEA" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</p>

Before going on to the tricks that were shown in the video, let us start by reducing the number of layers of a image. What actually is a layer? According to the [documentation](https://docs.docker.com/get-started/overview/#how-does-a-docker-image-work):

_To build your own image, you create a Dockerfile with a simple syntax for defining the steps needed to create the image and run it. Each instruction in a Dockerfile creates a layer in the image. When you change the Dockerfile and rebuild the image, only those layers which have changed are rebuilt. This is part of what makes images so lightweight, small, and fast, when compared to other virtualization._

So each command that is executed to the base image, forms a layer. The resulting image is the final layer, which combines the changes that all the intermediate layers contain. Each layer potentially adds something extra to the resulting image so it might be a good idea to minimize the number of layers.

To keep track of the improvements, we keep on note of the image size after each new Dockerfile. The starting point is

```dockerfile
FROM ubuntu:22.04

WORKDIR /mydir

RUN apt-get update && apt-get install -y curl python3
RUN curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
RUN chmod a+x /usr/local/bin/yt-dlp

RUN useradd -m appuser

RUN chown appuser .

USER appuser

ENTRYPOINT ["/usr/local/bin/yt-dlp"]
```

The built image has size **155MB**

As was said each command that is executed to the base image, forms a layer. The command here refers to one Dockerfile directive such as `RUN`. We could now glue all `RUN` commands together to reduce the number of layers that are created when building the image:

```dockerfile
FROM ubuntu:22.04

WORKDIR /mydir

RUN apt-get update && apt-get install -y curl python3 && \
    curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp && \
    chmod a+x /usr/local/bin/yt-dlp && \
    useradd -m appuser && \
    chown appuser .

USER appuser

ENTRYPOINT ["/usr/local/bin/yt-dlp"]
```

Image size is **153MB**.

There is not that much difference, the image with fewer layers is only 2 MB smaller.

As a sidenote not directly related to Docker: remember that if needed, it is possible to bind packages to versions with `curl=1.2.3` - this will ensure that if the image is built at a later date the image is more likely to work as the versions are exact. On the other hand, the packages will be old and have security issues.

With `docker image history` we can see that our single `RUN` layer adds 83.8 megabytes to the image:

```console
$ docker image history yt-dlp

IMAGE          CREATED         CREATED BY                                      SIZE      COMMENT
a3f296f27a17   3 minutes ago   ENTRYPOINT ["/usr/local/bin/yt-dlp"]            0B        buildkit.dockerfile.v0
<missing>      3 minutes ago   USER appuser                                    0B        buildkit.dockerfile.v0
<missing>      3 minutes ago   RUN /bin/sh -c apt-get update && apt-get ins…   83.8MB    buildkit.dockerfile.v0
  ...
```

The next step is to remove everything that is not needed in the final image. We don't need the apt source lists anymore, so we can glue the next line to our single `RUN`

```console
.. && \
rm -rf /var/lib/apt/lists/*
````

Now, after we build, the size of the layer is **108 megabytes**. We can optimize even further by removing the `curl` all the dependencies it installed. This is done by extending the command as follows:

```console
.. && \
apt-get purge -y --auto-remove curl && \
rm -rf /var/lib/apt/lists/*
````

This brings us down to **104 MB**.

## Exercise 3.6

:::info Exercise 3.6

  Return now back to our [frontend](https://github.com/docker-hy/material-applications/tree/main/example-frontend) and
  [backend](https://github.com/docker-hy/material-applications/tree/main/example-backend) Dockerfile.

  Document both image sizes at this point, as was done in the material. Optimize the Dockerfiles of both app frontend and backend, by joining the RUN commands and removing useless parts.

  After your improvements document the image sizes again.

:::

```
docker images
```

![screen6s1](screeny/e6s1.png)

Improved backend Dockerfile:

```
FROM golang:1.16-alpine

WORKDIR /usr/src/app
COPY . .

# Tworzenie użytkownika i grupy oraz nadanie uprawnień, zbudowanie oraz usunięcie nie potrzebnej zawartości w jednej komendzie
RUN addgroup -S appgroup && adduser -S appuser -G appgroup && chown -R appuser:appgroup /usr/src/app && go build && rm -rf /var/cache/apk/*

USER appuser
EXPOSE 8080
ENV REQUEST_ORIGIN=http://localhost:5000

CMD ["./server"]
```

Improved frontend Dockerfile:

```
FROM node:14
WORKDIR /usr/src/app
COPY . .

# Instalacja zależności, budowanie i czyszczenie w jednej komendzie
RUN useradd -m appuser && npm install && npm run build && npm install -g serve && rm -rf /root/.npm /tmp/*

USER appuser
EXPOSE 5000
ENV REACT_APP_BACKEND_URL=http://localhost:8080

CMD ["serve", "-s", "-l", "5000", "build"]
```

commands:

```
docker build . -t smaller-backend
docker build . -t smaller-frontend
docker images
```

![screen6s2](screeny/e6s2.png)


## Alpine Linux variant ##

Our Ubuntu base image adds the most megabytes to our image. [Alpine Linux](https://www.alpinelinux.org/) provides a popular alternative base in https://hub.docker.com/_/alpine/ that is around 8 megabytes. It's based on alternative glibc implementation [musl](https://musl.libc.org/) and [busybox](https://www.busybox.net/) binaries, so not all software runs well (or at all) with it, but our container should run just fine. We'll create the following `Dockerfile.alpine` file:

```dockerfile
FROM alpine:3.19

WORKDIR /mydir

RUN apk add --no-cache curl python3 ca-certificates && \
    curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp && \
    chmod a+x /usr/local/bin/yt-dlp && \
    adduser -D appuser && \
    chown appuser . && \
    apk del curl 

USER appuser

ENTRYPOINT ["/usr/local/bin/yt-dlp"]
```

Size of the resulting image is **57.6MB**

Notes:
 - The package manager is `apk` and it can work without downloading sources (caches) first with `--no-cache`.
 - For creating user the command `useradd` is missing, but `adduser` can be used instead.
 - Most of the package names are the same - there's a good package browser at https://pkgs.alpinelinux.org/packages.

We build this file with `:alpine-3.19` as the tag:

```console
$ docker build -t yt-dlp:alpine-3.19 -f Dockerfile.alpine .
```

It seems to run fine:

```console
$ docker run -v "$(pwd):/mydir" yt-dlp:alpine-3.19 https://www.youtube.com/watch\?v\=bNw2i-mRT4I
```

From the history, we can see that our single `RUN` layer size is 49.8MB

```console
$ docker image history yt-dlp:alpine-3.19

  ...
<missing>      6 minutes ago   RUN /bin/sh -c apk add --no-cache curl pytho…   49.8MB    buildkit.dockerfile.v0
  ...
<missing>      7 weeks ago     /bin/sh -c #(nop) ADD file:d0764a717d1e9d0af…   7.73MB
```

So in total, our Alpine variant is about 57.6 megabytes, significantly less than our Ubuntu-based image.

## Image with preinstalled environment

As seen, yt-dlp requires Python to function. Installing Python to Ubuntu- or Alpine-based image is very easy, it can be done with a single command. In general, installing the environment that is required to build and run a program inside a container can be quite a burden. 

Luckily, there are preinstalled images for many programming languages readily available on DockerHub, and instead of relying upon "manual" installation steps in a Dockerfile, it's quite often a good idea to use a pre-installed image.


Let us use the one made for [Python](https://hub.docker.com/_/python) to run the yt-dpl:

```dockerfile
# we are using a new base image
FROM python:3.12-alpine

WORKDIR /mydir

# no need to install python3 anymore
RUN apk add --no-cache curl ca-certificates && \
    curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp && \
    chmod a+x /usr/local/bin/yt-dlp && \
    adduser -D appuser && \
    chown appuser . && \
    apk del curl 

USER appuser

ENTRYPOINT ["/usr/local/bin/yt-dlp"]
```

There are many variants for the Python images, we have selected _python:3.12-alpine_ which has Python version 3.12 and is based on Alpine Linux.

The resulting image size is **59.5MB** so it is slightly larger than the previous one where we installed Python by ourselves.

Back in part 1, we published the Ubuntu version of yl-dlp with the tag _latest_.

We can publish whatever variants we want without overriding the others by publishing them with a describing tag:

```console
$ docker image tag yt-dlp:alpine-3.19 <username>/yt-dlp:alpine-3.19
$ docker image push <username>/yt-dlp:alpine-3.19
$ docker image tag yt-dlp:python-alpine <username>/yt-dlp:python-alpine
$ docker image push <username>/yt-dlp:python-alpine
```

Or if we don't want to keep the Ubuntu version anymore we can replace that pushing an Alpine-based image as the latest. Someone might depend on the image being Ubuntu though.

```console
$ docker image tag yt-dlp:python-alpine <username>/yt-dlp
$ docker image push <username>/yt-dlp
```

It's important to keep in mind that if not specified, the tag `:latest` simply refers to the most recent image that has been built and pushed, which can potentially contain any updates or changes.

## Exercise 3.7

:::info Exercise 3.7

  As you may have guessed, you shall now return to the frontend and backend from the previous exercise.

  Change the base image in FROM to something more suitable. To avoid the extra hassle, it is a good idea to use a pre-installed image for both [Node.js](https://hub.docker.com/_/node) and [Golang](https://hub.docker.com/_/golang). Both should have at least Alpine variants ready in DockerHub. 
   
  Note that the frontend requires Node.js version 16 to work, so you must search for a bit older image.

  Make sure the application still works after the changes.

  Document the size before and after your changes.

:::

updated backend Dockerfile:

```
FROM golang:1.16.15-alpine3.18

WORKDIR /usr/src/app
COPY . .

RUN apk add --no-cache git ca-certificates && addgroup -S appgroup && adduser -S appuser -G appgroup &&  go build -o server . && rm -rf /var/cache/apk/* /usr/src/app/.git

USER appuser
EXPOSE 8080
ENV REQUEST_ORIGIN=http://localhost:5000

CMD ["./server"]
```

updated frontend Dockerfile:

```
FROM node:16-alpine3.18

WORKDIR /usr/src/app
COPY . .

RUN adduser -D appuser && npm install && npm run build && npm install -g serve && rm -rf /root/.npm /tmp/* /var/cache/apk/* node_modules && npm cache clean --force

USER appuser
EXPOSE 5000
ENV REACT_APP_BACKEND_URL=http://localhost:8080

CMD ["serve", "-s", "-l", "5000", "build"]
```

commands:

```
docker build . -t smaller-backend
docker build . -t smaller-frontend
docker images
```

![screen7](screeny/e7.png)

## Multi-stage builds ##

Multi-stage builds are useful when you need some tools just for the build but not for the execution of the image (that is for CMD or ENTRYPOINT). This is an easy way to reduce size in some cases.

Let's create a website with [Jekyll](https://jekyllrb.com/), build the site for production and serve the static files with Nginx. Start by creating the recipe for Jekyll to build the site.

```dockerfile
FROM ruby:3

WORKDIR /usr/app

RUN gem install jekyll
RUN jekyll new .
RUN jekyll build
```

This creates a new Jekyll application and builds it. We are going to use Nginx to serve the site page but you can test how the site works if you add the following directive:

```dockerfile
CMD bundle exec jekyll serve --host 0.0.0.0
```

We could start thinking about optimizations at this point but instead, we're going to add a new FROM for Nginx, this is what the resulting image will be. Then we will copy the built static files from the Ruby image to our Nginx image:

```dockerfile
# the  first stage needs to be given a name
FROM ruby:3 AS build-stage
WORKDIR /usr/app

RUN gem install jekyll
RUN jekyll new .
RUN jekyll build

# we will now add a new stage
FROM nginx:1.19-alpine

COPY --from=build-stage /usr/app/_site/ /usr/share/nginx/html
```

Now Docker copies contents from the first image `/usr/app/_site/` to `/usr/share/nginx/html` Note the naming from Ruby to _build-stage_. We could also use an external image as a stage, `--from=python:3.12` for example.

Let's build and check the size difference:

```console
$ docker build . -t jekyll
$ docker image ls
  REPOSITORY    TAG     IMAGE ID         CREATED           SIZE
  jekyll        nginx   9e2f597ad99e     8 seconds ago     21.3MB
  jekyll        ruby    5dae3d9f8dfb     26 minutes ago    1.05GB
```

As you can see, even though our Jekyll image needed Ruby during the build stage, it is considerably smaller since it only has Nginx and the static files in the resulting image. `docker run -it -p 8080:80 jekyll:nginx` also works as expected.

Often the best choice is to use a FROM **scratch** image as it doesn't have anything we don't explicitly add there, making it the most secure option over time.

## Exercises 3.8 - 3.10


:::info Exercise 3.8: Multi-stage frontend

  Do now a multi-stage build for the example
  [frontend](https://github.com/docker-hy/material-applications/tree/main/example-frontend).

  Even though multi-stage builds are designed mostly for binaries in mind, we can leverage the benefits with our frontend project as having original source code with the final assets makes little sense. Build it with the
  instructions in README and the built assets should be in `build` folder.

  You can still use the `serve` to serve the static files or try out something else.

:::

Dockerfile:

```
FROM node:16-alpine3.18 AS build-stage

WORKDIR /usr/src/app
COPY . .

RUN npm install && npm run build && npm install -g serve && rm -rf /root/.npm /tmp/* /var/cache/apk/* node_modules && npm cache clean --force

FROM node:16-alpine3.18

WORKDIR /usr/src/app

RUN adduser -D appuser && npm install -g serve

# Kopiowanie tylko skompilowanych plików z poprzedniego etapu
COPY --from=build-stage /usr/src/app/build ./build

USER appuser
EXPOSE 5000
ENV REACT_APP_BACKEND_URL=http://localhost:8080

CMD ["serve", "-s", "-l", "5000", "build"]
```

commands:

```
docker build . -t multi-frontend
docker images
```

![screen8](screeny/e8.png)

:::info Exercise 3.9: Multi-stage backend

  Let us do a multi-stage build for the [backend](https://github.com/docker-hy/material-applications/tree/main/example-backend) project since we've come so far with the application.

  The project is in Golang and building a binary that runs in a container, while straightforward, isn't exactly trivial. Use resources that you have available (Google, example projects) to build the binary and run it inside a container that uses `FROM scratch`.

  To successfully complete the exercise the image must be smaller than <b>25MB</b>.

:::

Dockerfile:

```
FROM golang:1.16-alpine3.14 AS build-stage

WORKDIR /usr/src/app
COPY . .

RUN apk add --no-cache git ca-certificates && addgroup -S appgroup && adduser -S appuser -G appgroup &&  go build -o server . && rm -rf /var/cache/apk/* /usr/src/app/.git

FROM alpine:3.14 

WORKDIR /root/
COPY --from=build-stage /usr/src/app/server .

EXPOSE 8080
ENV REQUEST_ORIGIN=http://localhost:5000

CMD ["./server"]
```

commands:

```
docker build . -t multi-frontend
docker images
```

![screen9](screeny/e9.png)

:::info Exercise 3.10

  Do all or most of the optimizations from security to size for **one** other Dockerfile you have access to, in your own project or for example the ones used in previous "standalone" exercises.

  Please document Dockerfiles both before and after.

:::

Dockerfile:

```
FROM python:3.9-slim
COPY code /app/code
WORKDIR /app/code
# ENTRYPOINT uruchamia domyślną aplikację
ENTRYPOINT ["python", "script.py"]
# CMD umożliwia dodanie parametrów do ENTRYPOINT
CMD ["Kinga"]
```

updated Dockerfile:

```
FROM python:3.9-slim AS builder-stage
WORKDIR /app
COPY code /app/code

FROM python:3.9-alpine
WORKDIR /app/code

# Dodanie użytkownika
RUN adduser -D appuser

# Kopiowanie tylko potrzebnych plików z etapu buildera
COPY --from=builder-stage /app/code /app/code

USER appuser
ENTRYPOINT ["python", "script.py"]
CMD ["Kinga"]
```

![screen10](screeny/e10.png)

# Multi-host environments

Now that we've mastered containers in small systems with Docker Compose it's time to look beyond what the tools we practiced are capable of. 
In situations where we have more than a single host machine we cannot rely solely on Docker. However, Docker does contain other tools to help us with automatic 
deployment, scaling and management of dockerized applications.

In the scope of this course, we cannot go into how to use the tools in this section, but leaving them without a mention would be a disservice.

**Docker swarm mode** is built into Docker. It turns a pool of Docker hosts into a single virtual host. 
You can read the feature highlights [here](https://docs.docker.com/engine/swarm/). You can run right away with `docker swarm`. 
Docker swarm mode is the lightest way of utilizing multiple hosts.

**Kubernetes** is the de facto way of orchestrating your containers in large multi-host environments. The reason being it's customizability, large community and robust 
features. However, the drawback is the higher learning curve compared to Docker swarm mode. 
You can read their introduction [here](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/).

It is always good to remember that a single tool is rarely an optimal solution for all possible scenarios. 
In a 2-3 host environment for a hobby project, the gains from Kubernetes might not be as large compared to an environment where you need to orchestrate 
hundreds of hosts with multiple containers each.

You can get to know Kubernetes with [k3s](https://k3s.io/) a lightweight Kubernetes distribution that you can run inside containers 
with [k3d](https://github.com/rancher/k3d). Another similar solution is [kind](https://kind.sigs.k8s.io/).
These are a great way to get started as you don't have to worry about complicated setup or any credit limits that the cloud providers always have.

Rather than maintaining one yourself the most common way to use Kubernetes is by using a managed service by a cloud provider. Such as Google Kubernetes 
Engine (GKE) or Amazon Elastic Kubernetes Service (Amazon EKS) which are both offering some credits to get started.

## Exercise 3.11

:::info Exercise 3.11: Kubernetes

  Familiarize yourself with Kubernetes terminology and draw a diagram describing what "parts" the Kubernetes contain and how those are related to each other.

  You should draw a diagram of at least three host machines in a Kubernetes cluster. In the diagram assume that the cluster is running two applications. 
  The applications can be anything you want. An example could be a video game server and a blog website.

  You may take inspiration from the diagrams of [part 2](/part-2).

  The applications may utilize other machines or APIs that are not part of the cluster. At least three of the machines should be utilized. 
  Include "your own computer" in the diagram as the one sending instructions via kubectl to deploy an application. 
  In addition, include a HTTP message coming from the internet to your Kubernetes cluster and how it may reach an application.

  Make sure to label the diagram so that anyone else who has completed this exercise, and read the glossary, would understand it. 
  The diagram should contain at least four of the following labels: Pod, Cluster, Container, Service and Volume.

  [Glossary](https://kubernetes.io/docs/reference/glossary/?fundamental=true). 
  And some [helpful diagrams](https://medium.com/@tsuyoshiushio/kubernetes-in-three-diagrams-6aba8432541c)

  I prefer to use [draw.io](https://draw.io) but you can use whichever tool you want.

:::

Diagram created in [draw.io](https://draw.io):

![screen11](screeny/e11.png)

If you are interested, later this year the course [DevOps With Kubernetes](https://devopswithkubernetes.com/) will provide a comprehensive treatment on using Kubernetes.

---

