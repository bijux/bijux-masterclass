# Dockerfile
#
# Host policy: no Conda required.
# Container policy: use micromamba to create an environment from environment.yaml.

FROM mambaorg/micromamba:1.5.10

WORKDIR /work

# Reduce layer invalidation: copy only env spec first.
COPY environment.yaml /tmp/environment.yaml

# Create and activate environment. Use a fixed env name for determinism.
RUN micromamba create -y -n capstone -f /tmp/environment.yaml \
    && micromamba clean -a -y

ENV PATH=/opt/conda/envs/capstone/bin:$PATH

# Copy repository.
COPY . /work

# Default command is interactive shell; Makefile overrides for workflow runs.
CMD ["bash"]
