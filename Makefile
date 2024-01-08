serve:
	bundle exec jekyll serve -o -V

new_draft:
	python bin/new_draft.py --name $(name)

prepare_gh_page:
	bundle exec jekyll build
	rm -rf doc/
	mv _site docs/

clean_gh_page:
	rm -rf doc/
	rm -rf _site/

notebook_to_md:
	jupyter nbconvert --to markdown $(nb_name)

