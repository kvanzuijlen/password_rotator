> NOTE: This project is nowhere near production ready! Do not use unless you're 100% sure what you're doing!

# Password rotator
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=kvanzuijlen_password_rotator&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=kvanzuijlen_password_rotator)

This project aims to help with rotating all passwords in your password vault.
It does this by utilizing a Selenium script. Contributing is easy: write a Selenium script
to change a password for a not yet supported website and open a Pull Request.

Some websites might be supported by a, not yet implemented, generic fallback script making use
of the `/.well-known/change-password` specification proposal.
