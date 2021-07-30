"""ABINIT-MP input file (.ajf) generator.

ABINIT-MP is a Fragment Molecular Orbital method software for high-performance computer.
This software is highly parallelized with MPI (and OpenMP [Hybrid version]) interface

    ::

        mkinp.py < input.ajf | abinitmp > output.log

    or

    ::

        mkinp.py < input.ajf | mpirun -n {nproc} abinitmp > output.log


    Availability

    - FMO Drug Design Consortium
        - https://fmodd.jp/top-en/
    - ABINIT-MP Open Series
        - http://www.cenav.org/abinit-mp-open_ver-1-rev-22/

"""