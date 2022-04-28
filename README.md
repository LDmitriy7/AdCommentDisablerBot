1) You must create env.toml from env-sample.toml
2) docker build -t ad_comment_disabler_bot .
3) docker run --network=host --restart=unless-stopped -d ad_comment_disabler_bot