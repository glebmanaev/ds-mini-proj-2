# ds-mini-proj-2

## ML online bookshop

We used a pre-trained autoregressive language model (GPT-3 by OpenAI) to generate book names based on an input as small as a single keyword or larger.

  Usage is simple `<ML-list-recommend “keyword/part of the name/etc”>`:

``` 
ML-list-recommend melody lady
```
Output:
```
I suggest you: Melody Lady and the Quest for the Perfect Song
```

It generates input based on `"Generate a book name based on the keyword '{keyword}'. Name:"` query. Sometimes the result is too short or too long, so we are regenerationg the response until it has [5,50] symbols length.
