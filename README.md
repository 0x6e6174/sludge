# sludge: webthing for natalieee.net
it rhymes with kludge.

## config
```yaml
ssl-key: ./key.pem
ssl-cert: ./cert.pem
http-port: 5000 
https-port: # 5001
file-dir: 'site'
```
ssl-{cert,key} are self explanatory.
if the value of https? port is commented or not present, it will not run the https? server on that port.
file-dir is where the files for the site can be found. 
the above config is the config for the local version of my website, which is used for testing.
it runs an http server on 5000, but no https server.

## serving files 
- src/lib/router.py has the routing config for my website in it. it is easy to modify to your usecase.
- src/lib/patchers.py has the patching config for my website in it. it is also easy to modify.

## dynamic content
### embedded bash scripting 
sludge has support for inline bash inside of html documents.<br>
ex:
```html
<p>lorem ipsum $[echo foo]</p>
```
would resolve to 
```html 
<p>lorem ipsum foo</p>
```

### variables in html 
in addition to the above, you can have variables embedded in html.
```html 
<p>lorem ipsum {aoeu}</p> 
```
would normally resolve to
```html 
<p>lorem ipsum {aoeu}</p> 
```
however, if we assume that this text is in a file `foo.html`, then we can serve that file such that
```py 
parse_file('./foo.html', dict(aoeu='foo'))
```
in which case it would resolve to 
```html
<p>lorem ipsum foo</p>
```
<br> 

in practice, this may be seen here:
```py
Route(
    lambda path: os.path.isdir('.' + path.path), 
    [Method.GET],
    lambda request, *_: Response(
        ResponseCode.OK, 
        {'Content-Type': 'text/html'},
        parse_file('./dir_index.html', dict(path='.' + request.path.path)).encode('utf-8')
    )
)
```
