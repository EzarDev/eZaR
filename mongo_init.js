db.createUser({
  user: "ezar",
  pwd: "WhatAShame",
  roles: [
    {
      role: "readWrite",
      db: "eZaR",
    },
  ],
});
