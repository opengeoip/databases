FROM scratch
ARG DATABASE
COPY opengeoip-${DATABASE}.mmdb /
