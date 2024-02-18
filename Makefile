serve:
	bundle exec jekyll serve -o -V

new_draft:
	python bin/new_draft.py --name $(name)

prepare_gh_page:
	make clean_gh_page
	bundle exec jekyll build

notebook_to_md:
	jupyter nbconvert --to markdown $(nb_name)

new_nb:
	touch _notebooks/$(name).ipynb && code _notebooks/$(name).ipynb 
