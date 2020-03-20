html: index article

index:
	cp src/templates/index.html public/index.html

article:
	python src/github_issue.py DuyaoSS/SSR 1 --cache-dir /tmp

watch-html:
	watchexec -w src --exts html 'make html'

css:
	cp src/css/*.css public/css/
	npx tailwindcss build src/css/article.css -o public/css/article.css

watch-css:
	watchexec -w tailwind.config.js -w src/css 'make css'

server:
	python -m http.server 8000 --directory public

start-dev:
	npx pm2 start dev.config.js
	npx pm2 logs

restart-dev:
	npx pm2 restart dev.config.js
	npx pm2 logs

stop-dev:
	npx pm2 stop dev.config.js
