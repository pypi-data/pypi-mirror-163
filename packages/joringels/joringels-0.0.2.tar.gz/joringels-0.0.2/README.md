# Joringels manages your secrets across multiple VMs.

### run in Shell
```
    jo $action [-n safeName] -e entryName # actions: load, upload, fetch, serve
    on windows: curl "http://$env:DATASAFEIP:7000/entryName"
    on linux: curl "http://$DATASAFEIP:7000/entryName"
```

### use in Python
```
    from joringels.src.actions import fetch
    # using retain=False (default is False) will delete dataSafe in .ssp folder
    creds = fetch.alloc(safeName='mysafeName', entryName='myentryName', retain=True)
```
- NOTE: this is in alpha
- NOTE: holds password in environment variables (only use if env vars are safe)
- NOTE: Joringels assumes, that your source and target VMs are un-compromized.
- NOTE: ONLY serve secrets via http inside a protected local network

# Important def info
- Currently kdbx (password-manager) is the only supported secret source
- scp is used as connector for secrets file transfer to server



## 1 What joringels does
- efficiently manage your secrets while maintaining it in a save location i.e. kdbx
- create dataSafes (bundles of secrets) using combined entries in your secret source
- serve dataSafes secrets to a single network
    - source ~/.ssp directory serves secrets to a single client
    - source encrypted http connection serves secrets to multiple clients simultaneously
- extracts and uploads your encrypted dataSafes to multiple remote server simultaneously

## 2 Download and install from gitlab
- python3.9 +
- git clone https://gitlab.com/larsmielke2/joringels.git

### Install using repo Pipfile
- pipenv install (NOTE: this installs joringels as editable, change Pipfile if needed)

## 3 Setup
### secret host machine setup (mandatory)
- install password manager # Currently only keepass is supported !
- define some neccessary password variables
    - 'yourSafeName': 'pwd' (encrypts safeName.yml file when it is saved-locally or scp-send)
    - JORINGELS: 'pwd' (encrypts http secrets NOTE: must be equal on server and all clients)

### secret host machine setup (optional)
- define some helpful environment variables to avoid typing kwargs all the time
    - DATASAFEIP: ip the host server uses to serve secrets (ipv4 address of your server)
    - DATASAFENAME: name of dataSafe you want to use in a network
    - DATASAFEROLE: server or client
    - JORINGELSPATH: full path to where the Pipfile lives


### Joringels package setup (mandatory)
- create a  \~/.ssp directory (this will contain any en/decrpyted files)
- in keepass add Group -> name it like settings.py / groupName (i.e. joringels_data_safes)
- in keepass create a dataSafe entry inside the Group (i.e. myfirstdatasafe)

- for each dataSefe create a soures/targets yml file as shown in example below
- NOTE: targets AND entries contain full paths to keepass entries
````
    # entries for single or multiple target server logins (server using the dataSafe secrets)
    targets:
      - pyenvs/provider/droplets/testing/github-runner-token
    
    # entries for secrets your dataSafe will hold
    entries:
      - pyenvs/utils/dbs/my_db_login
      - pyenvs/provider/apiTokens/repo_download
      - pyenvs/provider/apiTokens/myprovider_api_token
      - pyenvs/provider/google_oauth
````
- attach the new file to your dataSafe entry (myfirstdatasafe): keepass>>advanced>>attach
- also attach the following \_joringels.yml (runtime parameters) file in the same dataSafe as above
```
    # only these hosts are allowed to request a secret
    allowedHosts:
        - 164.92.206.169
        - 188.166.87.121
    application: joringels
    decPrefix: decrypted_
    kPath: fullPath to your .kdbx file
    lastUpdate: 2022-06-06-11-22-21-842103
    secretsPort: 7000
    validator: text_is_valid
    # name of allowed develoment systems
    secureHosts:
        - BLUE-MOON_1
        - BLUE-MOON_2
```
- remove the unprotected .yml files, so they only exist in kdbx now

### Joringels setup (optional)
- if you whish, change relevant names and dirs in joringels/src/settings.py


### Try the folowing commands
1. jo info: (will show you more readme)
2. jo load: (will load your secrets file to .ssh)
3. jo chkey -n safeName -nk newPwd # not needed but propaply better to do so
4. jo serve -n safeName

## 5 Some Windows gimmics
### powershell functions to add to your $PROFILE
#### fjo
```
    function FJO($SECRET){
        $curr = $PWD
        cd $env:JORINGELSPATH
        pipenv run jo fetch -e $SECRET
        cd $curr
    }
```
- jo.serve from Windows start menu: copy joringels/prcs/jo.serve shortcut to startmenu
- then run like: fjo entryname

####loadloc
```
    function loadloc(){
        $curr = $PWD
        cd $env:JORINGELSPATH
        pipenv run jo load -n digiserver -src $env:secrets
        pipenv run jo chkey -n digiserver -nk os
        cd $curr
    }
```

## 6 Some docker stuff
- docker container is under construction
- to run use
    - docker run -itd --rm --name [joringels] -p [7000:7000] -w /home/gitlab-runner/python_venvs/libraries/joringels --network [illuminati] joringels bash ./prcs/jo.serve.sh


## 7 Known issues
- as of 06/2022 python10.5 not installing (use python10.4 instead)