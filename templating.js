var feed = new Instafeed({
  accessToken: '""" + secrets["instagram_user_token"] + """"',
  template:
    '<a href="{{link}}" target="_blank"><img style="max-height: 300px" title="{{caption}}" src="{{image}}" /></a>',
  transform: function (item) {
    //Transform receives each item as its argument
    // Over-write the original timestamp
    item.timestamp = new Date(item.timestamp).toLocaleString("en-AU", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    });
    // return the modified item
    return item;
  },
});
feed.run();
