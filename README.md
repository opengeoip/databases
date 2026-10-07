# databases

[![Databases](https://github.com/opengeoip/databases/actions/workflows/databases.yml/badge.svg)](https://github.com/opengeoip/databases/actions/workflows/databases.yml)
[![Latest](https://img.shields.io/github/v/release/opengeoip/databases?label=databases)](https://github.com/opengeoip/databases/releases/latest)

Free IP geolocation and ASN databases, rebuilt every day by [geoip-builder](https://github.com/opengeoip/geoip-builder) from public data only.

| File | Content | Schema |
|---|---|---|
| `opengeoip-country.mmdb` | country | GeoLite2 Country |
| `opengeoip-city.mmdb` | country, region, city | GeoLite2 City |
| `opengeoip-asn.mmdb` | origin AS and organization | GeoLite2 ASN |

The files are in the [MaxMind DB](https://maxmind.github.io/MaxMind-DB/) format, so any MaxMind DB library or tool reads them, as drop-in replacements for GeoLite2.

## Download

```sh
curl -LO https://github.com/opengeoip/databases/releases/latest/download/opengeoip-country.mmdb
curl -LO https://github.com/opengeoip/databases/releases/latest/download/opengeoip-city.mmdb
curl -LO https://github.com/opengeoip/databases/releases/latest/download/opengeoip-asn.mmdb
```

Each release also has a `SHA256SUMS` file and build provenance attestations:

```sh
gh attestation verify opengeoip-country.mmdb --owner opengeoip
```

## Container images

Each database is also published as an OCI image holding only its file, at the root: `ghcr.io/opengeoip/databases/country`, `ghcr.io/opengeoip/databases/city` and `ghcr.io/opengeoip/databases/asn`, tagged with the release name and `latest`. They suit Kubernetes [image volumes](https://kubernetes.io/docs/tasks/configure-pod-container/image-volumes/):

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  containers:
    - name: app
      image: example.org/app
      volumeMounts:
        - name: geoip
          mountPath: /usr/share/GeoIP
          readOnly: true
  volumes:
    - name: geoip
      image:
        reference: ghcr.io/opengeoip/databases/country:2026.10.7
```

The file is then `/usr/share/GeoIP/opengeoip-country.mmdb`. A pod keeps the database it started with, so a new tag reaches it on the next rollout.

To ship a database inside your own image instead, copy it from the image:

```dockerfile
FROM example.org/app
COPY --from=ghcr.io/opengeoip/databases/country:2026.10.7 /opengeoip-country.mmdb /usr/share/GeoIP/
```

```sh
gh attestation verify oci://ghcr.io/opengeoip/databases/country:latest --owner opengeoip
```

## Accuracy

Each release notes the share of RIPE Atlas probes whose country the database gets right. See [geoip-builder](https://github.com/opengeoip/geoip-builder/blob/main/docs/evaluation.md) for how it compares with GeoLite2.

## License

The publishing workflow is GPL-3.0-or-later, see [LICENSE](LICENSE). The databases are derived from third-party data with their own terms of use: internet registries, RIPE RIS and RIPE Atlas, RPKI repositories, PeeringDB and operators' geofeeds.
