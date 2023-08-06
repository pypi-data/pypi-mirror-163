# zencoreipinfo

Get outgoing ip from https://zencore.cn/ipinfo.

## Install

```
pip install zencoreipinfo
```

## Usage in Cli

```
test@test zencoreipinfo % ipinfo --help
Usage: ipinfo [OPTIONS]

Options:
  --url TEXT   Server url. Can apply multiple times.
  -q, --quiet  Don't show error information.
  --help       Show this message and exit.

test@test zencoreipinfo % ipinfo
aaa.xxx.yy.zz

```

1. By default, the program will use the default ipinfo server `https://zencore.cn/ipinfo`.
1. We ship cli program in name `ipinfo`, and `zencoreipinfo` as it's alias.

## Usage in Script

```
In [1]: from zencoreipinfo import get_outgoing_ip

In [2]: ip = get_outgoing_ip()

In [3]: print(ip)
aaa.xxx.yy.zz
```

## How to implement self ipinfo server?

You need a linux server with a public ip address, and you need to install nginx service on the linux server. Add the ipinfo location into your site.

```
# your other configs

location /ipinfo {
    add_header Content-Type text/plain;
    return 200 $remote_addr;
}

# your other configs

```

After you setup your ipinfo server. Run the ipinfo command with --url prarameter.

```
test@test zencoreipinfo % ipinfo --url https://you.site.domain.cn/ipinfo
aaa.xxx.yy.zz
```

## About the ipinfo server of zencore.cn

We do not promise continuity or reliability of the service.


## Release

### 0.1.0

- First release.
