# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build
BRANCH        =

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)/$(BRANCH)" $(SPHINXOPTS) $(O)

.PHONY: deploy
deploy: 
	make clean
	git checkout gh-pages
	git reset --hard develop
	make BRANCH=develop html
	git reset --hard main
	make BRANCH=main html
	cp index.html _build/html
	git add _build/html
	git commit -m "add html"
	git reset --hard $$(cd .. && git subtree split --prefix docs/_build/html/ gh-pages)
	git push -f origin gh-pages
	git checkout develop
