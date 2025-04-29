FROM golang:1.24-alpine

# Set environment variables for Hugo
ARG HUGO_VERSION

# Install Hugo dependencies
RUN apk add --no-cache \
    git \
    libc6-compat \
    libstdc++ \
    ca-certificates \
    && update-ca-certificates

# Download and install Hugo
RUN wget https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_${HUGO_VERSION}_Linux-64bit.tar.gz \
    && tar -xzvf hugo_${HUGO_VERSION}_Linux-64bit.tar.gz \
    && mv hugo /usr/local/bin/hugo \
    && rm hugo_${HUGO_VERSION}_Linux-64bit.tar.gz

# Set the working directory
WORKDIR /site

# Expose Hugo default server port
EXPOSE 1313

# Command to run Hugo server
CMD ["hugo", "server", "--bind", "0.0.0.0"]
