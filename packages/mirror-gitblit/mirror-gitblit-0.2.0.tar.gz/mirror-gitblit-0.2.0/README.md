# <del>Scripts</del> Module to mirror [gitblit](https://gitblit.github.io/gitblit/)

This package requires at least python 3.6.

---
**NOTE:**
This package is created for education only, not intended to be used 
in productive system!
---

The class `mirror_gitblit.GitblitMirror.Gitblit` provides methods to
talk to a Gitblit-Server via its [RPC-API](https://gitblit.github.io/gitblit/rpc.html).

To use this class, the command `curl` and `git` must available in the `PATH`-Variable.
One can test if these commands exist by using `which`. One possible output:

```sh
$ which curl
/usr/bin/curl
$ which git
/usr/bin/git
```

## Example

Running this file (after change some variables) will create at least these files: 

* `${HOME}/mirror-log.txt`,
* `f'{backupdir}/{HOST}-repos.json'`

and mirror of repositories in remote gitblit server --if any-- which are less than 1 GB,
in `{backupdir}`.


```python
# This script is written by an admin. It uses `mirror-gitblit` to mirror
# repositories of a gitblit-server

from mirror_gitblit.GitblitMirror import Gitblit
from mirror_gitblit import GitblitMirror
import logging

HOME = "/home/backup"
HOST = "gitblit"
DOMAIN = "somedomain.de"
GIT_SSH_PORT=8022


user = "backup"
source_web_url = f"https://{HOST}.{DOMAIN}/gitblit"
curl_credentials_file = f'{HOME}/curl-credential.txt'


source_base_url = f'ssh://{user}@{HOST}.de:{GIT_SSH_PORT}'
backup_dir = "/backup"
repositories_json = f"{backup_dir}/{HOST}-repos.json"

included_repos = [
    # name of repositories to be included without leading slash (/)
]

excluded_repos = [
    # name of repositories to be excluced without leading slash (/)
]

logging.basicConfig(filename=f"{HOME}/mirror-log.txt",
                    filemode='w', level=logging.INFO,
                    format='%(asctime)s - %(levelname)6s - %(message)s',
                    datefmt="%Y-%m-%dT%H:%M:%S%z")

gitblit = Gitblit(source_web_url, curl_credentials_file, source_base_url, repositories_json, backup_dir)
gitblit.download_repositories_list()

repo_filter = lambda repo : GitblitMirror.inclusive_exclusive_filter(repo, None, excluded_repos)
less_than_1GB = lambda repo: GitblitMirror.repo_size_to_int(repo) < 1000**3
less_than_2MB = lambda repo: GitblitMirror.repo_size_to_int(repo) < 2 * (1000**2)

gitblit.clone_repos(less_than_1GB, False)
gitblit.update_repos(less_than_1GB)
```


* One must also create a file named `$HOME/curl-credentials.txt`, which contents
authentication information against gitblit server in  [netrc](https://curl.se/docs/manual.html) format:

```
machine {gitblit.domain} login {username} password {user password}
```

This file is passed to cURL-Option `--netrc-file`. To test if your netrc file is
correct run

``` 
curl --netrc-file $HOME/curl-credentials.txt https://gitblit.domain.de/gitblit/rpc/?req=LIST_REPOSITORIES
```

* The SSH-public key of the gitblit user must be imported in Gitblit server.
