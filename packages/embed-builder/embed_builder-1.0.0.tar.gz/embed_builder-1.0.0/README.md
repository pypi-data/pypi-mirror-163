# embed_builder

I got tired of manually writing dictionaries to send embeds via Discord webhooks so I made this package to do it effortlessly.

## Installation

```shell
$ pip install embed_builder
```

## Usage

```python
from embed_builder import Embed

embed = Embed()
embed.set_title("Hello")
embed.set_description("How are you?")
my_embed = embed.build()

# Or via chaining...

my_embed = Embed().set_title("Hello").set_description("How are you?").build()

# Example usage with Discord webhooks and requests package

requests.post("webhook url", json={
    "content": "here is an embed",
    "embeds": [my_embed]
})
```

> **Warning**
> Discord's embed total character limit is not currently enforced through this package. Make sure your content is the correct size as you are building embeds.
