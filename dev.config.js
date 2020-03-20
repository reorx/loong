// Options doc: https://pm2.keymetrics.io/docs/usage/pm2-doc-single-page/#programmatic-api
module.exports = {
  apps : [
    {
      name: 'Watch HTML',
      script: 'make watch-html',
      interpreter: "none",
      time: true,
    },
    {
      name: 'Watch CSS',
      script: 'make watch-css',
      interpreter: "none",
      time: true,
    },
    {
      name: 'HTTP Server',
      script: 'make server',
      // script: 'python -m http.server 8000 --directory public',
      interpreter: "none",
      time: true,
    },
  ],
};
