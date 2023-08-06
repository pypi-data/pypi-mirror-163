##### Install iseqdockertools lib

Optional steps (create virtual environment):
```
python3 -m venv venv
source tutorial_env/bin/activate
```


Obligatory steps:
```
python3 -m pip install --upgrade pip
pip install iseqdockertools
```



##### Build docker images

Script automatically takes name and version of the docker image from its header.
It has to be in the following format (at the beginning of the Dockerfile):
```
# name: name
# version: 1.0.0
```

Building has default context to repository and you can use ADD with path to the files from here. 
Default option is to push to the dockerhub. If the dockerfile exists it won't be pushed. To develop dockerimage locally use flag --nopush. 

##### Usage (when you are in workflows' root directory):
```
dockerbuilder -d path/to/dockerfile
```
for example: 
```
dockerbuilder -d src/main/docker/reports/reports/Dockerfile
```
Script dockerbuider contains --help section with all the flags:

1. Print 'docker build' and 'docker push' logs
```
dockerbuilder -d path/to/dockerfile --quiet
```
2. Do not push docker image(s) to repository
```
dockerbuilder -d path/to/dockerfile --nopush
```
3. Do not use cache when building the docker image(s)
```
dockerbuilder -d path/to/dockerfile --nocache
```
4. Build separate images for all chromosomes
```
dockerbuilder -d path/to/dockerfile --chromosome
```
5. Push image even if exists in repository
```
dockerbuilder -d path/to/dockerfile --forcepush
```
6. Set current directory as context
```
dockerbuilder -d path/to/dockerfile --context
```

You can mix flags whenever you need to.

##### Name of the docker image vs location of its dockerfile

Location: 
```src/main/docker/[catalog-name]/[version]/Dockefile```

Name of the image: ```intelliseqngs/[catalog-name]:[version]```


More info here:
https://workflows-dev-documentation.readthedocs.io/en/latest/Docker.html