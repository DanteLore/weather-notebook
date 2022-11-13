

# Install Steps

```shell
brew install geos
brew install proj

pip3 install -r requirements.txt
```

You'll need to set up AWS access with `aws configure` to get the command line tools working, then set your profile
and default region in `~/.zshenv` thus:

```
export AWS_PROFILE="dantelore"
export AWS_DEFAULT_REGION="eu-west-1"
```


Cartopy makes this very hard work!  https://scitools.org.uk/cartopy/docs/latest/installing.html

In the end, this worked for me - I'm on a Mac.  Check your architecture with `uname -m`.
```shell
ARCHFLAGS="-arch x86_64" pip3 install cartopy
```