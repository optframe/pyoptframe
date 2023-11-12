FROM mcr.microsoft.com/devcontainers/cpp:0-ubuntu-22.04

# REFRESH!
RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y

# install pip (for cpplint and cmake)
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
     && apt-get -y install --no-install-recommends python3-pip

RUN pip install --upgrade cmake


# clang-tidy
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
     && apt-get -y install --no-install-recommends clang-tidy clang-format clangd

# install nvm (for npm)
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
RUN bash /root/.nvm/install.sh

# install npm (using nvm)
RUN bash -i -c "nvm install --lts"

# bazel (using npm)
RUN bash -i -c "npm install -g @bazel/bazelisk"

# install pip and cpplint
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
     && apt-get -y install --no-install-recommends python3-pip
# install cpplint into /usr/local/bin/cpplint
RUN pip install cpplint 

# bumpver
RUN python3 -m pip install bumpver

# bumpver
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
     && apt-get -y install --no-install-recommends virtualenv python3-venv
RUN python3 -m pip install bumpver
# build and twine
RUN python3 -m pip install build twine