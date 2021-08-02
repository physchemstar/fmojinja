.ONESHELL:
MD_ENGINE_MIN := pmemd.cuda# exec command for minimization.
MD_ENGINE := mpirun -n 4 pmemd.cuda.MPI# exec command for md.
SCHEDULER := none# scheduler type. (e.g. tsubame, openpbs)
SUBMIT := bash#Submit command. e.g. qsub -g your_group for OpenPBS or TSUBAME scheduler


.PHONY: sub
sub: amber.sh # Submit amber_min, amber_prep, amber_prod by scheduler.
	$(SUBMIT) $<

.PHONY: clean
clean: # Delete data
	rm -f amber_min.mk amber_prep.mk amber_prod.mk amber_min/* amber_prep/* amber_prod/* 

amber.sh: $(SCHEDULER)_header.sh amber_min.mk amber_prep.mk amber_prod.mk
	cat $(SCHEDULER)_header.sh > $@
	echo "make -f amber_min.mk MD_ENGINE='$(MD_ENGINE_MIN)' run" >> $@
	echo "make -f amber_prep.mk MD_ENGINE='$(MD_ENGINE)' run" >> $@
	echo "make -f amber_prod.mk MD_ENGINE='$(MD_ENGINE)' run" >> $@

amber_min.mk: amber_min
	python -m fmojinja.sander.makefile step_prep \
	-P $</dynamics \
	-drms 0.01 \
	-rm "!@H=" "@N,CA,C,O3',C3',C4',C5',O5',P" "" \
	-rw 10000 \
	-p dynamics.z.prmtop \
	-c dynamics.a.0.coor \
	-cut 14 \
	-j min min min > $@
	make -f $@ gen

amber_prep.mk: amber_prep
	python -m fmojinja.sander.makefile step_prep \
	-P $</dynamics \
	-cut 14.0 \
	-p amber_min/dynamics.prmtop \
	-c amber_min/dynamics_finish.restrt \
	-j heat dens dens dens dens dens dens equil \
	-rm "@C,CA,N,O3',C3',C4',C5',O5',P" \
	"@C,CA,N,O3',C3',C4',C5',O5',P" \
	"@C,CA,N,O3',C3',C4',C5',O5',P" \
	"@C,CA,N,O3',C3',C4',C5',O5',P" \
	"@C,CA,N,O3',C3',C4',C5',O5',P" \
	"@C,CA,N,O3',C3',C4',C5',O5',P" \
	"@C,CA,N,O3',C3',C4',C5',O5',P" \
	""  \
	-rw 3 3 3 3 3 3 3 0 \
	-nstlim 100000 10000 10000 20000 20000 20000 20000 1800000 > $@
	make -f $@ gen

amber_prod.mk: amber_prod
	python -m fmojinja.sander.makefile step_prod \
	-P $</dynamics \
	-ns 50 \
	-nstlim 2000000 \
	-dt 0.0005 \
	-cut 14.0 \
	-p amber_prep/dynamics.prmtop \
	-c amber_prep/dynamics_finish.restrt > $@
	make -f $@ gen

amber_min:
	mkdir $@
amber_prep:
	mkdir $@
amber_prod:
	mkdir $@

none_header.sh:
	touch $@

tsubame_header.sh: # TSUBAME header
	cat << EOF > $@
	#$$ -l f_node=1
	#$$ -l h_rt=24:00:00
	#$$ -p -5
	#$$ -cwd
	set -e
	. /etc/profile.d/modules.sh
	module load amber
	EOF

openpbs_header.sh: # OpenPBS header
	cat << EOF > $@
	set -e
	if [ ""$$PBS_O_WORKDIR != "" ]; then cd $$PBS_O_WORKDIR; fi
	. /etc/profile.d/modules.sh
	module load amber
	EOF


.PHONY: help
help:  # print this help
	@cat $(MAKEFILE_LIST) \
    | grep -E '^[^:# ]+ := .*?# .*' \
    | sort \
    | awk 'BEGIN {FS = "# "; print "\033[35m[Attributes]\033[0m"} {printf " \033[35m%-30s\033[0m %s\n", $$1, $$2}' \
	> .makehelp
	@cat $(MAKEFILE_LIST) \
    | grep -E '^[^:# ]+:.*?# .*$$' \
    | sort \
    | awk 'BEGIN {FS = ":.*?# "; print "\033[36m[Commands or Targets]\033[0m"} {printf " \033[36m%-30s\033[0m %s\n", $$1, $$2}' \
	>> .makehelp
	cat .makehelp
	@rm .makehelp

.PHONY: visdeps
visdeps: # visualize makefile dependency
	@echo 'digraph deps {' > visdeps.dot
	@cat $(MAKEFILE_LIST) \
	| grep -E '^[^:# ]+:' \
	| grep -vE '^(\.PHONY|help|visdeps):' \
	| sed -E 's/#.*$$//' \
    | sed -E 's/\\/\\\\/g' \
	| sed -E 's/"//g' \
	| sed -e 's/\r//g' \
	| awk 'BEGIN{FS="[ \n]*:?[ \n]*"} { for(i=2;i<=NF;i++){ if ($$i!="") print "\"" $$1 "\" -> \"" $$i "\"" } } END { print "}" }' \
	>> visdeps.dot
	dot -Tsvg -o visdeps.svg visdeps.dot
