FROM gitpod/workspace-python

RUN pyenv install 3.9.13 \
    && pyenv global 3.9.13
