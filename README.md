# Hiro's Home-Manager Outlook Oauth Hack

This is a generalization and adaptation of the fork of
[UvA-FNWI](https://github.com/UvA-FNWI/M365-IMAP) to get oauth imap
working on my machine with the McGill email server. I've added
multi-configuration and encryption support. Furthermore token
expiration is now being taken into account. *This has been hacked
together in an afternoon and works for me. No guarantees provided :).*

**If you want to see this in action with `mbsync + msmtp` head over
[here](https://github.com/vale981/nix-config/blob/master/home/hiro/software/email/default.nix)**

The tool is configured by `~/.o365-auth-config.toml` (see
`config.toml`) in this repo. The `[security]` section has only one
setting, namely the `PasswordPath` which can point to an optional
password file which is then used to decrypt the stored `refresh` and
`access` tokens. The expectation is, that a tool like
[agenix](https://github.com/ryantm/agenix) provides this file while
the computer is running.

The `[default]` section contains the OAuth `ClientId`, the
`ClientSecret` and the `Scopes`. I really don't have a clear idea what
those mean, but the values provided by default are taken from
Thunderbird. For a better explanation see [the work this is based
on](https://github.com/UvA-FNWI/M365-IMAP).

For each account one wishes to set up on can optionally add a section
`[<account name>]` which can override the above values.

The script `get_token.py` (accessible as `o365-get-token` if the
home-manager module is enabled) takes an argument `<account name>` and
launches the authentication flow. Once this has been done, the script
`refresh_token.py` (accessible as `o365-refresh-token`) can be called
with the same argument to obtain the currently valid `access key`. It
automatically refreshes said key upon its expiration. The `access key`
is printed to `stdout` and may be fed into `mbsync` or `msmtp`.

The flake provides a package which makes the above commands
available. It also provides a very basic and ugly home-manager module
that allows you to configure those scripts using, who'd have thought
it, home-manager.

Simply a add the `o365-auth.homeManagerModules.default` to your home-manager modules an
```nix
  programs.o365-auth.enable = true;
  programs.o365-auth.passwordPath = config.age.secrets.mail_token_storage_pw.path;
```
should get you started. 
